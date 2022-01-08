#!/usr/bin/env python3

from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext, intree_extensions

# ext_modules = [
#    Pybind11Extension(
#        "groupbyrule.lev",
#        sorted(glob("groupbyrule/src/*.cpp")),
#    ),
# ]

ext_modules = intree_extensions(["groupbyrule/comparator/_levenshtein.cpp"])


if __name__ == "__main__":
    setup(ext_modules=ext_modules, cmdclass={"build_ext": build_ext})
