import random
from pathlib import Path

file_path = Path('bv.txt')

# 读取所有行
lines = [line.rstrip('\n') for line in file_path.open(encoding='utf-8')]

# 按整行字典序排序
lines_sorted = sorted(lines)

# 删除完全重复的行
unique_lines = []
prev = object()
for line in lines_sorted:
    if line != prev:
        unique_lines.append(line)
        prev = line

# 随机打乱
random.shuffle(unique_lines)

# 覆盖写回原文件
file_path.write_text('\n'.join(unique_lines) + ('\n' if unique_lines else ''), encoding='utf-8')

print('处理完成，共删除', len(lines) - len(unique_lines), '行。')