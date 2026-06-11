@echo off
set /p repo="Enter your GitHub Repository URL: "
git init
git add .
git commit -m "Initial commit: PCDT Pro - AASHTO Girder Design with Dynamic Layout"
git branch -M main
git remote add origin %repo%
git push -u origin main
echo.
echo Project successfully uploaded to GitHub!
pause
