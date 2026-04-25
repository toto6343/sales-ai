#!/bin/bash
echo "=============================================="
echo "Sales AI Assistant - 초기 설정 및 실행 (Mac)"
echo "=============================================="

# 현재 스크립트가 있는 디렉토리로 이동 (경로 문제 방지)
cd "$(dirname "$0")"

# 파이썬 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "[오류] Python3가 설치되어 있지 않습니다."
    echo "Homebrew가 있다면 터미널에서 'brew install python'을 입력하거나,"
    echo "https://www.python.org/downloads/ 에서 Mac용 Python을 설치해주세요."
    read -p "엔터를 누르면 종료됩니다."
    exit 1
fi

# 가상환경 생성 (사용자 Mac의 기존 파이썬 환경과 완전히 격리)
if [ ! -d "venv" ]; then
    echo "[안내] 최초 실행입니다. 독립된 실행 환경(venv)을 생성합니다..."
    python3 -m venv venv
fi

# 가상환경 활성화 및 라이브러리 자동 설치
echo "[안내] 필요 라이브러리를 확인하고 설치합니다..."
source venv/bin/activate
python3 -m pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt

# 프로그램 실행
echo "[안내] Sales AI Assistant를 실행합니다..."
python3 main.py

# 실행 종료 후 가상환경 비활성화
deactivate
