ECHO CONFLUENCE SCRIPT RUNNER
ECHO --- start ---
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8

for /f "tokens=2,3,4,5,6 usebackq delims=:/ " %%a in ('%date%') do set yyyymmdd=%%c%%b%%a%
echo %yyyymmdd% 

python3 dependant-pages-reader.py > output.%yyyymmdd%.txt

ECHO --- stop --- 
exit 0

