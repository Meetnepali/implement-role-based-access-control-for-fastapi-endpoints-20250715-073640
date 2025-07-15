FROM python:3.11-slim
WORKDIR /code
COPY main.py /code/main.py
RUN pip install --no-cache-dir fastapi==0.110.0 "uvicorn[standard]"==0.29.0 pydantic==1.10.14
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]