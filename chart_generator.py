# chart_generator.py
import pandas as pd
from pyecharts.charts import Line, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

def create_water_level_chart(df, station_name):
    """创建水位变化折线图"""
    station_data = df[df['站名'] == station_name].copy().sort_values('时间')
    
    # 按天聚合数据（取每天的最后值）
    station_data['日期'] = station_data['时间'].dt.date
    daily_data = station_data.groupby('日期').agg({
        '库水位(m)': 'last',
        '时间': 'last'
    }).reset_index()
    
    dates = daily_data['时间'].dt.strftime('%Y-%m-%d').tolist()
    water_levels = daily_data['库水位(m)'].tolist()
    
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="550px"))
        .add_xaxis(dates)
        .add_yaxis(
            "库水位 (m)",
            water_levels,
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=3, color="#5470c6"),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3, color="#5470c6"),
            label_opts=opts.LabelOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(trigger="axis", formatter="日期: {b}<br/>水位: {c} m")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{station_name}水库水位变化趋势",
                pos_top="10",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_size=16, font_weight='bold')
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45, interval=max(1, len(dates)//15))
            ),
            yaxis_opts=opts.AxisOpts(
                name="水位 (m)", 
                name_location="middle", 
                name_gap=45,
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=100, type_="slider"),
                opts.DataZoomOpts(type_="inside")
            ]
        )
        .set_series_opts(
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最高水位"),
                    opts.MarkPointItem(type_="min", name="最低水位")
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均水位")]
            )
        )
    )
    return line

def create_flow_chart(df, station_name):
    """创建入库与出库流量对比图"""
    station_data = df[df['站名'] == station_name].copy().sort_values('时间')
    
    # 按天聚合数据
    station_data['日期'] = station_data['时间'].dt.date
    daily_data = station_data.groupby('日期').agg({
        '入库流量(m³/s)': 'mean',
        '出库流量(m³/s)': 'mean',
        '时间': 'last'
    }).reset_index()
    
    dates = daily_data['时间'].dt.strftime('%Y-%m-%d').tolist()
    inflow = daily_data['入库流量(m³/s)'].round(2).tolist()
    outflow = daily_data['出库流量(m³/s)'].round(2).tolist()
    
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="550px"))
        .add_xaxis(dates)
        .add_yaxis(
            "入库流量 (m³/s)",
            inflow,
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=2, color="#91cc75"),
            symbol="circle",
            symbol_size=6,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .add_yaxis(
            "出库流量 (m³/s)",
            outflow,
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=2, color="#fac858"),
            symbol="diamond",
            symbol_size=6,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{station_name}水库流量对比分析",
                pos_top="10",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_size=16, font_weight='bold')
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45, interval=max(1, len(dates)//15))
            ),
            yaxis_opts=opts.AxisOpts(
                name="流量 (m³/s)", 
                name_location="middle", 
                name_gap=45,
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                formatter="{b}<br/>入库: {c0} m³/s<br/>出库: {c1} m³/s"
            ),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=100, type_="slider"),
                opts.DataZoomOpts(type_="inside")
            ]
        )
    )
    return line

    
def create_storage_chart(df, station_name):
    """创建蓄水量变化柱状图"""
    station_data = df[df['站名'] == station_name].copy().sort_values('时间')
    
    # 按天聚合数据
    station_data['日期'] = station_data['时间'].dt.date
    daily_data = station_data.groupby('日期').agg({
        '蓄水量(百万m³)': 'last',
        '时间': 'last'
    }).reset_index()
    
    dates = daily_data['时间'].dt.strftime('%Y-%m-%d').tolist()
    storage = daily_data['蓄水量(百万m³)'].round(2).tolist()
    
    # 如果数据点太多，适当采样显示
    if len(dates) > 30:
        step = len(dates) // 30
        display_dates = dates[::step]
        display_storage = storage[::step]
    else:
        display_dates = dates
        display_storage = storage
    
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="550px"))
        .add_xaxis(display_dates)
        .add_yaxis(
            "蓄水量 (百万m³)",
            display_storage,
            label_opts=opts.LabelOpts(is_show=True, position="top", rotate=45 if len(display_dates) > 15 else 0, font_size=10),
            itemstyle_opts=opts.ItemStyleOpts(
                color="rgba(84, 112, 198, 0.7)",
                border_color="#5470c6",
                border_width=1
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{station_name}水库蓄水量变化",
                pos_top="10",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_size=16, font_weight='bold')
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45, interval=max(1, len(display_dates)//10))
            ),
            yaxis_opts=opts.AxisOpts(
                name="蓄水量 (百万m³)", 
                name_location="middle", 
                name_gap=45,
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                formatter="{b}<br/>蓄水量: {c} 百万m³"
            ),
            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider")]
        )
    )
    return bar