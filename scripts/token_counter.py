#!/usr/bin/env python3
"""
Token 计算器
支持多种模型的 Token 计算和成本估算

支持的模型：
- GPT-4 / GPT-3.5 (cl100k_base)
- Claude (claude tokenizer)
- 通义千问
- 文心一言
- 国产模型近似估算
"""

import json
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModelInfo:
    """模型信息"""
    name: str
    provider: str
    input_price: float  # 每 1K tokens 价格 (USD)
    output_price: float
    tokenizer_type: str


class TokenCounter:
    """Token 计算器"""
    
    def __init__(self):
        self.models = {
            "gpt-4": ModelInfo(
                name="GPT-4",
                provider="OpenAI",
                input_price=0.03,
                output_price=0.06,
                tokenizer_type="cl100k_base"
            ),
            "gpt-4-turbo": ModelInfo(
                name="GPT-4 Turbo",
                provider="OpenAI",
                input_price=0.01,
                output_price=0.03,
                tokenizer_type="cl100k_base"
            ),
            "gpt-3.5-turbo": ModelInfo(
                name="GPT-3.5 Turbo",
                provider="OpenAI",
                input_price=0.0005,
                output_price=0.0015,
                tokenizer_type="cl100k_base"
            ),
            "claude-3-opus": ModelInfo(
                name="Claude 3 Opus",
                provider="Anthropic",
                input_price=0.015,
                output_price=0.075,
                tokenizer_type="claude"
            ),
            "claude-3-sonnet": ModelInfo(
                name="Claude 3 Sonnet",
                provider="Anthropic",
                input_price=0.003,
                output_price=0.015,
                tokenizer_type="claude"
            ),
            "claude-3-haiku": ModelInfo(
                name="Claude 3 Haiku",
                provider="Anthropic",
                input_price=0.00025,
                output_price=0.00125,
                tokenizer_type="claude"
            ),
            "qwen-turbo": ModelInfo(
                name="通义千问 Turbo",
                provider="阿里云",
                input_price=0.002,  # ¥0.002/千tokens
                output_price=0.006,
                tokenizer_type="qwen"
            ),
            "qwen-plus": ModelInfo(
                name="通义千问 Plus",
                provider="阿里云",
                input_price=0.004,
                output_price=0.012,
                tokenizer_type="qwen"
            ),
            "ernie-bot": ModelInfo(
                name="文心一言",
                provider="百度",
                input_price=0.0012,  # ¥0.012/千tokens
                output_price=0.012,
                tokenizer_type="ernie"
            ),
            "glm-4": ModelInfo(
                name="GLM-4",
                provider="智谱AI",
                input_price=0.014,  # ¥0.1/千tokens ≈ $0.014
                output_price=0.014,
                tokenizer_type="glm"
            ),
        }
    
    def estimate_tokens(self, text: str, model: str = "gpt-4") -> int:
        """
        估算文本的 Token 数量
        
        不同模型的估算规则：
        - GPT-4: 中文字符约 1.5-2 tokens，英文单词约 0.75 tokens
        - Claude: 与 GPT-4 类似
        - 国产模型: 中文更友好，约 1-1.5 tokens
        """
        if not text:
            return 0
        
        model_info = self.models.get(model)
        if not model_info:
            model_info = self.models["gpt-4"]
        
        tokenizer_type = model_info.tokenizer_type
        
        if tokenizer_type == "cl100k_base":
            # GPT-4 tokenizer
            # 英文: ~4 字符 = 1 token
            # 中文: ~1.5-2 字符 = 1 token
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            english_chars = len(text) - chinese_chars
            
            tokens = int(chinese_chars * 0.6 + english_chars * 0.25)
            
        elif tokenizer_type == "claude":
            # Claude tokenizer (与 GPT-4 类似)
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            english_chars = len(text) - chinese_chars
            
            tokens = int(chinese_chars * 0.55 + english_chars * 0.25)
            
        elif tokenizer_type in ["qwen", "ernie", "glm"]:
            # 国产模型对中文更友好
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            english_chars = len(text) - chinese_chars
            
            tokens = int(chinese_chars * 0.5 + english_chars * 0.25)
        
        else:
            # 默认估算
            tokens = int(len(text) * 0.5)
        
        return max(tokens, 1)
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> Dict:
        """计算成本"""
        model_info = self.models.get(model)
        if not model_info:
            return {"error": f"未知模型: {model}"}
        
        input_cost = (input_tokens / 1000) * model_info.input_price
        output_cost = (output_tokens / 1000) * model_info.output_price
        total_cost = input_cost + output_cost
        
        return {
            "model": model_info.name,
            "provider": model_info.provider,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "total_cost_cny": round(total_cost * 7.2, 6),  # 假设汇率 1:7.2
        }
    
    def compare_models(self, text: str, output_tokens: int = 100) -> Dict:
        """比较不同模型的 Token 数和成本"""
        results = {}
        
        for model_id, model_info in self.models.items():
            input_tokens = self.estimate_tokens(text, model_id)
            cost_info = self.calculate_cost(input_tokens, output_tokens, model_id)
            results[model_id] = {
                "model_name": model_info.name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_cost_usd": cost_info["total_cost_usd"],
                "total_cost_cny": cost_info["total_cost_cny"],
            }
        
        return results
    
    def analyze_compression_savings(self, original: str, compressed: str, model: str = "gpt-4") -> Dict:
        """分析压缩节省"""
        original_tokens = self.estimate_tokens(original, model)
        compressed_tokens = self.estimate_tokens(compressed, model)
        saved_tokens = original_tokens - compressed_tokens
        
        original_cost = self.calculate_cost(original_tokens, 100, model)
        compressed_cost = self.calculate_cost(compressed_tokens, 100, model)
        
        return {
            "original": {
                "text": original,
                "tokens": original_tokens,
                "cost_usd": original_cost["total_cost_usd"],
            },
            "compressed": {
                "text": compressed,
                "tokens": compressed_tokens,
                "cost_usd": compressed_cost["total_cost_usd"],
            },
            "savings": {
                "tokens": saved_tokens,
                "percentage": round((saved_tokens / original_tokens * 100), 2) if original_tokens > 0 else 0,
                "cost_usd": round(original_cost["total_cost_usd"] - compressed_cost["total_cost_usd"], 6),
            }
        }


def main():
    """测试入口"""
    counter = TokenCounter()
    
    # 测试文本
    test_text = "今天我在使用这个功能的时候发现了一个问题，就是当我点击提交按钮之后，页面没有任何反应，我不知道是什么原因导致的，你能帮我看看吗？"
    compressed_text = "提交按钮无响应，需排查。"
    
    print("=" * 70)
    print("Token 计算器测试")
    print("=" * 70)
    
    print(f"\n原文: {test_text}")
    print(f"压缩后: {compressed_text}")
    
    print("\n" + "=" * 70)
    print("模型对比")
    print("=" * 70)
    
    comparison = counter.compare_models(test_text, output_tokens=50)
    
    print(f"\n{'模型':<20} {'输入Tokens':<12} {'总成本(USD)':<15} {'总成本(CNY)':<15}")
    print("-" * 70)
    
    for model_id, data in comparison.items():
        print(f"{data['model_name']:<20} {data['input_tokens']:<12} "
              f"${data['total_cost_usd']:<14.6f} ¥{data['total_cost_cny']:<14.6f}")
    
    print("\n" + "=" * 70)
    print("压缩节省分析 (GPT-4)")
    print("=" * 70)
    
    savings = counter.analyze_compression_savings(test_text, compressed_text, "gpt-4")
    
    print(f"\n原始 Tokens: {savings['original']['tokens']}")
    print(f"压缩后 Tokens: {savings['compressed']['tokens']}")
    print(f"节省 Tokens: {savings['savings']['tokens']} ({savings['savings']['percentage']}%)")
    print(f"节省成本: ${savings['savings']['cost_usd']:.6f}")


if __name__ == "__main__":
    main()
