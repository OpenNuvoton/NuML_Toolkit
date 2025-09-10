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

from generic_codegen.generic_codegen import GenericCodegen
PROJECT_GEN_DIR_PREFIX = 'ProjGen_'

board_list = [
    #board name, MCU, BSP name, BSP URL
    #['NuMaker-M467HJ', 'M467', 'm460BSP', 'git@github.com:OpenNuvoton/m460bsp.git'],
    #['NuMaker-M467HJ', 'M467', 'm460bsp', 'https://github.com/OpenNuvoton/m460bsp.git'],
    ['NuMaker-M55M1', 'M55M1', 'M55M1BSP', 'https://github.com/OpenNuvoton/M55M1BSP.git'],   
]

project_type_list = ['uvision5_armc6', 'make_gcc_arm']

application = {
    "generic"   : {
                    "board": ['NuMaker-M55M1'],
                    "example_tmpl_dir": "generic_template",
                    "example_tmpl_proj": "NN_ModelInference"
                  },
}

# git clone progress status
class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()

# add project generate argument parser
def add_generate_parser(subparsers, _):
    """Include parser for 'generate' subcommand"""
    parser = subparsers.add_parser("generate", help="generate ml project")
    parser.set_defaults(func=project_generate)
    parser.add_argument("--pte_file", help="specify PTE file", required=True)
    parser.add_argument("--output_path", help="specify output file path", required=True)
    parser.add_argument("--board", help="specify target board name", required=True)
    parser.add_argument("--project_type", help="specify project type uvision5_armc6/make_gcc_arm", default='make_gcc_arm')
    parser.add_argument("--templates_path", help="specify template path")
    parser.add_argument("--application", help="specify application scenario generic", default='generic')

# download board BSP
def download_bsp(board_info, templates_path):
    bsp_path = os.path.join(templates_path, board_info[2])
    if os.path.isdir(bsp_path):
        return
    print(f'git clone BSP {board_info[3]} {templates_path}')
    git.Repo.clone_from(board_info[3], bsp_path, branch='master', recursive=False, progress=CloneProgress())

# convert PTE to json
def pte_convert(output_path, flatc_dir_path, schema_dir_path, pte_file):
    cur_work_dir = os.getcwd()
    os.chdir(output_path)
    flatc_exe = os.path.join(flatc_dir_path, 'flatc.exe')    
    schema_file = os.path.join(schema_dir_path, 'program.fbs')
    print(output_path)
    print(pte_file)
    print(flatc_exe)

    flatc_cmd = [flatc_exe, '-t', '--strict-json', schema_file, '--', pte_file]

    print(flatc_cmd)
    ret =subprocess.run(flatc_cmd)
    if ret.returncode == 0:
        print('flatc convert done')
    else:
        print('Unable compile failee')
        return False

    os.chdir(cur_work_dir)
    return True

def prepare_proj_resource(board_info, project_path, templates_path, pte_file_path, example_tmpl_dir, example_tmpl_proj):
    print('copy resources to autogen project directory')

    bsp_lib_src_path = os.path.join(templates_path, board_info[2], 'Library')
    bsp_lib_dest_path = os.path.join(project_path, board_info[2],'Library')
    print('copy bsp library to autogen project directory')
    """ Temp del for testing
    """
    shutil.copytree(bsp_lib_src_path, bsp_lib_dest_path, dirs_exist_ok = True)    

    bsp_thirdparty_src_path = os.path.join(templates_path, board_info[2], 'ThirdParty')
    bsp_thirdparty_dest_path = os.path.join(project_path, board_info[2], 'ThirdParty')

    bsp_thirdparty_fatfs_src_path = os.path.join(bsp_thirdparty_src_path, 'FatFs')
    bsp_thirdparty_fatfs_dest_path = os.path.join(bsp_thirdparty_dest_path, 'FatFs') 
    print('copy BSP ThirdParty FatFs ...')
    shutil.copytree(bsp_thirdparty_fatfs_src_path, bsp_thirdparty_fatfs_dest_path, dirs_exist_ok = True)

    bsp_thirdparty_ml_evk_src_path = os.path.join(bsp_thirdparty_src_path, 'ml-embedded-evaluation-kit')
    bsp_thirdparty_ml_evk_dest_path = os.path.join(bsp_thirdparty_dest_path, 'ml-embedded-evaluation-kit')
    print('copy BSP ThirdParty ml-embedded-evaluation-kit ...')
    shutil.copytree(bsp_thirdparty_ml_evk_src_path, bsp_thirdparty_ml_evk_dest_path, dirs_exist_ok = True)
    #copy .cc to .cpp
    ml_evk_source_dir = os.path.join(bsp_thirdparty_ml_evk_dest_path, 'source', 'application', 'api', 'common', 'source')

    # Loop through all files in the directory
    for filename in os.listdir(ml_evk_source_dir):
        if filename.endswith('.cc'):
            # Construct full file path
            old_file = os.path.join(ml_evk_source_dir, filename)
            new_file = os.path.join(ml_evk_source_dir, filename.replace('.cc', '.cpp'))
            
            # copy the file
            shutil.copyfile(old_file, new_file)
            print(f'copy {old_file} to {new_file}')

    ml_evk_source_dir = os.path.join(bsp_thirdparty_ml_evk_dest_path, 'source', 'math')

    # Loop through all files in the directory
    for filename in os.listdir(ml_evk_source_dir):
        if filename.endswith('.cc'):
            # Construct full file path
            old_file = os.path.join(ml_evk_source_dir, filename)
            new_file = os.path.join(ml_evk_source_dir, filename.replace('.cc', '.cpp'))
            
            # copy the file
            shutil.copyfile(old_file, new_file)
            print(f'copy {old_file} to {new_file}')


    ml_evk_source_dir = os.path.join(bsp_thirdparty_ml_evk_dest_path, 'source', 'profiler')

    # Loop through all files in the directory
    for filename in os.listdir(ml_evk_source_dir):
        if filename.endswith('.cc'):
            # Construct full file path
            old_file = os.path.join(ml_evk_source_dir, filename)
            new_file = os.path.join(ml_evk_source_dir, filename.replace('.cc', '.cpp'))
            
            # copy the file
            shutil.copyfile(old_file, new_file)
            print(f'copy {old_file} to {new_file}')


    bsp_patch_src_path = os.path.join(templates_path, board_info[1], 'BSP_patch')
    bsp_dest_path = os.path.join(project_path, board_info[2])
    if os.path.exists(bsp_patch_src_path):
        print('copy bsp library patch to autogen project directory')
        shutil.copytree(bsp_patch_src_path, bsp_dest_path, dirs_exist_ok = True)

    example_template_path = os.path.join(templates_path, board_info[1], board_info[0], example_tmpl_dir)
    example_project_path = os.path.join(bsp_dest_path, 'SampleCode', 'MachineLearning')
    example_project_src_path = os.path.join(example_template_path, example_tmpl_proj)

    print(example_template_path)
    print(example_project_src_path)
    print(example_project_path)

    print('copy example template project to autogen MachineLearning example folder')
    example_project_path = os.path.join(example_project_path, example_tmpl_proj)
    shutil.copytree(example_project_src_path, example_project_path, dirs_exist_ok = True)
    
    example_project_model_dir = os.path.join(example_project_path, 'Model')
    shutil.copy(pte_file_path, example_project_model_dir)

    print('copy link script')
    link_script_keil_src_file = os.path.join(templates_path, board_info[1], board_info[0], example_tmpl_dir, 'link_script', 'armcc', 'armcc.scatter')
    link_script_keil_dest_file = os.path.join(example_project_path, 'KEIL', 'armcc.scatter')
    shutil.copyfile(link_script_keil_src_file, link_script_keil_dest_file)

    link_script_gcc_src_file = os.path.join(templates_path, board_info[1], board_info[0], example_tmpl_dir, 'link_script', 'gcc', 'gcc.ld')
    link_script_gcc_dest_file = os.path.join(example_project_path, 'GCC', 'gcc.ld')
    shutil.copyfile(link_script_gcc_src_file, link_script_gcc_dest_file)

    print('copy progen records to autogen project directory')
    progen_src_path = os.path.join(templates_path, board_info[1], board_info[0], example_tmpl_dir, 'progen')
    progen_dest_path = os.path.join(example_project_path, '..')

    shutil.copytree(os.path.join(progen_src_path, 'tools'), os.path.join(progen_dest_path, 'tools'), dirs_exist_ok = True)
    shutil.copyfile(os.path.join(progen_src_path, 'project.yaml'), os.path.join(progen_dest_path, 'project.yaml'))

    return example_project_path

def proj_gen(progen_path, project_type, project_dir_name):
    cur_work_dir = os.getcwd()
    os.chdir(progen_path)
    progen_cmd = ['progen', 'generate', '-f', 'project.yaml', '-p', project_dir_name]
    progen_cmd.append('-t')
    progen_cmd.append(project_type)
    ret =subprocess.run(progen_cmd)
    if ret.returncode == 0:
        print('Success generation')
    else:
        print('Unable generation')

    #copy project file to project folder
    toolchain_project = project_type + '_' + project_dir_name
    toolchain_project_src_dir = os.path.join('generated_projects', toolchain_project)

    if project_type == 'uvision5_armc6':
        toolchain_project_dest_dir = os.path.join(project_dir_name, 'KEIL') 
    else:
        toolchain_project_dest_dir = os.path.join(project_dir_name, 'GCC')

    print(toolchain_project_src_dir)
    print(toolchain_project_dest_dir)

    shutil.copytree(toolchain_project_src_dir, toolchain_project_dest_dir, dirs_exist_ok = True)

    #delete progen files
    shutil.rmtree('generated_projects')
    shutil.rmtree('tools')
    os.remove('project.yaml')

    os.chdir(cur_work_dir)

#project generate main function
def project_generate(args):
    print(f"project type is {args.project_type}")
    templates_path = args.templates_path 
    application_usage = args.application

    if not application_usage in application:
        print("applicaiton not found! using generic instead")
        application_usage = "generic"

    application_param = application[application_usage]

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
    if not os.path.exists(project_path):
        os.mkdir(project_path)

    #convert PTE to json
    pte_file_path = os.path.abspath(args.pte_file)
    flatc_dir_path = os.path.join(os.path.dirname(__file__), '..', 'tools', 'flatc')
    schema_dir_path = os.path.join(os.path.dirname(__file__), 'schema')

    ret = pte_convert(args.output_path, flatc_dir_path, schema_dir_path, pte_file_path)
    if ret == False:
        return 'unable_convert'

    pte_json_file_basename = os.path.splitext(os.path.basename(args.pte_file))[0]
    pte_json_file_path = os.path.join(args.output_path, pte_json_file_basename + '.json')
    print(pte_json_file_path)

    #prepare project resource
    example_tmpl_dir = application_param["example_tmpl_dir"]
    example_tmpl_proj = application_param["example_tmpl_proj"]

    project_example_path = prepare_proj_resource(board_info, project_path, templates_path, pte_file_path, example_tmpl_dir, example_tmpl_proj)
    print(project_example_path)

    # Generate reference_kernel.cpp and main.cpp
    if application_usage == 'generic':
        codegen = GenericCodegen.from_args(pte_json_file_path, project_example_path, app='generic')

    codegen.code_gen()
    os.remove(pte_json_file_path)

    #start generate project file (*.uvprojx, Makefile)
    progen_path = os.path.join(project_example_path, '..')
    proj_gen(progen_path, args.project_type, os.path.basename(project_example_path))
    print(f'Example project completed at {os.path.abspath(project_example_path)}')
    return project_example_path
