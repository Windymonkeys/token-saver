#!/usr/bin/env python3
"""
对话历史摘要模块
自动总结多轮对话内容，提取关键信息

功能：
1. 识别核心决策
2. 提取待办事项
3. 标记已解决/未解决问题
4. 生成结构化摘要
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """消息"""
    role: str  # user/assistant
    content: str
    timestamp: str = ""


@dataclass
class SessionSummary:
    """会话摘要"""
    topic: str = ""
    decisions: List[str] = field(default_factory=list)
    completed: List[str] = field(default_factory=list)
    pending: List[str] = field(default_factory=list)
    key_files: List[str] = field(default_factory=list)
    key_concepts: List[str] = field(default_factory=list)
    token_saved: int = 0


class SessionSummarizer:
    """对话摘要器"""
    
    def __init__(self):
        # 决策标记词
        self.decision_markers = [
            r'(决定|确定|选择|采用|使用)',
            r'(最终|最后)',
            r'(方案[ABCD]?\d*)',
        ]
        
        # 待办标记词
        self.todo_markers = [
            r'(需要|要|必须)',
            r'(待|等待)',
            r'(TODO|FIXME)',
            r'(下一步|接下来)',
        ]
        
        # 完成标记词
        self.done_markers = [
            r'(完成|已|成功)',
            r'(解决|修复)',
            r'(✓|✅)',
        ]
        
        # 文件路径模式
        self.file_pattern = r'[~/]?[\w/.-]+\.[a-zA-Z]{1,4}'
        
        # 技术术语模式
        self.tech_pattern = r'[A-Z]{2,}|API|SDK|CLI|GUI'
    
    def extract_decisions(self, messages: List[Message]) -> List[str]:
        """提取决策"""
        decisions = []
        
        for msg in messages:
            for pattern in self.decision_markers:
                matches = re.findall(f'{pattern}(.{{1,50}})', msg.content)
                for match in matches:
                    decision = match.strip()
                    if len(decision) > 5:
                        decisions.append(decision)
        
        return list(set(decisions))[:5]  # 最多5条
    
    def extract_todos(self, messages: List[Message]) -> Tuple[List[str], List[str]]:
        """提取待办和已完成事项"""
        pending = []
        completed = []
        
        for msg in messages:
            # 检查待办
            for pattern in self.todo_markers:
                matches = re.findall(f'{pattern}(.{{1,50}})', msg.content)
                for match in matches:
                    todo = match.strip()
                    if len(todo) > 5:
                        pending.append(todo)
            
            # 检查完成
            for pattern in self.done_markers:
                matches = re.findall(f'{pattern}(.{{1,50}})', msg.content)
                for match in matches:
                    done = match.strip()
                    if len(done) > 5:
                        completed.append(done)
        
        # 去重
        pending = list(set(pending))[:5]
        completed = list(set(completed))[:5]
        
        # 移除已完成的事项
        pending = [p for p in pending if not any(c in p for c in completed)]
        
        return pending, completed
    
    def extract_files(self, messages: List[Message]) -> List[str]:
        """提取文件路径"""
        files = []
        
        for msg in messages:
            matches = re.findall(self.file_pattern, msg.content)
            files.extend(matches)
        
        return list(set(files))[:10]
    
    def extract_tech_terms(self, messages: List[Message]) -> List[str]:
        """提取技术术语"""
        terms = []
        
        for msg in messages:
            matches = re.findall(self.tech_pattern, msg.content)
            terms.extend(matches)
        
        return list(set(terms))[:10]
    
    def infer_topic(self, messages: List[Message]) -> str:
        """推断对话主题"""
        if not messages:
            return ""
        
        # 从第一条用户消息推断主题
        first_user_msg = next((m for m in messages if m.role == "user"), None)
        if not first_user_msg:
            return ""
        
        content = first_user_msg.content
        
        # 提取关键词
        keywords = re.findall(r'[\u4e00-\u9fff]{2,}|[A-Z][a-z]+', content)
        
        if keywords:
            return " ".join(keywords[:3])
        
        return content[:50]
    
    def summarize(self, messages: List[Message]) -> SessionSummary:
        """生成对话摘要"""
        summary = SessionSummary()
        
        # 推断主题
        summary.topic = self.infer_topic(messages)
        
        # 提取决策
        summary.decisions = self.extract_decisions(messages)
        
        # 提取待办和完成
        summary.pending, summary.completed = self.extract_todos(messages)
        
        # 提取文件
        summary.key_files = self.extract_files(messages)
        
        # 提取技术术语
        summary.key_concepts = self.extract_tech_terms(messages)
        
        # 估算节省的 token
        original_length = sum(len(m.content) for m in messages)
        summary_length = len(summary.topic) + sum(len(d) for d in summary.decisions) + \
                        sum(len(p) for p in summary.pending) + sum(len(c) for c in summary.completed)
        summary.token_saved = original_length - summary_length
        
        return summary
    
    def to_json(self, summary: SessionSummary) -> Dict:
        """转换为 JSON 格式"""
        return {
            "session_summary": {
                "topic": summary.topic,
                "decisions": summary.decisions,
                "completed": summary.completed,
                "pending": summary.pending,
                "key_files": summary.key_files,
                "key_concepts": summary.key_concepts,
            },
            "stats": {
                "original_messages": 0,  # 需要外部传入
                "token_saved": summary.token_saved,
            }
        }
    
    def to_markdown(self, summary: SessionSummary) -> str:
        """转换为 Markdown 格式"""
        md = f"""# 会话摘要

## 主题
{summary.topic}

## 决策
"""
        for i, decision in enumerate(summary.decisions, 1):
            md += f"{i}. {decision}\n"
        
        md += "\n## 已完成\n"
        for item in summary.completed:
            md += f"- ✓ {item}\n"
        
        md += "\n## 待办\n"
        for item in summary.pending:
            md += f"- [ ] {item}\n"
        
        if summary.key_files:
            md += "\n## 关键文件\n"
            for file in summary.key_files:
                md += f"- `{file}`\n"
        
        if summary.key_concepts:
            md += "\n## 关键概念\n"
            md += ", ".join(summary.key_concepts)
        
        return md


def main():
    """测试入口"""
    summarizer = SessionSummarizer()
    
    # 模拟对话
    messages = [
        Message(role="user", content="我想创建一个 token-saver 技能，用于节省 AI 对话的 token"),
        Message(role="assistant", content="好的，我们可以用文言文压缩和结构化输出来节省 token"),
        Message(role="user", content="决定使用文言文压缩方案"),
        Message(role="assistant", content="已完成词库创建，位于 ~/.workbuddy/skills/token-saver/references/wenyan_mapping.json"),
        Message(role="user", content="需要添加一个自动化脚本"),
        Message(role="assistant", content="好的，我会创建 translate.py 脚本"),
        Message(role="user", content="脚本已完成，现在需要推送到 GitHub"),
        Message(role="assistant", content="已成功推送到 https://github.com/Windymonkeys/token-saver"),
    ]
    
    summary = summarizer.summarize(messages)
    
    print("=" * 70)
    print("对话历史摘要测试")
    print("=" * 70)
    
    print("\n【JSON 格式】")
    print(json.dumps(summarizer.to_json(summary), ensure_ascii=False, indent=2))
    
    print("\n【Markdown 格式】")
    print(summarizer.to_markdown(summary))


if __name__ == "__main__":
    import json
    main()
