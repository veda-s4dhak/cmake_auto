"""
Description: What's that? Its a bird, no its a plane, no its an Automatic CMake Generator!

Copyright (C) Okane Labs, Inc. - All rights reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

__author__ = "Anish Agarwal"
__copyright__ = "Copyright 2020, Okane Labs"
__version__ = "0.0.2"

import os
import pathlib
from .CMakeIndexer import CMakeIndexer

class CMakeAuto(CMakeIndexer):

    def __init__(self, **kwargs):

        CMakeIndexer.__init__(self, kwargs['proj_dir'])

        self.proj_name = kwargs['proj_name']
        self.version = kwargs['version']
        self.cmake_version = kwargs['cmake_version']
        self.include_dirs = kwargs['include_dirs']
        self.exclude_dirs = kwargs['exclude_dirs']


        self.library_paths = []
        self.library_names = []
        self.sources = []

    def clear(self):

        self.cmake = ''

    def add(self, line):
        self.cmake += (line + "\n")

    def write(self, path):

        with open(os.path.join(path, "CMakeLists.txt"), "w") as file:
            file.write(self.cmake)

    def get_posix_path(self, path):

        return str(pathlib.PureWindowsPath(path).as_posix())

    def check_for_source(self, files):

        for file in files:
            if (".c" in file) or (".cpp" in file):
                return True
        return False

    def construct_lib(self, lib_path, lib_name, lib_files):

        self.clear()
        self.add("add_library(")
        self.add("   " + lib_name)
        for lib_file in lib_files:
            if (not "CMakeLists" in lib_file):
                self.add("    " + lib_file)
            if (".cpp" in lib_file) or (".c" in lib_file):
                self.sources.append(os.path.join(lib_path,lib_file))
        self.add(")\n")
        self.add('target_include_directories({} PUBLIC "{}")'.format(lib_name, lib_path))
        self.write(lib_path)

        print("Added library {}".format(lib_name))

    def add_library(self, path):

        files = self.get_files(path)
        contains_source = self.check_for_source(files)

        if (len(files) > 0) and (contains_source):

            # Getting the library name while checking for repeats
            raw_lib_name = os.path.basename(path)
            lib_name_index = 1
            lib_name = raw_lib_name
            while (lib_name in self.library_names):
                lib_name = raw_lib_name + "_{}".format(lib_name_index)
                lib_name_index+=1

            # Constructing lib path
            lib_path = self.get_posix_path(path)

            # Adding the library path
            self.library_paths.append(lib_path)
            self.library_names.append(lib_name)

            # Adding the library
            self.construct_lib(lib_path, lib_name, files)

    def add_libraries(self, path):

        if (self.sub_dirs_exist(path)):
            for dir in self.get_sub_dirs(path):
                if dir not in self.exclude_dirs:
                    self.add_libraries(os.path.join(path,dir))

        self.add_library(path)