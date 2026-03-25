import pandas as pd
def read_reservoir_data(csv_file):
    """
    读取水库数据CSV文件
    """
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        df['时间'] = pd.to_datetime(df['时间'])
        df = df.sort_values('时间')
        stations = df['站名'].unique().tolist()
        
        return df, stations
    except Exception as e:
        print(f" 读取文件失败: {e}")
        return None, None