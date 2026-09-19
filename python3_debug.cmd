@echo off
echo [%date% %time%] python3 called >> "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\python3_debug.log"
echo ARGS: %* >> "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\python3_debug.log"
echo CMDLINE: %CMDCMDLINE% >> "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\python3_debug.log"
"C:\Users\ZhouXuan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" %*