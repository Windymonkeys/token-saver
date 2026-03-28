---
name: token-saver
description: 当用户希望节省 Token、压缩文本、提高对话效率时使用。触发关键词：文言、古文、翻译、压缩、JSON、模板、格式化、结构化、英语压缩、对话摘要、RAG优化。支持多种压缩模式和多模型Token计算。安装后默认开启节省模式，可通过命令开启/关闭。
---

# Token Saver - Token 节省技能

## ⚡ 快速使用

### 命令行工具

```bash
# 压缩文本（自动选择最佳方式）
token-saver "你的文本"

# 全局开关
token-saver --enable       # 开启节省模式（默认已开启）
token-saver --disable      # 关闭节省模式
token-saver --status       # 查看状态

# 批量处理
token-saver --batch ./docs/

# 查看历史
token-saver --history
```

---

## 触发条件

**文言文模式触发词**：
- "用文言文说..."
- "翻译成文言"
- "压缩这段话"

**结构化模式触发词**：
- "用 JSON 格式"
- "给我一个模板"
- "格式化输出"

**英语压缩触发词**：
- "压缩英语"
- "简化英语文本"

**其他触发词**：
- "计算 token"
- "对话摘要"
- "RAG 优化"

---

## 核心功能

### 1. 统一命令行工具

`scripts/token-saver.py` - 一站式压缩工具

**特性**：
- ✅ 默认开启节省模式
- ✅ 智能推荐最佳压缩方式
- ✅ 支持全局开关（enable/disable）
- ✅ 批量处理文件夹
- ✅ 历史记录查看
- ✅ Token 成本计算

### 2. 文言文压缩

`references/wenyan_mapping.json`（450+ 词条）

### 3. 智能上下文压缩

`scripts/smart_compress.py` - 语义权重分析

### 4. 英语压缩

`scripts/english_compressor.py`

### 5. Token 计算器

`scripts/token_counter.py` - 支持 10+ 主流模型

### 6. Prompt 模板库

`references/prompt_templates.md` - 8 大类 30+ 模板

### 7. 对话历史摘要

`scripts/session_summarizer.py`

### 8. RAG 优化

`scripts/rag_optimizer.py`

### 9. 缓存机制

`scripts/cache.py` - LRU 缓存

---

## 安装

### 自动安装

```bash
cd ~/.workbuddy/skills/token-saver
bash scripts/install.sh
```

### 手动安装

```bash
# 添加别名
echo 'alias token-saver="python3 ~/.workbuddy/skills/token-saver/scripts/token-saver.py"' >> ~/.zshrc
source ~/.zshrc
```

---

## 使用示例

### 开启/关闭节省模式

```
用户：token-saver --disable
AI：❌ Token 节省模式已关闭
    输入文本将保持原样

用户：token-saver --enable
AI：✅ Token 节省模式已开启
    所有输入文本将自动压缩
```

### 自动压缩

```
用户：token-saver "今天我在使用这个功能的时候发现了一个问题"
AI：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
压缩模式: wenyan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

原文 (19 字):
  今天我在使用这个功能的时候发现了一个问题

压缩后 (12 字):
  今日吾用此功能时发现一疑

✨ 节省: 7 字 (36.84%)
💰 节省: 4 tokens
💵 节省: $0.000120
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 批量处理

```
用户：token-saver --batch ./docs/
AI：
正在处理: ./docs/
输出目录: ./docs_compressed/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ report.md: 节省 42 字 (35%)
✓ api.md: 节省 28 字 (28%)
✓ tutorial.md: 节省 56 字 (51%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
处理完成: 3 个文件
总共节省: 126 字
```

---

## 配置

位置：`~/.token-saver/config.json`

```json
{
  "enabled": true,
  "default_mode": "auto",
  "default_level": "medium",
  "default_model": "gpt-4",
  "show_stats": true,
  "auto_cache": true,
  "max_history": 100
}
```

---

## 文件结构

```
token-saver/
├── scripts/
│   ├── token-saver.py          # 统一入口 ⭐
│   ├── install.sh              # 安装脚本
│   ├── translate.py            # 文言文转换
│   ├── smart_compress.py       # 智能压缩
│   ├── english_compressor.py   # 英语压缩
│   ├── token_counter.py        # Token 计算
│   ├── session_summarizer.py   # 对话摘要
│   ├── rag_optimizer.py        # RAG 优化
│   └── cache.py                # 缓存机制
├── references/
│   ├── wenyan_mapping.json     # 文言文词库
│   ├── struct_templates.md     # 结构化模板
│   └── prompt_templates.md     # Prompt 模板
├── tests/
│   └── test_cases.json
└── SKILL.md
```

---

## 效果分析

| 功能 | 平均节省率 | 最佳场景 |
|------|-----------|----------|
| 文言文压缩 | 20-40% | 中文长文本 |
| 智能压缩 | 25-80% | 问题描述 |
| 英语压缩 | 15-30% | 英文文档 |
| RAG 优化 | 30-60% | 检索结果 |
| 对话摘要 | 50-70% | 多轮对话 |
