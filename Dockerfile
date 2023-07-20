FROM python:3.10.5

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

copy requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

WORKDIR /

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000