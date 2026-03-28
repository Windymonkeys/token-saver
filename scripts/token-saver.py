#!/usr/bin/env python3
"""
Token Saver - 统一入口

使用方法:
    token-saver "你的文本"                    # 自动压缩
    token-saver "你的文本" --mode wenyan      # 文言文模式
    token-saver "你的文本" --stats            # 显示统计
    token-saver --batch ./docs/               # 批量处理
    token-saver --enable                      # 开启全局节省模式
    token-saver --disable                     # 关闭全局节省模式
    token-saver --status                      # 查看状态
    token-saver --history                     # 查看历史
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

# 导入各模块
try:
    from translate import WenyanTranslator
    from smart_compress import SmartCompressor
    from english_compressor import EnglishCompressor
    from token_counter import TokenCounter
    from cache import CompressionCache
except ImportError:
    # 如果导入失败，使用相对路径
    pass


class TokenSaver:
    """Token Saver 主类"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".token-saver"
        self.config_file = self.config_dir / "config.json"
        self.history_file = self.config_dir / "history.json"
        
        # 创建配置目录
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化各模块
        self.wenyan = WenyanTranslator() if 'WenyanTranslator' in dir() else None
        self.smart = SmartCompressor() if 'SmartCompressor' in dir() else None
        self.english = EnglishCompressor() if 'EnglishCompressor' in dir() else None
        self.counter = TokenCounter() if 'TokenCounter' in dir() else None
        self.cache = CompressionCache() if 'CompressionCache' in dir() else None
    
    def _load_config(self) -> dict:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认配置
        return {
            "enabled": True,  # 默认开启节省模式
            "default_mode": "auto",
            "default_level": "medium",
            "default_model": "gpt-4",
            "show_stats": True,
            "auto_cache": True,
            "max_history": 100,
        }
    
    def _save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _load_history(self) -> list:
        """加载历史"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_history(self, history: list):
        """保存历史"""
        # 限制历史记录数量
        max_history = self.config.get("max_history", 100)
        if len(history) > max_history:
            history = history[-max_history:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def enable(self):
        """开启节省模式"""
        self.config["enabled"] = True
        self._save_config()
        print("✅ Token 节省模式已开启")
        print("   所有输入文本将自动压缩")
    
    def disable(self):
        """关闭节省模式"""
        self.config["enabled"] = False
        self._save_config()
        print("❌ Token 节省模式已关闭")
        print("   输入文本将保持原样")
    
    def status(self):
        """查看状态"""
        print("=" * 50)
        print("Token Saver 状态")
        print("=" * 50)
        print(f"节省模式: {'✅ 已开启' if self.config['enabled'] else '❌ 已关闭'}")
        print(f"默认模式: {self.config['default_mode']}")
        print(f"压缩级别: {self.config['default_level']}")
        print(f"默认模型: {self.config['default_model']}")
        print(f"显示统计: {'是' if self.config['show_stats'] else '否'}")
        print(f"自动缓存: {'是' if self.config['auto_cache'] else '否'}")
        print("=" * 50)
        
        # 显示缓存统计
        if self.cache:
            stats = self.cache.get_stats()
            print(f"\n缓存统计:")
            print(f"  命中率: {stats['hit_rate']}%")
            print(f"  已缓存: {stats['size']} 条")
    
    def recommend_mode(self, text: str) -> str:
        """智能推荐压缩模式"""
        # 分析文本特征
        chinese_ratio = len([c for c in text if '\u4e00' <= c <= '\u9fff']) / len(text) if text else 0
        english_ratio = len([c for c in text if c.isascii() and c.isalpha()]) / len(text) if text else 0
        has_code = '```' in text or 'def ' in text or 'function ' in text
        
        # 推荐逻辑
        if has_code:
            return "smart"  # 代码用智能压缩
        elif chinese_ratio > 0.5:
            return "wenyan"  # 中文多用文言文
        elif english_ratio > 0.5:
            return "english"  # 英文多用英语压缩
        else:
            return "smart"  # 默认智能压缩
    
    def compress(self, text: str, mode: str = None, level: str = None, show_stats: bool = None) -> dict:
        """
        压缩文本
        
        Args:
            text: 原始文本
            mode: 压缩模式 (auto/wenyan/english/smart)
            level: 压缩级别 (light/medium/aggressive)
            show_stats: 是否显示统计
        
        Returns:
            {
                "original": 原文,
                "compressed": 压缩后,
                "mode": 使用的模式,
                "stats": 统计信息
            }
        """
        # 检查是否开启节省模式
        if not self.config["enabled"]:
            return {
                "original": text,
                "compressed": text,
                "mode": "disabled",
                "stats": {"saved_chars": 0, "compression_ratio": 0}
            }
        
        # 使用默认值
        if mode is None:
            mode = self.config.get("default_mode", "auto")
        if level is None:
            level = self.config.get("default_level", "medium")
        if show_stats is None:
            show_stats = self.config.get("show_stats", True)
        
        # 自动模式：智能推荐
        if mode == "auto":
            mode = self.recommend_mode(text)
        
        # 检查缓存
        if self.cache and self.config.get("auto_cache"):
            cached = self.cache.get_compressed(text, mode)
            if cached:
                compressed = cached
            else:
                compressed = self._do_compress(text, mode, level)
                self.cache.save_compressed(text, compressed, mode)
        else:
            compressed = self._do_compress(text, mode, level)
        
        # 计算统计
        stats = {
            "original_length": len(text),
            "compressed_length": len(compressed),
            "saved_chars": len(text) - len(compressed),
            "compression_ratio": round((1 - len(compressed) / len(text)) * 100, 2) if text else 0,
        }
        
        # 计算 token
        if self.counter:
            stats["original_tokens"] = self.counter.estimate_tokens(text)
            stats["compressed_tokens"] = self.counter.estimate_tokens(compressed)
            stats["saved_tokens"] = stats["original_tokens"] - stats["compressed_tokens"]
            
            # 计算成本
            model = self.config.get("default_model", "gpt-4")
            cost_info = self.counter.calculate_cost(stats["original_tokens"], 100, model)
            stats["original_cost"] = cost_info["total_cost_usd"]
            
            cost_info = self.counter.calculate_cost(stats["compressed_tokens"], 100, model)
            stats["compressed_cost"] = cost_info["total_cost_usd"]
            stats["saved_cost"] = stats["original_cost"] - stats["compressed_cost"]
        
        # 保存到历史
        self._add_to_history(text, compressed, mode, stats)
        
        # 显示统计
        if show_stats:
            self._print_stats(text, compressed, mode, stats)
        
        return {
            "original": text,
            "compressed": compressed,
            "mode": mode,
            "stats": stats,
        }
    
    def _do_compress(self, text: str, mode: str, level: str) -> str:
        """执行压缩"""
        if mode == "wenyan" and self.wenyan:
            return self.wenyan.translate(text)
        
        elif mode == "english" and self.english:
            result = self.english.compress(text, level)
            return result["compressed"]
        
        elif mode == "smart" and self.smart:
            result = self.smart.compress(text, level)
            return result["compressed"]
        
        else:
            # 降级：简单压缩
            return text
    
    def _print_stats(self, original: str, compressed: str, mode: str, stats: dict):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print(f"压缩模式: {mode}")
        print("=" * 60)
        
        print(f"\n原文 ({stats['original_length']} 字):")
        print(f"  {original[:50]}{'...' if len(original) > 50 else ''}")
        
        print(f"\n压缩后 ({stats['compressed_length']} 字):")
        print(f"  {compressed}")
        
        print(f"\n✨ 节省: {stats['saved_chars']} 字 ({stats['compression_ratio']}%)")
        
        if "saved_tokens" in stats:
            print(f"💰 节省: {stats['saved_tokens']} tokens")
            print(f"💵 节省: ${stats['saved_cost']:.6f}")
        
        print("=" * 60)
    
    def _add_to_history(self, original: str, compressed: str, mode: str, stats: dict):
        """添加到历史"""
        history = self._load_history()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "original": original[:100],  # 只保存前100字符
            "compressed": compressed,
            "mode": mode,
            "saved_chars": stats["saved_chars"],
            "compression_ratio": stats["compression_ratio"],
        }
        
        history.append(entry)
        self._save_history(history)
    
    def show_history(self, limit: int = 10):
        """显示历史"""
        history = self._load_history()
        
        if not history:
            print("暂无历史记录")
            return
        
        print("=" * 70)
        print("压缩历史")
        print("=" * 70)
        
        for i, entry in enumerate(history[-limit:], 1):
            print(f"\n{i}. [{entry['timestamp'][:16]}]")
            print(f"   模式: {entry['mode']}")
            print(f"   原文: {entry['original'][:50]}...")
            print(f"   压缩: {entry['compressed'][:50]}...")
            print(f"   节省: {entry['saved_chars']} 字 ({entry['compression_ratio']}%)")
        
        print("=" * 70)
    
    def batch_process(self, input_dir: str, output_dir: str = None, mode: str = "auto"):
        """批量处理"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"❌ 目录不存在: {input_dir}")
            return
        
        if output_dir is None:
            output_dir = str(input_path.parent / f"{input_path.name}_compressed")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"正在处理: {input_dir}")
        print(f"输出目录: {output_dir}")
        print("=" * 60)
        
        total_saved = 0
        total_files = 0
        
        for file_path in input_path.rglob("*.md"):
            if file_path.is_file():
                # 读取文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 压缩
                result = self.compress(content, mode=mode, show_stats=False)
                
                # 计算相对路径
                rel_path = file_path.relative_to(input_path)
                output_file = output_path / rel_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 写入文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result["compressed"])
                
                saved = result["stats"]["saved_chars"]
                ratio = result["stats"]["compression_ratio"]
                total_saved += saved
                total_files += 1
                
                print(f"✓ {rel_path}: 节省 {saved} 字 ({ratio}%)")
        
        print("=" * 60)
        print(f"处理完成: {total_files} 个文件")
        print(f"总共节省: {total_saved} 字")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Token Saver - 智能节省 AI Token",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  token-saver "你的文本"                # 自动压缩
  token-saver "文本" --mode wenyan      # 文言文模式
  token-saver "文本" --level aggressive # 激进压缩
  token-saver --batch ./docs/           # 批量处理
  token-saver --enable                  # 开启节省模式
  token-saver --disable                 # 关闭节省模式
  token-saver --status                  # 查看状态
  token-saver --history                 # 查看历史
        """
    )
    
    parser.add_argument("text", nargs="?", help="要压缩的文本")
    parser.add_argument("--mode", "-m", choices=["auto", "wenyan", "english", "smart"],
                       default=None, help="压缩模式")
    parser.add_argument("--level", "-l", choices=["light", "medium", "aggressive"],
                       default=None, help="压缩级别")
    parser.add_argument("--stats", "-s", action="store_true", help="显示统计")
    parser.add_argument("--batch", "-b", metavar="DIR", help="批量处理目录")
    parser.add_argument("--output", "-o", metavar="DIR", help="输出目录")
    parser.add_argument("--enable", action="store_true", help="开启节省模式")
    parser.add_argument("--disable", action="store_true", help="关闭节省模式")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--history", action="store_true", help="查看历史")
    
    args = parser.parse_args()
    
    saver = TokenSaver()
    
    # 处理各种命令
    if args.enable:
        saver.enable()
        return
    
    if args.disable:
        saver.disable()
        return
    
    if args.status:
        saver.status()
        return
    
    if args.history:
        saver.show_history()
        return
    
    if args.batch:
        saver.batch_process(args.batch, args.output, args.mode or "auto")
        return
    
    # 压缩文本
    if args.text:
        result = saver.compress(
            args.text,
            mode=args.mode,
            level=args.level,
            show_stats=True
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
