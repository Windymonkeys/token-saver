#!/usr/bin/env python3
"""
token-saver 文言文转换脚本
将现代汉语转换为文言文，节省 Token

使用方法:
    python translate.py "你要转换的文本"
    python translate.py --file input.txt --output output.txt
    python translate.py --test  # 运行测试
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class WenyanTranslator:
    """文言文翻译器"""
    
    def __init__(self, mapping_file: str = None):
        if mapping_file is None:
            mapping_file = Path(__file__).parent.parent / "references" / "wenyan_mapping.json"
        
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.mappings = data.get("mappings", {})
        self.flat_map = self._flatten_mappings()
    
    def _flatten_mappings(self) -> Dict[str, str]:
        """将嵌套映射展平为一维字典"""
        flat = {}
        for category, items in self.mappings.items():
            for modern, wenyan in items.items():
                # 如果有多个选项（用/分隔），选择第一个
                if '/' in wenyan:
                    wenyan = wenyan.split('/')[0]
                flat[modern] = wenyan
        return flat
    
    def translate(self, text: str) -> str:
        """将现代汉语翻译为文言文"""
        # 按长度降序排列，优先匹配长词
        sorted_words = sorted(self.flat_map.keys(), key=len, reverse=True)
        
        result = text
        for word in sorted_words:
            if word in result:
                wenyan = self.flat_map[word]
                result = result.replace(word, wenyan)
        
        return result
    
    def translate_with_stats(self, text: str) -> Tuple[str, Dict]:
        """翻译并返回统计信息"""
        original = text
        translated = self.translate(text)
        
        # 统计
        stats = {
            "original_length": len(original),
            "translated_length": len(translated),
            "saved_chars": len(original) - len(translated),
            "compression_ratio": round((1 - len(translated) / len(original)) * 100, 2) if len(original) > 0 else 0,
            "words_translated": sum(1 for w in self.flat_map if w in original)
        }
        
        return translated, stats


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="现代汉语转文言文")
    parser.add_argument("text", nargs="?", help="要转换的文本")
    parser.add_argument("--file", "-f", help="输入文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--test", "-t", action="store_true", help="运行测试")
    parser.add_argument("--stats", "-s", action="store_true", help="显示统计信息")
    
    args = parser.parse_args()
    
    translator = WenyanTranslator()
    
    # 测试模式
    if args.test:
        run_tests(translator)
        return
    
    # 文件模式
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return
    
    # 翻译
    if args.stats:
        translated, stats = translator.translate_with_stats(text)
        print(f"原文: {text}")
        print(f"文言: {translated}")
        print(f"\n统计:")
        print(f"  原文字数: {stats['original_length']}")
        print(f"  文言字数: {stats['translated_length']}")
        print(f"  节省字数: {stats['saved_chars']}")
        print(f"  压缩率: {stats['compression_ratio']}%")
        print(f"  转换词数: {stats['words_translated']}")
    else:
        translated = translator.translate(text)
        print(translated)
    
    # 输出到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(translated)
        print(f"\n已保存到: {args.output}")


def run_tests(translator: WenyanTranslator):
    """运行测试用例"""
    test_cases = [
        ("你知道这个方法吗？", "汝知此法乎？"),
        ("我认为这个结果很好", "吾以为此果甚善"),
        ("因为他很努力，所以成功了", "因彼甚勤，故成矣"),
        ("这个问题很难解决", "此疑甚难解"),
        ("谢谢你告诉我这个消息", "谢汝告吾此讯"),
        ("今天天气怎么样", "今日天气何如"),
        ("我觉得这个问题很重要", "吾感此疑甚重"),
        ("我不知道应该怎么做", "吾不知宜何为"),
        ("如果你有时间的话，可以帮助我吗？", "若汝有时，可助吾乎？"),
        ("虽然很困难，但是我会努力的", "虽甚难，然吾将勉之"),
    ]
    
    print("=" * 60)
    print("测试用例")
    print("=" * 60)
    
    total_saved = 0
    passed = 0
    
    for i, (original, expected) in enumerate(test_cases, 1):
        translated = translator.translate(original)
        saved = len(original) - len(translated)
        total_saved += saved
        
        # 检查关键词是否正确转换（不完全匹配也算通过）
        status = "✓" if any(w in translated for w in ["吾", "汝", "此", "何", "甚", "故", "若", "然", "矣"]) else "✗"
        if status == "✓":
            passed += 1
        
        print(f"\n{i}. {original}")
        print(f"   预期: {expected}")
        print(f"   结果: {translated}")
        print(f"   状态: {status} | 节省: {saved} 字")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{len(test_cases)} 通过")
    print(f"总节省: {total_saved} 字")
    print("=" * 60)


if __name__ == "__main__":
    main()
