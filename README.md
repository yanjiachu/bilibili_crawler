# B站榜单 & 推荐爬虫

> 把 B 站「热门」和「推荐」搬到本地，一键保存标题、UP 主、播放量、弹幕数、封面等信息。

## 能干啥
- 抓取 **全站/分区排行榜**（bilibili API仅提供3日榜单）
- 抓取 **首页推荐流**（可使用cookie获取用户的个性化推荐）
- 导出为 **JSON**，方便做数据分析或备份

## 快速开始
1. 获取bv号：  
   ```bash
   python crawler_rcmd_bv.py
   python crawler_top100_bv.py
   ```
   获取到的bv号保存在 `bv.txt` 文件中
2. bv号清洗：
   ```bash
   python bv_clean.py
   ```
   打乱并且清除重复的bv号（多次爬取可能会得到重复的bv号）

   此外，如果你只想获得推荐视频的话，你也可以输入以下指令：
   ```bash
   sh run.sh
   ```
   一次性完成爬取和清洗操作
3. 拆分数据集：
   ```bash
   python shuffle.py
   ```
4. 爬取视频信息：
   ```bash
   python crawler_detail.py
   ```
5. 查看输出结果：
   输出结果保存在`../data/raw/*.json`中
7. 清洗数据：
   ```bash
   python data_clean.py
   ```
   可以自行调整清洗规则，结果保存在`../data/cleaned/*.json`中

## 声明
仅用于学习和研究，请遵守 B 站用户协议。
