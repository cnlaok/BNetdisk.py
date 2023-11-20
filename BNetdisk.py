import os

def create_backup():
    # 获取用户输入的源目录和目标目录路径
    src_dir = input("请输入源目录的路径：")
    dest_dir = input("请输入目标目录的路径：")

    # 检查目标目录是否是源目录或其子目录
    if dest_dir.startswith(src_dir):
        print("错误：不能将备份保存到源目录或其子目录下。")
        return

    # 创建一个用于记录已备份文件和目录的集合
    backed_up = set()

    # 尝试从文件中读取已备份的文件和目录
    try:
        with open('backup_log.txt', 'r') as f:
            for line in f:
                backed_up.add(line.strip())
    except FileNotFoundError:
        pass  # 如果文件不存在，那么我们就假设没有任何文件被备份

    # 记录已备份和未备份的文件数量
    num_backed_up = len(backed_up)
    num_skipped = 0

    # 遍历源目录
    for dirpath, dirnames, filenames in os.walk(src_dir):
        # 创建在目标目录中对应的目录
        dest_path = dirpath.replace(src_dir, dest_dir)
        try:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
        except Exception as e:
            print(f"创建目录 {dest_path} 时出错: {e}")
            continue

        # 对于源目录中的每个文件，如果它还没有被备份，那么就创建一个同名的1KB大小的文件
        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            if src_file in backed_up:
                num_skipped += 1
                continue  # 如果这个文件已经被备份，那么就跳过它

            dest_file = os.path.join(dest_path, filename)
            try:
                with open(dest_file, 'w') as f:
                    f.write(' ' * 1024)  # 创建1KB大小的文件
                # 记录这个文件已经被备份
                backed_up.add(src_file)
                num_backed_up += 1
                print(f"已备份 {num_backed_up} 个文件，跳过 {num_skipped} 个文件")
            except Exception as e:
                print(f"创建文件 {dest_file} 时出错: {e}")

    # 将已备份的文件和目录写入到文件中
    with open('backup_log.txt', 'w') as f:
        for item in backed_up:
            f.write(item + '\n')

    print("备份完成！")

# 使用方法
create_backup()
