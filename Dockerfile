FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV HOST=0.0.0.0
ENV PORT=8787
EXPOSE 8787

CMD ["sh", "-c", "python -m uvicorn app.server:app --host ${HOST} --port ${PORT}"]
