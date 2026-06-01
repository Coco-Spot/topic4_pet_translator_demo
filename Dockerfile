FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt pyproject.toml ./
COPY src ./src
COPY configs ./configs
COPY scripts ./scripts
COPY web ./web

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src
EXPOSE 8004
CMD ["python3", "-m", "pet_translator_demo.api"]
