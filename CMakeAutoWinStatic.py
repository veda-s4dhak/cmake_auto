#!/usr/bin/env python

"""
Description: Generates a windows static library
"""

__author__ = "Anish Agarwal"
__license__ = "MIT"
__version__ = "2021.03.01"

import os

from .CMakeAuto import CMakeAuto

class CMakeAutoWinStatic():

    def __init__(self, **cmake_config):

        # Creating instance
        self.cm = CMakeAuto(**cmake_config)

    def run(self):

        # Recursively adding all source
        for _dir in self.cm.include_dirs:
            self.cm.add_libraries(os.path.join(self.cm.proj_dir, _dir))
            self.cm.clear()

        # Adding the compile config
        self.cm.add("cmake_minimum_required(VERSION {})".format(self.cm.cmake_version))
        self.cm.add("project({} VERSION {})".format(self.cm.proj_name, self.cm.version))
        self.cm.add("set(CMAKE_CXX_STANDARD 11)")
        self.cm.add('set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")\n')

        # Set headers and sources
        self.cm.add("set(SOURCES".format(self.cm.proj_name))
        for source in self.cm.sources:
            self.cm.add('    "{}"'.format(self.cm.get_posix_path(source)))
        for headers in self.cm.headers:
            self.cm.add('    "{}"'.format(self.cm.get_posix_path(headers)))
        self.cm.add(")\n")

        # Adding the shared lib
        self.cm.add("add_library({} STATIC {})\n".format(self.cm.proj_name, r"${SOURCES}"))

        # Setting static lib properties
        self.cm.add('set_target_properties({} PROPERTIES COMPILE_FLAGS "-fPIC")'.format(self.cm.proj_name))

        # Adding include directories
        for include in self.cm.includes:
            if include not in self.cm.library_paths:
                self.cm.add('target_include_directories({} PUBLIC "{}")'.format(self.cm.proj_name, include))
        self.cm.add("")

        # Adding include directories
        for path in self.cm.library_paths:
            self.cm.add('target_include_directories({} PUBLIC "{}")'.format(self.cm.proj_name, path))
        self.cm.add("")

        # Writing main CMakeLists.txt
        cmake_build_path = self.cm.get_posix_path(os.path.join(self.cm.proj_dir, "cmake-build-debug"))
        if not os.path.exists(cmake_build_path):
            os.makedirs(cmake_build_path)
        self.cm.write(cmake_build_path)