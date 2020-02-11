#!/bin/sh

echo > staticpython.py
$YSHELL ./freeze.sh "$1" staticpython.py '-DPy_FrozenMain=Py_BytesMain'
