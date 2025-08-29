import json
import os

json_name = 'train'
raw_data_path = f'../data/raw/{json_name}.json'
cleaned_data_path = f'../data/cleaned/{json_name}.json'

try:
    with open(raw_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"原始数据文件未找到: {raw_data_path}")
except json.JSONDecodeError as e:
    raise ValueError(f"JSON 文件格式错误: {e}")

def is_tag_in_text(tag: str, text: str) -> bool:
    tag = tag.lower()
    text = text.lower()
    return tag in text

new_videos = []

for v in data['videos']:
    title_desc = f"{v['title']} {v['description']}"
    matched_tags = []
    unmatched_tags = []

    for tag in v.get('tags', []):
        if is_tag_in_text(tag, title_desc):
            matched_tags.append(tag)
        else:
            unmatched_tags.append(tag)

    no_description = (v.get('description') == '-') or (v.get('description') == '')

    # 丢弃条件：无匹配标签且无简介
    if not matched_tags and no_description:
        continue

    new_videos.append({
        'bvid': v['bvid'],
        'title': v['title'],
        'description': v['description'],
        'tags': v['tags'],
        'matched_tags': matched_tags,
        'extra_tags': unmatched_tags
    })

os.makedirs(os.path.dirname(cleaned_data_path), exist_ok=True)
try:
    with open(cleaned_data_path, 'w', encoding='utf-8') as f:
        json.dump({'videos': new_videos}, f, ensure_ascii=False, indent=2)
except IOError as e:
    raise IOError(f"写入文件失败: {e}")