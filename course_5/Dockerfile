FROM python:3.12.4-slim-bullseye

WORKDIR /usr/src/spimex

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src

RUN adduser --disabled-password --gecos '' myuser

WORKDIR /usr/src/spimex/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
