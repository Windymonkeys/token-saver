# 结构化输出模板库

本文件提供常用的结构化输出模板，用于减少自然语言描述，提升 Token 效率。

---

## 1. JSON Schema 模板

### API 标准响应
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 分页数据
```json
{
  "items": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### 列表数据
```json
{
  "items": [],
  "count": 0,
  "hasMore": false
}
```

### 嵌套对象
```json
{
  "user": {
    "id": "",
    "name": "",
    "email": "",
    "profile": {
      "avatar": "",
      "bio": ""
    }
  }
}
```

### 批量操作结果
```json
{
  "success": [],
  "failed": [],
  "total": 0,
  "successCount": 0,
  "failedCount": 0
}
```

---

## 2. Markdown 表格模板

### 基础表格
```
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 内容 | 内容 | 内容 |
```

### 对齐表格
```
| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| 内容 | 内容 | 内容 |
```

### 功能对比表
```
| 功能 | 版本A | 版本B |
|------|-------|-------|
| 特性1 | ✓ | ✗ |
| 特性2 | ✓ | ✓ |
```

### 状态表
```
| 任务 | 状态 | 备注 |
|------|------|------|
| | 待办/进行中/完成 | |
```

---

## 3. 代码注释模板

### JavaScript 函数
```javascript
/**
 * 函数功能简述
 * @param {类型} 参数名 - 参数描述
 * @returns {类型} 返回值描述
 */
```

### Python 函数
```python
def function_name(param: type) -> return_type:
    """
    函数功能简述
    
    Args:
        param: 参数描述
    
    Returns:
        返回值描述
    """
```

### TypeScript 接口
```typescript
/**
 * 接口描述
 */
interface IExample {
  /** 属性描述 */
  property: type;
}
```

### TODO 注释
```javascript
// TODO: 待完成事项
// FIXME: 已知问题
// NOTE: 注意事项
// HACK: 临时方案
```

---

## 4. API 文档模板

### RESTful API
```
## 接口名称

**METHOD** `/api/path`

### 参数
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| | | | |

### 响应
```json
{}
```

### 示例
```bash
curl -X METHOD "url"
```
```

### GraphQL 查询
```graphql
query QueryName($var: Type) {
  field(arg: $var) {
    subField
  }
}
```

---

## 5. 配置文件模板

### package.json
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "scripts": {},
  "dependencies": {}
}
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true
  }
}
```

### .env
```bash
# 环境变量
NODE_ENV=development
API_URL=
DB_HOST=
```

### Docker Compose
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
```

---

## 6. 数据结构模板

### 树形结构
```json
{
  "id": "",
  "name": "",
  "children": []
}
```

### 图结构
```json
{
  "nodes": [
    { "id": "", "label": "" }
  ],
  "edges": [
    { "from": "", "to": "" }
  ]
}
```

### 状态机
```json
{
  "states": ["state1", "state2"],
  "initial": "state1",
  "transitions": {
    "state1": ["state2"]
  }
}
```

---

## 7. 测试用例模板

### 单元测试
```javascript
describe('模块名', () => {
  test('测试用例描述', () => {
    // arrange
    // act
    // assert
  });
});
```

### 测试数据
```json
{
  "testCases": [
    {
      "id": "TC001",
      "input": {},
      "expected": {},
      "actual": null
    }
  ]
}
```

---

## 8. 项目文档模板

### README 结构
```markdown
# 项目名称

简短描述

## 安装

## 使用

## API

## 配置

## 贡献

## 许可证
```

### CHANGELOG
```markdown
## [1.0.0] - 2024-01-01

### Added
- 新功能

### Changed
- 变更

### Fixed
- 修复
```

---

## 使用建议

| 场景 | 推荐模板 |
|------|----------|
| API 设计 | JSON Schema + API 文档 |
| 数据结构 | JSON Schema |
| 代码注释 | 函数/接口注释 |
| 功能对比 | Markdown 表格 |
| 测试 | 测试用例模板 |
| 配置 | 对应配置文件模板 |
