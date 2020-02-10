#!/bin/sh

>staticpython.py
source ./freeze.sh "$1" staticpython.py '-DPy_FrozenMain=Py_BytesMain'
