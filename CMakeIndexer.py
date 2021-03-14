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

class CMakeIndexer():

    def __init__(self, proj_dir):

        # Getting the project dir
        self.proj_dir = proj_dir

        # Directory indices
        self.all_dirs = []
        self.include_dirs = []

        # File indices
        self.files = dict()

    def get_sub_dirs(self, path):
        return next(os.walk(path))[1]

    def sub_dirs_exist(self, path):
        print(path)
        print(type(os.walk(path)))
        print(next(os.walk(path)))
        print(len(next(os.walk(path))))
        return (len(next(os.walk(path))[1]) > 0)

    def index_dirs(self, path):

        if (self.sub_dirs_exist(path)):
            for dir in self.get_sub_dirs(path):
                self.index_dirs(os.path.join(path, dir))

        self.all_dirs.append(path)

    def get_files(self, path):
        return next(os.walk(path))[2]