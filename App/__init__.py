

class App:
    def __init__(self, config_file_path: str, data_directory_path: str) -> None:
        print(f"初始化实例")

    def __enter__(self):
        print("进入 with 语句块")
        # 返回的对象会被 as 关键字接收（可以是实例自身或其他对象）
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("离开 with 语句块")
        # 处理异常（返回True表示已处理异常，False会向上传播异常）
        if exc_type:
            print(f"发生异常: {exc_type}, {exc_value}")
        # 如果需要资源清理，可在此操作
        return True  # 忽略所有异常

    def show(self):
        print(f"执行方法")

# # 使用 with 语句
# with App("测试实例") as obj:
#     obj.show()  # 正常执行
#     # raise ValueError("故意触发异常")  # 取消注释测试异常处理

# print("with 块外操作")