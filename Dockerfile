FROM python:3.8.10-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk --update --no-cache add python3-dev libffi-dev gcc musl-dev make libevent-dev build-base

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "run.py"]