---
name: china-map
description: "生成中国地图可视化，支持省份/城市数据展示。触发词：生成中国地图、中国地图可视化、省份地图、地域分布、区域数据地图、冠军地图。"
---

# China Map - 中国地图可视化

生成中国地图可视化，支持省份/城市数据展示。

## 适用场景

- 省份销售数据分布
- 城市市场覆盖分析
- 区域业绩热力图
- 地理位置相关数据展示

## 核心原则

**简单优先**：使用默认配置，按需定制

1. **数据源**：使用 `cn-atlas` 的 TopoJSON 数据
2. **投影方式**：使用 `mercator` 投影，中心坐标 `[104, 35]`
3. **颜色填充**：默认使用浅蓝填充 `#e6f2ff`
4. **边框样式**：灰色边框 `#666`，宽度 `0.5`
5. **交互提示**：在 tooltip 中显示省份名称和区划码
6. **⚠️ 数据关联（重要）**：必须使用 `properties.地名` 字段进行数据关联，省份名称必须是完整的省份全称（如"黑龙江省"、"北京市"）

## 地图数据源

中国地图使用在线 TopoJSON 数据：

```json
{
  "data": {
    "url": "https://unpkg.com/cn-atlas/cn-atlas.json",
    "format": {
      "type": "topojson",
      "feature": "provinces"
    }
  }
}
```

**可用字段：**
- `properties.地名` - 省份简称
- `properties.区划码` - 区划码
- `properties.名称` - 省份全称

## 投影配置

使用墨卡托投影（Mercator projection）：

```json
{
  "projection": {
    "type": "mercator",
    "center": [104, 35],
    "scale": 650
  }
}
```

- **center**: 投影中心 `[经度, 纬度]`，默认 `[104, 35]` 是中国地理中心
- **scale**: 缩放级别，默认 `650`，可根据需要调整

## 基础地图示例

完整示例请参见 `examples.json` 文件。

### 标准中国地图

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": 800,
  "height": 600,
  "title": "中国地图",
  "data": {
    "url": "https://unpkg.com/cn-atlas/cn-atlas.json",
    "format": {
      "type": "topojson",
      "feature": "provinces"
    }
  },
  "projection": {
    "type": "mercator",
    "center": [104, 35],
    "scale": 650
  },
  "mark": {
    "type": "geoshape",
    "fill": "#e6f2ff",
    "stroke": "#666",
    "strokeWidth": 0.5
  },
  "encoding": {
    "tooltip": [
      {"field": "properties.地名", "type": "nominal", "title": "简称"},
      {"field": "properties.区划码", "type": "nominal", "title": "区划码"}
    ]
  }
}
```

## 数据可视化地图

### 热力图（按数据值着色）

当需要按数据值（如销售额、覆盖率）着色时：

```json
{
  "mark": {
    "type": "geoshape",
    "stroke": "#666",
    "strokeWidth": 0.5
  },
  "encoding": {
    "color": {
      "field": "sales",
      "type": "quantitative",
      "title": "销售额",
      "legend": {"orient": "right"}
    },
    "tooltip": [
      {"field": "properties.地名", "type": "nominal", "title": "省份"},
      {"field": "sales", "type": "quantitative", "title": "销售额", "format": ","}
    ]
  }
}
```

**注意**：需要将业务数据与地图数据通过省份名称关联。

### 数据关联方式

**⚠️ 重要：必须使用 `properties.地名` 进行数据关联**

在 data 中添加业务字段，如 `sales`：

```json
{
  "data": {
    "url": "https://unpkg.com/cn-atlas/cn-atlas.json",
    "format": {"type": "topojson", "feature": "provinces"}
  },
  "transform": [
    {
      "lookup": "properties.地名",
      "from": {
        "data": {"values": [
          {"province": "黑龙江省", "sales": 1000000},
          {"province": "北京市", "sales": 2000000}
        ]},
        "key": "province",
        "fields": ["sales"]
      }
    }
  ]
}
```

**注意事项：**
1. 使用 `lookup: "properties.地名"` 而不是 `properties.名称`
2. 省份名称必须是完整的省份全称（如"黑龙江省"、"北京市"、"内蒙古自治区"）
3. 不要使用简称（如"黑龙江"、"北京"）或不含后缀的名称

**方法 2：使用单独的数据源**

```json
{
  "data": {"values": [...]},
  "transform": [
    {"lookup": "省份", "from": {...}, "as": "geo"}
  ],
  "mark": "geoshape",
  "encoding": {
    "shape": {"field": "geo.geometry", "type": "geojson"}
  }
}
```

## 常见错误

### ❌ 错误 1：缺少 projection 配置

**问题**：地图无法正确显示或严重变形。

**错误代码：**
```json
{
  "mark": {"type": "geoshape"}
  // 缺少 projection
}
```

**✅ 正确做法：**
```json
{
  "projection": {
    "type": "mercator",
    "center": [104, 35],
    "scale": 650
  },
  "mark": {"type": "geoshape"}
}
```

### ❌ 错误 2：数据字段路径错误

**问题**：tooltip 无法显示省份信息。

**错误代码：**
```json
{
  "encoding": {
    "tooltip": [
      {"field": "地名", "type": "nominal"}  // 错误路径
    ]
  }
}
```

**✅ 正确做法：**
```json
{
  "encoding": {
    "tooltip": [
      {"field": "properties.地名", "type": "nominal"},  // 正确路径
      {"field": "properties.区划码", "type": "nominal"}
    ]
  }
}
```

**原因**：TopoJSON 数据的属性存储在 `properties` 对象中。

### ❌ 错误 3：投影中心设置不当

**问题**：地图显示不完整或偏移。

**✅ 正确做法：**
- 中国地理中心：`[104, 35]`（经度 104°E，纬度 35°N）
- 如需调整，可微调 `center` 和 `scale` 值

## 样式定制

### 调整地图尺寸

```json
{
  "width": 1000,
  "height": 800
}
```

### 自定义颜色方案

**单色填充：**
```json
{
  "mark": {
    "fill": "#e6f2ff",
    "stroke": "#666",
    "strokeWidth": 0.5
  }
}
```

**按数据值着色：**
```json
{
  "encoding": {
    "color": {
      "field": "sales",
      "type": "quantitative",
      "scale": {
        "scheme": "blues"  // 使用蓝色渐变
      }
    }
  }
}
```

**可用配色方案**（Vega-Lite 内置）：
- `blues` - 蓝色渐变
- `reds` - 红色渐变
- `greens` - 绿色渐变
- `oranges` - 橙色渐变
- `viridis` - 紫-绿渐变

## 最佳实践

1. **使用在线数据源**：`https://unpkg.com/cn-atlas/cn-atlas.json`
2. **配置投影参数**：`center: [104, 35]`, `scale: 650`
3. **添加交互提示**：显示省份名称和业务数据
4. **使用默认配色**：除非有明确需求，使用默认填充色 `#e6f2ff`
5. **边框统一**：灰色 `#666`，宽度 `0.5`

## 多品牌地图可视化

### 场景：冠军品牌地图

需要展示不同品牌的市场分布，且同一品牌用颜色深浅表示市占率。

**实现要点**：

1. **市占率分档**：按照 0-10%, 10-20%, 20-30%, 30-50%, 50-100% 分档
2. **品牌-分档组合**：每个品牌+市占率范围定义唯一标识
3. **颜色映射**：为每个品牌-分档组合手动定义颜色，确保同一品牌内颜色逐渐加深
4. **图例显示**：右侧显示所有出现的品牌-市占率组合
5. **无数据处理**：无数据省份显示为白色

**示例代码**：参见 `examples.json` 中的 `champion_brand_map` 示例。

### 常见问题及解决方案

#### ❌ 问题 1：地图只显示一半或被压缩

**原因**：
- 使用 `hconcat` 导致宽度超出显示范围
- 地图尺寸设置不当
- 图例覆盖地图区域

**解决方案**：
- 不使用 `hconcat`，使用单张地图
- 合理设置 width/height（建议 1000×700）
- 确保总宽度在屏幕内（地图宽度 + 图例宽度 < 屏幕宽度）

#### ❌ 问题 2：颜色显示不正确

**原因**：
- 使用 `layer` 叠加导致颜色覆盖
- 填充字段与描边字段冲突

**解决方案**：
- 使用单个 `fill` encoding
- 不使用 `layer` 叠加（除非各图层完全不重叠）
- 确保颜色 scale 的 domain 与实际数据匹配

#### ❌ 问题 3：图例不显示

**原因**：
- 设置 `legend: null`
- 使用 `opacity` 或 `fillOpacity` 导致图例被隐藏
- 图例超出显示区域

**解决方案**：
- 移除 `legend: null` 或设置为配置对象
- 使用 `fill` 而不是 `fillOpacity`
- 检查图例的 `orient` 方向和位置

#### ❌ 问题 4：省份名称匹配不上

**原因**：
- 使用了错误的字段路径
- 数据源中的省份名称格式不正确

**解决方案**：
- ✅ **必须使用** `lookup: "properties.地名"` 进行数据关联
- ✅ 省份名称必须是**完整的省份全称**（如"黑龙江省"、"北京市"、"内蒙古自治区"）
- ❌ **不要使用** `properties.名称` 进行 lookup
- ❌ **不要使用** 简称（如"黑龙江"、"北京"、"内蒙"）

**示例：**
```json
{
  "transform": [
    {
      "lookup": "properties.地名",  // ✅ 正确
      "from": {
        "data": {"values": [
          {"province": "黑龙江省", "sales": 1000000},  // ✅ 正确格式
          {"province": "北京市", "sales": 2000000}     // ✅ 正确格式
        ]},
        "key": "province",
        "fields": ["sales"]
      }
    }
  ]
}
```

**错误示例：**
```json
{
  "lookup": "properties.名称",  // ❌ 错误：不要用这个字段
  ...
  {"province": "黑龙江", "sales": 1000000},  // ❌ 错误：缺少"省"字
  {"province": "北京", "sales": 2000000}      // ❌ 错误：缺少"市"字
}
```

#### ❌ 问题 5：想要渐变图例但显示为离散方块

**原因**：
- Vega-Lite 单个地图只能有一个图例
- 使用 `nominal` 类型导致离散图例
- 使用 `quantitative` 类型只能有一个渐变

**解决方案**：
- 如果需要每个品牌独立的渐变图例，必须使用 `hconcat` 或 `facet`
- 单张地图的限制：只能有一个 color encoding，因此只能有一个 legend
- 折中方案：显示所有品牌-分档组合，用离散方块图例，颜色从浅到深排列

## 使用步骤

1. 从 `examples.json` 选择合适的示例
2. 根据需求调整 `projection` 参数（center, scale）
3. 如需数据可视化，准备业务数据并关联
4. 配置 `tooltip` 显示必要信息
5. （可选）自定义颜色和边框样式
