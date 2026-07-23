@echo off
REM ══════════════════════════════════════════════════════════
REM  N'Aset OFM — Build local complet (personnage + scenes)
REM  Usage :  naset_build.bat            (build seul)
REM           naset_build.bat test       (build + rendu test 1 frame)
REM ══════════════════════════════════════════════════════════
setlocal
set BLENDER="C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
set SCRIPT=%~dp0scripts\blender\naset_pipeline.py

if not exist %BLENDER% (
  echo [ERREUR] Blender introuvable : %BLENDER%
  exit /b 1
)

if "%1"=="test" (
  %BLENDER% --background --python "%SCRIPT%" -- --render test
) else (
  %BLENDER% --background --python "%SCRIPT%"
)
endlocal
