FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

EXPOSE 8000

# Run the API (uvicorn directly is slightly faster)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
