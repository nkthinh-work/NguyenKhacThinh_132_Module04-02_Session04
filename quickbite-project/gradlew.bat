@echo off
cd /d "%~dp0"
where gradle >nul 2>&1
if %errorlevel% == 0 (
    gradle %*
    exit /b %errorlevel%
)
where docker >nul 2>&1
if not %errorlevel% == 0 (
    echo Can Gradle hoac Docker de build Java. 1>&2
    exit /b 1
)
docker run --rm -e GRADLE_USER_HOME=/workspace/.gradle -v "%cd%:/workspace" -w /workspace gradle:8.10.2-jdk17 gradle --no-daemon %*
exit /b %errorlevel%
