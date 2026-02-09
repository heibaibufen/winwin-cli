---
name: pie-chart
description: "生成饼图或环形图，展示各部分占整体的比例关系。触发词：生成饼图、创建饼图、显示占比、销售构成、市场份额分布、分类占比。"
---

# Pie Chart - 饼图/环形图

生成饼图或环形图，展示各部分占整体的比例关系。

## 适用场景

- 市场份额分布
- 销售构成分析
- 预算分配展示
- 人口统计分类

## MCP 工具

生成图表前，先用 vega-lite 知识库查询相关文档：

```bash
# 搜索 arc mark 相关文档
mcp__vega-lite__search_documents(query="arc mark pie chart")

# 获取文档详细内容
mcp__vega-lite__get_document_content(path="vega-lite/marks.md")
```

## 核心原则

**简单优先**：使用默认配置，不要过度定制

1. **颜色**：使用 Vega-Lite 默认配色（不要自定义 scale 和 range）
2. **图例**：饼图禁用图例（`legend: null`），标签已在图表上
3. **标签位置**：外部标签 `radius` = `outerRadius` + 30
4. **百分比显示**：在 tooltip 中显示百分比

## 示例

完整示例请参见 `examples.json` 文件，包含以下示例：

| 示例名称 | 说明 |
|---------|------|
| `standard_pie_chart` | 标准饼图，包含外部标签和 tooltip 百分比显示 |
| `donut_chart` | 甜甜圈图（环形图），环形区域显示百分比 |
| `tooltip_with_joinaggregate` | 使用 joinaggregate 计算百分比 |

### 使用示例

从 `examples.json` 中选择合适的示例，替换数据即可使用：

```python
# 读取示例
import json
with open('examples.json', 'r') as f:
    examples = json.load(f)

# 获取标准饼图示例
spec = examples['standard_pie_chart']['spec']

# 替换数据
spec['data']['values'] = your_data
```

**关键要素：**
1. **标准饼图**：不设置 `innerRadius`，如需甜甜圈图可添加 `"innerRadius": 80`
2. **Encoding 位置**：在顶层定义 `theta` 和 `color`，供所有图层共享
3. **百分比计算**：在 data 中添加 `total` 字段，使用 `transform` 计算百分比
4. **标签位置**：使用 `radius` 参数控制标签位置
   - 外部标签：`radius` = `outerRadius` + 30（如 `outerRadius: 120`，则 `radius: 150`）
   - 内部标签：`radius` 在 `innerRadius` 和 `outerRadius` 之间
5. **Tooltip 配置**：在 arc 图层的 encoding 中单独定义 tooltip
6. **Legend 禁用**：设置 `"legend": null` 避免重复（标签已在图表上）

## 饼图 vs 甜甜圈图

**饼图（标准）：**
```json
{
  "mark": {"type": "arc", "outerRadius": 120}
}
```

**甜甜圈图（环形）：**
```json
{
  "mark": {"type": "arc", "outerRadius": 120, "innerRadius": 70}
}
```

在甜甜圈图中，可以在环形区域中间显示百分比。具体实现参见 `examples.json` 中的 `donut_chart` 示例。

## Tooltip 中显示百分比的两种方法

**方法 1：在 data 中添加 total 字段（推荐）**
- 参见 `standard_pie_chart` 示例

**方法 2：使用 joinaggregate 计算总和**
- 参见 `tooltip_with_joinaggregate` 示例

## 常见错误

### ❌ 错误 1：饼图标签位置不当

**问题：** 饼图的标签位置设置不当，导致标签重叠或不清晰。

**错误代码：**
```json
{
  "mark": {"type": "text", "radius": 50}
}
```

**原因：** `radius` 值设置不当可能导致标签在饼图内部，与扇区颜色对比度不足。

**✅ 正确做法：**

**根据图表类型选择合适的 radius：**
```json
{
  "layer": [
    {
      "mark": {"type": "arc", "outerRadius": 120}
    },
    {
      // 外部标签（推荐用于标准饼图）
      "mark": {"type": "text", "radius": 150, "fontSize": 12},
      "encoding": {"text": {"field": "brand", "type": "nominal"}}
    }
  ]
}
```

**radius 选择原则：**
- 外部标签：`radius` = `outerRadius` + 30（确保标签清晰可见）
- 内部标签：`radius` 在 `innerRadius` 和 `outerRadius` 之间
- 甜甜圈图环形区：`radius` = (innerRadius + outerRadius) / 2
- **标签字体大小**：外部标签推荐 `fontSize: 12`

### ❌ 错误 2：饼图 encoding 位置不当

**问题：** 将 `theta` 和 `color` 放在单个图层的 encoding 中，导致其他图层无法共享。

**错误代码：**
```json
{
  "layer": [
    {
      "mark": {"type": "arc"},
      "encoding": {
        "theta": {"field": "value", "type": "quantitative", "stack": true},
        "color": {"field": "brand", "type": "nominal"}
      }
    },
    {
      "mark": {"type": "text"},
      "encoding": {
        "text": {"field": "brand", "type": "nominal"}
        // 缺少 theta，标签位置会错误
      }
    }
  ]
}
```

**原因：** `theta` 定义了数据在圆周上的位置，文本图层也需要 `theta` 来确定标签位置。

**✅ 正确做法：**

**在顶层定义共享的 encoding：**
```json
{
  "encoding": {
    "theta": {"field": "value", "type": "quantitative", "stack": true},
    "color": {"field": "brand", "type": "nominal", "legend": null}
  },
  "layer": [
    {
      "mark": {"type": "arc", "outerRadius": 120},
      "encoding": {
        // 图层特有的 encoding（如 tooltip）
        "tooltip": [
          {"field": "brand", "type": "nominal"},
          {"field": "value", "type": "quantitative"}
        ]
      }
    },
    {
      "mark": {"type": "text", "radius": 150},
      "encoding": {
        "text": {"field": "brand", "type": "nominal"}
        // theta 自动继承自顶层 encoding
      }
    }
  ]
}
```

### ❌ 错误 3：混淆饼图和甜甜圈图

**问题：** 用户要求饼图，却生成了甜甜圈图（或相反）。

**关键区别：**
- **饼图**：不设置 `innerRadius` 或 `"innerRadius": 0`
- **甜甜圈图**：设置 `"innerRadius"` 为非零值（如 70）

**提示：** 甜甜圈图的 `innerRadius` 建议值为 `outerRadius` 的 50%~70%。

### ❌ 错误 4：饼图中直接使用数值显示百分比

**问题：** 在饼图的 tooltip 或标签中直接显示销售额数值，而不是百分比。

**原因：** 饼图的主要目的是展示占比关系，直接显示数值不够直观。

**✅ 正确做法：**

**在 data 中添加 total 字段，计算百分比：**
```json
{
  "data": {
    "values": [
      {"brand": "品牌A", "value": 100, "total": 500},
      {"brand": "品牌B", "value": 200, "total": 500}
    ]
  },
  "transform": [
    {"calculate": "datum.value / datum.total", "as": "percent"}
  ],
  "encoding": {
    "tooltip": [
      {"field": "brand", "type": "nominal", "title": "品牌"},
      {"field": "value", "type": "quantitative", "title": "数值", "format": ","},
      {"field": "percent", "type": "quantitative", "title": "占比", "format": ".1%"}
    ]
  }
}
```

### ❌ 错误 5：过度配置颜色

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
      "legend": null
    }
  }
}
```

Vega-Lite 的默认配色方案已经足够优秀，无需自定义。

## 最佳实践

1. **使用默认配色**：不要自定义颜色（除非用户明确要求）
2. **标签位置**：外部标签 `radius` = `outerRadius` + 30
3. **Encoding 位置**：在顶层定义 `theta` 和 `color`，让所有图层共享
4. **百分比计算**：在 data 中添加 `total` 字段，使用 `transform` 计算
5. **禁用图例**：饼图设置 `"legend": null`，避免与标签重复

## 数据校验

- 所有数值为非负数
- 分类数量不超过 10 个
- 按数值从大到小排序
- 扇区数量建议 2-8 个

## 使用步骤

1. 准备数据：确保数据包含类别、数值和总计字段
2. 从 `examples.json` 选择合适的示例
3. 替换 `spec.data.values` 中的数据
4. 修改字段名（如 `brand`、`sales`）为实际字段名
5. 调整 `radius` 值以适应标签位置
6. （可选）添加 `innerRadius` 转换为甜甜圈图
