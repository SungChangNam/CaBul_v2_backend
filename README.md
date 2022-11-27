## 프로젝트 이름

### CaBul ver.2

## 프로젝트 소개

### 자신의 사진을 유화 스타일로 바꾸고 자동으로 카테고리를 분류해주는 사이트

## 팀 이름

### 싸지방

## 팀원 소개

박준석 

[devjunseok - Overview](https://github.com/devjunseok)

노우석 

[WooSeok-Nho - Overview](https://github.com/WooSeok-Nho/)

성창남 

[SungChangNam - Overview](https://github.com/SungChangNam)

양기철 

[hanmariyang - Overview](https://github.com/hanmariyang)

이태겸 

[poro625 - Overview](https://github.com/poro625)

## 개발 역할 분담

### 프론트엔드 - 팀원 모두

### 최상위 템플릿

- [ ]  index.html
- [ ]  base.html

### users 템플릿

- [ ]  login.html (로그인페이지)
- [ ]  signup.html (회원가입페이지)
- [ ]  profile_edit.html (회원정보 수정 페이지)
- [ ]  profile_edit_password.html(비밀번호 수정 페이지)
- [ ]  follow.html (회원정보 읽기, 팔로우,팔로워 페이지)

### articles템플릿

- [ ]  home.html (영화 목록, 영화 클릭하면 영화 상세 페이지로 이동(모달로 처리))
- [ ]  upload.html (게시 업로드)
- [ ]  update.html (게시글 수정 페이지)
- [ ]  search.html (검색페이지)
- [ ]  detail.html (게시글 상세 페이지)
- [ ]  base.html (위에 navbar, 검색창, 글쓰기버튼, 홈버튼, 알림, 베이스 html)
- [ ]  footer.html (하단에 팀 소개)

### JavaScript

- users api 자바스크립트 - 박준석, 노우석
    
    
- contents api 자바스크립트 - 박준석, 양기철, 성창남, 이태겸
    
    

### 백엔드 - 팀원 모두

- 로그인 기능(users)
    - [x]  회원가입 (email, 이름,비밀번호) - 박준석
    - [x]  로그인 - 박준석
    - [x]  내 프로필 편집(비밀번호 변경, 이메일 변경, 프로필 사진 변) - 노우석
    - [x]  회원탈퇴 - 노우석
    - [x]  마이페이지(유저정보 조회 기능) - 노우석
- 게시글 기능(articles)
    - [ ]  사진 업로드, 수정 및 삭 - 박준석, 양기철
    - [ ]  댓글올리기+ 댓글 수정(본인의 댓글만)  - 성창남
    - [ ]  좋아요 - 이태겸
    - [ ]  검색 - 이태겸
    - [ ]  태그 - 이태겸
- 딥러닝 - 유화제작
    - [ ]  유화 제작 -  박준석, 양기철
    - [ ]  카테고리 자동 분류 - 박준석, 양기철
- 배포 - 팀원 모두
    - [ ]  EC2, Docker 사용
- 추가로 시도해 볼 기능들
    - [ ]  팔로우, 팔로워
    - [ ]  소셜 로그인
    - [ ]  대댓글
    - [ ]  pagigantion

## 개발 일정

- 11-22 (SA 작성 및 프로젝트 세팅)
- 11-23 (백엔드 API 구현)
- 11-24 (백엔드 API 구현)
- 11-25 (백엔드 API 마무리 및 프론트 API 구현)
- 11-26 (프론트 API 구현)
- 11-27 (프로젝트 마무리)
- 11-28 (발표 및 발표준비)
- 토요일은 자율적으로 시간이 될 때 참여하고 일요일은 풀타임으로 참여!

## 사용하는 기술

- python (3.10.8)
- Django (4.1.3)
- HTML
- JavaScript
- sqlite
- git
- yolov5
- PyTorch
- opencv
- Docker
- gunicorn
- nginx

## 와이어프레임

[https://www.figma.com/embed?embed_host=notion&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FMFJqOD0rR4XhZFmudkHHLz%2FCaBul%3Fnode-id%3D0%253A1%26t%3DSyMiLU8R9dtuJsyP-1](https://www.figma.com/embed?embed_host=notion&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FMFJqOD0rR4XhZFmudkHHLz%2FCaBul%3Fnode-id%3D0%253A1%26t%3DSyMiLU8R9dtuJsyP-1)

## DB erd

![CaBul_v2 (1).png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a6ef1c5c-030b-47c1-8772-8b232bf3141d/CaBul_v2_(1).png)

## API 명세서

[프로젝트 API 설계하기](https://www.notion.so/6e706e8087d54bf691f13f8f2bb12481)
