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

from .CMakeAuto import CMakeAuto

class CMakeAutoEXE():

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

        # Adding the executable
        self.cm.add("add_executable({}".format(self.cm.proj_name))
        for source in self.cm.sources:
            self.cm.add('    "{}"'.format(self.cm.get_posix_path(source)))
        self.cm.add(")\n")

        # Setting executable properties
        self.cm.add('set_target_properties({} PROPERTIES COMPILE_FLAGS "-fPIC")'.format(self.cm.proj_name))
        self.cm.add('target_include_directories({} PUBLIC "{}")'.format(self.cm.proj_name, self.cm.get_posix_path(self.cm.proj_dir)))

        # Writing main CMakeLists.txt
        self.cm.write(self.cm.proj_dir)




