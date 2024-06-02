FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY src/ /app
COPY mock/ /app/mock

EXPOSE 5000

CMD ["gunicorn","-w","3","main:create_app()","-b","0.0.0.0:5000"]
#CMD ["python","main.py"]
