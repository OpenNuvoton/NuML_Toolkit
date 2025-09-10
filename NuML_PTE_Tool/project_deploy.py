import argparse
import sys
import os
from project_generate import project_generate
from project_build import project_build
from project_flash import project_flash

def add_deploy_parser(subparsers, _):
    """Include parser for 'deploy' subcommand"""
    parser = subparsers.add_parser("deploy", help="deploy ml project")
    parser.set_defaults(func=project_deploy)
    parser.add_argument("--pte_file", help="specify PTE file", required=True)
    parser.add_argument("--output_path", help="specify output file path", required=True)
    parser.add_argument("--board", help="specify target board name", required=True)
    parser.add_argument("--project_type", help="specify project type uvision5_armc6/make_gcc_arm", default='make_gcc_arm')
    parser.add_argument("--templates_path", help="specify template path")
    parser.add_argument("--ide_tool", help="specify IDE tool")
    parser.add_argument("--application", help="specify application scenario generic", default='generic')

def project_deploy(args):
    project_path = project_generate(args)
    if project_path == None:
        return

    print(project_path)
    setattr(args, 'project_path', project_path)
    project_bin_fiile = project_build(args)

    if project_bin_fiile == None:
        return

    setattr(args, 'binary_file', project_bin_fiile)
    project_flash(args)
