FROM python:3.12-slim
WORKDIR /app
RUN pip install flask requests beautifulsoup4
COPY app.py .
COPY routes/ /app/routes/
CMD ["python", "app.py"]
