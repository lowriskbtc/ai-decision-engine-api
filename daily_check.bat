@echo off
echo ========================================
echo AI WEED COMPANY - DAILY CHECK
echo ========================================
echo.

echo [1] Checking System Status...
python monitor_system.py
echo.

echo [2] Generating Report...
python generate_report.py
echo.

echo [3] Checking Progress...
python update_progress.py
echo.

echo [4] Checking Memory...
python check_memory.py
echo.

echo ========================================
echo Daily check complete!
echo ========================================
echo.
echo Review the outputs above for any issues.
pause

