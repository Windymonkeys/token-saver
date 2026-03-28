#!/usr/bin/env python3
"""
英语文本压缩模块
去除冗余词汇，简化句子结构

优化策略：
1. 去除填充词 (very, really, basically...)
2. 简化冗长表达
3. 合并重复内容
4. 使用缩写形式
"""

import re
from typing import Dict, List, Tuple


class EnglishCompressor:
    """英语压缩器"""
    
    def __init__(self):
        # 填充词（可删除）
        self.filler_words = [
            r'\bvery\b', r'\breally\b', r'\bquite\b', r'\brather\b',
            r'\bactually\b', r'\bbasically\b', r'\bessentially\b',
            r'\bjust\b', r'\bsimply\b', r'\bmerely\b',
            r'\bsort of\b', r'\bkind of\b', r'\btype of\b',
            r'\ba little bit\b', r'\ba bit\b',
            r'\bI think\b', r'\bI believe\b', r'\bI feel\b',
            r'\bin my opinion\b', r'\bto be honest\b',
            r'\bto be fair\b', r'\bto be sure\b',
            r'\bfor the most part\b', r'\bmore or less\b',
        ]
        
        # 冗长表达 → 简洁表达
        self.word_replacements = {
            r'\bin order to\b': 'to',
            r'\bdue to the fact that\b': 'because',
            r'\bat this point in time\b': 'now',
            r'\bin the event that\b': 'if',
            r'\bfor the purpose of\b': 'for',
            r'\bin spite of the fact that\b': 'although',
            r'\bwith regard to\b': 'about',
            r'\bwith respect to\b': 'about',
            r'\bin terms of\b': 'about',
            r'\bfor the reason that\b': 'because',
            r'\bby means of\b': 'by',
            r'\bas a matter of fact\b': 'actually',
            r'\bat the present time\b': 'now',
            r'\bin the near future\b': 'soon',
            r'\buntil such time as\b': 'until',
            r'\bthe majority of\b': 'most',
            r'\ba large number of\b': 'many',
            r'\ba small number of\b': 'few',
            r'\bthe fact that\b': 'that',
            r'\bit is important to note that\b': 'note that',
            r'\bit should be noted that\b': 'note that',
            r'\bplease be advised that\b': 'note that',
            r'\bI would like to\b': 'I want to',
            r'\bI am going to\b': 'I will',
            r'\bI have to\b': 'I must',
            r'\bI need to\b': 'I must',
            r'\bwe are going to\b': 'we will',
            r'\bdo not\b': "don't",
            r'\bcannot\b': "can't",
            r'\bwill not\b': "won't",
            r'\bshould not\b': "shouldn't",
            r'\bwould not\b': "wouldn't",
            r'\bcould not\b': "couldn't",
        }
        
        # 被动语态 → 主动语态（简化）
        self.passive_to_active = {
            r'\bwas created by\b': 'created',
            r'\bwas developed by\b': 'developed',
            r'\bwas written by\b': 'wrote',
            r'\bwas designed by\b': 'designed',
            r'\bwas implemented by\b': 'implemented',
            r'\bhas been completed\b': 'completed',
            r'\bhas been done\b': 'done',
            r'\bneeds to be\b': 'must be',
        }
    
    def remove_fillers(self, text: str) -> str:
        """去除填充词"""
        result = text
        for pattern in self.filler_words:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        # 清理多余空格
        result = re.sub(r'\s+', ' ', result)
        return result.strip()
    
    def simplify_expressions(self, text: str) -> str:
        """简化冗长表达"""
        result = text
        for pattern, replacement in self.word_replacements.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
    
    def passive_to_active_voice(self, text: str) -> str:
        """被动语态转主动语态"""
        result = text
        for pattern, replacement in self.passive_to_active.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
    
    def compress(self, text: str, level: str = "medium") -> Dict:
        """
        压缩英语文本
        
        Args:
            text: 原始文本
            level: 压缩级别 (light/medium/aggressive)
        
        Returns:
            {
                "original": 原文,
                "compressed": 压缩后,
                "stats": 统计信息
            }
        """
        original = text
        
        if level == "light":
            # 轻度压缩：只简化表达
            compressed = self.simplify_expressions(text)
        
        elif level == "aggressive":
            # 激进压缩：全部优化
            compressed = self.remove_fillers(text)
            compressed = self.simplify_expressions(compressed)
            compressed = self.passive_to_active_voice(compressed)
        
        else:
            # 中等压缩（默认）
            compressed = self.remove_fillers(text)
            compressed = self.simplify_expressions(compressed)
        
        # 统计
        stats = {
            "original_length": len(original),
            "compressed_length": len(compressed),
            "saved_chars": len(original) - len(compressed),
            "compression_ratio": round((1 - len(compressed) / len(original)) * 100, 2) if original else 0,
        }
        
        return {
            "original": original,
            "compressed": compressed,
            "stats": stats,
        }


def main():
    """测试入口"""
    compressor = EnglishCompressor()
    
    # 测试用例
    test_cases = [
        "I think that we should probably consider the fact that the system was created by the development team and has been completed successfully.",
        "At this point in time, I would like to basically say that we really need to focus on the most important aspects of the project.",
        "The very large number of users are actually using the system on a daily basis, which is quite impressive.",
        "In order to achieve our goals, we need to implement a solution that will be created by our team in the near future.",
    ]
    
    print("=" * 70)
    print("英语压缩测试")
    print("=" * 70)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【测试 {i}】")
        print(f"原文: {text}")
        
        for level in ["light", "medium", "aggressive"]:
            result = compressor.compress(text, level)
            print(f"\n{level.upper()}: {result['compressed']}")
            print(f"节省: {result['stats']['saved_chars']} 字 ({result['stats']['compression_ratio']}%)")
        
        print("-" * 70)


if __name__ == "__main__":
    main()
