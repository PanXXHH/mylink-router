from datetime import datetime
from pathlib import Path
import sys
from time import sleep
from libs.GUIProgressDecorator import GUIProgressDecorator
from libs.MylinkGUI import MylinkGUI
import importlib
import os
import urllib.parse
import subprocess
# 其他导入
import shelve
# from mysupport.Pather.Pather3 import Pather
from ruamel.yaml import YAML
from typing import Optional
from mysupport.PopupWindowGenerator._2 import PopupWindowGenerator, checkbox
import uuid
import _private_config
# import App



# 获取脚本的绝对路径
script_directory = Path(__file__).parent

# 将数据库文件名附加到脚本的目录中
CACHE_PATH = script_directory / "file_search_cache.db"


def file_exists_in_dir(filename: str, dir: str) -> bool:
    return (Path(dir) / filename).exists()


def explore(dir: str):
    subprocess.run('explorer %s' % dir)


def get_config(file_path: str) -> dict:
    yaml = YAML()
    try:
        with open(file_path, 'r') as file:
            config_data = yaml.load(file)
            return config_data.get('CONFIG', {})
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def process_root_path(root_value: Optional[str], conf_dir: str) -> str:
    """
    根据 root_value 和 conf_dir 计算最终的绝对路径。

    参数:
    - root_value: 配置文件中指定的根目录。
    - conf_dir: 配置文件所在的目录。

    返回值:
    基于 root_value 和 conf_dir 计算出的绝对路径。
    """
    if not root_value or root_value == '.\\':  # 如果 root_value 为空或者为 '.\\'，则返回 conf_dir
        return conf_dir
    if root_value == '..\\':  # 如果 root_value 为 '..\\'，则返回 conf_dir 的父目录
        return os.path.dirname(conf_dir)

    # 使用 os.path.abspath 确保返回的是绝对路径
    return os.path.abspath(
        root_value if os.path.isabs(
            root_value) else os.path.join(conf_dir, root_value)
    )


def search_config(filename: str, target_dirs: list[str], query=None):
    unique_id = str(uuid.getnode())
    with shelve.open(CACHE_PATH) as cache:
        # print(dict(cache))
        if unique_id not in cache:
            cache[unique_id] = {}

        user_cache: dict = cache[unique_id]

        # 转换 filename 为小写
        filename_lower = filename.lower()

        if filename_lower in (name.lower() for name in user_cache.keys()):
            cached_dir = user_cache[filename_lower]
            if file_exists_in_dir(filename, cached_dir):
                print('从缓存中找到：{}'.format(Path(cached_dir) / filename))
                return cached_dir, Path(cached_dir) / filename

            print(f"缓存路径{cached_dir}不再有效，重新搜索文件...")

        for target_dir in target_dirs:
            for root, dirs, files in os.walk(target_dir):
                # 使用生成器表达式和 any() 来查找匹配的文件（忽略大小写）
                if any(f.lower() == filename_lower for f in files):
                    # 存储小写的文件名以便于忽略大小写的匹配
                    user_cache[filename_lower] = root
                    cache[unique_id] = user_cache
                    print(Path(root) / filename)
                    # print(dict(cache))
                    return root, Path(root) / filename

    return None, None  # 返回 None


def custom_on_close(stop_event=None):
    os._exit(0)


@GUIProgressDecorator(gui_class=MylinkGUI, on_close_callback=custom_on_close)
def main_withgui(parse_result, target_dirs: list[str], gui=None, stop_event=None):

    return main(parse_result, target_dirs)


def main(parse_result, target_dirs: list[str]):

    host = parse_result.netloc  # 获取主机名
    filename = f"mylink.{host}.yml"  # 格式化文件名

    config_directory, config_file = search_config(filename, target_dirs)

    return config_directory, config_file


def post(parse_result, target_dirs: list[str]):
    config_directory, config_file = main_withgui(parse_result, target_dirs)
    if config_directory is None:
        return

    config = get_config(Path(config_directory) / config_file)

    pwg = PopupWindowGenerator(title=f"Post", buttons=[
                               '确定', '取消'], esc_exit=True)
    pwg.add_input_element(str, "内容")
    event, values = pwg.popup(
        f"收件方：{(Path(config_directory) / str(config['service_path'])).resolve().name}(.postbox@service_path.{parse_result.netloc}.mylink)")

    print(event, values)
    if not event or event == "取消":
        return

    content = str(values[0])

    if not content:
        pwg = PopupWindowGenerator().popup("内容不能为空！")
        exit()

    postbox_path = Path(config_directory) / \
        str(config['service_path']) / ".postbox"
    postbox_path.mkdir(exist_ok=True)

    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 获取当前日期并格式化
    filename = postbox_path / f'{current_date}.txt'

    if filename.exists():
        pwg = PopupWindowGenerator().popup("发送消息太频繁，稍后重试！")
        exit()

    with filename.open(mode="w", encoding="utf8") as file:
        file.write(content)

    PopupWindowGenerator().popup("邮件发送成功！")

# from dotenv import load_dotenv

# sys.argv.append("mylink://d.overtime/")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请传入要显示的消息作为参数！")
        exit()

    # # 加载.env文件
    # load_dotenv()
    # # 读取COOKIE变量
    # self._cookies = cookies or os.getenv('COOKIE')




    # 开发模式
    if sys.argv[1] == "dev":
        if len(sys.argv) < 3:
            print("参数量不足！")
            exit()

        parse_result = urllib.parse.urlparse(f"mylink://{sys.argv[2]}")
        config_directory, config_file = main(parse_result, _private_config.TARGET_PATHS)
        if config_directory is not None:
            print(Path(config_directory) / config_file)
        exit()

    parse_result = urllib.parse.urlparse(sys.argv[1])

    if parse_result.fragment == "post":
        post(parse_result, _private_config.TARGET_PATHS)
        exit()

    config_directory, config_file = main_withgui(parse_result, _private_config.TARGET_PATHS)
    if config_directory is not None:
        config = get_config(Path(config_directory) / config_file)

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

                files = [entry for entry in postbox.iterdir() if (
                    postbox / entry).is_file() and not entry.name.startswith(".")]
                if files:
                    # 获取今天的日期，格式化为 'YYYY-MM-DD'
                    today_str = datetime.today().strftime('%Y-%m-%d')
                    if "Do_Not_Remind_Within_Today" not in config_data or config_data["Do_Not_Remind_Within_Today"] != today_str:
                        pwg = PopupWindowGenerator(title="Postbox", buttons=[
                                                   "查看并继续", "仅查看", "忽略", "取消"], esc_exit=True)
                        pwg.add_input_element(checkbox(["今天内不再提示"]))
                        event, values = pwg.popup(f"你有未读文件{len(files)}条！是否查看？")
                        print(event, )

                        if not event:
                            exit()

                        if values[0][0][1]:
                            config_data["Do_Not_Remind_Within_Today"] = today_str
                            print(config_data)

                            file.seek(0)
                            file.truncate()
                            yaml.dump(config_data, file)
                        if event == "取消":
                            exit()
                        elif event == "查看并继续":
                            explore(postbox)
                        elif event == "仅查看":
                            explore(postbox)
                            exit()
                    else:
                        sleep(3)
                        ...

        # 将 config 文件夹添加到系统路径
        sys.path.append(str(config_directory))

        targetfilename = config['index']
        # 检查目标文件是否存在，不存在则退出
        abstf = Path(config_directory) / str(targetfilename)
        if not abstf.exists():
            exit(-1)

        # 导入 index 模块
        index = importlib.import_module('index')

        # print(Pather(config_directory)(config["service_path"]).str())
        init = getattr(index, config["entrypoint"])
        init(service_path, parse_result)

    else:
        pwg = PopupWindowGenerator().popup("未找到站点，请检查输入是否有误！")
