@echo off

:: MCDR Installer by Alex3236
:: https://github.com/MCDReforged/MCDRInstaller
:: For Windows only!

:: Constant Set
set VERSION=1.2.0
set PYVER=3.8.10
set BETAVER=3.9.6
:: RefreshEnv.bat in base64 format
set RefreshEnv_B64=QGVjaG8gb2ZmCmNoY3AgNjUwMDEgPiBudWwKZ290byBtYWluCjpTZXRGcm9tUmVnCiAgICAiJVdpbkRpciVcU3lzdGVtMzJcUmVnIiBRVUVSWSAiJX4xIiAvdiAiJX4yIiA+ICIlVEVNUCVcX2VudnNldC50bXAiIDI+TlVMCiAgICBmb3IgL2YgInVzZWJhY2txIHNraXA9MiB0b2tlbnM9MiwqIiAlJUEgSU4gKCIlVEVNUCVcX2VudnNldC50bXAiKSBkbyAoCiAgICAgICAgZWNoby9zZXQgIiV+Mz0lJUIiCiAgICApCiAgICBnb3RvIDpFT0YKOkdldFJlZ0VudgogICAgIiVXaW5EaXIlXFN5c3RlbTMyXFJlZyIgUVVFUlkgIiV+MSIgPiAiJVRFTVAlXF9lbnZnZXQudG1wIgogICAgZm9yIC9mICJ1c2ViYWNrcSBza2lwPTIiICUlQSBJTiAoIiVURU1QJVxfZW52Z2V0LnRtcCIpIGRvICgKICAgICAgICBpZiAvSSBub3QgIiUlfkEiPT0iUGF0aCIgKAogICAgICAgICAgICBjYWxsIDpTZXRGcm9tUmVnICIlfjEiICIlJX5BIiAiJSV+QSIKICAgICAgICApCiAgICApCiAgICBnb3RvIDpFT0YKOm1haW4KICAgIGVjaG8vQGVjaG8gb2ZmID4iJVRFTVAlXF9lbnYuY21kIgogICAgY2FsbCA6R2V0UmVnRW52ICJIS0xNXFN5c3RlbVxDdXJyZW50Q29udHJvbFNldFxDb250cm9sXFNlc3Npb24gTWFuYWdlclxFbnZpcm9ubWVudCIgPj4gIiVURU1QJVxfZW52LmNtZCIKICAgIGNhbGwgOkdldFJlZ0VudiAiSEtDVVxFbnZpcm9ubWVudCI+PiIlVEVNUCVcX2Vudi5jbWQiID4+ICIlVEVNUCVcX2Vudi5jbWQiCiAgICBjYWxsIDpTZXRGcm9tUmVnICJIS0xNXFN5c3RlbVxDdXJyZW50Q29udHJvbFNldFxDb250cm9sXFNlc3Npb24gTWFuYWdlclxFbnZpcm9ubWVudCIgUGF0aCBQYXRoX0hLTE0gPj4gIiVURU1QJVxfZW52LmNtZCIKICAgIGNhbGwgOlNldEZyb21SZWcgIkhLQ1VcRW52aXJvbm1lbnQiIFBhdGggUGF0aF9IS0NVID4+ICIlVEVNUCVcX2Vudi5jbWQiCiAgICBlY2hvL3NldCAiUGF0aD0lJVBhdGhfSEtMTSUlOyUlUGF0aF9IS0NVJSUiID4+ICIlVEVNUCVcX2Vudi5jbWQiCiAgICBkZWwgL2YgL3EgIiVURU1QJVxfZW52c2V0LnRtcCIgMj5udWwKICAgIGRlbCAvZiAvcSAiJVRFTVAlXF9lbnZnZXQudG1wIiAyPm51bAogICAgU0VUICJPcmlnaW5hbFVzZXJOYW1lPSVVU0VSTkFNRSUiCiAgICBTRVQgIk9yaWdpbmFsQXJjaGl0ZWN0dXJlPSVQUk9DRVNTT1JfQVJDSElURUNUVVJFJSIKICAgIGNhbGwgIiVURU1QJVxfZW52LmNtZCIKICAgIGRlbCAvZiAvcSAiJVRFTVAlXF9lbnYuY21kIiAyPm51bAogICAgU0VUICJVU0VSTkFNRT0lT3JpZ2luYWxVc2VyTmFtZSUiCiAgICBTRVQgIlBST0NFU1NPUl9BUkNISVRFQ1RVUkU9JU9yaWdpbmFsQXJjaGl0ZWN0dXJlJSI=

:: Init
pushd "%~dp0"
chcp 65001 > nul
color 0b
title MCDR 一键配置包 ver%VERSION% By Alex3236

:: Check administor permission
openfiles > NUL 2>&1
if %errorlevel%==0 (
        echo.
) else (
		echo.
        echo  :: 您正在以 非管理员 权限运行.
        echo.
        echo     请尝试右键脚本并选择「以管理员权限运行」.
        echo     按任意键退出...
        pause > NUL
        exit
)

:: Welcome message
cls
echo.
echo  :: MCDR 一键配置包 By Alex3236
echo.
echo  :: 此脚本可以帮助你安装 Python 并配置 MCDR.
echo     请确保当前文件夹为空!
echo.
echo  :: 按任意键开始.
echo.
pause >nul

:: Check Python
cls
echo.
python -c "" > nul
if %errorlevel%==0 (
        echo  :: 检测到现有 Python.
        goto check_mcdr
)

:install_python
cls
echo.
echo  :: 安装 Python
echo     将执行 Python 安装.
echo.
set continue=1
echo  :: 「1」使用大陆镜像下载并安装 Python (默认)
echo  :: 「2」使用源网站下载并安装 Python
echo     「9」使用源网站下载并安装 Python %BETAVER% (可能不稳定)
echo     「n」取消
echo.
set /P continue=1
IF %continue%==n exit
IF %continue%==1 (
        set PY64BIT=https://tenapi.cn/lanzou/?url=https://alex3236.lanzoui.com/iOyQcqqe7eh^^^&type=down
        set PY32BIT=https://tenapi.cn/lanzou/?url=https://alex3236.lanzoui.com/iOyQcqqe7eh^^^&type=down
)
IF %continue%==9 (
        set PYVER=%BETAVER%
        set continue=2
)
IF %continue%==2 (
        set PY64BIT=https://www.python.org/ftp/python/%PYVER%/python-%PYVER%-amd64.exe
        set PY32BIT=https://www.python.org/ftp/python/%PYVER%/python-%PYVER%.exe
)
cls
echo.
echo  :: 正在下载 Python...
echo.

call :clear

:: Use powershell to download Python
if /i %PROCESSOR_IDENTIFIER:~0,3%==x86 (
        @powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile(%\"PY32BIT%\", \"%TEMP%\python-installer.exe\")"
        set PIP=%ProgramFiles%\Python*\Scripts
) else (
        @powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile(%\"PY64BIT%\", \"%TEMP%\python-installer.exe\")"
)
if not exist %temp%\python-installer.exe (
	echo  :: 下载 Python 失败.
	echo.
	echo  :: 按任意键退出.
	pause >nul
	exit
)
echo.
echo :: 正在安装 Python...
echo.
:: Call python-installer.exe to install Python
%temp%\python-installer.exe /passive /PrependPath=1 /InstallAllUsers=1
echo.
echo :: 刷新环境变量...
echo.
@powershell -Command "& {[System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('%RefreshEnv_B64%')) | out-file %TEMP%\RefreshEnv.bat -encoding utf8}"
call %TEMP%\RefreshEnv.bat
goto install_mcdr

:check_mcdr
echo.
python -c "import mcdreforged" > nul
if %errorlevel%==0 (
	echo  :: 检测到现有 MCDR 包.
	goto config_mcdr
)

:install_mcdr
cls
echo.
echo  :: 安装 MCDR
echo     将执行 MCDR 安装.
echo.
set continue=Y
echo  :: 按「Enter」继续, 或输入「n」取消.
set /P continue=
IF %continue%==n exit

cls
echo.
echo :: 正在安装 MCDR...
echo.
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install_mcdr mcdreforged -q -i https://mirrors.aliyun.com/pypi/simple
echo  :: 安装成功.
timeout /NOBREAK 1 >nul

:config_mcdr
cls
echo.
echo  :: 配置 MCDR
echo     将在当前文件夹配置 MCDR. 请确保当前文件夹为空!
echo.
set continue=Y
echo  :: 按「Enter」继续, 或输入「n」取消.
set /P continue=
IF %continue%==n exit

cls
echo.
echo  :: 正在生成启动脚本...
echo.
SetLocal EnableDelayedExpansion
(
echo @echo off
echo title MCDReforged ^(%%^~dp0^)
echo python -m mcdreforged
echo pause
) >> Start-MCDR.bat
(
echo @echo off
echo title MCDReforged Updater ^(%%^~dp0^)
echo echo Updating...
echo echo.
echo pip install mcdreforged --upgrade -q
echo echo.
echo echo Done.
echo pause ^>nul
) >> Update-MCDR.bat
(
echo [InternetShortcut]
echo URL=https://hub.fastgit.org/MCDReforged-Plugins/PluginCatalogue/blob/master/readme_cn.md
) >> MCDR-PluginCatalogue.url
python -m mcdreforged > nul
echo  :: 配置完成！ 生成的脚本如下:
echo     「Start-MCDR.bat」一键运行 MCDR
echo     「Update-MCDR.bat」一键升级 MCDR
echo     「MCDR-PluginCatalogue.url」打开 MCDR 官方插件库
echo.
echo  :: 现在，把你的服务端文件放入「server」文件夹里，然后修改配置文件「config.yml」以满足你的需求。
echo     完成后，启动 MCDR,开始你的 MCDR 之旅.
echo.
echo  :: MCDR 官方Q群为「1101314858」,有问题请加群讨论.
echo     脚本作者为 Alex3236, Bilibili-UID=275212628
echo.
echo  :: 按任意键退出.
echo.
call :clear
pause >nul
del /f /q %0

:clear
del /f /q %TEMP%\python-installer.exe
del /f /q %TEMP%\RefreshEnv.bat


