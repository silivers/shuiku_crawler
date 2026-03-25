# 水库水文数据可视化看板

本项目是一个完整的水库水文数据采集与可视化工具，能够从四川省政务服务平台爬取水库水文数据，并生成交互式 HTML 数据看板。

## 功能特点

- **数据爬取**：从指定 API 接口获取水库水文数据，支持按日期范围批量爬取
- **数据处理**：自动清洗、去重、按站名和时间排序
- **可视化图表**：
  - 水位变化趋势折线图
  - 入库/出库流量对比折线图
  - 蓄水量变化柱状图
- **交互式看板**：
  - 支持多站点切换
  - 支持图表类型切换
  - 图表支持缩放、数据点标记（最高/最低水位、平均水位等）

## 项目结构
- | 文件名               | 说明                           |
  | -------------------- | ------------------------------ |
  | `main.py`            | 主程序入口                     |
  | `get_csv.py`         | 数据爬虫模块                   |
  | `data_reader.py`     | 数据读取模块                   |
  | `chart_generator.py` | 图表生成模块                   |
  | `html_generator.py`  | HTML 看板生成模块              |
  | `reservoir.csv`      | 爬取的数据文件（运行时生成）   |
  | `example.html`       | 生成的可视化网页（运行时生成） |

## 技术栈

- **Python**
- **pandas**：数据处理
- **pyecharts**：图表生成
- **requests**：HTTP 请求

## 安装与配置

### 1. 克隆项目

```bash
git clone <repository-url>
cd <project-directory>
pip install pandas pyecharts requests
python main.py
```
##  交互式命令行流程
输入起始日期：格式 YYYY-MM-DD，例如 2025-03-21

输入截止日期：格式 YYYY-MM-DD

确认开始：输入 y 确认爬取并生成看板
## 输出文件

- `reservoir.csv`：爬取的原始数据
- `example.html`：生成的交互式数据看板
