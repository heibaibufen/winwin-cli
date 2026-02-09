---
name: quadrant-chart
description: "生成四象限图（波士顿矩阵），根据市场份额和销售增长将品牌划分为明星、潜力、成熟、衰退四个象限。触发词：生成四象限图、波士顿矩阵、象限分析、品牌分类。"
---

# Quadrant Chart - 四象限图（波士顿矩阵）

生成四象限图（波士顿矩阵），根据两个关键指标将品牌/产品划分为四个象限。

## 适用场景

将品牌/产品按两个关键指标划分为四个象限：
- **明星区域**（右上）：高增长，高份额
- **潜力区域**（左上）：高增长，低份额
- **成熟区域**（右下）：低增长，高份额
- **衰退区域**（左下）：低增长，低份额

## MCP 工具

生成图表前，先用 vega-lite 知识库查询相关文档：

```bash
# 搜索 point mark 和 layer 相关文档
mcp__vega-lite__search_documents(query="point mark layer scatter")

# 查询配置和 axis 文档
mcp__vega-lite__search_documents(query="config axis")
```

## 核心原则

**简单优先**：使用默认配置，不要过度定制

1. **颜色**：使用 Vega-Lite 默认配色
2. **图例**：使用 `orient: "right"` 避免遮挡图表
3. **标签位置**：使用 `baseline: "bottom"` + `dy: -8` 将标签放在点上方
4. **参考线**：使用中位数而非随意设置的值
5. **图层顺序**：背景标签 → 参考线 → 参考线数值 → 散点 → 品类标注 → 交互散点
6. **象限标签**：使用独立图层在四角显示，设置 `scale: null` 避免坐标轴干扰

## 示例

完整示例请参见 `examples.json` 文件，包含以下示例：

| 示例名称 | 说明 |
|---------|------|
| `standard_quadrant_chart` | 标准四象限图（波士顿矩阵）- 带象限标签，包含四角象限标签、参考虚线、散点、品类标注 |

### 使用示例

从 `examples.json` 中选择合适的示例，替换数据即可使用：

```python
# 读取示例
import json
with open('examples.json', 'r') as f:
    examples = json.load(f)

# 获取标准四象限图示例
spec = examples['standard_quadrant_chart']['spec']

# 替换数据（注意有两个 data.values）
# 1. 第一个 data.values 是象限标签数据（通常不需要修改）
# 2. 第二个 data.values 是业务数据，需要替换
spec['layer'][1]['data']['values'] = your_data
```

**关键要素：**
1. **四象限背景标签**：使用独立图层，在四个角落显示"潜力"、"明星"、"衰退"、"成熟"
2. **虚线参考线**：使用 `strokeDash: [4, 4]` 创建红色虚线效果
3. **中位数位置**：参考线基于实际数据中位数（非随意设置）
4. **参考线数值标注**：在参考线上显示具体百分比数值
5. **散点图层**：数据点，支持交互 tooltip
6. **品类标注**：在数据点上方显示品类名称
7. **图层顺序**：背景标签 → 参考线 → 参考线数值 → 散点 → 品类标注 → 交互散点

## 象限划分说明

| 象限 | 位置 | 特征 | 策略建议 |
|------|------|------|----------|
| **明星** | 右上 | 高增长 + 高份额 | 重点投资，扩大优势 |
| **潜力** | 左上 | 高增长 + 低份额 | 选择性投资，培养增长 |
| **成熟** | 右下 | 低增长 + 高份额 | 维持利润，优化成本 |
| **衰退** | 左下 | 低增长 + 低份额 | 减仓或退出 |

## 常见错误

### ❌ 错误 1：Y轴0线贴边（坐标轴范围设置不当）

**问题：** Y轴的0线贴在图表左边缘，视觉效果不佳，且无法清晰展示象限划分。

**错误代码：**
```json
{
  "encoding": {
    "x": {
      "field": "market_share",
      "type": "quantitative",
      "scale": {"domain": [0, 0.23]}  // ❌ 从0开始，导致Y轴0线贴边
    }
  }
}
```

**原因：** X轴（横轴）从0开始时，Y轴的0线会出现在图表最左侧，贴在边缘上。

**✅ 正确做法：**

**让横轴从负值开始，为Y轴0线留出空间：**
```json
{
  "encoding": {
    "x": {
      "field": "market_share",
      "type": "quantitative",
      "scale": {"domain": [-0.05, 0.25]}  // ✅ 从负值开始，Y轴0线居中显示
    }
  }
}
```

**推荐配置：**
- X轴最小值：`-0.05` 或数据最小值的80%（取较小者）
- X轴最大值：数据最大值的110-120%
- Y轴最小值：数据最小值的110-120%（留出呼吸空间）
- Y轴最大值：数据最大值的110-120%

**示例配置：**
```json
{
  "width": 1100,
  "height": 750,
  "padding": {"top": 80, "bottom": 80, "left": 100, "right": 100},
  "encoding": {
    "x": {
      "field": "market_share",
      "type": "quantitative",
      "scale": {"domain": [-0.05, 0.25]},  // 横轴从负值开始
      "axis": {"grid": false, "format": ".1%"}
    },
    "y": {
      "field": "growth",
      "type": "quantitative",
      "scale": {"domain": [-0.028, 0.02]},  // 留出呼吸空间
      "axis": {"grid": false, "format": ".1%"}
    }
  }
}
```

### ❌ 错误 2：散点图标签覆盖数据点

**问题：** 散点图/四象限图中，文本标签直接显示在数据点位置，导致标签覆盖数据点。

**错误代码：**
```json
{
  "mark": {
    "type": "text",
    "align": "left",
    "dx": 8  // 只向右偏移，仍可能覆盖点
  },
  "encoding": {
    "x": {"field": "market_share", "type": "quantitative"},
    "y": {"field": "growth", "type": "quantitative"},
    "text": {"field": "brand", "type": "nominal"}
  }
}
```

**原因：** 仅使用水平偏移 `dx` 不足以避免标签覆盖圆形数据点。

**✅ 正确做法：**

**使用 baseline + dy 将标签移到点的上方/下方：**
```json
{
  "mark": {
    "type": "text",
    "align": "left",
    "baseline": "bottom",  // 关键：设置基线为底部
    "dx": 10,              // 水平向右偏移
    "dy": -8,              // 垂直向上偏移（负值）
    "fontSize": 11,
    "fontWeight": "bold"
  },
  "encoding": {
    "x": {"field": "market_share", "type": "quantitative"},
    "y": {"field": "growth", "type": "quantitative"},
    "text": {"field": "brand", "type": "nominal"},
    "color": {"value": "#333"}
  }
}
```

**关键属性说明：**
- `baseline: "bottom"` - 文本基线在底部，配合负 `dy` 将文本向上移
- `dy: -8` - 负值向上偏移（正值向下）
- `dx: 10` - 向右偏移，避免与点重叠
- 组合使用确保标签在点的**右上方**，完全不遮挡数据点

**如果需要多个标签（如品牌名+数值）：**
```json
{
  "layer": [
    {
      "mark": {
        "type": "text",
        "align": "left",
        "baseline": "bottom",
        "dx": 10,
        "dy": -8,  // 上方：品牌名
        "fontSize": 11,
        "fontWeight": "bold"
      },
      "encoding": {
        "text": {"field": "brand", "type": "nominal"}
      }
    },
    {
      "mark": {
        "type": "text",
        "align": "left",
        "baseline": "top",
        "dx": 10,
        "dy": 8,  // 下方：数值
        "fontSize": 10
      },
      "encoding": {
        "text": {"field": "value", "type": "quantitative"}
      }
    }
  ]
}
```

### ❌ 错误 3：参考线样式不清晰

**问题：** 四象限图的参考线使用实线，不够明显，容易与数据混淆。

**错误代码：**
```json
{
  "mark": {"type": "rule", "color": "gray", "strokeWidth": 1}
}
```

**✅ 正确做法：**

**使用虚线样式：**
```json
{
  "mark": {
    "type": "rule",
    "color": "gray",
    "strokeWidth": 1,
    "strokeDash": [6, 4]  // 6像素实线 + 4像素间隔
  }
}
```

**参考线位置建议：**
- 使用**中位数**而非随意设置的值
- 垂直线：`"datum": 0.043`（根据实际数据中位数）
- 水平线：`"datum": -0.001`（根据实际数据中位数）

### ❌ 错误 4：图例覆盖图表内容

**问题：** 图例位置配置不当，导致图例覆盖在图表上。

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

**使用外部位置：**
```json
{
  "encoding": {
    "color": {
      "legend": {
        "title": "品牌",
        "orient": "right",  // 右侧外部
        "columns": 2,
        "labelFontSize": 11
      }
    }
  }
}
```

## 最佳实践

1. **坐标轴范围设置**（重要）：
   - **横轴（X轴）必须从负值开始**（如-0.05），避免Y轴0线贴边
   - **在坐标轴域外留出呼吸空间**，上下/左右各增加10-20%的空间
   - 示例：`x: {"scale": {"domain": [-0.05, 0.25]}}, y: {"scale": {"domain": [-0.028, 0.02]}}`
2. **图表尺寸和内边距**：
   - 推荐尺寸：`1100×750`
   - 推荐padding：`{"top": 80, "bottom": 80, "left": 100, "right": 100}`
   - 充足的padding避免标签和标题贴边
3. **使用默认配色**：不要自定义颜色（除非用户明确要求）
4. **标签位置**：使用 `baseline: "bottom"` + `dy: -8` 将标签放在点右上方
5. **虚线参考线**：使用 `strokeDash: [4, 4]` 让参考线更清晰
6. **参考线位置**：使用中位数而非随意设置的值
7. **图例位置**：使用 `orient: "right"` 避免遮挡图表

## 四象限背景标签实现

### 原理

在图表的四个角落添加象限标签，帮助用户快速识别每个象限的含义。

### 实现方法

**使用独立的背景标签图层：**

```json
{
  "data": {
    "values": [
      {"tag": "潜力", "x_pos": -60, "y_pos": -40, "bg": "#f9ebf2", "c": "#d64a93"},
      {"tag": "明星", "x_pos": 1060, "y_pos": -40, "bg": "#fff2e6", "c": "#f3a358"},
      {"tag": "衰退", "x_pos": -60, "y_pos": 740, "bg": "#fde8e8", "c": "#e66767"},
      {"tag": "成熟", "x_pos": 1060, "y_pos": 740, "bg": "#eef7ed", "c": "#6ab06d"}
    ]
  },
  "layer": [
    {
      "mark": {
        "type": "rect",
        "cornerRadius": 5,
        "width": 80,
        "height": 40
      },
      "encoding": {
        "x": {"field": "x_pos", "type": "quantitative", "scale": null},
        "y": {"field": "y_pos", "type": "quantitative", "scale": null},
        "color": {"field": "bg", "type": "nominal", "scale": null}
      }
    },
    {
      "mark": {
        "type": "text",
        "fontSize": 16,
        "fontWeight": "bold",
        "align": "center",
        "baseline": "middle"
      },
      "encoding": {
        "x": {"field": "x_pos", "type": "quantitative", "scale": null},
        "y": {"field": "y_pos", "type": "quantitative", "scale": null},
        "text": {"field": "tag", "type": "nominal"},
        "color": {"field": "c", "type": "nominal", "scale": null}
      }
    }
  ]
}
```

### 调整位置

象限标签位置需要根据图表尺寸和内边距调整：

| 图表尺寸 | 左上（潜力） | 右上（明星） | 左下（衰退） | 右下（成熟） |
|---------|-------------|-------------|-------------|-------------|
| 1000×700, padding: 80/60 | `x: -60, y: -40` | `x: 1060, y: -40` | `x: -60, y: 740` | `x: 1060, y: 740` |
| 800×600, padding: 60/40 | `x: -50, y: -30` | `x: 850, y: -30` | `x: -50, y: 630` | `x: 850, y: 630` |

**计算公式：**
- 左侧 x 坐标 = `0 - padding.left - 矩形宽度`
- 右侧 x 坐标 = `图表宽度 + padding.right`
- 上方 y 坐标 = `0 - padding.top - 矩形高度`
- 下方 y 坐标 = `图表高度 + padding.bottom`

### 颜色方案

标准象限颜色方案：

| 象限 | 背景色 | 文字色 | 说明 |
|------|--------|--------|------|
| 潜力 | `#f9ebf2` | `#d64a93` | 粉色系 |
| 明星 | `#fff2e6` | `#f3a358` | 橙色系 |
| 衰退 | `#fde8e8` | `#e66767` | 红色系 |
| 成熟 | `#eef7ed` | `#6ab06d` | 绿色系 |

### 图层顺序

**重要**：图层顺序决定了视觉层级，必须按以下顺序：

1. **背景标签图层**（最底层）
2. **0轴灰色参考线**（可选，x=0 和 y=0）
3. **中位数红色参考线**
4. **参考线数值标注图层**
5. **散点图层**
6. **品类标注图层**

错误的图层顺序会导致标签被参考线遮挡或其他显示问题。

### 0轴参考线（可选）

**用途**：显示经过0点的水平和垂直参考线，帮助区分正负值。

**实现方式**：
```json
{
  "mark": {"type": "rule", "color": "gray", "strokeWidth": 1, "strokeDash": [2, 2]},
  "encoding": {"x": {"datum": 0, "type": "quantitative"}}
}
```

**特点**：
- 颜色：灰色（`gray`）
- 线宽：1（比中位数参考线细）
- 虚线样式：`[2, 2]`（2像素实线 + 2像素间隔）
- 位置：x=0（垂直线），y=0（水平线）

**与中位数参考线的区别**：
| 特性 | 0轴参考线 | 中位数参考线 |
|------|----------|-------------|
| 颜色 | 灰色 | 红色 (#e74c3c) |
| 线宽 | 1 | 2 |
| 虚线样式 | [2, 2] | [4, 4] |
| 用途 | 标识0点，区分正负 | 标识中位数，划分象限 |
| 数值标注 | 无 | 有 |

## 数据格式

**重要**：数据应使用小数形式（0-1范围），配合 axis 的百分比格式显示。

### 数值格式
- **X轴（占比）**：使用小数形式，如 `0.2268` 表示 22.68%
- **Y轴（增长率）**：使用小数形式，如 `-0.3784` 表示 -37.84%

### 为什么使用小数形式？
如果数据是百分比数值（如 22.68），在使用 `format: ".1%"` 时会被格式化为 2268%，因为百分比格式会自动乘以100。

**正确做法**：
```json
{
  "data": {"values": [
    {"brand": "乳饮料", "market_share": 0.2268, "growth": -0.3784}
  ]},
  "mark": {"type": "point"},
  "encoding": {
    "x": {"field": "market_share", "axis": {"format": ".1%"}},
    "y": {"field": "growth", "axis": {"format": ".1%"}}
  }
}
```

**错误做法**：
```json
{
  "data": {"values": [
    {"brand": "乳饮料", "market_share": 22.68, "growth": -37.84}  // ❌ 错误：会被格式化为 2268%
  ]}
}
```

### 数据量建议
- 建议数据量 5-30 个效果最佳
- 自动计算中位线

## 使用步骤

1. **准备数据**：确保数据包含品类、X轴值（市场份额）、Y轴值（增长率），使用小数形式
2. **计算中位数**：作为参考线位置
3. **配置坐标轴**（可选优化）：
   ```json
   {
     "axis": {
       "grid": false,      // 隐藏网格线
       "format": ".1%",    // 百分比格式
       "domain": false,    // 隐藏坐标轴线
       "ticks": false      // 隐藏刻度线
     }
   }
   ```
   **说明**：
   - `grid: false`：隐藏网格线，使图表更简洁
   - `format: ".1%"`：显示百分比格式（数据需为小数形式）
   - `domain: false`：隐藏坐标轴线条（适用于有0轴参考线的场景）
   - `ticks: false`：隐藏刻度线，使图表更简洁
4. **选择模板**：使用 `examples.json` 中的 `standard_quadrant_chart`
5. **替换业务数据**：修改 `layer[1]['data']['values']` 中的数据
6. **调整象限标签位置**（可选）：
   - 根据图表尺寸调整 `x_pos` 和 `y_pos`
   - 参考上方"调整位置"表格
7. **更新参考线数值**：修改参考线上的百分比标注
8. **修改标题和坐标轴标签**：根据实际业务调整
9. **调整坐标轴范围**（可选）：根据数据分布调整 `scale.domain`
