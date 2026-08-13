#########################################################
# Copyright © 2022 Nikita Smirnov. All rights reserved. #
#########################################################

from beauty import Color

MAIN_HELP = f'''
Usage:
    {Color.ITALIC}neogram [-h] [-option] [option args]{Color.END}\n
Example:
    {Color.ITALIC}neogram create auto_shop{Color.END}
    
Options:
    create {"{name_project}"}    Create project of a telegram bot
    run {"{name_project}"}       Run a telegram bot
    remove {"{name_project}"}    Remove project of a telegram bot'''


CREATE_HELP = f'''
Usage:
    {Color.ITALIC}neogram create {"{name_project}"}{Color.END}\n
Example:
    {Color.ITALIC}neogram create auto_shop{Color.END}
'''

RUN_HELP = f'''
Usage:
    {Color.ITALIC}neogram run {"{name_project}"}{Color.END}\n
Example:
    {Color.ITALIC}neogram run auto_shop{Color.END}
'''

REMOVE_HELP = f'''
Usage:
    {Color.ITALIC}neogram remove {"{name_project}"}{Color.END}\n
Example:
    {Color.ITALIC}neogram remove auto_shop{Color.END}
'''