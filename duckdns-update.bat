@echo off
REM DuckDNS Auto-Update Script for Windows
REM Save this as: duckdns-update.bat

REM ===== CONFIGURE THESE =====
set DOMAIN=cognitiveload.duckdns.org
set TOKEN=26be0877-e5b1-493d-92a0-9773fe19eac0

REM ===== Script =====
echo Updating DuckDNS...
curl "https://www.duckdns.org/update?domains=%DOMAIN%&token=%TOKEN%&ip=" > nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] DuckDNS updated successfully >> duckdns.log
) else (
    echo [%date% %time%] Failed to update DuckDNS >> duckdns.log
)

