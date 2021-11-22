FROM python:3.9-slim-buster

WORKDIR /prodaja_stanova

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "run.py"]


