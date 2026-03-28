#!/usr/bin/env python3
"""
缓存机制模块
使用 LRU 策略缓存压缩结果，避免重复计算

功能：
1. LRU 缓存
2. 持久化存储
3. 缓存命中率统计
"""

import json
import hashlib
from typing import Dict, Optional, Any
from collections import OrderedDict
from pathlib import Path
from datetime import datetime


class LRUCache:
    """LRU 缓存"""
    
    def __init__(self, capacity: int = 1000, persist_file: str = None):
        """
        初始化 LRU 缓存
        
        Args:
            capacity: 缓存容量
            persist_file: 持久化文件路径
        """
        self.capacity = capacity
        self.cache = OrderedDict()
        self.persist_file = persist_file
        self.hits = 0
        self.misses = 0
        
        # 从文件加载缓存
        if persist_file:
            self._load_from_file()
    
    def _hash_key(self, key: str) -> str:
        """生成缓存键的哈希值"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值（如果存在），否则返回 None
        """
        hashed_key = self._hash_key(key)
        
        if hashed_key in self.cache:
            # 命中，移动到末尾（最近使用）
            self.cache.move_to_end(hashed_key)
            self.hits += 1
            return self.cache[hashed_key]
        
        self.misses += 1
        return None
    
    def put(self, key: str, value: Any) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        hashed_key = self._hash_key(key)
        
        if hashed_key in self.cache:
            # 已存在，更新并移动到末尾
            self.cache.move_to_end(hashed_key)
        
        self.cache[hashed_key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "original_key": key[:100],  # 保存原始键的前100字符
        }
        
        # 检查容量
        if len(self.cache) > self.capacity:
            # 删除最久未使用的项
            self.cache.popitem(last=False)
        
        # 持久化
        if self.persist_file:
            self._save_to_file()
    
    def _load_from_file(self) -> None:
        """从文件加载缓存"""
        if not self.persist_file:
            return
        
        path = Path(self.persist_file)
        if not path.exists():
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cache = OrderedDict(data.get("cache", {}))
                self.hits = data.get("hits", 0)
                self.misses = data.get("misses", 0)
        except Exception as e:
            print(f"加载缓存失败: {e}")
    
    def _save_to_file(self) -> None:
        """保存缓存到文件"""
        if not self.persist_file:
            return
        
        path = Path(self.persist_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = {
                "cache": dict(self.cache),
                "hits": self.hits,
                "misses": self.misses,
                "updated_at": datetime.now().isoformat(),
            }
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存失败: {e}")
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        
        if self.persist_file:
            self._save_to_file()
    
    def stats(self) -> Dict:
        """获取缓存统计"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "capacity": self.capacity,
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
        }
    
    def get_all_keys(self) -> list:
        """获取所有缓存键"""
        return [
            item.get("original_key", "")
            for item in self.cache.values()
        ]


class CompressionCache:
    """压缩结果缓存"""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "cache"
        
        cache_file = Path(cache_dir) / "compression_cache.json"
        self.cache = LRUCache(capacity=1000, persist_file=str(cache_file))
    
    def get_compressed(self, text: str, mode: str = "wenyan") -> Optional[str]:
        """
        获取压缩结果
        
        Args:
            text: 原始文本
            mode: 压缩模式
        
        Returns:
            压缩后的文本（如果存在）
        """
        key = f"{mode}:{text}"
        result = self.cache.get(key)
        
        if result:
            return result.get("value")
        
        return None
    
    def save_compressed(self, text: str, compressed: str, mode: str = "wenyan") -> None:
        """
        保存压缩结果
        
        Args:
            text: 原始文本
            compressed: 压缩后文本
            mode: 压缩模式
        """
        key = f"{mode}:{text}"
        self.cache.put(key, compressed)
    
    def get_stats(self) -> Dict:
        """获取缓存统计"""
        return self.cache.stats()


def main():
    """测试入口"""
    cache = CompressionCache()
    
    print("=" * 70)
    print("缓存机制测试")
    print("=" * 70)
    
    # 测试数据
    test_texts = [
        "今天我在使用这个功能的时候发现了一个问题",
        "我认为这个结果很好",
        "因为他很努力，所以成功了",
    ]
    
    print("\n【首次访问（应该全部 miss）】")
    for text in test_texts:
        result = cache.get_compressed(text)
        print(f"  '{text[:20]}...' -> {'命中' if result else '未命中'}")
    
    print("\n【模拟压缩并保存】")
    for text in test_texts:
        # 模拟压缩
        compressed = text[:10] + "...（压缩）"
        cache.save_compressed(text, compressed)
        print(f"  保存: '{text[:20]}...'")
    
    print("\n【再次访问（应该全部 hit）】")
    for text in test_texts:
        result = cache.get_compressed(text)
        print(f"  '{text[:20]}...' -> {'命中: ' + result if result else '未命中'}")
    
    print("\n【缓存统计】")
    stats = cache.get_stats()
    print(f"  容量: {stats['capacity']}")
    print(f"  大小: {stats['size']}")
    print(f"  命中: {stats['hits']}")
    print(f"  未命中: {stats['misses']}")
    print(f"  命中率: {stats['hit_rate']}%")


if __name__ == "__main__":
    main()
