---
name: gain-loss-analysis
description: "生成增长柱为绿色、下跌柱为红色的柱状图，分析品牌、产品、类目的市场份额变化。触发词：生成柱状图、对比增长、得失分析、市场份额变化。"
---

# Gain and Loss Analysis - 得失分析柱状图

生成增长柱为绿色、下跌柱为红色的柱状图，分析市场份额变化。

## 适用场景

分析品牌/产品/类目的市场份额变化：
- 正数显示绿色增长柱
- 负数显示红色下跌柱
- 便于对比正负值的大小关系
- **推荐使用垂直柱状图**（横坐标：类别名称，纵坐标：增长率）

## 图表版本选择

**重要：在生成得失分析图之前，必须询问用户需要哪个版本**

### 版本对比

| 特性 | 简化版（推荐） | 完整版 |
|------|--------------|--------|
| 零基准线 | ✅ 有（中间） | ✅ 有（底部） |
| 坐标轴 | ❌ 隐藏（更简洁） | ✅ 显示（带刻度和标签） |
| 柱子样式 | 细柱（width: 20） | 标准宽度 |
| 品牌标签位置 | 正值在下，负值在上 | X轴下方统一显示 |
| 视觉风格 | 极简、现代 | 传统统计图风格 |
| 适用场景 | 演示、报告、仪表板 | 详细数据分析、技术文档 |

### 询问用户

当用户要求生成得失分析图时，使用以下话术：

```
需要生成得失分析图，请选择版本：
1. 简化版（推荐）：无坐标轴，细柱子，品牌标签智能定位，视觉更简洁
2. 完整版：完整坐标轴，标准柱子，适合详细数据分析
```

**默认使用简化版**，除非用户明确要求完整版。

## MCP 工具

生成图表前，先用 vega-lite 知识库查询相关文档：

```bash
# 搜索 bar mark 和 color 相关文档
mcp__vega-lite__search_documents(query="bar mark color expr")

# 查询 layer 和 condition 文档
mcp__vega-lite__search_documents(query="layer condition")
```

## 核心原则

**简单优先**：使用默认配置，但正负值必须区分颜色

1. **颜色**：正负值必须使用阈值颜色区分（红色/绿色）
2. **图表方向**：推荐垂直柱状图（X轴：类别，Y轴：数值）
3. **标签位置**：正值标签在柱子上方，负值标签在柱子下方
4. **零基线**：Y轴域必须包含零点
5. **柱子比例**：**柱子高宽比约为1.5:1**，柱子宽度设置为20（默认值，除非用户明确指定）

## 示例

完整示例请参见 `examples.json` 文件，包含以下示例：

| 示例名称 | 说明 |
|---------|------|
| `simplified_gain_loss` | 简化版得失分析图（推荐），极简风格，无坐标轴，细柱子，品牌标签智能定位 |
| `full_gain_loss` | 完整版得失分析图，包含完整坐标轴和标签，适合详细数据分析 |

### 使用示例

从 `examples.json` 中选择合适的示例，替换数据即可使用：

```python
# 读取示例
import json
with open('examples.json', 'r') as f:
    examples = json.load(f)

# 获取简化版示例（推荐）
spec = examples['simplified_gain_loss']['spec']

# 替换数据
spec['data']['values'] = your_data
```

**简化版关键要素：**
1. **零基准线**：中间黑色半透明参考线
2. **隐藏坐标轴**：通过 `config.axis` 隐藏所有坐标轴元素
3. **柱子宽度**：`"width": 20`，保持柱子高宽比约为1.5:1（默认值，除非用户明确指定）
4. **智能标签定位**：
   - 正值品牌：数值在柱子上方，品牌在零线下方
   - 负值品牌：数值在柱子下方，品牌在零线上方
5. **无边框**：`"view": {"stroke": null}` 隐藏图表边框

**完整版关键要素：**
1. **数据排序**：在数据数组中直接按从高到低排序
2. **禁用自动排序**：所有图层的 x 轴都设置 `"sort": null`
3. **三个图层**：柱状图 + 正值标签 + 负值标签
4. **阈值颜色**：使用 `threshold` 类型比例尺区分正负
5. **条件显示**：使用 `opacity` 条件控制标签显示
6. **图例位置**：使用 `"orient": "right"` 避免覆盖图表
7. **零基线**：Y 轴域包含负数到正数，确保零基线可见
8. **柱子宽度**：默认 `"width": 20`，保持合适的高宽比（除非用户明确指定）

## 垂直 vs 水平柱状图

**推荐：垂直柱状图**
```json
{
  "encoding": {
    "x": {"field": "brand", "type": "nominal"},  // 类别在横轴
    "y": {"field": "value", "type": "quantitative"}  // 数值在纵轴
  }
}
```

**水平柱状图**（仅在类别标签很少且短时使用）
```json
{
  "encoding": {
    "y": {"field": "brand", "type": "nominal"},  // 类别在纵轴
    "x": {"field": "value", "type": "quantitative"}  // 数值在横轴
  }
}
```

**选择建议：**
- 类别标签较长（如品牌名称）→ 使用**垂直柱状图** + `labelAngle: -45`
- 类别标签较少且短 → 可使用**水平柱状图**
- 用户明确要求时按用户需求

## 常见错误

### ❌ 错误 1：Nominal 字段排序不生效

**问题：** 使用 `{"field": "value", "order": "descending"}` 对 nominal 类型字段排序时，排序不生效。

**错误代码：**
```json
{
  "encoding": {
    "x": {
      "field": "brand",
      "type": "nominal",
      "sort": {"field": "value", "order": "descending"}
    }
  }
}
```

**原因：** Vega-Lite 对 nominal 类型字段的排序行为不一致，特别是当数据已预处理时。

**✅ 正确做法：**

**方法 1：在数据中直接排序 + 禁用自动排序**（推荐）
```json
{
  "data": {
    "values": [
      {"brand": "旺仔", "value": 0.014},
      {"brand": "优酸乳", "value": 0.010},
      {"brand": "伊利", "value": 0.006}
    ]
  },
  "layer": [
    {
      "mark": "bar",
      "encoding": {
        "x": {
          "field": "brand",
          "type": "nominal",
          "sort": null  // 关键：禁用自动排序
        }
      }
    }
  ]
}
```

**重要提醒：** 如果使用多图层（如柱状图 + 标签），**必须在所有图层的 encoding 中都添加 `"sort": null`**：
```json
{
  "layer": [
    {
      "mark": "bar",
      "encoding": {
        "x": {"field": "brand", "type": "nominal", "sort": null}
      }
    },
    {
      "mark": "text",
      "encoding": {
        "x": {"field": "brand", "type": "nominal", "sort": null}  // 也需要
      }
    }
  ]
}
```

**方法 2：使用数组指定顺序**
```json
{
  "encoding": {
    "x": {
      "field": "brand",
      "type": "nominal",
      "sort": ["旺仔", "优酸乳", "伊利", "蒙牛"]
    }
  }
}
```

### ❌ 错误 2：在不支持的字段使用表达式

**错误代码：**
```json
{
  "mark": {
    "type": "text",
    "align": {"expr": "datum.value < 0 ? 'left' : 'left'"},
    "dx": {"expr": "datum.value < 0 ? 5 : 5"}
  }
}
```

**错误信息：** `Illegal callee type: MemberExpression`

**原因：** `mark` 对象中的属性（如 `align`、`dx`、`dy`、`xOffset` 等）**不支持表达式**，只能使用固定值。

**✅ 正确做法：**

对于需要根据数据值动态调整的情况，使用以下方法：

1. **使用条件表达式在 encoding 中**：
```json
{
  "encoding": {
    "color": {
      "condition": {
        "test": "datum.value < 0",
        "value": "#d62728"
      },
      "value": "#2ca02c"
    }
  }
}
```

2. **使用多个图层 + opacity 条件**（用于正负值标签位置不同时）：
```json
{
  "layer": [
    {
      "mark": {
        "type": "text",
        "baseline": "bottom",
        "dy": -5
      },
      "encoding": {
        "opacity": {
          "condition": {"test": "datum.value >= 0", "value": 1},
          "value": 0
        }
      }
    },
    {
      "mark": {
        "type": "text",
        "baseline": "top",
        "dy": 5
      },
      "encoding": {
        "opacity": {
          "condition": {"test": "datum.value < 0", "value": 1},
          "value": 0
        }
      }
    }
  ]
}
```

### ❌ 错误 3：Y 轴不包含零基线

**问题：** Y 轴域不包含零点，导致图表无法清晰显示正负对比。

**错误代码：**
```json
{
  "encoding": {
    "y": {
      "field": "value",
      "type": "quantitative",
      "scale": {"domain": [0.01, 0.02]}  // 缺少负数和零
    }
  }
}
```

**✅ 正确做法：**

**确保 Y 轴域包含零点：**
```json
{
  "encoding": {
    "y": {
      "field": "value",
      "type": "quantitative",
      "scale": {"domain": [-0.035, 0.018]}  // 包含负数、零、正数
    }
  }
}
```

### ❌ 错误 4：图例覆盖图表内容

**问题：** 图例位置配置不当，导致图例覆盖在柱状图或其他图表元素上。

**错误代码：**
```json
{
  "encoding": {
    "color": {
      "legend": {
        "orient": "top-right"  // 可能导致图例在图表内部
      }
    }
  }
}
```

**✅ 正确做法：**

**方法 1：使用外部位置**
```json
{
  "encoding": {
    "color": {
      "legend": {
        "title": "增长情况",
        "orient": "right",  // 右侧外部
        "symbolSize": 150
      }
    }
  }
}
```

**方法 2：完全禁用图例**（如果颜色已经很直观）
```json
{
  "encoding": {
    "color": {
      "legend": null  // 不显示图例
    }
  }
}
```

**可选的 orient 值：**
- `"right"` - 右侧（推荐，不遮挡内容）
- `"left"` - 左侧
- `"top"` - 顶部
- `"bottom"` - 底部
- `"top-right"` - 右上角（可能遮挡内容）
- `"top-left"` - 左上角（可能遮挡内容）
- `"bottom-left"` - 左下角（可能遮挡内容）
- `"bottom-right"` - 右下角（可能遮挡内容）

### ❌ 错误 5：labelExpr 使用过于复杂的表达式

**错误代码：**
```json
{
  "legend": {
    "labelExpr": "datum.value < 0 ? '损失 (-' + (datum.value * -100).toFixed(1) + '%' + ')' : '得利 (+' + (datum.value * 100).toFixed(1) + '%' + ')'"
  }
}
```

**原因：** `labelExpr` 支持的表达式有限，复杂的字符串拼接和函数调用可能导致错误。

**✅ 正确做法：**
```json
{
  "legend": {
    "format": ".1%"
  }
}
```
使用简单的 `format` 格式化，让 Vega-Lite 自动处理。

### ❌ 错误 6：横纵轴选择不当

**问题：** 默认生成水平柱状图，但用户需要垂直柱状图。

**✅ 正确做法：**
- **垂直柱状图**（X 轴是类别，Y 轴是数值）：
  ```json
  {
    "encoding": {
      "x": {"field": "brand", "type": "nominal"},
      "y": {"field": "value", "type": "quantitative"}
    }
  }
  ```

- **水平柱状图**（Y 轴是类别，X 轴是数值）：
  ```json
  {
    "encoding": {
      "y": {"field": "brand", "type": "nominal"},
      "x": {"field": "value", "type": "quantitative"}
    }
  }
  ```

**选择建议：**
- 类别标签较长（如品牌名称）→ 使用**垂直柱状图** + `labelAngle: -45`
- 类别标签较少且短 → 使用**水平柱状图**或垂直柱状图
- 用户明确要求时按用户需求

## 最佳实践

1. **Y轴域配置**（重要）：
   - **Y轴域必须包含零点**，且上下留出呼吸空间
   - 示例：如果数据范围是[-0.025, 0.017]，建议设置为 `[-0.028, 0.02]`
   - **避免0线贴边**：确保上下各增加10-20%的空间
   - 配置示例：
     ```json
     {
       "y": {
         "field": "value",
         "type": "quantitative",
         "scale": {"domain": [-0.028, 0.02]}  // 留出呼吸空间
       }
     }
     ```

2. **图表尺寸和内边距**：
   - 推荐尺寸：`1100×650`
   - 推荐padding：`{"top": 80, "bottom": 80, "left": 80, "right": 150}`
   - 充足的padding避免标签、标题和图例贴边

3. **正负值颜色配置**：得失分析必须使用阈值颜色区分
   ```json
   {
     "color": {
       "field": "value",
       "type": "quantitative",
       "scale": {
         "domain": [-0.035, 0, 0.016],
         "range": ["#d62728", "#d62728", "#2ca02c"],
         "type": "threshold"
       }
     }
   }
   ```

4. **数据标签**：
   - 优先在 `encoding` 中使用条件表达式
   - 避免在 `mark` 属性中使用表达式
   - 使用推荐的默认标签位置

5. **图表尺寸**：
   - 多类别（>10个）时，增加宽度：`"width": 1000`
   - 使用 `labelAngle: -45` 避免标签重叠
   - **用户明确指定尺寸时**，使用用户给出的尺寸

6. **柱子宽度**：
   - **默认宽度**：`"width": 20`，保持柱子高宽比约为1.5:1
   - 用户明确指定宽度时，使用用户指定的宽度

7. **数据排序**：
   - 在数据中直接排序
   - 所有图层都设置 `"sort": null`

## 数据格式

- 支持正负百分比或小数（如 `0.05` 表示 5%，`-0.03` 表示 -3%）
- 建议数据量 5-30 个效果最佳
- 按数值从大到小排序

## 使用步骤

1. 准备数据：确保数据包含类别、数值字段（支持正负值）
2. 数据按数值从大到小排序
3. 使用完整示例模板，替换 `data.values` 中的数据
4. 修改字段名（如 `brand`、`value`）为实际字段名
5. 确认 Y 轴域包含零点
6. 调整标题和坐标轴标签
