FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary
RUN pip install Pillow

COPY . .

RUN mkdir -p staticfiles media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
