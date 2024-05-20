# fastapi-app/Dockerfile
FROM python:3.11.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000 18000

CMD ["python", "fastapi-app.py", "bin/mnist-digitclassifier-model.keras"]
