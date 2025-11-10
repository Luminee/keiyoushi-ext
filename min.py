import json
import os

# 预设需要过滤掉的关键词列表（不需要包含前缀）
# 系统会自动添加 'Tachiyomi: ' 前缀并进行全等匹配
filter_keywords = ['3Hentai']

# 名称前缀
NAME_PREFIX = 'Tachiyomi: '

# 读取 index.json 文件
with open('index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 过滤数据，保留不需要舍弃的项
filtered_data = []
for item in data:
    item_name = item.get('name', '')
    # 检查名称是否与任何带前缀的关键词完全匹配
    should_filter = False
    for keyword in filter_keywords:
        # 自动添加前缀并进行全等匹配
        full_name_to_filter = f'{NAME_PREFIX}{keyword}'
        if item_name == full_name_to_filter:
            should_filter = True
            break
    # 如果不应该过滤，则保留该项
    if not should_filter:
        filtered_data.append(item)

# 确保输出目录存在
output_dir = 'luminee'
os.makedirs(output_dir, exist_ok=True)

# 将过滤后的数据写入 luminee/index.min.json
with open(os.path.join(output_dir, 'index.min.json'), 'w', encoding='utf-8') as f:
    # 使用 ensure_ascii=False 保证中文等非ASCII字符正确显示
    # 使用 separators 移除不必要的空格，生成紧凑的JSON
    json.dump(filtered_data, f, ensure_ascii=False, separators=(',', ':'))

print(f"处理完成！\n- 原数据项数: {len(data)}\n- 过滤后数据项数: {len(filtered_data)}\n- 输出文件: {os.path.join(output_dir, 'index.min.json')}")