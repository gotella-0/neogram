#!/usr/bin/python3

#########################################################
# Copyright © 2022 Nikita Smirnov. All rights reserved. #
#########################################################

from imports import * # import all


def check_cmd_args():
    args = sys.argv[1:]

    if "create" in args:
        
        if len(args) == 1:
            print(CREATE_HELP)
        else:
            name_project = args[1]
            print(f"{Color.Yellow}[*]{Color.END} Start Creating project...")
            create_project(name_project)
    
    elif "run" in args:

        if len(args) == 1:
            print(RUN_HELP)
        else:
            name_project = args[1]
            print(f"{Color.Yellow}[*]{Color.END} Running project...")
            run_project(name_project)

    elif "remove" in args:

        if len(args) == 1:
            print(REMOVE_HELP)
        else:
            name_project = args[1]
            print(f"{Color.Yellow}[*]{Color.END} Preparing to remove a project...")
            remove_project(name_project)

    else:
        print(MAIN_HELP)



if __name__ == "__main__":
    check_cmd_args()