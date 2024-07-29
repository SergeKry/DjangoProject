FROM python:3.12-slim
EXPOSE 8000
WORKDIR /app
COPY ./mysite /app/mysite
RUN pip install --no-cache-dir -r mysite/requirements.txt
WORKDIR /app/mysite