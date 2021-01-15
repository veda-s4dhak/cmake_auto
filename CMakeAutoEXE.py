"""
Description: What's that? Its a bird, no its a plane, no its an Automatic CMake Generator!

Copyright (C) Okane Labs, Inc. - All rights reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

__author__ = "Anish Agarwal"
__copyright__ = "Copyright 2020, Okane Labs"
__version__ = "0.0.2"

from CMakeAuto import CMakeAuto
import os

if __name__ == '__main__':

    # Configuration
    cmake_config = dict()
    cmake_config['proj_name'] = 'okane_crypt'
    cmake_config['proj_dir'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    cmake_config['version'] = '0.01'
    cmake_config['cmake_version'] = '3.15'
    cmake_config['exclude_folders'] = ['tfm', 'port']

    # Creating instance
    cm = CMakeAuto(**cmake_config)

    # Recursively adding all source
    cm.add_libraries(os.path.join(cmake_config['proj_dir'], 'src'))
    cm.clear()

    # Recursively adding all tests
    cm.add_libraries(os.path.join(cmake_config['proj_dir'], 'tests'))
    cm.clear()

    # Recursively adding all libs
    cm.add_libraries(os.path.join(cmake_config['proj_dir'], 'libs'))
    cm.clear()

    # Adding the compile config
    cm.add("cmake_minimum_required(VERSION {})".format(cm.cmake_version))
    cm.add("project({} VERSION {})".format(cm.proj_name, cm.version))
    cm.add("set(CMAKE_CXX_STANDARD 11)")
    cm.add('set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")\n')

    # Adding the executable
    cm.add("add_executable(okane_crypt")
    for source in cm.sources:
        cm.add('    "{}"'.format(cm.get_posix_path(source)))
    cm.add(")\n")

    # Setting executable properties
    cm.add('set_target_properties(okane_crypt PROPERTIES COMPILE_FLAGS "-fPIC")')
    cm.add('target_include_directories(okane_crypt PUBLIC "{}")'.format(cm.get_posix_path(cmake_config['proj_dir'])))

    # Writing main CMakeLists.txt
    cm.write(cmake_config['proj_dir'])






