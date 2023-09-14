# Shopping Keyword extractor
쇼핑몰에서의 상품 소싱을 위한 인기검색어 (키워드) 자동 추출 매크로 프로그램 (네이버 데이터랩, 헬프스토어)

## What can we extract using this extractor?
### 추출 항목:
- 사전에 설정한 기준(프로그램 코드에서 설정)에 부합하는 상품 키워드(소싱에 적합한 상품의 이름)
- 해당 키워드 상품의 경쟁강도
- 해당 키워드의 조회수
- 해당 키워드로 업로드 되어있는 상품 수
  
## How to Use
### * 프로그램 실행을 위한 필수적인 추가 사전 작업
  1. 컴퓨터에 크롬 버전에 맞는 google chrome driver 설치
  2. PyCharm 프로젝트 폴더(클론된 폴더)에 chromedriver.exe파일 집어넣기 혹은 PyCharm에서 프로젝트에 이미 있는 chromedriver.exe파일 찾아서 chromedriver_win32 밖으로 빼기

### -> 진행 순서 안내:
1. 크롬버전확인
2. 크롬버전에 맞는 드라이버 다운
3. 프로젝트 폴더에 드라이버 exe파일 압축 해제하기. 이동/ 복붙하기
4. install packages
