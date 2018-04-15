rem Activate virtual env
call ..\venv\Scripts\activate.bat

rem Remove existing builds
rmdir /s /q build

rem Build Linux executables
python setup.py build

rem Create installer
"C:\Program Files (x86)\NSIS\makensis" R421A08_installer.nsi
