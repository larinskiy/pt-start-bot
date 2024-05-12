FROM python:3.12-slim
WORKDIR /app
COPY bot.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]