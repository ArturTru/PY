FROM python:3.11-slim

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -e . && playwright install chromium

ENV HEADLESS_MODE=True

CMD ["pytest", "tests/", "-v", "--tb=short"]
