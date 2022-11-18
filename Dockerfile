FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY aspaara ./aspaara

CMD ["uvicorn", "aspaara.api:app", "--reload", "--host", "0.0.0.0"]
