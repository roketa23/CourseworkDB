REM 
CLS
ECHO OFF
CHCP 1251
REM 
SET PGBIN=C:\Program Files\PostgreSQL\14\bin
SET PGDATABASE=ad_forum
SET PGHOST=localhost
SET PGPORT=5432
SET PGUSER=postgres
SET PGPASSWORD=123
REM 
%~d0
CD %~dp0
REM 
SET DATETIME=%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2% %TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
SET DUMPFILE=backup_here.backup
SET LOGFILE=backup_here.log

SET DUMPPATH="C:\Program Files\backup\%DUMPFILE%"
SET LOGPATH="C:\Program Files\backup\%LOGFILE%"
REM 
IF NOT EXIST Backup MD Backup
CALL "%PGBIN%\pg_dump.exe" --format=custom --verbose --file=%DUMPPATH% 2>%LOGPATH%
REM 
IF NOT %ERRORLEVEL%==0 GOTO Error
GOTO Successfull
REM 
:Error
DEL %DUMPPATH%
MSG * "Ошибка при создании резервной копии базы данных. Смотрите backup.log."
ECHO %DATETIME% Ошибки при создании резервной копии базы данных %DUMPFILE%. Смотрите отчет %LOGFILE%. >> backup.log
GOTO End
REM 
:Successfull
ECHO %DATETIME% Успешное создание резервной копии %DUMPFILE% >> backup.log
GOTO End
:End
pause
