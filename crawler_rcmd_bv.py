import requests
import time
import random


class BiliBiliHotVideoSpider:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'Referer': 'https://www.bilibili.com/',
            'Origin': 'https://www.bilibili.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            # 'Cookie': ''
        }
        self.min_play_count = 250000  # 最小播放量要求
        self.empty_count = 0  # 记录连续无新数据的次数

    def get_recommend_videos(self, page=1):
        url = "https://api.bilibili.com/x/web-interface/index/top/feed/rcmd"
        params = {
            'y_num': 5,
            'fresh_type': 4,
            'feed_version': 'V5',
            'fresh_idx': page,
            'fresh_idx_1h': page,
            'fetch_row': page,
            'ps': 20
        }

        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None

    def parse_videos(self, data):
        new_bv = []
        if data and data.get('code') == 0:
            for item in data.get('data', {}).get('item', []):
                bvid = item.get('bvid')
                play_count = item.get('stat', {}).get('view', 0)

                if bvid and play_count >= self.min_play_count:
                    new_bv.append(bvid)

        return new_bv

    def save_bv_to_file(self, bv_list):
        with open('bv.txt', 'a', encoding='utf-8') as f:
            for bv in bv_list:
                f.write(bv + '\n')

    def collect_videos(self, target_count):
        all_bv_count = 0
        print(f"开始采集，目标获取 {target_count} 个BV号")

        recommend_page = 1
        while all_bv_count < target_count:
            data = self.get_recommend_videos(recommend_page)
            new_bv = self.parse_videos(data)

            if new_bv:
                # 立即保存新获取的BV号
                self.save_bv_to_file(new_bv)
                all_bv_count += len(new_bv)
                print(f"推荐页 {recommend_page}: 获取 {len(new_bv)} 个, 总计 {all_bv_count} 个")
                self.empty_count = 0  # 重置连续无数据计数
            else:
                self.empty_count += 1
                print(f"推荐页 {recommend_page}: 未获取到新数据，连续无数据次数: {self.empty_count}")

            # 检查是否连续三次无新数据
            if self.empty_count >= 3:
                print("连续三次未获取到新数据，自动停止采集")
                break

            recommend_page += 1

            if recommend_page % 10 == 0:
                time.sleep(random.uniform(1, 1.5))
            else:
                time.sleep(random.uniform(0.3, 0.5))

            # 防止无限循环
            if recommend_page > 1000:
                print("已采集1000页，停止采集")
                break

        return all_bv_count


if __name__ == '__main__':
    spider = BiliBiliHotVideoSpider()
    final_count = spider.collect_videos(1000)
    print(f"共获取 {final_count} 个推荐视频的BV号")