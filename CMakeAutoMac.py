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
    type = "SHARED"

    cmake_config = dict()
    cmake_config['proj_name'] = 'okane_crypt'
    cmake_config['proj_dir'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    cmake_config['version'] = '1.0.0.0'
    cmake_config['cmake_version'] = '3.15'
    cmake_config['exclude_folders'] = ["tfm", "port"]

    # Creating instance
    cm = CMakeAuto(**cmake_config)

    # Recursively adding all libs
    cm.add_libraries(os.path.join(cmake_config['proj_dir'], 'src'))
    cm.clear()

    # Adding the compile config
    cm.add("cmake_minimum_required(VERSION {})".format(cm.cmake_version))
    cm.add("project({} VERSION {})".format(cm.proj_name, cm.version))
    cm.add("set(CMAKE_CXX_STANDARD 11)")
    cm.add('set(CMAKE_CXX_FLAGS "-m64")\n')

    # Adding the shared lib
    cm.add("add_library(okane_crypt STATIC")
    cm.add('    "{}"'.format(cm.get_posix_path(os.path.join(cmake_config['proj_dir'], 'oc_config.h'))))
    cm.add('    "{}"'.format(cm.get_posix_path(os.path.join(cmake_config['proj_dir'], 'oc_err.h'))))
    cm.add('    "{}"'.format(cm.get_posix_path(os.path.join(cmake_config['proj_dir'], 'oc_import.h'))))
    for source in cm.sources:
        cm.add('    "{}"'.format(cm.get_posix_path(source)))
    cm.add(")\n")

    # Setting shared lib properties
    cm.add('set_target_properties(okane_crypt PROPERTIES COMPILE_FLAGS "-fPIC")')

    # Writing the shared lib
    cm.write(cmake_config['proj_dir'])