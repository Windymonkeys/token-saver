# 结构化输出模板库

本文件提供常用的结构化输出模板，用于减少自然语言描述，提升 Token 效率。

## 使用方式

在需要输出结构化内容时，选择对应模板并填充数据。

---

## 1. JSON Schema 模板

### 基础对象
```json
{
  "type": "object",
  "properties": {
    "field_name": {
      "type": "string|number|boolean|array|object",
      "description": "字段说明",
      "required": true|false
    }
  },
  "required": ["field_name"]
}
```

### 响应格式
```json
{
  "success": true|false,
  "data": {},
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

### 分页结果
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
  "hasMore": true|false
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
|:-------|:----:|------:|
| 内容 | 内容 | 内容 |
```

### 复杂表头
```
| 功能 | 描述 | 参数 | 返回值 |
|------|------|------|--------|
| | | | |
```

---

## 3. 代码注释模板

### 函数注释
```javascript
/**
 * 函数功能简述
 * @param {类型} 参数名 - 参数描述
 * @param {类型} 参数名 - 参数描述
 * @returns {类型} 返回值描述
 * @throws {错误类型} 异常情况描述
 */
```

### 类注释
```javascript
/**
 * 类名：类功能描述
 * @class
 * @author 作者
 * @date 创建日期
 * @description 详细描述
 */
```

### 文件头注释
```javascript
/**
 * @file 文件名
 * @description 文件功能描述
 * @author 作者
 * @date 日期
 * @version 版本号
 */
```

### TODO 注释
```javascript
// TODO: [日期] 待完成事项 - 负责人
// FIXME: [日期] 已知问题 - 负责人
// NOTE: 注意事项
// HACK: 临时解决方案
```

---

## 4. API 响应模板

### 成功响应
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
  "code": 400|401|403|404|500,
  "message": "错误信息",
  "data": null
}
```

### 分页响应
```json
{
  "code": 200,
  "data": {
    "list": [],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 100
    }
  }
}
```

---

## 5. 数据字典模板

### 枚举值
```json
{
  "fieldName": {
    "type": "enum",
    "values": [
      { "value": "value1", "label": "标签1", "description": "描述" },
      { "value": "value2", "label": "标签2", "description": "描述" }
    ]
  }
}
```

### 字段定义
```json
{
  "fieldName": {
    "type": "string|number|boolean",
    "maxLength": 100,
    "required": true,
    "description": "字段描述",
    "example": "示例值"
  }
}
```

---

## 6. 状态机模板

```json
{
  "states": ["状态1", "状态2", "状态3"],
  "initial": "状态1",
  "transitions": {
    "状态1": ["状态2", "状态3"],
    "状态2": ["状态3"],
    "状态3": []
  },
  "finalStates": ["状态3"]
}
```

---

## 7. 测试用例模板

```json
{
  "testCases": [
    {
      "id": "TC001",
      "name": "用例名称",
      "input": {},
      "expected": {},
      "priority": "high|medium|low"
    }
  ]
}
```

---

## 8. 配置文件模板

### JSON 配置
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "config": {
    "key": "value"
  }
}
```

### 环境变量
```bash
# 格式: KEY=默认值 # 说明
ENV_VAR=value # 环境变量说明
```
