FROM python:3.9
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY .env /app/
COPY insert_data_in_db.py /app/
COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "insert_data_in_db.py"]
