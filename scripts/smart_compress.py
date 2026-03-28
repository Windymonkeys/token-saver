#!/usr/bin/env python3
"""
智能上下文压缩模块
基于语义权重分析，智能识别和压缩文本

核心功能：
1. 识别核心信息 vs 冗余信息
2. 分层压缩：关键保留、次要压缩、噪音删除
3. 支持多种压缩级别
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class Importance(Enum):
    """信息重要性级别"""
    CRITICAL = 3    # 关键信息，必须保留
    IMPORTANT = 2   # 重要信息，可以压缩
    NORMAL = 1      # 普通信息，可以大幅压缩
    NOISE = 0       # 噪音信息，可以删除


@dataclass
class Segment:
    """文本片段"""
    text: str
    importance: Importance
    compressed: str = ""


class SmartCompressor:
    """智能压缩器"""
    
    def __init__(self):
        # 关键词模式（高重要性）
        self.critical_patterns = [
            r'\d+',  # 数字
            r'[A-Z]{2,}',  # 缩写
            r'(错误|error|bug|问题|异常|失败)',  # 问题词
            r'(必须|需要|要求|重要|关键)',  # 强调词
            r'(API|SDK|URL|ID|token|password)',  # 技术术语
        ]
        
        # 噪音模式（低重要性）
        self.noise_patterns = [
            r'(我觉得|我想|我认为|我感觉)',  # 主观表达
            r'(可能|大概|也许|应该)',  # 不确定词
            r'(然后|接着|之后)',  # 连接词
            r'(的话|之类的|什么的)',  # 口语化表达
            r'(真的|非常|特别|相当)',  # 程度副词
        ]
        
        # 可压缩模式
        self.compressible_patterns = {
            r'今天(早上|下午|晚上)?': '今日',
            r'这个(问题|事情|东西)': '此',
            r'那个(问题|事情|东西)': '彼',
            r'因为(.+?)所以': r'因\1故',
            r'如果(.+?)的话': r'若\1',
            r'虽然(.+?)但是': r'虽\1然',
            r'不知道(为|是)什么': '不知何故',
            r'有没有(可能|办法)': '可否',
            r'能不能(帮|给)': '可否',
            r'我想(问|知道|了解)': '吾欲',
            r'你需要': '汝须',
            r'我应该': '吾宜',
        }
    
    def analyze_importance(self, text: str) -> Importance:
        """分析文本片段的重要性"""
        # 检查关键模式
        for pattern in self.critical_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return Importance.CRITICAL
        
        # 检查噪音模式
        noise_count = 0
        for pattern in self.noise_patterns:
            if re.search(pattern, text):
                noise_count += 1
        
        if noise_count >= 2:
            return Importance.NOISE
        elif noise_count == 1:
            return Importance.NORMAL
        
        return Importance.IMPORTANT
    
    def segment_text(self, text: str) -> List[Segment]:
        """将文本分段并分析重要性"""
        # 按句子分割
        sentences = re.split(r'[，。！？；\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        segments = []
        for sentence in sentences:
            importance = self.analyze_importance(sentence)
            segments.append(Segment(text=sentence, importance=importance))
        
        return segments
    
    def compress_segment(self, segment: Segment) -> str:
        """压缩单个片段"""
        if segment.importance == Importance.CRITICAL:
            return segment.text  # 关键信息不压缩
        
        if segment.importance == Importance.NOISE:
            return ""  # 噪音信息删除
        
        # 应用压缩模式
        compressed = segment.text
        for pattern, replacement in self.compressible_patterns.items():
            compressed = re.sub(pattern, replacement, compressed)
        
        # 去除多余空格
        compressed = re.sub(r'\s+', '', compressed)
        
        return compressed
    
    def compress(self, text: str, level: str = "medium") -> Dict:
        """
        智能压缩文本
        
        Args:
            text: 原始文本
            level: 压缩级别 (light/medium/aggressive)
        
        Returns:
            {
                "original": 原文,
                "compressed": 压缩后,
                "stats": 统计信息,
                "segments": 分段详情
            }
        """
        segments = self.segment_text(text)
        
        # 根据压缩级别调整策略
        if level == "light":
            # 轻度压缩：只删除噪音
            compressed_segments = [
                s.text if s.importance != Importance.NOISE else ""
                for s in segments
            ]
        elif level == "aggressive":
            # 激进压缩：只保留关键信息
            compressed_segments = [
                s.text if s.importance == Importance.CRITICAL else
                self.compress_segment(s) if s.importance == Importance.IMPORTANT else ""
                for s in segments
            ]
        else:
            # 中等压缩（默认）
            compressed_segments = [
                self.compress_segment(s) for s in segments
            ]
        
        # 组合结果
        compressed_text = "。".join(s for s in compressed_segments if s)
        
        # 统计
        stats = {
            "original_length": len(text),
            "compressed_length": len(compressed_text),
            "saved_chars": len(text) - len(compressed_text),
            "compression_ratio": round((1 - len(compressed_text) / len(text)) * 100, 2) if text else 0,
            "critical_segments": sum(1 for s in segments if s.importance == Importance.CRITICAL),
            "noise_segments": sum(1 for s in segments if s.importance == Importance.NOISE),
        }
        
        return {
            "original": text,
            "compressed": compressed_text,
            "stats": stats,
            "segments": [
                {
                    "text": s.text,
                    "importance": s.importance.name,
                    "compressed": compressed_segments[i]
                }
                for i, s in enumerate(segments)
            ]
        }


def main():
    """测试入口"""
    compressor = SmartCompressor()
    
    # 测试用例
    test_cases = [
        "今天我在使用这个功能的时候发现了一个问题，就是当我点击提交按钮之后，页面没有任何反应，我不知道是什么原因导致的，你能帮我看看吗？",
        "我觉得这个项目的代码质量非常好，但是可能需要优化一下性能，因为有时候会感觉有点慢。",
        "API 返回 500 错误，请求 ID 是 abc123，需要立即修复！",
        "我想要一个用户登录页面，要求界面简洁美观，支持手机号和邮箱两种登录方式，还需要有忘记密码的功能。",
    ]
    
    print("=" * 70)
    print("智能上下文压缩测试")
    print("=" * 70)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【测试 {i}】")
        print(f"原文: {text}")
        
        for level in ["light", "medium", "aggressive"]:
            result = compressor.compress(text, level)
            print(f"\n{level.upper()} 压缩: {result['compressed']}")
            print(f"节省: {result['stats']['saved_chars']} 字 ({result['stats']['compression_ratio']}%)")
        
        print("-" * 70)


if __name__ == "__main__":
    main()
