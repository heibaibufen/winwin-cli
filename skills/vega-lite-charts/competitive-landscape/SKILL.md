---
name: competitive-landscape
description: "生成竞争格局分析图（堆叠柱状图），展示多个集团/品牌在不同时期的市场份额对比和变化趋势。触发词：竞争格局、市场份额对比、多品牌份额、堆叠柱状图、竞争分析。"
---

# Competitive Landscape - 竞争格局分析图

生成堆叠柱状图，展示多个集团/品牌在不同时期的市场份额对比和变化趋势。

## 适用场景

- 竞争格局分析（多个品牌/集团的市场份额对比）
- 市场份额变化趋势（不同时期对比）
- 集团/品牌排名变化（CR5、CR10等集中度分析）
- 市场结构演变（头部品牌份额变化）

## 图表类型

**堆叠柱状图（Stacked Bar Chart）**：
- X 轴：时间周期（如 24Q4、25Q4）
- Y 轴：市场份额百分比
- 颜色：集团/品牌名称
- 堆叠方式：按市场份额从大到小堆叠

## MCP 工具

生成图表前，先用 vega-lite 知识库查询相关文档：

```bash
# 搜索 stack bar 相关文档
mcp__vega-lite__search_documents(query="stack bar chart")

# 查询 color 和 axis 文档
mcp__vega-lite__search_documents(query="color scale axis")
```

## 核心原则

**简单优先**：使用默认配置，堆叠柱状图特殊配置

1. **颜色**：使用 Vega-Lite 默认配色（不要自定义 scale 和 range）
2. **堆叠方式**：使用 `"stack": "normalize"` 显示百分比，或 `"stack": "zero"` 显示绝对值
3. **图例**：使用 `"orient": "right"` 避免遮挡图表
4. **排序**：按市场份额从大到小排序（在数据中直接排序）
5. **数据标签**：每个堆叠块显示百分比数值

## 示例

完整示例请参见 `examples.json` 文件，包含以下示例：

| 示例名称 | 说明 |
|---------|------|
| `standard_stacked_bar` | 标准堆叠柱状图（绝对值），展示总量变化和结构变化 |
| `percentage_stacked_bar` | 百分比堆叠柱状图（100%堆叠，推荐），按份额大小排序堆叠 |
| `grouped_bar` | 分组柱状图（并排对比），适合品牌数量少（<8个）的情况 |

### 使用示例

从 `examples.json` 中选择合适的示例，替换数据即可使用：

```python
# 读取示例
import json
with open('examples.json', 'r') as f:
    examples = json.load(f)

# 获取百分比堆叠柱状图示例（推荐）
spec = examples['percentage_stacked_bar']['spec']

# 替换数据
spec['data']['values'] = your_data
```

**关键要素说明：**

**标准堆叠柱状图（绝对值）：**
1. **数据结构**：长格式（long format），每行包含时期、品牌、份额
2. **堆叠方式**：默认 `"stack": "zero"` 显示绝对值堆叠
3. **排序**：按总份额从大到小排序（`sort: {"field": "percent", "op": "sum", "order": "descending"}`）
4. **数据标签**：使用 `opacity` 条件只显示大于 3% 的标签
5. **Tooltip**：显示详细信息（时期、品牌、份额）

**百分比堆叠柱状图（100%堆叠）：**
1. **百分比堆叠**：使用 `"stack": "normalize"` 将每个柱子归一化为 100%
2. **排序方式**：使用 `transform` + `order` 通道实现堆叠排序
   - `joinaggregate`: 计算每个品牌在所有时期的总份额
   - `window`: 按总份额降序排名
   - `calculate`: 创建 `orderValue` 字段（排名取负，使份额大的显示在上方）
   - `order` 通道: 控制堆叠顺序
3. **重要**：`color.sort` 只影响图例顺序，**不影响堆叠顺序**
4. **数据标签**：使用 `bandPosition: 0.5` 使标签居中，只显示大于 5% 的份额

**分组柱状图（并排对比）：**
1. **分组方式**：使用 `xOffset` 实现分组柱状图
2. **X 轴**：品牌名称，按总份额从大到小排序
3. **颜色**：按时期区分颜色
4. **数据标签**：每个柱子上方显示百分比

## 数据格式

### 长格式（推荐）

```json
{
  "values": [
    {"period": "24Q4", "brand": "品牌A", "share": 0.234},
    {"period": "24Q4", "brand": "品牌B", "share": 0.196},
    {"period": "25Q4", "brand": "品牌A", "share": 0.232},
    {"period": "25Q4", "brand": "品牌B", "share": 0.186}
  ]
}
```

### 宽格式（需要转换）

如果用户提供的是宽格式（每个品牌一列），需要转换为长格式：

**原始数据（宽格式）：**
```
集团      24Q4    25Q4    份额同比
君乐宝    23.4%   23.2%   -0.2%
伊利股份  17.5%   18.6%   1.1%
```

**转换后（长格式）：**
```json
{
  "values": [
    {"period": "24Q4", "brand": "君乐宝", "share": 0.234},
    {"period": "25Q4", "brand": "君乐宝", "share": 0.232},
    {"period": "24Q4", "brand": "伊利股份", "share": 0.175},
    {"period": "25Q4", "brand": "伊利股份", "share": 0.186}
  ]
}
```

## 常见错误

### ❌ 错误 1：数据格式错误

**问题：** 使用宽格式数据导致图表无法正确显示。

**错误代码：**
```json
{
  "data": {
    "values": [
      {"brand": "君乐宝", "24Q4": 0.234, "25Q4": 0.232},
      {"brand": "伊利股份", "24Q4": 0.175, "25Q4": 0.186}
    ]
  }
}
```

**✅ 正确做法：**

**转换为长格式：**
```json
{
  "data": {
    "values": [
      {"period": "24Q4", "brand": "君乐宝", "share": 0.234},
      {"period": "25Q4", "brand": "君乐宝", "share": 0.232},
      {"period": "24Q4", "brand": "伊利股份", "share": 0.175},
      {"period": "25Q4", "brand": "伊利股份", "share": 0.186}
    ]
  }
}
```

### ❌ 错误 2：堆叠顺序不正确（常见问题）

**问题：** 堆叠顺序混乱，或使用 `color.sort` 后堆叠顺序仍然不正确。

#### 错误做法 1：只使用 `color.sort`

**问题：** `color.sort` 只影响图例顺序，**不影响堆叠顺序**！

```json
{
  "encoding": {
    "color": {
      "field": "brand",
      "type": "nominal",
      "sort": {"field": "share", "op": "sum", "order": "descending"}
    }
  }
}
```

结果：图例会按份额排序，但堆叠块仍然按原始数据顺序堆叠。

#### 错误做法 2：在 `order` 中使用 `aggregate`

```json
{
  "encoding": {
    "order": {
      "aggregate": "sum",      // ❌ order 通道不支持 aggregate
      "field": "share",
      "order": "descending"
    }
  }
}
```

**错误信息：**
```
Validation: /encoding/order must NOT have additional properties
Validation: /encoding/order must be array
```

**✅ 正确做法：使用 `transform` + `order` 通道**

```json
{
  "transform": [
    {
      "joinaggregate": [{"op": "sum", "field": "share", "as": "totalShare"}],
      "groupby": ["brand"]
    },
    {
      "window": [{"op": "row_number", "as": "rank"}],
      "sort": [{"field": "totalShare", "order": "descending"}]
    },
    {
      "calculate": "datum.rank * -1",
      "as": "orderValue"
    }
  ],
  "encoding": {
    "color": {"field": "brand"},
    "order": {"field": "orderValue"}  // ✅ 使用字段名，不是 aggregate
  }
}
```

**原理解释：**
1. `joinaggregate`: 计算每个品牌在所有时期的总份额
2. `window`: 按总份额降序排名
3. `calculate`: 创建排序字段（排名取负，使份额大的显示在上方）
4. `order` 通道: 引用这个字段控制堆叠顺序

**关键点：**
- `order` 通道只接受 `"field"` 字段，不支持 `"aggregate"`
- 必须使用 `transform` 预先计算排序值
- 所有 `layer` 都需要添加相同的 `order` 配置

### ❌ 错误 3：数据标签过多导致重叠

**问题：** 所有堆叠块都显示标签，导致小份额的标签重叠。

**✅ 正确做法：**

**使用条件过滤小份额标签：**
```json
{
  "encoding": {
    "opacity": {
      "condition": {"test": "datum.percent > 3", "value": 1},
      "value": 0
    }
  }
}
```

### ❌ 错误 4：过度配置颜色

**问题：** 不必要地自定义颜色配置。

**错误代码：**
```json
{
  "encoding": {
    "color": {
      "field": "brand",
      "type": "nominal",
      "scale": {
        "domain": ["品牌A", "品牌B", "品牌C"],
        "range": ["#1f77b4", "#ff7f0e", "#2ca02c"]
      }
    }
  }
}
```

**✅ 正确做法：**

**使用默认配色：**
```json
{
  "encoding": {
    "color": {
      "field": "brand",
      "type": "nominal",
      "legend": {"orient": "right", "title": "集团"}
    }
  }
}
```

## 最佳实践

1. **数据格式**：使用长格式（long format）
   - 每行包含：时期、品牌、份额
   - 便于 Vega-Lite 处理和堆叠

2. **排序规则**：按总份额从大到小排序
   ```json
   {
     "encoding": {
       "color": {
         "sort": {"field": "share", "op": "sum", "order": "descending"}
       }
     }
   }
   ```

3. **数据标签**：使用条件过滤小份额标签
   ```json
   {
     "opacity": {
       "condition": {"test": "datum.percent > 3", "value": 1},
       "value": 0
     }
   }
   ```

4. **堆叠方式**：
   - **绝对值堆叠**：使用 `"stack": "zero"`（默认）
   - **百分比堆叠**：使用 `"stack": "normalize"`
   - **不堆叠（并排）**：使用 `xOffset` 实现分组柱状图

5. **颜色配置**：使用默认配色，不要自定义

6. **图例位置**：使用 `"orient": "right"` 避免遮挡图表

## 使用步骤

1. **准备数据**：转换为长格式（period, brand, share）
2. **选择图表类型**：
   - 堆叠柱状图（绝对值）→ 使用示例 1
   - 百分比堆叠柱状图（100%）→ 使用示例 2
   - 分组柱状图（并排对比）→ 使用示例 3
3. **替换数据**：修改 `data.values` 中的数据
4. **修改字段名**：根据实际数据调整字段名
5. **调整排序**：按总份额从大到小排序
6. **配置数据标签**：设置合适的阈值（如 `datum.percent > 3`）

## 图表选择指南

| 图表类型 | 适用场景 | 优点 | 缺点 |
|---------|---------|------|------|
| **堆叠柱状图（绝对值）** | 展示总市场份额变化 + 各品牌份额 | 可以看出总量变化和结构变化 | 难以对比中间份额的品牌 |
| **百分比堆叠柱状图** | 展示各品牌占比变化 | 清晰显示占比变化，总和为 100% | 无法看出总量变化 |
| **分组柱状图（并排）** | 直接对比各品牌份额 | 最直观，容易对比各品牌 | 适合品牌数量少（<8个） |

**推荐选择：**
- 重点关注总量变化 → 使用**堆叠柱状图（绝对值）**
- 重点关注结构变化 → 使用**百分比堆叠柱状图**
- 品牌数量少（<8个） → 使用**分组柱状图（并排）**
