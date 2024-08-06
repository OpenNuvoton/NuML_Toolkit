import os
import re
import shutil
import subprocess

board_list = [
    #board name, MCU, NuLinkTool
    ['NuMaker_TC8263', 'TC8263', 'NuLink.exe'],
    ['NuMaker-M467HJ', 'M467', 'NuLink_M460_M2L31.exe'],
    ['NuMaker-M55M1', 'M55M1', 'NuLink_M55M1.exe'],
]

def add_flash_parser(subparsers, _):
    """Include parser for 'flash' subcommand"""
    parser = subparsers.add_parser("flash", help="flash binary code")
    parser.set_defaults(func=project_flash)
    parser.add_argument("--project_path", help="specify prjoect path", required=True)
    parser.add_argument("--board", help="specify target board name", required=True)
    parser.add_argument("--project_type", help="specify project type uvision5_armc6/make_gcc_arm", default='make_gcc_arm')

def project_flash(args):
    print('checking binary code ...')
    app_dir = args.project_type + '_nn_inference'
    binary_file = os.path.join(args.project_path, 'generated_projects', app_dir, 'build', 'nn_inference.bin')

    if not os.path.isfile(binary_file):
        print('binary file not found')
        return 1 

    binary_file_abspath = os.path.abspath(binary_file)

    board_found = False

    for board_info in board_list:
        if board_info[0] == args.board:
            board_found = True
            break

    if board_found == False:
        print("board not support")
        return 2

    #check nulink
    nulink_util = shutil.which(board_info[2])

    if nulink_util == None:
        nulink_util = os.path.join(os.path.dirname(__file__), '..', 'tools', 'NuLink Command Tool', board_info[2])
        if not os.path.isfile(nulink_util):
            print('nulink not found')
            return 3

    print(f'NuLink tool: {nulink_util}')
    nulink_util_dir = os.path.dirname(nulink_util)
    cur_dir = os.getcwd()
    os.chdir(nulink_util_dir)

    nulink_connect_cmd = [nulink_util, '-C']
    nulink_erase_cmd = [nulink_util, '-E', 'APROM']
    # Erase + Program APROM
    nulink_write_cmd = [nulink_util, '-W', 'APROM', binary_file_abspath, '1']
    nulink_reset_cmd = [nulink_util, '-S']

    print('connect target board')
    ret =subprocess.run(nulink_connect_cmd, shell=True)
    if ret.returncode == 0:
        print('connect MCU done')
    else:
        print('unable connect MCU')
        return 4

    """
    print('erase target')
    ret =subprocess.run(nulink_erase_cmd, shell=True, check=True)
    if ret.returncode == 0:
        print('erase MCU done')
    else:
        print('unable erase MCU')
        return 5
    """

    print(f'start program target MCU: {binary_file_abspath}')
    ret =subprocess.run(nulink_write_cmd, shell=True)
    if ret.returncode == 0:
        print('program MCU done')
    else:
        print('unable program MCU')
        return 6

    print('reset target')
    ret =subprocess.run(nulink_connect_cmd, shell=True)
    if ret.returncode == 0:
        print('connect MCU done')
    else:
        print('unable connect MCU')
        return 7

    ret =subprocess.run(nulink_reset_cmd, shell=True, check=True)
    if ret.returncode == 0:
        print('reset MCU done')
    else:
        print('reset erase MCU')
        return 8

    os.chdir(cur_dir)
    return 0
