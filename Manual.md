## Manual 과 TODO

## 페이지
### 관리자 페이지
1. GitHub 사용자 ID 입력
   * 프로젝트 철학(?)도 같이
2. 자기 소개 입력
   * Blog, Instagram 등도 아이디만 입력되면 되게
3. GitHub Stat 출력
4. Tech Stack 선택 
5. 결과 Markdown 내용 출력 및 복사 기능

### 사용자 페이지
* User는 관리자만 할당
* 관리자만 Tech Category, Stack 등 접근 및 제어 가능 
* 

## ERD

## TODO:
* [X] GitHub Action Lint & Test workflow 작성
* [X] GitHub Action AWS 배포 작성
  * [ ] Dockerfile 작성
  * [ ] Docker-compose file 작성
* [X] JWT 구현
* [ ] Redis cache 적용
* [ ] GitHub REST API 연동 구현
  * https://docs.github.com/en/rest/overview/resources-in-the-rest-api#schema
* [ ] sqlalchemy.exc.IntegrityError Handle 구현
* [ ] pytest conftest 정리 

---
### Lint
```shell
# Install package
pip install flake8

# create flake config file
create '.flake8' file

# Start lint with flake
flake8 .
```

### pytest and coverage
```shell
# Install package
pip install pytest pytest-cov coverage coverage-badge

# pytest
pytest .

# coverage
coverage run -m pytest app/tests/ 

# pytest coverage
pytest --cov-report term-missing --cov=. app/tests/

# 통계
coverage report
# Html 로
coverage html
# 이전 기록 삭제
coverage erase

# Create coverage badge
coverage-badge -o coverage.svg
```

## Ref
* Google UI Icon Font
  * https://fonts.google.com/icons