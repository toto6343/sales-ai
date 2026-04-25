# 🚀 Sales AI Assistant Pro

Sales AI Assistant Pro는 영업 사원과 비즈니스 팀을 위한 지능형 영업 지원 도구입니다. 최신 AI 엔진(OpenAI GPT-4o, Anthropic Claude 3.5, Google Gemini 2.0)을 활용하여 리드 발굴부터 고객 문의 대응까지 영업의 전 과정을 자동화하고 최적화합니다.

## 🌟 주요 기능

### 1. 🏠 홈 대시보드
- **영업 현황 요약**: 발굴된 리드, 생성된 답변, Notion 연동 횟수를 한눈에 확인.
- **📊 AI 토큰 사용량 시각화**: 각 AI 엔진별(OpenAI, Anthropic, Gemini) 실시간 토큰 사용량을 프로그레스 바를 통해 시각적으로 모니터링.

### 2. 🎯 지능형 리드 발굴 (Lead Generation)
- **산업군/규모 맞춤형 분석**: 타겟 업종과 고객사 규모에 맞는 잠재 고객 페르소나 분석.
- **문서 기반 분석**: PDF, Excel, Markdown, Text 파일을 업로드하여 해당 문서의 컨텍스트를 반영한 정교한 리드 발굴 가능.
- **Notion 연동**: 분석된 리포트를 클릭 한 번으로 Notion 데이터베이스에 즉시 저장.

### 3. 💬 스마트 문의 답변 (Smart Inquiry)
- **📥 인바운드 대응 (세분화된 카테고리)**:
  - **가격/견적**: ROI와 가치를 강조하는 답변 생성.
  - **경쟁사 비교**: 자사 제품의 강점을 부각하는 전략적 답변.
  - **크레딧/결제**: 결제 정책 및 크레딧 시스템 안내.
  - **기능/스펙**: 기술 상세 및 실제 활용 사례(Use Case) 중심 안내.
  - **기술 지원**: 공감 기반의 빠른 장애 대응 문구 작성.
- **📤 아웃바운드 영업 (도메인 특화)**:
  - **대상 도메인 맞춤화**: IT/SW, 제조업, 금융, 의료 등 산업군별 특수 용어와 Pain Point를 반영한 커스터마이징.
  - **콜드 메일/커피챗**: 높은 오픈율과 전환율을 보장하는 맞춤형 영업 메일 및 제안서 작성.

### 4. ⚙️ 기업 맞춤 설정
- **AI 엔진 선택**: 선호하는 AI 모델(OpenAI, Anthropic, Gemini) 선택 및 API 키 관리.
- **회사 정보 설정**: 회사명, 담당자명, 제품 상세 설명을 설정하여 모든 AI 답변에 자동으로 반영.

## 🛠 기술 스택
- **UI**: CustomTkinter (Modern Python GUI)
- **AI SDK**: OpenAI, Anthropic, Google Generative AI
- **Document Parsing**: pdfplumber, pandas, openpyxl
- **Database**: Notion API
- **Language**: Python 3.9+

## 🚀 시작하기 및 실행 방법

### 1. 원클릭 실행 (권장)
복잡한 설치 과정 없이 제공된 스크립트 파일을 통해 자동으로 환경 설정(가상환경 생성 및 라이브러리 설치)과 프로그램 실행이 가능합니다.
- **Windows**: `run_windows.bat` 파일을 더블 클릭하여 실행합니다.
- **macOS**: `run_mac.command` 파일을 마우스 오른쪽 버튼으로 클릭 후 '열기'를 선택하여 실행합니다.

### 2. 수동 실행 (터미널)
직접 터미널을 통해 실행하려면 다음 명령어를 순서대로 입력하세요.
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt

# 프로그램 실행
python main.py
```

## 📦 프로그램 빌드 (배포용 실행 파일 만들기)

파이썬이 설치되지 않은 PC에서도 사용할 수 있도록 단일 실행 파일(`.exe` 또는 `.app`)로 빌드할 수 있습니다. 본 프로젝트는 `PyInstaller`를 사용하며, 이미 최적화된 빌드 설정(`SalesAI_Assistant.spec`)이 포함되어 있습니다.

### 빌드 방법
1. **PyInstaller 설치**:
   ```bash
   pip install pyinstaller
   ```
2. **빌드 실행**:
   터미널에서 아래 명령어를 입력하여 빌드를 시작합니다.
   ```bash
   pyinstaller SalesAI_Assistant.spec
   ```
3. **결과 확인**:
   빌드가 완료되면 `dist/` 폴더 내에 `SalesAI_Assistant.exe` (Windows 기준) 파일이 생성됩니다. 이 파일만 배포하여 사용할 수 있습니다.

## 📔 데이터 보안 및 연동
- 모든 API 키와 설정 정보는 로컬 환경의 `settings.json`에 저장됩니다. (최초 빌드 시 기본 설정 파일이 포함됩니다.)
- Notion 연동을 위해서는 Notion 개발자 포털에서 API 키(Internal Integration Token)와 데이터베이스 ID를 발급받아야 합니다.

---
*Developed with Sales Efficiency in mind.*