#!/usr/bin/env python3
"""
RAG 检索结果优化模块
压缩和优化检索到的文档片段

功能：
1. 提取关键句子
2. 去除重复内容
3. 合并相似段落
4. 生成精简摘要
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class Document:
    """文档片段"""
    content: str
    source: str = ""
    score: float = 0.0


class RAGOptimizer:
    """RAG 优化器"""
    
    def __init__(self):
        # 关键词权重
        self.keyword_patterns = [
            r'\b\d+\b',  # 数字
            r'\b[A-Z]{2,}\b',  # 缩写
            r'(function|class|method|api|error|bug|issue)',  # 技术词
            r'(重要|关键|必须|注意|警告)',  # 强调词
        ]
        
        # 噪音句子模式
        self.noise_patterns = [
            r'^(例如|比如|举例来说)',
            r'^(如图所示|如下图)',
            r'^(参见|参考)',
            r'(点击这里|查看更多|了解更多)',
        ]
    
    def extract_sentences(self, text: str) -> List[str]:
        """提取句子"""
        # 按句号、问号、感叹号分割
        sentences = re.split(r'[。！？.!?]\s*', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def calculate_sentence_importance(self, sentence: str, query: str = "") -> float:
        """计算句子重要性"""
        score = 0.0
        
        # 长度分数（适中的长度更重要）
        length = len(sentence)
        if 20 <= length <= 100:
            score += 1.0
        elif length < 10:
            score -= 0.5
        
        # 关键词分数
        for pattern in self.keyword_patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            score += len(matches) * 0.5
        
        # 查询相关性
        if query:
            query_words = set(query.lower().split())
            sentence_words = set(sentence.lower().split())
            overlap = len(query_words & sentence_words)
            score += overlap * 0.3
        
        # 惩罚噪音句子
        for pattern in self.noise_patterns:
            if re.search(pattern, sentence):
                score -= 1.0
        
        return score
    
    def remove_duplicates(self, sentences: List[str], threshold: float = 0.8) -> List[str]:
        """去除重复句子"""
        unique = []
        
        for sentence in sentences:
            is_duplicate = False
            
            for existing in unique:
                # 简单的相似度计算
                similarity = self._calculate_similarity(sentence, existing)
                if similarity > threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(sentence)
        
        return unique
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单版本）"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def merge_similar_paragraphs(self, paragraphs: List[str]) -> List[str]:
        """合并相似段落"""
        if len(paragraphs) <= 1:
            return paragraphs
        
        merged = []
        current = paragraphs[0]
        
        for i in range(1, len(paragraphs)):
            similarity = self._calculate_similarity(current, paragraphs[i])
            
            if similarity > 0.5:
                # 合并
                current = current + " " + paragraphs[i]
            else:
                merged.append(current)
                current = paragraphs[i]
        
        merged.append(current)
        return merged
    
    def extract_key_sentences(self, text: str, query: str = "", top_k: int = 5) -> List[str]:
        """提取关键句子"""
        sentences = self.extract_sentences(text)
        
        # 计算重要性
        scored = [
            (sentence, self.calculate_sentence_importance(sentence, query))
            for sentence in sentences
        ]
        
        # 排序
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前 K 个
        return [s[0] for s in scored[:top_k]]
    
    def optimize(self, documents: List[Document], query: str = "", max_length: int = 500) -> Dict:
        """
        优化 RAG 检索结果
        
        Args:
            documents: 文档列表
            query: 查询字符串
            max_length: 最大长度
        
        Returns:
            {
                "original": 原始内容,
                "optimized": 优化后内容,
                "stats": 统计信息
            }
        """
        # 提取所有句子
        all_sentences = []
        for doc in documents:
            sentences = self.extract_sentences(doc.content)
            all_sentences.extend(sentences)
        
        # 去重
        unique_sentences = self.remove_duplicates(all_sentences)
        
        # 提取关键句子
        key_sentences = self.extract_key_sentences(
            " ".join(unique_sentences),
            query,
            top_k=10
        )
        
        # 组合结果
        optimized = "。".join(key_sentences)
        
        # 截断到最大长度
        if len(optimized) > max_length:
            optimized = optimized[:max_length] + "..."
        
        # 统计
        original_length = sum(len(doc.content) for doc in documents)
        
        stats = {
            "original_length": original_length,
            "optimized_length": len(optimized),
            "saved_chars": original_length - len(optimized),
            "compression_ratio": round((1 - len(optimized) / original_length) * 100, 2) if original_length else 0,
            "original_documents": len(documents),
            "original_sentences": len(all_sentences),
            "unique_sentences": len(unique_sentences),
            "key_sentences": len(key_sentences),
        }
        
        return {
            "original": "\n\n".join(doc.content for doc in documents),
            "optimized": optimized,
            "stats": stats,
        }


def main():
    """测试入口"""
    optimizer = RAGOptimizer()
    
    # 模拟 RAG 检索结果
    documents = [
        Document(
            content="Python 是一种高级编程语言，由 Guido van Rossum 创建。Python 的设计哲学强调代码的可读性。Python 支持多种编程范式。",
            source="doc1.md",
            score=0.9
        ),
        Document(
            content="Python 广泛应用于 Web 开发、数据分析、人工智能等领域。Python 拥有丰富的第三方库，如 NumPy、Pandas、TensorFlow。",
            source="doc2.md",
            score=0.85
        ),
        Document(
            content="Python 3.0 于 2008 年发布。Python 2.7 是 Python 2 的最后一个版本，于 2020 年停止维护。建议使用 Python 3.x。",
            source="doc3.md",
            score=0.8
        ),
    ]
    
    query = "Python 应用场景"
    
    print("=" * 70)
    print("RAG 优化测试")
    print("=" * 70)
    
    print(f"\n查询: {query}")
    print(f"\n原始文档数: {len(documents)}")
    
    result = optimizer.optimize(documents, query)
    
    print("\n【原始内容】")
    print(result["original"][:200] + "...")
    
    print("\n【优化后内容】")
    print(result["optimized"])
    
    print("\n【统计】")
    for key, value in result["stats"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
