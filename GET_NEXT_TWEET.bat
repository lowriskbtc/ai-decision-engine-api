@echo off
REM Autonomous Tweet Generator - Run this to get AI-selected tweet
cd /d "%~dp0"
python autonomous_tweet_scheduler.py
echo.
echo Tweet saved to: next_tweet.txt
echo Schedule saved to: tweet_schedule.json
echo.
pause

