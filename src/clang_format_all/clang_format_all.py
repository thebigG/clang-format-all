
import os
import subprocess
from pathlib import Path
import argparse
import logging

import yaml

logging.basicConfig()
logger = logging.getLogger('check-all')
logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(
        description='clang_format_all starts at this directory and drills down recursively')

    parser.add_argument('--config', type=str, required=True,
                        help='Yaml file path with configuration.')

    args = parser.parse_args()
    return args


def is_cpp_or_c_file(path: Path):
    return path.suffix in ['.cpp', '.cc', '.C', 'CPP', '.c++', 'cp', '.cxx', '.h', '.hh', '.hpp']


def check_all_walk_recursive(root_dir: str, exclude_files=None):
    if exclude_files is None:
        exclude_files = set()
    for root, dirs, files in os.walk(root_dir):
        if dirs:
            for d in dirs:
                check_all_walk_recursive((os.path.join(root, d)), exclude_files)
        for file in files:
            path = Path(os.path.join(root, file))
            if str(path) in exclude_files:
                continue
            if is_cpp_or_c_file(path):
                if subprocess.run(["clang-format", "--dry-run", "--Werror", "-style=file",
                                   path]).returncode != 0:
                    logger.info("\"%s\": does not comply to format according to clang-format", path)
                    exit(-1)
                else:
                    logger.info("\"%s\": looks fine according to clang-format", path)


def format_all_walk_recursive(root_dir: str, exclude_files=None):
    if exclude_files is None:
        exclude_files = set()
    for root, dirs, files in os.walk(root_dir):
        if dirs:
            for d in dirs:
                format_all_walk_recursive((os.path.join(root, d)))
        for file in files:
            path = Path(os.path.join(root, file))
            if str(path) in exclude_files:
                continue
            if is_cpp_or_c_file(path):
                if subprocess.run(["clang-format", "--Werror", "-style=file",
                                   path], capture_output=True).returncode != 0:
                    logger.info("\"%s\": An error occurred while parsing this file.", path)
                    exit(-1)
                else:
                    logger.info("\"%s\": parsed successfully.", path)


def get_all_files(root_dir: str) -> []:
    files_array = []
    for root, dirs, files in os.walk(root_dir):
        if dirs:
            for d in dirs:
                files_array += get_all_files((os.path.join(root, d)))
        for file in files:
            files_array.append(os.path.join(root, file))
    return files_array


def get_resolved_paths(unresolved_paths: [str]) -> [str]:
    resolved_paths = []
    for p in unresolved_paths:
        resolved_paths += get_all_files(str(Path(p).resolve()))

    return set(resolved_paths)


def main():
    args = parse_args()
    excluded_dirs = None
    with open(args.exclude_dirs) as yaml_stream:
        excludes = yaml.load(yaml_stream, Loader=yaml.CSafeLoader)
        if 'exclude_dirs' not in excludes:
            logger.error(f"No key 'exclude_dirs' found in {args.exclude_dirs}")
            return -1
        excluded_dirs = get_resolved_paths(excludes['exclude_dirs'])

    if args.check_all:
        check_all_walk_recursive(str(Path(args.root_dir).resolve()), excluded_dirs)
    else:
        format_all_walk_recursive(args.root_dir, excluded_dirs)
