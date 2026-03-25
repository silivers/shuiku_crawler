# reservoir_crawler.py
import requests
import json
import time
import pandas as pd
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReservoirCrawler:
    def __init__(self):
        # API 地址
        self.gateway_url = "https://tftb.sczwfw.gov.cn:8085/jmas-api-gateway-server/gateway.do"
        self.create_sign_url = "https://tftb.sczwfw.gov.cn:8085/jmas-api-gateway-server/createsign.do"
        
        # 固定参数
        self.app_id = "sltqszdsksssqxxpc"
        self.charset = "UTF-8"
        self.origin = "0"
        self.version = "1"
        
        # Cookie
        self.cookies = {
            'access_token': 'admin-token'
        }
        
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.sczwfw.gov.cn',
            'Referer': 'https://www.sczwfw.gov.cn/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)
    
    def get_sign(self, interface_id: str, biz_content: dict) -> tuple:
        """
        调用 createsign.do 接口获取签名
        返回: (sign, timestamp, biz_content_str)
        """
        timestamp = str(int(time.time() * 1000))
        biz_content_str = json.dumps(biz_content, separators=(',', ':'))
        
        # 构建 multipart/form-data
        boundary = f"----WebKitFormBoundary{int(time.time())}"
        
        data_parts = []
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="app_id"')
        data_parts.append('')
        data_parts.append(self.app_id)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="interface_id"')
        data_parts.append('')
        data_parts.append(interface_id)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="charset"')
        data_parts.append('')
        data_parts.append(self.charset)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="timestamp"')
        data_parts.append('')
        data_parts.append(timestamp)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="biz_content"')
        data_parts.append('')
        data_parts.append(biz_content_str)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="origin"')
        data_parts.append('')
        data_parts.append(self.origin)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="version"')
        data_parts.append('')
        data_parts.append(self.version)
        
        data_parts.append(f'--{boundary}--')
        
        data = '\r\n'.join(data_parts)
        
        headers = {
            **self.headers,
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(data))
        }
        
        try:
            response = self.session.post(
                self.create_sign_url,
                data=data.encode('utf-8'),
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') == True:
                    sign_data = result.get('data', {})
                    if isinstance(sign_data, dict):
                        sign = sign_data.get('sign', '')
                        if sign:
                            return sign, timestamp, biz_content_str
            return None, None, None
        except Exception as e:
            logger.error(f"获取签名失败: {e}")
            return None, None, None
    
    def get_reservoir_data(self, page_num: int = 1, page_size: int = 20, 
                          conditions: List[Dict] = None) -> dict:
        """
        获取水库数据
        
        Args:
            page_num: 页码
            page_size: 每页数量
            conditions: 查询条件列表，格式：
                [
                    {
                        "fieldEn": "sj",           # 字段名: sj(时间)等
                        "fieldValue": "2025",      # 查询值
                        "whereCondition": "like"   # 条件: like(模糊), eq(等于), gt(大于), lt(小于)
                    }
                ]
        
        Returns:
            API响应的JSON数据
        """
        # 构建 biz_content
        biz_content = {
            "currentPage": page_num,
            "pageSize": page_size,
            "conditionList": conditions or []
        }
        
        # 获取签名
        sign, timestamp, biz_content_str = self.get_sign("sltqszdsksssqxx", biz_content)
        
        if not sign:
            logger.error("无法获取签名")
            return {}
        
        # 构建请求
        boundary = f"----WebKitFormBoundary{int(time.time())}"
        
        data_parts = []
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="app_id"')
        data_parts.append('')
        data_parts.append(self.app_id)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="interface_id"')
        data_parts.append('')
        data_parts.append('sltqszdsksssqxx')
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="charset"')
        data_parts.append('')
        data_parts.append(self.charset)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="timestamp"')
        data_parts.append('')
        data_parts.append(timestamp)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="biz_content"')
        data_parts.append('')
        data_parts.append(biz_content_str)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="origin"')
        data_parts.append('')
        data_parts.append(self.origin)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="version"')
        data_parts.append('')
        data_parts.append(self.version)
        
        data_parts.append(f'--{boundary}')
        data_parts.append('Content-Disposition: form-data; name="sign"')
        data_parts.append('')
        data_parts.append(sign)
        
        data_parts.append(f'--{boundary}--')
        
        data = '\r\n'.join(data_parts)
        
        headers = {
            **self.headers,
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(data))
        }
        
        try:
            response = self.session.post(
                self.gateway_url,
                data=data.encode('utf-8'),
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.debug(f"第 {page_num} 页响应: {result.get('msg', 'success')}")
                return result
            else:
                logger.error(f"请求失败: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"请求异常: {e}")
            return {}
    
    def parse_reservoir_data(self, api_response: dict) -> List[Dict]:
        """解析水库数据"""
        reservoirs = []
        
        try:
            if not api_response or api_response.get('success') != True:
                return reservoirs
            
            # 解析 data 字段
            data_content = api_response.get('data', {})
            if isinstance(data_content, str):
                try:
                    data_content = json.loads(data_content)
                except:
                    return reservoirs
            
            # 提取数据列表
            data_list = []
            if isinstance(data_content, dict):
                if 'result' in data_content and 'data' in data_content['result']:
                    data_list = data_content['result']['data'].get('list', [])
                elif 'data' in data_content:
                    data_list = data_content['data'].get('list', [])
            
            for item in data_list:
                reservoir = {
                    '站名': item.get('zhanming', ''),
                    '站码': item.get('zm', ''),
                    '河流名称': item.get('hlmc', ''),
                    '行政区划': item.get('xzqh', ''),
                    '流域名称': item.get('lymc', ''),
                    '库水位(m)': item.get('ksw', ''),
                    '入库流量(m³/s)': item.get('rkll', ''),
                    '出库流量(m³/s)': item.get('ckll', ''),
                    '蓄水量(百万m³)': item.get('xsl', ''),
                    '时间': item.get('sj', '')
                }
                reservoirs.append(reservoir)
                
        except Exception as e:
            logger.error(f"解析数据失败: {e}")
            
        return reservoirs
    
    def get_total_count(self, api_response: dict) -> int:
        """获取总记录数"""
        try:
            if not api_response or api_response.get('success') != True:
                return 0
            
            data_content = api_response.get('data', {})
            if isinstance(data_content, str):
                data_content = json.loads(data_content)
            
            if isinstance(data_content, dict):
                if 'result' in data_content and 'data' in data_content['result']:
                    return data_content['result']['data'].get('total', 0)
                elif 'data' in data_content:
                    return data_content['data'].get('total', 0)
            
            return 0
        except:
            return 0
    
    def query_by_date(self, date_str: str, page_size: int = 20) -> List[Dict]:
        """
        按具体日期爬取
        
        Args:
            date_str: 日期字符串，格式: YYYY-MM-DD 
            page_size: 每页数量
            
        Returns:
            该日期的水库数据列表
        """
        conditions = [
            {
                "fieldEn": "sj",
                "fieldValue": date_str,
                "whereCondition": "like"
            }
        ]
        
        return self._query_with_conditions(conditions, page_size)
    
    def query_by_date_range(self, start_date: str, end_date: str, 
                           page_size: int = 20) -> List[Dict]:
        """
        按日期范围爬取
        
        Args:
            start_date: 开始日期，格式: YYYY-MM-DD
            end_date: 结束日期，格式: YYYY-MM-DD
            page_size: 每页数量
            
        Returns:
            日期范围内的水库数据列表
        """
        all_data = []
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        total_days = (end - start).days + 1
        current_day = 1
        
        current = start
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            logger.info(f"正在爬取 [{current_day}/{total_days}] {date_str}...")
            
            data = self.query_by_date(date_str, page_size)
            all_data.extend(data)
            
            if data:
                logger.info(f"✓ {date_str} 获取 {len(data)} 条数据")
            else:
                logger.info(f"○ {date_str} 无数据")
            
            current += timedelta(days=1)
            current_day += 1
        
        return all_data
    
    def _query_with_conditions(self, conditions: List[Dict], 
                               page_size: int = 20) -> List[Dict]:
        """
        内部方法：使用条件查询获取所有分页数据
        """
        all_data = []
        page = 1
        total = 0
        
        while True:
            response = self.get_reservoir_data(page, page_size, conditions)

            # 检查响应
            if response.get('success') != True:
                logger.error(f"第 {page} 页 API 错误: {response.get('msg')}")
                # 验签失败重试一次
                if response.get('code') == 40007:
                    logger.info("验签失败，尝试重新获取签名...")
                    response = self.get_reservoir_data(page, page_size, conditions)
                    if not response or response.get('success') != True:
                        break
                else:
                    break
            
            # 获取总记录数
            if total == 0:
                total = self.get_total_count(response)
                if total > 0:
                    logger.info(f"总记录数: {total}")
            
            # 解析数据
            reservoirs = self.parse_reservoir_data(response)
            
            if not reservoirs:
                logger.info(f"第 {page} 页无数据")
                break
            
            all_data.extend(reservoirs)
            logger.info(f"第 {page} 页累计 {len(all_data)}/{total}条")
            
            # 判断是否完成
            if total > 0 and len(all_data) >= total:
                logger.info("已获取全部数据")
                break
            
            if len(reservoirs) < page_size:
                logger.info("已到达最后一页")
                break
            
            page += 1
        
        return all_data
    
    def save_to_csv(self, data: List[Dict], filename: str = "reservoir.csv"):
        """保存为 CSV，按站名和时间排序，并清理所有含空数据的条目"""
        if data:
            df = pd.DataFrame(data)
            original_count = len(df)
            
            # 清理所有包含空数据的行
            df = df.replace('', pd.NA).dropna()
            
            # 排序
            df['_datetime'] = pd.to_datetime(df['时间'], format='%Y/%m/%d  %H:%M:%S', errors='coerce')
            df = df.sort_values(by=['站名', '_datetime']).drop(columns=['_datetime'])
            
            # 保存
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            # 输出信息
            print(f" 成功保存 {len(df)} 条数据到 {filename}")
            return True
        else:
            logger.warning("没有数据可保存")
            return False