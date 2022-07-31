FROM python:3.10

ENV     CONFIG_ENV .env.prod

WORKDIR /app
COPY    ./requirements.txt /app/requirements.txt
RUN     pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY    . /app

#CMD     ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]