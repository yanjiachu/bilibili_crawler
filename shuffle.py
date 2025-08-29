import random


def split_dataset(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    random.shuffle(lines)

    total_size = len(lines)
    train_size = int(total_size * 0.8)
    eval_size = int(total_size * 0.1)

    train = lines[:train_size]
    eval = lines[train_size:train_size + eval_size]
    test = lines[train_size + eval_size:]

    with open('train.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(train))
    with open('eval.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(eval))
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(test))

    # 打印划分结果信息
    print(f"数据集总大小: {total_size}")
    print(f"训练集大小: {len(train)} ({len(train) / total_size * 100:.1f}%)")
    print(f"验证集大小: {len(eval)} ({len(eval) / total_size * 100:.1f}%)")
    print(f"测试集大小: {len(test)} ({len(test) / total_size * 100:.1f}%)")


if __name__ == '__main__':
    split_dataset("bv.txt")