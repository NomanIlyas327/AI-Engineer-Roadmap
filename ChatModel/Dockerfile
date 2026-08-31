FROM python:3.10-slim

WORKDIR /app

# Requirements install karein
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Complete code copy karein
COPY . .

EXPOSE 7860

# FastAPI launch karein
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]