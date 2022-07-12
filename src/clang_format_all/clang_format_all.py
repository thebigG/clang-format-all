#!/usr/bin/env python3

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
    parser.add_argument('--root_dir', type=str, required=True,
                        help='Directory to start running clang-format at.', default=[])

    parser.add_argument('--exclude_dirs', type=str, required=False,
                        help='Excludes yaml with directories to ignore.')

    parser.add_argument('--check_all',
                        help='Only check files without modifying them. Returns non-zero value on failure;'
                             'useful for CI workflows.',
                        action="store_true")

    args = parser.parse_args()
    return args


def is_cpp_or_c_file(path: Path):
    return path.suffix in ['.cpp', '.cc', '.C', 'CPP', '.c++', 'cp', '.cxx', '.h', '.hh', '.hpp']


def check_all_walk_recursive(root_dir: str):
    for root, dirs, files in os.walk(root_dir):
        if dirs:
            for d in dirs:
                check_all_walk_recursive((os.path.join(root, d)))
        for file in files:
            path = Path(os.path.join(root, file))
            if is_cpp_or_c_file(path):
                if subprocess.run(["clang-format", "--dry-run", "--Werror", "-style=file",
                                   path]).returncode != 0:
                    logger.info("\"%s\": does not comply to format according to clang-format", path)
                    exit(1)
                else:
                    logger.info("\"%s\": looks fine according to clang-format", path)


def format_all_walk_recursive(root_dir: str):
    for root, dirs, files in os.walk(root_dir):
        if dirs:
            for d in dirs:
                format_all_walk_recursive((os.path.join(root, d)))
        for file in files:
            path = Path(os.path.join(root, file))
            if is_cpp_or_c_file(path):
                if subprocess.run(["clang-format", "--Werror", "-style=file",
                                   path], capture_output=True).returncode != 0:
                    logger.info("\"%s\": An error occurred while parsing this file.", path)
                    exit(1)
                else:
                    logger.info("\"%s\": parsed successfully.", path)


def get_resolved_paths(unresolved_paths: [str]) -> [str]:
    resolved_paths = []
    for p in unresolved_paths:
        resolved_paths.append(Path(p).resolve())
    return resolved_paths


def main():
    args = parse_args()
    if args.exclude_dirs:
        with open(args.exclude_dirs) as yaml_stream:
            excludes = yaml.load(yaml_stream, Loader=yaml.CSafeLoader)
            if 'exclude_dirs' not in excludes:
                logger.error(f"No key 'exclude_dirs' found in {args.exclude_dirs}")
                return -1

    if args.check_all:
        check_all_walk_recursive(args.root_dir)
    else:
        format_all_walk_recursive(args.root_dir)
