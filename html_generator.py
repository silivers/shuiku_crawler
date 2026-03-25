# html_generator.py
def generate_html_page(df, stations, charts_data, output_file="reservoir_dashboard.html"):
    """生成完整的HTML页面"""
    
    # 生成完整的HTML
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>水库水文数据对比看板</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
        }}
        
        .header h1 {{
            font-size: 24px;
            margin: 0;
        }}
        
        /* 站点选择区域 */
        .station-section {{
            background: white;
            border-bottom: 1px solid #e8e8e8;
            padding: 15px 0 0 0;
        }}
        
        .section-label {{
            font-size: 12px;
            color: #999;
            padding: 0 30px 8px 30px;
            font-weight: 500;
            letter-spacing: 1px;
        }}
        
        .tabs {{
            padding: 0 30px;
        }}
        
        .tab-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            max-height: 160px;
            overflow-y: auto;
            padding: 5px 0 15px 0;
        }}
        
        .tab-buttons::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        .tab-buttons::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 3px;
        }}
        
        .tab-buttons::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 3px;
        }}
        
        .tab-buttons::-webkit-scrollbar-thumb:hover {{
            background: #a8a8a8;
        }}
        
        .tab-btn {{
            padding: 6px 16px;
            background: #f5f5f5;
            border: 1px solid #e0e0e0;
            cursor: pointer;
            font-size: 13px;
            color: #666;
            transition: all 0.3s;
            border-radius: 20px;
            white-space: nowrap;
        }}
        
        .tab-btn:hover {{
            background: #e8e8e8;
            color: #667eea;
            border-color: #667eea;
        }}
        
        .tab-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        /* 图表类型选择区域 */
        .chart-type-section {{
            background: #fafafa;
            border-bottom: 1px solid #e8e8e8;
            padding: 15px 0;
        }}
        
        .sub-tabs {{
            display: flex;
            gap: 12px;
            padding: 0 30px;
        }}
        
        .sub-tab-btn {{
            padding: 8px 24px;
            background: white;
            border: 1px solid #ddd;
            cursor: pointer;
            font-size: 14px;
            color: #666;
            border-radius: 6px;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        .sub-tab-btn:hover {{
            background: #f0f0f0;
            border-color: #667eea;
        }}
        
        .sub-tab-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .tab-content {{
            display: none;
            padding: 20px 30px 30px 30px;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .sub-tab-content {{
            display: none;
        }}
        
        .sub-tab-content.active {{
            display: block;
        }}
        
        .chart-container {{
            width: 100%;
            height: 550px;
            background: white;
            border-radius: 8px;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .tab-btn {{
                padding: 4px 12px;
                font-size: 11px;
            }}
            
            .sub-tab-btn {{
                padding: 6px 16px;
                font-size: 12px;
            }}
            
            .chart-container {{
                height: 400px;
            }}
            
            .tabs, .sub-tabs {{
                padding: 0 15px;
            }}
            
            .section-label {{
                padding: 0 15px 8px 15px;
            }}
            
            .tab-content {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏞️ 水库水文数据对比看板</h1>
        </div>
        
        <div class="station-section">
            <div class="section-label">📌 选择水库站点</div>
            <div class="tabs">
                <div class="tab-buttons" id="stationTabs">
"""
    
    # 添加所有站点的标签按钮
    for i, station in enumerate(stations):
        active = 'active' if i == 0 else ''
        html_content += f'<button class="tab-btn {active}" data-station="{station}">{station}</button>\n'
    
    html_content += """
                </div>
            </div>
        </div>
        
        <div class="chart-type-section">
            <div class="sub-tabs">
                <button class="sub-tab-btn active" data-subtab="water">📈 水位变化趋势</button>
                <button class="sub-tab-btn" data-subtab="flow">💧 流量对比分析</button>
                <button class="sub-tab-btn" data-subtab="storage">🏔️ 蓄水量变化</button>
            </div>
        </div>
"""
    
    # 添加所有站点的内容
    for i, chart_data in enumerate(charts_data):
        active = 'active' if i == 0 else ''
        html_content += f"""
        <div class="tab-content {active}" id="station-{chart_data['name']}">
            <div class="sub-tab-content active" id="subtab-water-{chart_data['name']}">
                <div class="chart-container" id="chart-water-{chart_data['clean_name']}"></div>
            </div>
            <div class="sub-tab-content" id="subtab-flow-{chart_data['name']}">
                <div class="chart-container" id="chart-flow-{chart_data['clean_name']}"></div>
            </div>
            <div class="sub-tab-content" id="subtab-storage-{chart_data['name']}">
                <div class="chart-container" id="chart-storage-{chart_data['clean_name']}"></div>
            </div>
        </div>
"""
    
    html_content += """
    </div>
    
    <script>
        // 存储图表实例
        var charts = {};
        
        // 初始化所有图表
"""
    
    # 添加所有站点的图表初始化代码
    for chart_data in charts_data:
        html_content += f"""
        // {chart_data['name']} 的图表
        var waterChart_{chart_data['clean_name']} = echarts.init(document.getElementById('chart-water-{chart_data['clean_name']}'));
        waterChart_{chart_data['clean_name']}.setOption({chart_data['water']});
        charts['water-{chart_data['name']}'] = waterChart_{chart_data['clean_name']};
        
        var flowChart_{chart_data['clean_name']} = echarts.init(document.getElementById('chart-flow-{chart_data['clean_name']}'));
        flowChart_{chart_data['clean_name']}.setOption({chart_data['flow']});
        charts['flow-{chart_data['name']}'] = flowChart_{chart_data['clean_name']};
        
        var storageChart_{chart_data['clean_name']} = echarts.init(document.getElementById('chart-storage-{chart_data['clean_name']}'));
        storageChart_{chart_data['clean_name']}.setOption({chart_data['storage']});
        charts['storage-{chart_data['name']}'] = storageChart_{chart_data['clean_name']};
"""
    
    html_content += """
        // 站点标签页切换
        var stationBtns = document.querySelectorAll('.tab-btn[data-station]');
        var stationContents = document.querySelectorAll('.tab-content');
        
        stationBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var station = this.getAttribute('data-station');
                if (!station) return;
                
                stationBtns.forEach(function(b) { b.classList.remove('active'); });
                this.classList.add('active');
                
                stationContents.forEach(function(content) {
                    content.classList.remove('active');
                });
                
                var activeContent = document.getElementById('station-' + station);
                if (activeContent) {
                    activeContent.classList.add('active');
                }
                
                // 调整所有图表大小
                setTimeout(function() {
                    for (var key in charts) {
                        if (charts[key] && charts[key].resize) {
                            charts[key].resize();
                        }
                    }
                }, 100);
            });
        });
        
        // 子标签页切换
        var subTabBtns = document.querySelectorAll('.sub-tab-btn');
        
        subTabBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var subtab = this.getAttribute('data-subtab');
                var activeStation = document.querySelector('.tab-btn.active');
                if (!activeStation) return;
                
                var station = activeStation.getAttribute('data-station');
                if (!station) return;
                
                subTabBtns.forEach(function(b) { b.classList.remove('active'); });
                this.classList.add('active');
                
                // 隐藏所有子标签内容
                var subContents = document.querySelectorAll('.sub-tab-content');
                subContents.forEach(function(content) {
                    content.classList.remove('active');
                });
                
                // 显示选中的子标签内容
                var activeSubContent = document.getElementById('subtab-' + subtab + '-' + station);
                if (activeSubContent) {
                    activeSubContent.classList.add('active');
                }
                
                // 调整图表大小
                setTimeout(function() {
                    var chartKey = subtab + '-' + station;
                    if (charts[chartKey] && charts[chartKey].resize) {
                        charts[chartKey].resize();
                    }
                }, 100);
            });
        });
        
        // 窗口大小改变时调整所有图表
        window.addEventListener('resize', function() {
            for (var key in charts) {
                if (charts[key] && charts[key].resize) {
                    charts[key].resize();
                }
            }
        });
    </script>
</body>
</html>
"""
    
    # 保存文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return output_file