## Manual 과 TODO

## 페이지
### 관리자 페이지

### 사용자 페이지


## ERD

## TODO:
* [ ] GitHub Action Lint & Test workflow 작성
* [ ] sqlalchemy.exc.IntegrityError 핸들


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

### pytest Coverage
```shell
# Install package
pip install pytest-cov coverage coverage-badge

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