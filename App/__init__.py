# from .. import _private_config as _config_template

from datetime import datetime
from pathlib import Path

import sys
from time import sleep
import importlib
import urllib.parse

from ruamel.yaml import YAML
from mysupport.PopupWindowGenerator._2 import PopupWindowGenerator, checkbox
import _private_config

from . import utils


class App:
    def __init__(self, SCRIPT_DIRECTORY: Path, config_module, sys_argv: list) -> None:
        self.MV_SCRIPT_DIRECTORY = SCRIPT_DIRECTORY
        self.config_module = config_module
        self.sys_argv = sys_argv

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

    def uri(self):

        if len(self.sys_argv) < 2:
            print("请传入要显示的消息作为参数！")
            exit()

        cache_path = self.MV_SCRIPT_DIRECTORY / "file_search_cache.db"

        # 开发模式
        if self.sys_argv[1] == "dev":
            if len(self.sys_argv) < 3:
                print("参数量不足！")
                exit()

            parse_result = urllib.parse.urlparse(f"mylink://{self.sys_argv[2]}")
            config_directory, config_file = utils.main(
                parse_result, cache_path, _private_config.TARGET_PATHS
            )
            if config_directory is not None:
                print(Path(config_directory) / config_file)
            exit()

        parse_result = urllib.parse.urlparse(self.sys_argv[1])

        if parse_result.fragment == "post":
            utils.post(parse_result, _private_config.TARGET_PATHS)
            exit()

        config_directory, config_file = utils.main_withgui(
            parse_result, cache_path, _private_config.TARGET_PATHS
        )
        if config_directory is not None:
            config = utils.get_config(Path(config_directory) / config_file)

            service_path = Path(config_directory) / str(config["service_path"])
            postbox = service_path / ".postbox"

            if postbox.exists():
                if not (postbox / ".config.yml").exists():
                    with (postbox / ".config.yml").open(mode="w"):
                        ...

                with (postbox / ".config.yml").open(mode="r+") as file:
                    yaml = YAML()
                    config_data = yaml.load(file)
                    if not config_data:
                        config_data = {}

                    files = [
                        entry
                        for entry in postbox.iterdir()
                        if (postbox / entry).is_file()
                        and not entry.name.startswith(".")
                    ]
                    if files:
                        # 获取今天的日期，格式化为 'YYYY-MM-DD'
                        today_str = datetime.today().strftime("%Y-%m-%d")
                        if (
                            "Do_Not_Remind_Within_Today" not in config_data
                            or config_data["Do_Not_Remind_Within_Today"] != today_str
                        ):
                            pwg = PopupWindowGenerator(
                                title="Postbox",
                                buttons=["查看并继续", "仅查看", "忽略", "取消"],
                                esc_exit=True,
                            )
                            pwg.add_input_element(checkbox(["今天内不再提示"]))
                            event, values = pwg.popup(
                                f"你有未读文件{len(files)}条！是否查看？"
                            )
                            print(
                                event,
                            )

                            if not event or event == "取消":
                                exit()

                            if values[0][0][1]:
                                config_data["Do_Not_Remind_Within_Today"] = today_str
                                print(config_data)

                                file.seek(0)
                                file.truncate()
                                yaml.dump(config_data, file)
                            elif event == "查看并继续":
                                utils.explore(postbox)
                            elif event == "仅查看":
                                utils.explore(postbox)
                                exit()
                        else:
                            sleep(3)
                            ...

            # 将 config 文件夹添加到系统路径
            sys.path.append(str(config_directory))

            targetfilename = config["index"]
            # 检查目标文件是否存在，不存在则退出
            abstf = Path(config_directory) / str(targetfilename)
            if not abstf.exists():
                exit(-1)

            # 导入 index 模块
            index = importlib.import_module("index")

            # print(Pather(config_directory)(config["service_path"]).str())
            init = getattr(index, config["entrypoint"])
            init(service_path, parse_result)

        else:
            pwg = PopupWindowGenerator().popup("未找到站点，请检查输入是否有误！")

    def run(self):
        pass

# # 使用 with 语句
# with App("测试实例") as obj:
#     obj.show()  # 正常执行
#     # raise ValueError("故意触发异常")  # 取消注释测试异常处理

# print("with 块外操作")
