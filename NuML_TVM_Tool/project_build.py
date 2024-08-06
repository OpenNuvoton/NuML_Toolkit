import os
import re
import shutil
import subprocess


def uvision5_build(args, proj_file_dir):
    print('checking build tool ...')
    uv4_util = args.ide_tool

    if not uv4_util:
        uv4_util = shutil.which('UV4.exe')

    if uv4_util == None or not os.path.isfile(uv4_util):
        print('UV4.exe not found, you must specify correct UV4.exe path!')
        return

    print('start building ...')
    cur_work_dir = os.getcwd()
    os.chdir(proj_file_dir)
    build_cmd = [uv4_util, '-b', 'nn_inference.uvprojx']
    subprocess.run(build_cmd)
    print('build done')
    os.chdir(cur_work_dir)


def make_gcc_build(args, proj_file_dir):
    print(proj_file_dir)
    print('checking build tool ...')
    #check toolchain
    if not shutil.which('arm-none-eabi-gcc'):
        print('arm gun gcc not found')
        return

    #check make
    make_util = shutil.which('make')

    if make_util == None:
        make_util = os.path.join(os.path.dirname(__file__), '..', 'tools', 'make-3.81-bin', 'bin', 'make.exe')
        if not os.path.isfile(make_util):
            print('make not found')
            return 
    print('start building ...')
    cur_work_dir = os.getcwd()
    os.chdir(proj_file_dir)
    build_cmd = [make_util, '-f', 'Makefile']
    #ret =subprocess.Popen(build_cmd)
    ret =subprocess.run(build_cmd)
    if ret.returncode == 0:
        print('Success build')
    else:
        print('Unable build')
    os.chdir(cur_work_dir)

project_type_list = [
    ['make_gcc_arm', make_gcc_build],
    ['uvision5_armc6', uvision5_build]
]

def add_build_parser(subparsers, _):
    """Include parser for 'build' subcommand"""
    parser = subparsers.add_parser("build", help="build ml project")
    parser.set_defaults(func=project_build)
    parser.add_argument("--project_path", help="specify prjoect path", required=True)
    parser.add_argument("--ide_tool", help="specify IDE tool")

def project_build(args):
    print('checking prjoect type ...')
    generated_project_dir = os.path.join(args.project_path, 'generated_projects')

    if not os.path.exists(generated_project_dir):
        print('generated_projects directory not found')
        return 1
    
    dir_files = os.listdir(generated_project_dir)

    for f in dir_files:
        fullpath = os.path.join(generated_project_dir, f)
        if os.path.isdir(fullpath):
            for project_type in project_type_list:
                if re.match(project_type[0], f):
                    print(f'find {project_type[0]} project type')
                    project_type[1](args, fullpath)
