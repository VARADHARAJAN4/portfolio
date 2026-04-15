@echo off
echo [1/3] Staging files...
git add .
echo [2/3] Committing changes...
git commit -m "Portfolio upload - %date% %time%"
echo [3/3] Pushing to GitHub...
git push origin main
echo.
echo Upload Complete! 
pause
