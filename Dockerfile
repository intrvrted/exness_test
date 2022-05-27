FROM python:3.10-slim

WORKDIR /app

COPY ["requirements.txt", "."]

RUN ["pip", "install", "--no-cache-dir", "--upgrade", "-r", "requirements.txt"]

COPY ["./app/main.py", "./app/db_support.py", "."]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "critical"]
