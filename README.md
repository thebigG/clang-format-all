[![PyPI version](https://badge.fury.io/py/clang-format-all.svg)](https://badge.fury.io/py/clang-format-all)
[![Run Python Tests](https://github.com/thebigG/clang_format_all/actions/workflows/ci.yaml/badge.svg)](https://github.com/thebigG/clang_format_all/actions/workflows/ci.yaml)
# Format All The Things!

This is a python script that will run `clang-format -i` on your code.

Basic usage:

    clang_format_all --config config.yaml

The yaml file should look like this:
```
root_dir: "."

#When true, files will only be checked. None will be modified.
check_all: true

file_extensions: ['.cpp', '.cc', '.C', 'CPP', '.c++', 'cp', '.cxx', '.h', '.hh', '.hpp']

exclude_dirs:
  - "fmt"
  - "simple_gpio"
  - "build"
```
