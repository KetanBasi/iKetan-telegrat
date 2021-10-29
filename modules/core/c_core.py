import configparser
import os
import platform
import random
import requests
import tempfile
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Union, TextIO


# ? ==================
# ? Notes
# ? ==================

#

# ? ==================
# ? Define Variables
# ? ==================

# * Characters for pretty_print()
corner_top_left = "╔"
corner_top_right = "╗"
corner_bottom_left = "╚"
corner_bottom_right = "╝"
hor_double = "═"
hor_double_divide_left = "╠"
hor_double_divide_right = "╣"
hor_single = "─"
hor_single_divide_left = "╟"
hor_single_divide_right = "╢"
ver_double = "║"

# * Default config
default_config = """[base]
name                = iKetan
version             = 0.1
description         = iKetan Telegram Bot
owner               = @KetanBasi
"""


class BotInfo:
    def __init__(
            self, name, version, description, owner, logfile_limit_by,
            logfile_limit_count, logfile_format):
        self.name = name
        self.version = version
        self.description = description
        self.owner = owner
        self.logfile_limit_by = logfile_limit_by
        self.logfile_limit_count = logfile_limit_count
        self.logfile_format = logfile_format.replace("$", "%")
        self._check()

    def __str__(self):
        return self.name
    
    def _check(self):
        if self.logfile_limit_by not in ("count", "day", "week",
                                         "month", "year"):
            raise RuntimeError("Invalid logfile_limit_by on config file")


# ? ==================
# ? Functions
# ? ==================


def get_token(token_name: str) -> Union[str, None]:
    """
    get token from OS environment, read a file if not found
    """
    main_location = os.path.normpath(f"{os.path.dirname(__file__)}/../..")

    if ".env" in os.listdir(main_location):
        # ? Load .env file
        load_dotenv(os.path.join(main_location, ".env"))
    
    try:
        return os.environ[token_name]

    except KeyError:
        raise RuntimeError(f"NO '{token_name}' TOKEN FOUND")


def is_owner(user) -> bool:
    """
    Check if user is bot owner
    """
    owners = get_token("owner")
    return user in owners


def read_file(file, raw=False) -> Union[TextIO, List[str], None]:
    """
    To read a file, get either raw file or list of lines
    """
    try:
        with open(file, "r") as _file:
            if raw:
                return _file
            return [i.strip() for i in _file.readlines()]

    except FileNotFoundError:
        return None


def get_random(file) -> str:
    """
    Get random line from a file
    """
    word_list = read_file(f"assets/{file}")
    return random.choice(word_list)


def create_config(mode) -> bool:
    """
    create config file and fill it with provided default value
    """
    try:
        with open("config.ini", mode) as config_file:
            config_file.write(default_config)
        return True

    except FileNotFoundError:
        return False


def read_config(file) -> BotInfo:
    """
    Read config file
    """
    # * Read config file
    config = configparser.ConfigParser()
    config.read(file)

    try:
        config.read(file)

    except Exception as error:
        if create_config(mode="w"):
            config.read(file)

        else:
            raise error

    config.base = config["base"]
    config.operation = config["operation"]
    new_bot_info = BotInfo(
        config.base.get("name", "bot - iketan"),
        config.base.getfloat("version", "0.1"),
        config.base.get("description", "an iKetan bot"),
        config.operation.getint("cycle_status_delay", 5000),
        config.operation.get("logfile_limit_by", "count"),
        config.operation.getint("logfile_limit_count", 100),
        config.operation.get("logfile_format", "$Y-$m-$d $H.$M.$S"))
    return new_bot_info


def time():
    time_format = this_bot.logfile_format
    return datetime.now().strftime(time_format.strip())


# ? Each line length should be less than 52-78 characters long,
# ?     including spaces and always use space instead of tabs
# ?     for better output result (based on default terminal setting
# ?     which may vary for each device)
def pretty_print(text_list: list):
    max_len = max([len(max(text_block, key=len))
                   for text_block in text_list]) + 2
    text_list_len = len(text_list)
    top_edge = corner_top_left + hor_double * max_len + corner_top_right + "\n"
    main_divide = (
        hor_double_divide_left + hor_double * max_len
        + hor_double_divide_right + "\n")
    bottom_edge = corner_bottom_left + hor_double * max_len + corner_bottom_right
    result_text = top_edge
    for i_block in range(text_list_len):
        for line in text_list[i_block]:
            right_spaces = " " * (max_len - len(line) - 1)
            result_text += ver_double + " " + line + right_spaces + ver_double
            result_text += "\n"

        if i_block != text_list_len - 1:
            result_text += main_divide

    result_text += bottom_edge
    print(result_text)


def read_url_file(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(response.status_code)
    return response.content


def save_file(ctx, file, data_url):
    guild = str(ctx.message.guild.id)
    channel = str(ctx.message.channel.id)
    location = os.path.join(my_work_dir, guild, channel)
    os.makedirs(location, exist_ok=True)
    file_target = os.path.join(location, file)
    response = requests.get(data_url)
    if 200 <= response.status_code < 300:
        with open(file_target, "wb") as target:
            target.write(response.content)
        return file_target
    raise RuntimeError(response.status_code)


def get_file(ctx, file):
    guild = str(ctx.message.guild.id)
    channel = str(ctx.message.channel.id)
    file_path = os.path.join(my_work_dir, guild, channel, file)
    
    if os.path.isfile(file_path):
        with open(file_path, "rb") as target:
            return target.read


def log_limit_exceed():
    last_date = None
    counter = 0
    for item in os.listdir(my_work_dir):
        if item.startswith(this_bot.name) and item.endswith(".log"):
            if this_bot.logfile_limit_by == "count":
                counter += 1
            
            else:
                item_date = datetime.strptime(
                    item[:-4],
                    f"{this_bot.name} {this_bot.logfile_format}")

                if (
                        (last_date is None)
                        or (
                            this_bot.logfile_limit_by == "day"
                            and item_date.day != last_date.day)
                        or (
                            this_bot.logfile_limit_by == "month"
                            and item_date.month != last_date.month)
                        or (
                            this_bot.logfile_limit_by == "year"
                            and item_date.year != last_date.year)
                        ):
                    last_date = item_date

                elif (
                        (
                            this_bot.logfile_limit_by == "day"
                            and item_date.day == last_date.day)
                        or (
                            this_bot.logfile_limit_by == "month"
                            and item_date.month == last_date.month)
                        or (
                            this_bot.logfile_limit_by == "year"
                            and item_date.year == last_date.year)
                        ):
                    continue
                
                else:
                    raise RuntimeError(
                        f"Unexpected error, limit by {this_bot.logfile_limit_by}"
                        )

                counter += 1

    return counter >= this_bot.logfile_limit_count


def clean_log(count=1):
    if count < 0:
        raise RuntimeError("Invalid number of logs to delete.")

    if log_limit_exceed():
        for item in os.listdir(my_work_dir):
            if count == 0:
                break
            
            elif (
                    item.startswith(this_bot.name)
                    and item.endswith(".log")):
                os.remove(item)
                count -= 1


# ? ==================
# ? Addl Variables
# ? ==================


this_machine = platform.system()
this_python = platform.python_version()
this_bot = read_config("config.ini")

my_work_dir = os.path.join(tempfile.gettempdir(), this_bot.name)
