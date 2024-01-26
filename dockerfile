FROM python:3.11.7-bookworm

RUN apt-get update && apt-get install -y python-dev-is-python3 build-essential ffmpeg libsm6 libxext6

WORKDIR /app

EXPOSE 8000
ENV OPENAI_API_KEY=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
ENV GOOGLE_CLOUD_PROJECT_ID=tsmccareerhack2024-tsid-grp3
ENV GOOGLE_CLOUD_STORAGE_BUCKET=tsmccareerhack2024-tsid-grp3-bucket
ENV HUGGINGFACEHUB_API_TOKEN=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

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]