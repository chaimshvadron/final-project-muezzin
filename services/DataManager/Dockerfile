FROM python:3.11-slim

WORKDIR /app

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../utils ./utils
COPY ../../services/DataManager ./services/DataManager

RUN mkdir -p /app/data/podcasts

CMD ["python", "-m", "services.DataManager.main"]
