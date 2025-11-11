import json
import os

# 预设需要过滤掉的关键词列表（不需要包含前缀）
# 系统会自动添加 'Tachiyomi: ' 前缀并进行全等匹配
filter_keywords = ['3Hentai', '3600000 Beauty', 'BlackToon', 'Dragon Ball Multiverse', 'E-Hentai', 'Hachiraw', 'MangaRaw', 'Manhwa Raw', 'Manhwa Toon', 'ManyToonClub', 'Meitua.top', 'MyReadingManga', 'NovelCrow', 'NovelCool', 'Picacomic', 'PornComix', 'Raw18', 'Roumanwu', 'YKMH']

# 名称前缀
NAME_PREFIX = 'Tachiyomi: '

# 定义允许保留的语言列表
allowed_languages = ['all', 'en', 'ja', 'ko', 'zh']

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
    
    # 如果不应该过滤，则保留该项并处理sources
    if not should_filter:
        # 检查并过滤sources字段中的语言
        if 'sources' in item and isinstance(item['sources'], list):
            # 过滤sources，只保留允许的语言
            filtered_sources = []
            for source in item['sources']:
                source_lang = source.get('lang', '')
                if source_lang in allowed_languages:
                    filtered_sources.append(source)
            # 更新item的sources为过滤后的列表
            item['sources'] = filtered_sources
        
        # 只有当source不为空时，才添加到filtered_data
        if len(item.get('sources', [])) > 0:
            filtered_data.append(item)

# 将过滤后的数据写入当前目录的 luminee-index.min.json
output_file = 'index.min.json'
with open(output_file, 'w', encoding='utf-8') as f:
    # 使用 ensure_ascii=False 保证中文等非ASCII字符正确显示
    # 使用 separators 移除不必要的空格，生成紧凑的JSON
    json.dump(filtered_data, f, ensure_ascii=False, separators=(',', ':'))

# 按source数量从少到多排序输出资源信息
# 按资源数量分组资源名称
resource_by_count = {}

for item in filtered_data:
    sources = item.get('sources', [])
    source_count = len(sources)
    
    # 当source为空时，忽略当前资源
    if source_count > 0:
        resource_name = item.get('name', 'Unknown Resource')
        
        # 移除资源名称中的前缀（如果存在）
        if resource_name.startswith(NAME_PREFIX):
            resource_name = resource_name[len(NAME_PREFIX):]
        
        # 按资源数量分组
        if source_count not in resource_by_count:
            resource_by_count[source_count] = []
        
        # 添加资源名称到对应分组
        resource_by_count[source_count].append(resource_name)

# 输出统计信息
print(f"处理完成！")
print(f"- 原数据项数: {len(data)}")
print(f"- 过滤后数据项数: {len(filtered_data)}")
print(f"- 输出文件: {output_file}")

# 准备写入status.md的内容
status_content = []
status_content.append("# 资源统计报告")
status_content.append("\n## 基本信息")
status_content.append(f"- 原数据项数: {len(data)}")
status_content.append(f"- 过滤后数据项数: {len(filtered_data)}")
status_content.append(f"- 输出文件: {output_file}")
status_content.append("\n## 按资源数量分组")

print("\n按资源数量从少到多排序:")

# 按资源数量从少到多输出所有资源
for count in sorted(resource_by_count.keys()):
    resources = resource_by_count[count]
    print(f"资源数 {count}: [")
    # 逐行显示资源名称，避免输出过长被截断
    for i, resource in enumerate(resources):
        comma = "," if i < len(resources) - 1 else ""
        print(f"  '{resource}'{comma}")
    print("]")
    
    # 将分组信息添加到status.md内容
    status_content.append(f"\n### 资源数 {count} ({len(resources)}个)")
    status_content.append("```")
    for resource in resources:
        status_content.append(resource)
    status_content.append("```")

# 输出整体统计
# 统计含有source的资源数（只计算source_count > 0的资源）
resources_with_positive_sources = 0
for count, resources in resource_by_count.items():
    if count > 0:
        resources_with_positive_sources += len(resources)

total_sources = sum(count * len(resources) for count, resources in resource_by_count.items())
print(f"\n整体统计:")
print(f"- 总资源数: {len(filtered_data)}")
print(f"- 含有source的资源数: {resources_with_positive_sources}")
print(f"- 总source数: {total_sources}")

# 将整体统计添加到status.md内容
status_content.append("\n## 整体统计")
status_content.append(f"- 总资源数: {len(filtered_data)}")
status_content.append(f"- 含有source的资源数: {resources_with_positive_sources}")
status_content.append(f"- 总source数: {total_sources}")

# 写入status.md文件
status_file = 'status.md'
with open(status_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(status_content))
    
print(f"\n统计报告已写入到 {status_file}")