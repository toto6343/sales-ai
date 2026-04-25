@echo off
chcp 65001 >nul
echo ==============================================
echo Sales AI Assistant - 초기 설정 및 실행 (Windows)
echo ==============================================

:: 파이썬 설치 확인
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [오류] Python이 설치되어 있지 않거나 시스템 환경 변수(PATH)에 등록되어 있지 않습니다.
    echo Python 설치 시 "Add Python to PATH" 체크박스를 반드시 선택해주세요.
    echo 다운로드: https://www.python.org/downloads/
    pause
    exit /b
)

:: 가상환경 생성 (사용자 PC의 기존 파이썬 환경과 완전히 격리)
IF NOT EXIST "venv" (
    echo [안내] 최초 실행입니다. 독립된 실행 환경(venv)을 생성합니다...
    python -m venv venv
)

:: 가상환경 활성화 및 라이브러리 자동 설치
echo [안내] 필요 라이브러리를 확인하고 설치합니다...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

:: 프로그램 실행
echo [안내] Sales AI Assistant를 실행합니다...
python main.py

:: 실행 종료 후 가상환경 비활성화
deactivate
