FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY . .

#  COPY scripts folder (IMPORTANT)
COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]