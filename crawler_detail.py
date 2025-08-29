import requests
import json
import time
import os
import random
from tqdm import tqdm


class BilibiliVideoCrawler:
    def __init__(self, json_output_file):
        self.json_output_file = json_output_file
        self._init_output_file()

    def _init_output_file(self):
        os.makedirs(os.path.dirname(self.json_output_file), exist_ok=True)
        if not os.path.exists(self.json_output_file):
            with open(self.json_output_file, 'w', encoding='utf-8') as f:
                json.dump({"videos": [], "total_count": 0, "success_count": 0, "failed_count": 0}, f,
                          ensure_ascii=False, indent=2)

    def _append_to_json(self, video_info):
        try:
            # 读取现有数据
            with open(self.json_output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 更新数据
            if video_info is not None:
                data["videos"].append(video_info)
                data["success_count"] += 1
            else:
                data["failed_count"] += 1
            data["total_count"] += 1

            # 写回文件
            with open(self.json_output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存到JSON文件出错: {e}")
            return False

    def save_video_info(self, video_info):
        return self._append_to_json(video_info)


def get_video_tags(bvid):
    tags_url = f"https://api.bilibili.com/x/web-interface/view/detail/tag?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    try:
        response = requests.get(tags_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data['code'] == 0 and 'data' in data:
            return [tag['tag_name'] for tag in data['data']]
        else:
            print(f"获取标签失败 {bvid}")
            return []

    except Exception as e:
        print(f"获取标签请求出错 {bvid}: {e}")
        return []


def get_video_info(bvid):
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data['code'] == 0:
            video_data = data['data']
            tags = get_video_tags(bvid)

            return {
                "bvid": bvid,
                "title": video_data.get('title', ''),
                "description": video_data.get('desc', ''),
                "tags": tags,
                "owner": video_data.get('owner', {}).get('name', ''),
                "view_count": video_data.get('stat', {}).get('view', 0),
                "like_count": video_data.get('stat', {}).get('like', 0),
                "favorite_count": video_data.get('stat', {}).get('favorite', 0),
                "pub_date": video_data.get('pubdate', 0),
                "video_url": f"https://www.bilibili.com/video/{bvid}"
            }
        else:
            print(f"\n获取 {bvid} 失败")
            return None

    except Exception as e:
        print(f"\n请求 {bvid} 出错: {e}")
        return None


def read_bv_file(filename):
    if not os.path.exists(filename):
        print(f"文件 {filename} 不存在")
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            bv_list = [line.strip() for line in f if line.strip()]

        valid_bv_list = []
        for bvid in bv_list:
            if bvid.startswith('BV') and len(bvid) == 12:
                valid_bv_list.append(bvid)
            else:
                print(f"跳过无效的BV号: {bvid}")

        print(f"找到 {len(valid_bv_list)} 个有效的BV号")
        return valid_bv_list

    except Exception as e:
        print(f"读取文件出错: {e}")
        return []


def main():
    # 文件路径
    name = 'train'
    input_file = ("last.txt")
    # input_file = f"{name}.txt"
    json_output_file = f"../data/raw/{name}.json"
    sleep_time = 0.5

    # 读取BV号列表
    print("正在读取BV号文件...")
    bv_list = read_bv_file(input_file)

    if not bv_list:
        print("没有找到有效的BV号，程序退出")
        return

    crawler = BilibiliVideoCrawler(json_output_file)

    print("\n开始爬取视频信息...")
    start_time = time.time()
    success_count = 0

    pbar = tqdm(bv_list, desc="爬取进度", unit="video")

    for i, bvid in enumerate(pbar):
        video_info = get_video_info(bvid)

        if crawler.save_video_info(video_info):
            if video_info is not None:
                success_count += 1

        # 更新进度条描述信息
        pbar.set_postfix({
            "成功": success_count,
            "失败": i + 1 - success_count,
            "成功率": f"{(success_count / (i + 1)) * 100:.1f}%"
        })

        time.sleep(sleep_time)

        if (i + 1) % 10 == 0:
            time.sleep(random.uniform(2, 3))

    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print(f"爬取完成！总计: {len(bv_list)}, 成功: {success_count}, 失败: {len(bv_list) - success_count}")
    print(f"成功率: {(success_count / len(bv_list)) * 100:.1f}%, 总耗时: {elapsed:.0f}s")
    print(f"数据已保存到: {json_output_file}")


if __name__ == "__main__":
    main()