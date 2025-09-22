for /f "tokens=2,3,4,5,6 usebackq delims=:/ " %%a in ('%date%') do set yyyymmdd=%%c%%b%%a%
echo %yyyymmdd% 

