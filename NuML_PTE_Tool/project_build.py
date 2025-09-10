import os
import re
import shutil
import subprocess

def uvision5_build(args, proj_file_dir, proj_name):
    print('checking build tool ...')
    uv4_util = args.ide_tool
    print(uv4_util)

    if uv4_util == None:
        uv4_util = shutil.which('UV4.exe')

    if uv4_util == None or not os.path.isfile(uv4_util):
        print('UV4.exe not found, you must specify correct UV4.exe path!')
        return None

    print('start building ...')
    cur_work_dir = os.getcwd()
    os.chdir(proj_file_dir)
    build_cmd = [uv4_util, '-b', proj_name + '.uvprojx']
    subprocess.run(build_cmd)
    print('build done')
    os.chdir(cur_work_dir)

    binary_file = os.path.join(proj_file_dir, 'build', proj_name + '.bin')
    if os.path.exists(binary_file): 
        return binary_file
    else:
        return None

def make_gcc_build(args, proj_file_dir, proj_name):
    print(proj_file_dir)
    print('checking build tool ...')
    #check toolchain
    if not shutil.which('arm-none-eabi-gcc'):
        print('arm gun gcc not found')
        return None

    #check make
    make_util = shutil.which('make')

    if make_util == None:
        make_util = os.path.join(os.path.dirname(__file__), '..', 'tools', 'make-3.81-bin', 'bin', 'make.exe')
        if not os.path.isfile(make_util):
            print('make not found')
            return None
    print('start building ...')
    cur_work_dir = os.getcwd()
    os.chdir(proj_file_dir)
    build_cmd = [make_util, '-f', 'Makefile']
    ret =subprocess.run(build_cmd)
    if ret.returncode == 0:
        print('Success build')
        os.chdir(cur_work_dir)
        binary_file = os.path.join(proj_file_dir, 'build', proj_name + '.bin')
        if os.path.exists(binary_file): 
            return binary_file
        else:
            return None
    else:
        print('Unable build')
        os.chdir(cur_work_dir)
        return None

project_type_list = [
    ['Makefile', make_gcc_build],
    ['uvprojx', uvision5_build]
]

def add_build_parser(subparsers, _):
    """Include parser for 'build' subcommand"""
    parser = subparsers.add_parser("build", help="build ml project")
    parser.set_defaults(func=project_build)
    parser.add_argument("--project_path", help="specify prjoect path", required=True)
    parser.add_argument("--project_type", help="specify project type uvision5_armc6/make_gcc_arm", default='make_gcc_arm')
    parser.add_argument("--ide_tool", help="specify IDE tool")

def project_build(args):
    print('checking prjoect type ...')

    project_name = os.path.basename(args.project_path)

    if args.project_type == 'uvision5_armc6':
        IDE_project_dir = os.path.join(args.project_path, 'KEIL')
    else:
        IDE_project_dir = os.path.join(args.project_path, 'GCC')

    if not os.path.exists(IDE_project_dir):
        print('Build project file not fount')
        return None

    dir_files = os.listdir(IDE_project_dir)

    for f in dir_files:
        fullpath = os.path.join(IDE_project_dir, f)
        if not os.path.isdir(fullpath):
            for project_type in project_type_list:
                if re.search(project_type[0], f):
                    print(f'find {project_type[0]} project type')
                    return project_type[1](args, IDE_project_dir, project_name)

    return None

