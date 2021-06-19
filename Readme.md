
- [프로젝트 소개](#프로젝트-소개)
  - [프로젝트 목적](#프로젝트-목적)
  - [프로젝트 목표](#프로젝트-목표)
- [필요조건](#필요조건)
- [설치](#설치)
  - [python venv 생성과 활성화](#python-venv-생성과-활성화)
  - [파이썬 패키지 설치](#파이썬-패키지-설치)
- [실행방법](#실행방법)
  - [DB 생성](#db-생성)
  - [flask 애플리케이션 실행](#flask-애플리케이션-실행)
- [api 목록](#api-목록)

<br>

# 프로젝트 소개
## 프로젝트 목적
개발자(사용자)가 자신이 원할 때 개발환경을 구축해주는 시스템

## 프로젝트 목표
> 프로토타입은 앱 생성만 구현(삭제, 수정 미구현)

1. 사용자가 신청한 개발환경이 쿠버네티스에 구축
   * 1차 목표: private 쿠버네티스
   * 2차 목표: public 쿠버네티스
     * EKS
2. CI/CD 자동화
   * 1차 목표
     * CI: 젠킨스와 blueocean
     * CD: argocd
   * 2차 목표
     * CI: tekton 또는 Gitlab CI
     * CD: argocd
3. 개발환경 마이그레이션
   * 1차 목표: Dev환경만 구축
   * 2차 목표: Dev, Prod
   * 3차 목표: Dev -> Stage -> Prod
4. 로그 시스템
   * 쿠버네티스에서 동작하는 애플리케이션 로그를 보여주는 웹 대시보드
   * 1차 목표: PLG를 구축하고 수동으로 찾아가도록
   * 2차 목표: 자동 연동
   * 3차 목표: 쿼리 추가
5. 메트릭(Metrics) 시스템
   * 쿠버네티스에서 동작하는 애플리케이션 로그 메트릭(cpu, memory 등)정보를 보여주는 웹 대시보드
   * 1차 목표: 프로메테우스 구축하고 수동으로 찾아가도록
   * 2차 목표: 자동 연동
   * 3차 목표: 쿼리 추가
6. 애플리케이션 템플릿
   * 사용자가 생성할
7. 컨테이너 이미지 버전관리
   * 1차 목표: 버전 1로만 
   * 2차 목표: tood
8. UI/UX
   * 1차 목표: html로만 기능이 동작하는지 확인
   * 2차 목표: vuejs 또는 reactjs
9. 통합인증(SSO)
   * 1차 목표: 구현 X
   * 2차 목표: LDAP, 커버로스 사용, 앱 연동
10. 백엔드
    * 1차 목표: flask
    * 2차 목표: flask 또는 springboot
11. workflow 관리
    * 1차 목표: 구현 X
    * 2차 목표: airflow 또는 argo workflow

<br>

# 필요조건
* python 3.6이상

<br>

# 설치
## python venv 생성과 활성화
```sh
python -m venv venv
venv\Script\activate.bat ; 윈도우
venv/Script/activate ; 리눅스
```

## 파이썬 패키지 설치
```sh
pip install -r requirement.txt
```

<br>

# 실행방법
## DB 생성
* DB는 sqlite3를 사용한다. sqlite3는 설치가 필요없으며 sqlite패키지가 파이썬 기본패키지에 있다. <br>
* flask에서 DB를 다룰 떄 쿼리문이 아닌 ORM을 사용한다. 그리고 DDL로 DB를 관리하는 것이 아니라 ORM을 DB를 관리한다. <br>
* 명령어가 잘 실행되면 db.sqlite3파일이 생성된다.
```sh
(venv)$ flask db init
(venv)$ flask db migrate
(venv)$ flask db upgrade
```

## flask 애플리케이션 실행
```sh
(venv)$ python run.py
```

<br>

# api 목록
* flask 애플리케이션 실행 후 swagger 문서 참고
```
예: 127.0.0.1:8888/api/v1
```

<br>
