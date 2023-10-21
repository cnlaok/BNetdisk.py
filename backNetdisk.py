import os

def create_backup():
    # 获取用户输入的源目录和目标目录路径
    src_dir = input("请输入源目录的路径：")
    dest_dir = input("请输入目标目录的路径：")

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

        # 对于源目录中的每个文件，创建一个同名的1KB大小的文件
        for filename in filenames:
            dest_file = os.path.join(dest_path, filename)
            try:
                with open(dest_file, 'w') as f:
                    f.write(' ' * 1024)  # 创建1KB大小的文件
            except Exception as e:
                print(f"创建文件 {dest_file} 时出错: {e}")

# 使用方法
create_backup()
