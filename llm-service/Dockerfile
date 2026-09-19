FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN addgroup --system securellm && adduser --system --ingroup securellm securellm
USER securellm

EXPOSE 8001

ENV OLLAMA_URL=http://host.docker.internal:11434/api/generate
ENV OLLAMA_MODEL=qwen2.5:1.5b

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]