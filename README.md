# 네이버 부동산 매물 검색기 🏠

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

네이버 부동산의 아파트 매물 정보를 쉽고 빠르게 검색하고 관리할 수 있는 데스크톱 애플리케이션입니다.

## 🚀 개발 배경

이 프로젝트는 **바이브 코딩(Vibe Coding)** 방식으로 개발되었습니다. Claude AI와 PyCharm의 조합을 통해 실시간 대화형 개발을 진행했으며, MCP(Model Context Protocol) 서버를 활용하여 AI가 직접 코드를 작성하고 수정할 수 있었습니다.

### 개발 스택
- **AI Assistant**: Claude (Anthropic)
- **IDE**: PyCharm + MCP 서버 연동
- **개발 방식**: 대화형 프로그래밍, 실시간 코드 생성 및 수정
- **Made by**: lala-friends

## ✨ 주요 기능

### 1. 아파트 검색 🔍
- 지역명 또는 아파트명으로 검색
- 검색 결과를 테이블 형태로 표시
- 더블클릭으로 아파트 선택

### 2. 매물 필터링 📊
- **거래 유형**: 전체, 매매, 전세, 월세
- **가격 범위**: 최소/최대 가격 설정 (만원 단위)
- 실시간 필터 적용

### 3. 매물 정보 표시 📋
- 동, 층, 평형, 가격, 방향, 등록일 등 상세 정보
- 동일한 동/층의 매물을 그룹화하여 표시
- 등록일 기준 최신순 정렬
- 중개사무소 수 표시

### 4. 중개사무소 상세 정보 🏢
- 매물 더블클릭 시 중개사무소 정보 팝업
- 중개사무소명, 매물번호, 특징 설명 확인
- 등록일 및 수정일 정보 제공

### 5. 데이터 내보내기 💾
- CSV 형식으로 매물 정보 다운로드
- 엑셀에서 바로 열기 가능
- UTF-8 인코딩으로 한글 깨짐 방지

## 🛠️ 기술 스택

- **Language**: Python 3.8+
- **GUI Framework**: PySide6 (Qt for Python)
- **HTTP Client**: requests
- **Data Processing**: pandas (옵션)
- **Excel Export**: openpyxl (옵션)

## 📦 설치 방법

### 1. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 개별 패키지 설치
```bash
pip install PySide6 requests pandas openpyxl
```

## 🚀 실행 방법

### Python으로 직접 실행
```bash
python realEstate.py
```

### 실행 파일 (.exe) 빌드
```bash
python simple_build.py
```
빌드가 완료되면 `dist` 폴더에 `RealEstateSearch.exe` 파일이 생성됩니다.

## 📱 사용 방법

1. **아파트 검색**
   - 검색창에 지역명 또는 아파트명 입력
   - Enter 키 또는 검색 버튼 클릭

2. **아파트 선택**
   - 검색 결과에서 원하는 아파트 더블클릭
   - 하단 상태바에 선택된 아파트 표시

3. **매물 검색**
   - 거래 유형 선택 (전체/매매/전세/월세)
   - 가격 범위 설정
   - '매물 검색' 버튼 클릭

4. **매물 정보 확인**
   - 매물 목록에서 상세 정보 확인
   - 매물 더블클릭으로 중개사무소 정보 확인

5. **데이터 다운로드**
   - '엑셀 다운로드' 버튼 클릭
   - 저장 위치 선택 후 저장

## 🎨 UI/UX 특징

- **컴팩트한 디자인**: 1000x800 픽셀의 적절한 윈도우 크기
- **반응형 레이아웃**: 칼럼 크기 자동 조정
- **직관적인 인터페이스**: 사용자 친화적인 버튼 배치
- **실시간 상태 표시**: 하단 상태바에 현재 작업 표시
- **커스텀 파비콘**: 프로그램 고유 아이콘

## ⚙️ 환경 설정

### API 인증 정보
네이버 부동산 API 접근을 위한 쿠키와 헤더 정보가 필요합니다. `NaverRealEstateAPI` 클래스의 `cookies`와 `headers`를 업데이트하세요.

## 🐛 알려진 문제

- exe 파일 실행 시 Windows Defender가 차단할 수 있음 → '추가 정보' → '실행' 클릭
- pandas 라이브러리가 없을 경우 CSV 형식으로 대체 저장

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙏 감사의 말

이 프로젝트는 Claude AI와의 협업으로 만들어졌습니다. AI와 인간의 창의적인 협업이 만들어낸 결과물입니다.

---

**Made with ❤️ by lala-friends**

*Powered by Claude AI + PyCharm MCP Integration*