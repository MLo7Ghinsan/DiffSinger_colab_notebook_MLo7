@echo off

rem check for python and its version for 3."10" lmao
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set python_ver=%%i
for /f "tokens=1-3 delims=." %%a in ("%python_ver%") do (
    set maj=%%a
    set min=%%b
)
if not "%maj%"=="3" (
    echo yuwu duwu nowt have python instawwed, pwease instaww python 3.10
    goto end
)
if not "%min%"=="10" (
    if %min% gtr 10 (
        echo yuwu have a vewsion of python gweater than 3.10 instawwed, pwease downgwade tuwu python 3.10
    ) else (
        echo ywu have a vewsion of python wess than 3.10 instawwed, pwease upgwade tuwu python 3.10
    )
    goto end
)

rem force pip install cus it doesn't really matter if you already have the modules plus PyYAML is a pain to deal with for checking and im lAzY
pip install tk tqdm PyYAML requests -q

rem cd the dir into the current directory cus why not <3
cd /d "%~dp0"
python ds_gui.py
