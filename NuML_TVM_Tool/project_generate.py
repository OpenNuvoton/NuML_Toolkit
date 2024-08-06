import argparse
import logging
import sys
import os
import pathlib
import git
import shutil
import subprocess
import tarfile

from git import RemoteProgress
from tqdm import tqdm
from tvm_header_parser import HeaderParser
from main_c_codegen import MainCCodegen


PROJECT_GEN_DIR_PREFIX = 'ProjGen_'
PROJECT_GEN_EXAMPLE_DIR = 'example'

board_list = [
    #board name, MCU, BSP name, BSP URL
    ['NuMaker_TC8263', 'TC8263', 'TC8263BSP', 'https://github.com/chchen59/M55A1BSP.git'],
    #['NuMaker-M467HJ', 'M467', 'm460BSP', 'git@github.com:OpenNuvoton/m460bsp.git'],
    ['NuMaker-M55M1', 'M55M1', 'M55M1BSP', 'https://github.com/OpenNuvoton/M55M1BSP.git'],
    ['NuMaker-M467HJ', 'M467', 'm460bsp', 'https://github.com/OpenNuvoton/m460bsp.git'],
    
]

project_type_list = ['uvision5_armc6', 'make_gcc_arm']

class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()

def add_generate_parser(subparsers, _):
    """Include parser for 'generate' subcommand"""
    parser = subparsers.add_parser("generate", help="generate ml project")
    parser.set_defaults(func=project_generate)
    parser.add_argument("--model_file", help="specify tflte file", required=True)
    parser.add_argument("--output_path", help="specify output file path", required=True)
    parser.add_argument("--board", help="specify target board name", required=True)
    parser.add_argument("--project_type", help="specify project type uvision5_armc6/make_gcc_arm", default='make_gcc_arm')
    parser.add_argument("--templates_path", help="specify template path")

def model_compile(board_info, output_path, tvmc_dir_path, model_file):
    cur_work_dir = os.getcwd()
    os.chdir(output_path)
    tvmc_exe = os.path.join(tvmc_dir_path, 'tvmc.exe')
    tvmc_config_file =  board_info[1] + '.json'
    tvmc_conifg_option = '--config=' + os.path.join(tvmc_dir_path, 'config', tvmc_config_file)
    tvmc_cmd = [tvmc_exe, tvmc_conifg_option, 'compile', model_file]
    print('tvmc compile start ...')
    print(tvmc_cmd)
    ret =subprocess.run(tvmc_cmd)
    if ret.returncode == 0:
        print('tvmc compile done')
    else:
        print('Unable compile failee')
        return False

    #untar modulet.tar
    module_tar = tarfile.open('module.tar')
    module_tar.extractall('module')
    module_tar.close()
    #remove module.tar from output_path
    os.remove('module.tar')
    os.chdir(cur_work_dir)
    return True

def download_bsp(board_info, templates_path):
    bsp_path = os.path.join(templates_path, board_info[2])
    if os.path.isdir(bsp_path):
        return
    print(f'git clone BSP {board_info[3]} {templates_path}')
    git.Repo.clone_from(board_info[3], bsp_path, branch='master', recursive=False, progress=CloneProgress())

def prepare_proj_resource(board_info, project_path, templates_path, tvmgen_path):
    print('copy resources to autogen project directory')
    bsp_lib_src_path = os.path.join(templates_path, board_info[2], 'Library')
    bsp_lib_dest_path = os.path.join(project_path, board_info[2])

    if not os.path.exists(bsp_lib_dest_path):
        os.mkdir(bsp_lib_dest_path)

    bsp_lib_dest_path = os.path.join(bsp_lib_dest_path, 'Library')

    print('copy bsp library to autogen project directory')
    shutil.copytree(bsp_lib_src_path, bsp_lib_dest_path, dirs_exist_ok = True)

    bsp_patch_src_path = os.path.join(templates_path, board_info[1], 'BSP_patch')
    bsp_dest_path = os.path.join(project_path, board_info[2])
    if os.path.exists(bsp_patch_src_path):
        print('copy bsp library patch to autogen project directory')
        shutil.copytree(bsp_patch_src_path, bsp_dest_path, dirs_exist_ok = True)

    tvm_module_src_path = tvmgen_path
    tvm_module_dest_path = os.path.join(project_path, 'module')

    if not os.path.exists(tvm_module_dest_path):
        os.mkdir(tvm_module_dest_path)

    print('copy tvm module codegen to autogen project directory')
    shutil.copytree(os.path.join(tvm_module_src_path, 'codegen'), os.path.join(tvm_module_dest_path, 'codegen'), dirs_exist_ok = True)

    print('copy tvm module runtime to autogen project directory')
    shutil.copytree(os.path.join(tvm_module_src_path, 'runtime'), os.path.join(tvm_module_dest_path, 'runtime'), dirs_exist_ok = True)

    microtvm_src_path = os.path.join(templates_path, 'microtvm')
    microtvm_dest_path = os.path.join(project_path, 'microtvm')

    print('copy microtvm to autogen project directory')
    shutil.copytree(microtvm_src_path, microtvm_dest_path, dirs_exist_ok = True)

    board_src_path = os.path.join(templates_path, board_info[1], board_info[0], 'board_templates')
    board_dest_path = os.path.join(project_path, 'example')

    print('copy board init code to autogen project directory')
    shutil.copytree(board_src_path, board_dest_path, dirs_exist_ok = True)

    crt_config_src_path = os.path.join(templates_path, 'crt_config.h.template')
    crt_config_dest_path = os.path.join(tvm_module_dest_path, 'runtime', 'include', 'crt_config.h')

    print('copy crt_config.h to autogen project directory')
    shutil.copyfile(crt_config_src_path, crt_config_dest_path)

    link_script_src_path = os.path.join(templates_path, board_info[1], board_info[0], 'link_script')
    link_script_dest_path = os.path.join(project_path, 'link_script')

    print('copy link script to autogen project directory')
    #print(link_script_src_path)
    #print(link_script_dest_path)
    shutil.copytree(link_script_src_path, link_script_dest_path, dirs_exist_ok = True)

    progen_src_path = os.path.join(templates_path, board_info[1], board_info[0], 'progen')
    progen_dest_path = project_path

    print('copy progen records to autogen project directory')
    print(progen_src_path)
    print(progen_dest_path)
    shutil.copytree(os.path.join(progen_src_path, 'tools'), os.path.join(progen_dest_path, 'tools'), dirs_exist_ok = True)
    shutil.copyfile(os.path.join(progen_src_path, 'project.yaml'), os.path.join(progen_dest_path, 'project.yaml'))

    #remove module directory from output_path
    shutil.rmtree(tvm_module_src_path)

def proj_gen(project_path, project_type):
    cur_work_dir = os.getcwd()
    os.chdir(project_path)
    print(os.getcwd())
    progen_cmd = ['progen', 'generate', '-f', 'project.yaml', '-p', 'nn_inference']
    progen_cmd.append('-t')
    progen_cmd.append(project_type)
    ret =subprocess.run(progen_cmd)
    if ret.returncode == 0:
        print('Success generation')
    else:
        print('Unable generation')
    os.chdir(cur_work_dir)

def project_generate(args):

    print(f"project type is {args.project_type}")
    templates_path = args.templates_path 

    if templates_path == None:
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')

    board_found = False

    for board_info in board_list:
        if board_info[0] == args.board:
            board_found = True
            download_bsp(board_info, templates_path)
            break

    if board_found == False:
        print("board not support")
        return 'unable_generate'

    if not args.project_type in project_type_list:
        print(f"Only support {project_type_list} projtect type")
        return 'unable_generate'

    #create ouput directory, if output directory is not exist
    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)

    #generated project directory
    project_path = os.path.join(args.output_path, PROJECT_GEN_DIR_PREFIX + args.board)
    project_example_path = os.path.join(project_path, PROJECT_GEN_EXAMPLE_DIR)
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    if not os.path.exists(project_example_path):
        os.mkdir(project_example_path)

    #model compile
    tvmc_dir_path = os.path.join(os.path.dirname(__file__), '..', 'tvmc')
    ret = model_compile(board_info, args.output_path, tvmc_dir_path, os.path.abspath(args.model_file))
    if ret == False:
        return 'unable_generate'

    #copy resource file to project directory
    tvmgen_path = os.path.join(args.output_path, 'module')
    prepare_proj_resource(board_info, project_path, templates_path, tvmgen_path)

    tvmgen_default_header_file = os.path.join(project_path, 'module', 'codegen', 'host', 'include', 'tvmgen_default.h')
    #Parser TVMC generate default header file (tvmgen_default.h)
    print(f'Start parser {tvmgen_default_header_file}')
    try:
        header_file = open(tvmgen_default_header_file, "r")
    except OSError:
        print("Could not open header file")
        return 'unable_generate'

    with header_file:
        header_parser = HeaderParser()
        header_parser.parser(header_file)

    #Generate main.c file
    main_file_path = os.path.join(project_example_path, 'main.c')
    main_temp_file_path = os.path.join(templates_path, 'main.c.template')
    print(f'template path {main_temp_file_path}')
    print(f'main file path {main_file_path}')

    try:
        main_temp_file = open(main_temp_file_path, "r")
    except OSError:
        print("Could not open main template file")
        return 'unable_generate'

    try:
        main_file = open(main_file_path, "w")
    except OSError:
        print("Could not open main file")
        return 'unable_generate'

    with main_file:
        main_codegen = MainCCodegen()
        main_codegen.code_gen(main_file, main_temp_file, header_parser)

    main_temp_file.close()

    #start generate project file (*.uvprojx, Makefile)
    proj_gen(project_path, args.project_type)
    print(f'NN inference project completed at {os.path.abspath(project_path)}')
    return project_path
