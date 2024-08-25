FROM python:3.8-slim

WORKDIR /app

# Install PostgreSQL development package
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
