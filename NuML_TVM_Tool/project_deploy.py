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
    parser.add_argument("--model_file", help="specify tflite file", required=True)
    parser.add_argument("--output_path", help="specify output file path", required=True)
    parser.add_argument("--board", help="specify target board name", required=True)
    parser.add_argument("--project_type", help="specify project type uvision5_armc6/make_gcc_arm", default='make_gcc_arm')
    parser.add_argument("--templates_path", help="specify template path")
    parser.add_argument("--ide_tool", help="specify IDE tool")

def project_deploy(args):
    projectpath = project_generate(args)
    setattr(args, 'project_path', projectpath)
    project_build(args)
    project_flash(args)

