import os

def create_backup():
    # 获取用户输入的源目录和目标目录路径
    src_dir = input("请输入源目录的路径：")
    dest_dir = input("请输入目标目录的路径：")

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
                print(f"备份路径：{dest_file}")
            except Exception as e:
                print(f"创建文件 {dest_file} 时出错: {e}")

    # 将已备份的文件和目录写入到文件中
    with open('backup_log.txt', 'w') as f:
        for item in backed_up:
            f.write(item + '\n')

    print("备份完成！")

    # 遍历目标目录并检查是否有缺失的文件或目录
    print("开始检查是否有缺失的文件或目录...")
    for dirpath, dirnames, filenames in os.walk(dest_dir):
        for dirname in dirnames:
            src_dirname = dirpath.replace(dest_dir, src_dir) + '/' + dirname
            if src_dirname not in backed_up:
                print(f"发现缺失的目录：{src_dirname}")
                try:
                    os.makedirs(src_dirname)
                    print(f"已创建缺失的目录：{src_dirname}")
                except Exception as e:
                    print(f"创建缺失的目录 {src_dirname} 时出错: {e}")

        for filename in filenames:
            src_filename = dirpath.replace(dest_dir, src_dir) + '/' + filename
            if src_filename not in backed_up:
                print(f"发现缺失的文件：{src_filename}")
                try:
                    with open(src_filename, 'w') as f:
                        f.write(' ' * 1024)  # 创建1KB大小的文件
                    print(f"已创建缺失的文件：{src_filename}")
                except Exception as e:
                    print(f"创建缺失的文件 {src_filename} 时出错: {e}")

# 使用方法
create_backup()
