# OCR_Receipt
### 1. 주제 : OCR 기반 영수증 속 필수 정보 추출
- 영수증 속에 있는 필요한 정보들을 일일이 사람이 확인하지 않아도 출력해주는 AI Model을 1차적으로 개발하고자 한다.
- 최종적으로 영수증을 찍으면 가계부에 자동으로 기입이 되는 프로그램을 개발하는 것이 목적이다.
- 필수정보의 예시
    - 구매하는 물건의 이름, 수량, 가격, 총액
    - 점포 및 주소
    - 시간
- 기타정보의 예시
    - WIFI 비밀번호
    - 화장실 비밀번호
- 추가정보의 예시
    - 점포의 이름이 정확하게 나오지 않는 경우 구매하는 물건을 통해 점포의 카테고리를 예측해 알려준다.

### 2. 개발 환경
(1) OS : windows 10

(2) python version : 3.8

(3) gpu = rtx 3070ti

(4) 형상 관리 : git, github

(5) text editor : Vscode

(6) DB : Maria DB, Mongo DB

#### 3. 라이브러리 
(1) pytorch : 1.7.1

(2) torchvision : 0.8.2

(3) torchaudio : 0.7.2

(4) cuda : cu110

(5) opencv : 4.0.1

(6) matplotlib : 3.5.1

### Time Table
- 2021.12.26
    - 내용 : 프로젝트 기획 및 초안 작성, github 연동, 개발 환경 설정 
    - 추후계획 : 편의점, 카페, 식당에 대한 영수증 이미지를 10장씩 뽑아오고 Labeling 하기 
- 2021.12.30
    - 내용 : labeling 한 데이터 병합, augmentation 진행