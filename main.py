# main.py
import pandas as pd
from datetime import datetime
import logging
from data_reader import read_reservoir_data
from chart_generator import create_water_level_chart, create_flow_chart, create_storage_chart
from html_generator import generate_html_page
from get_csv import ReservoirCrawler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    
    # 输入起始日期
    start_date = input("\n 起始日期 (格式: YYYY-MM-DD，如 2025-03-21): ").strip()
    # 输入截止日期
    end_date = input(" 截止日期 (格式: YYYY-MM-DD): ").strip()

    
    # 输入输出文件名
    output_file = "example.html"
    print(f" 爬取范围: {start_date} 至 {end_date}")

    # 确认开始
    confirm = input("\n确认开始爬取并生成网页? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print(" 已取消操作")
        return
    
    print("\n开始执行...")
    
    try:
        # ========== 第一步：爬取数据 ==========
        
        crawler = ReservoirCrawler()
        
        # 执行爬取
        data = crawler.query_by_date_range(start_date, end_date)
        
        print(f" 共获取 {len(data)} 条数据")
        
        # 保存原始数据
        if data:
            crawler.save_to_csv(data, "reservoir.csv")
            print(f" 数据已保存到 reservoir.csv")
        else:
            print(" 未获取到任何数据，程序退出")
            return
        # ========== 第二步：生成可视化 ==========
        df, stations = read_reservoir_data("reservoir.csv")

        # 生成图表
        charts_data = []
        
        for i, station in enumerate(stations):
            print(f"   - 生成 {station} 的图表... ({i+1}/{len(stations)})")
            
            # 创建图表
            chart1 = create_water_level_chart(df, station)
            chart2 = create_flow_chart(df, station)
            chart3 = create_storage_chart(df, station)
            
            # 获取图表的JSON配置
            chart1_json = chart1.dump_options()
            chart2_json = chart2.dump_options()
            chart3_json = chart3.dump_options()
            
            # 清理站点名称中的特殊字符，用于JS变量名
            clean_name = station.replace('-', '_').replace(' ', '_').replace('（', '_').replace('）', '_').replace('.', '_')
            
            charts_data.append({
                'name': station,
                'clean_name': clean_name,
                'water': chart1_json,
                'flow': chart2_json,
                'storage': chart3_json
            })
        
        # 生成HTML页面
        output_file = generate_html_page(df, stations, charts_data, output_file)

        print(" 水库数据可视化看板已生成")
        
    except Exception as e:
        print(f"\n 执行失败: {e}")

if __name__ == "__main__":
    main()