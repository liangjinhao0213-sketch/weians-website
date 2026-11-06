@echo off
rem ---------------------------------------------------------------
rem  Weinas site - local preview server
rem
rem  Desktop : http://127.0.0.1:8080/
rem  Phone   : http://<this-PC-LAN-IP>:8080/   (same Wi-Fi / hotspot)
rem
rem  The server binds 0.0.0.0 so a phone on the same network can
rem  reach it. Windows may ask to allow Python through the firewall
rem  the first time - choose "Private networks" and "Public".
rem ---------------------------------------------------------------
setlocal
cd /d "%~dp0"
set PORT=8080

powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
if not errorlevel 1 goto already_running

where py >nul 2>nul
if not errorlevel 1 goto use_py
where python >nul 2>nul
if not errorlevel 1 goto use_python

echo.
echo   Python was not found on this computer.
echo   Opening index.html directly - the site works from disk too.
echo.
start "" "%~dp0index.html"
goto end

:already_running
echo.
echo   A server is already running on port %PORT%.
call :show_urls
start "" "http://127.0.0.1:%PORT%/"
goto end

:use_py
call :show_urls
start "" "http://127.0.0.1:%PORT%/"
py -m http.server %PORT% --bind 0.0.0.0
goto end

:use_python
call :show_urls
start "" "http://127.0.0.1:%PORT%/"
python -m http.server %PORT% --bind 0.0.0.0
goto end

:show_urls
echo.
echo   Desktop : http://127.0.0.1:%PORT%/
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 ^| Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254*' -and $_.InterfaceAlias -notlike '*VMnet*' } ^| Select-Object -First 1).IPAddress"`) do echo   Phone   : http://%%i:%PORT%/
echo.
echo   Keep this window open while previewing. Press Ctrl+C to stop.
echo.
goto :eof

:end
endlocal
