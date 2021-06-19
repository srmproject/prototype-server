# 개요
* 1차목표: 프로젝트 생성, 관리를 자동화 하는 프로젝트
* 2차목표: kubeflow 연동
* [요구사항 바로가기](documentation/요구사항.md)

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
