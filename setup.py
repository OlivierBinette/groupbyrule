#!/usr/bin/env python3
from setuptools import setup

import warnings

if __name__ == "__main__":
    try:
        from pybind11.setup_helpers import Pybind11Extension, build_ext, intree_extensions
        ext_modules = intree_extensions(
            ["groupbyrule/comparator/_levenshtein.cpp", "groupbyrule/comparator/_comparator.cpp", "groupbyrule/comparator/_lcs.cpp"])
        setup(ext_modules=ext_modules, cmdclass={"build_ext": build_ext})
    except:
        warnings.warn(
            "Could not build package using C++ source. Trying again in pure Python.")
        setup()
