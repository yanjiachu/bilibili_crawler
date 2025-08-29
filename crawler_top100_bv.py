import requests
import time
import random
from typing import List


class BilibiliRankSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/ranking',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.bilibili.com',
            'Connection': 'keep-alive',
        }
        self.base_url = "https://api.bilibili.com/x/web-interface/ranking"
        self.bv_list = []

    def get_params(self, page_num: int):
        return {
            'rid': '0', # 分区编号
            'type': 'all',
            'page': page_num,
            'page_size': 100
        }

    def fetch_page(self, page_num: int) -> List[str]:
        try:
            params = self.get_params(page_num)
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )

            if response.status_code != 200:
                print(f"第{page_num}页请求失败，状态码：{response.status_code}")
                return []

            data = response.json()
            if data['code'] != 0:
                print(f"第{page_num}页API返回错误：{data['message']}")
                return []

            videos = data['data']['list']
            page_bv_list = []

            for video in videos:
                bvid = video.get('bvid')
                if bvid:
                    page_bv_list.append(bvid)

            print(f"第{page_num}页获取到{len(page_bv_list)}个BV号")
            return page_bv_list

        except Exception as e:
            print(f"第{page_num}页获取失败：{str(e)}")
            return []

    def fetch_all(self, total: int = 100):
        pages = total // 100
        if total % 100 != 0:
            pages += 1

        for page in range(1, pages + 1):
            print(f"正在获取第{page}页...")
            page_bv_list = self.fetch_page(page)
            self.bv_list.extend(page_bv_list)

            # 随机延迟，避免请求过于频繁
            time.sleep(random.uniform(1, 2))

            # 如果已经达到目标数量，提前结束
            if len(self.bv_list) >= total:
                self.bv_list = self.bv_list[:total]
                break

        print(f"共获取{len(self.bv_list)}个BV号")

    def save_to_file(self, filename):
        with open(filename, 'a', encoding='utf-8') as f:
            for bv in self.bv_list:
                f.write(bv + '\n')
        print(f"BV号已保存到{filename}")


def main():
    spider = BilibiliRankSpider()
    spider.fetch_all(100) # 只能获取100个，因为排行榜只有top100的视频
    spider.save_to_file("bv.txt")


if __name__ == "__main__":
    main()