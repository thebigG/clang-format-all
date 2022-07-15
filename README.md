# Format All The Things!

This is a python script that will run `clang-format -i` on your code.

Install:
```
pip install
```

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
