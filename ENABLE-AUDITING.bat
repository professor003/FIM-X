@echo off
REM Enables Windows File System object-access auditing, which FIM-X needs for
REM HIGH-confidence user attribution. MUST be run as Administrator.
REM
REM This only enables the audit POLICY. You must ALSO add a SACL to each folder
REM you intend to monitor:
REM   Folder > Properties > Security > Advanced > Auditing > Add
REM   Principal: Everyone   Type: Success   Applies to: This folder, subfolders and files
REM   Permissions: Modify (at minimum Write data, Delete, Change permissions, Take ownership)
REM
REM Note: object-access auditing writes a Security log entry for every matching
REM access. On a busy folder this can generate a large volume of log data. Size the
REM Security log accordingly and review with your unit's IT policy first.
net session >nul 2>&1 || (echo Run this file as Administrator. & pause & exit /b 1)
auditpol /set /subcategory:"File System" /success:enable
auditpol /get /subcategory:"File System"
echo.
echo Audit policy set. Now add a SACL to each monitored folder as described above.
pause
