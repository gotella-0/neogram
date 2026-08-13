#########################################################
# Copyright © 2022 Nikita Smirnov. All rights reserved. #
#########################################################

import configparser
import os
import time

path = 'config.ini'


def create_config():

    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "bot_token", "token")
    config.set("Settings", "admin_owner", "0:1")
    config.set("Settings", "name_project", "0:1")
    config.set("Settings", "qiwi_token", "0")
    config.set("Settings", "price_for_1_day", "15")
    config.set("Settings", "price_for_1_month", "100")
    config.set("Settings", "price_for_2_month", "190")
    config.set("Settings", "price_for_5_month", "430")
    config.set("Settings", "price_for_1_year", "1100")
    config.set("Settings", "price_for_always", "5000")
    config.set("Settings", "nonce", "4EE/9uqhoZ3mQXmm")
    config.set("Settings", "username_bot", "nickname")

    config.set("Settings", "price_access_to_accounts", "150")
    config.set("Settings", "price_access_to_chats", "19")
    config.set("Settings", "price_antipr", "190")
    config.set("Settings", "price_all", "320")

    config.set("Settings", "api_id", "0")
    config.set("Settings", "api_hash", "0")

    with open(path, "w") as config_file:
        config.write(config_file)


def check_config_file():
    if not os.path.exists(path):
        create_config()

        time.sleep(3)
        exit(0)


def config(what):

    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    value = config.get("Settings", what)

    return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    config.set(section="Settings", option=setting, value=value)

    with open(path, "w", "utf-8") as config_file:
        config.write(config_file)


check_config_file()
