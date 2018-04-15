@echo off
rem Usage: cover filename [test_ suffix] # proper case required by coverage
rem filename without .py, 2nd parameter if test is not test_filename

setlocal
set py=C:\Python36\Python.exe

%py% -m coverage run relay_cmdline.py
%py% -m coverage report
%py% -m coverage html
start htmlcov\index.html
