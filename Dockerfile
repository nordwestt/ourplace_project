FROM python:3.7

WORKDIR /

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations ourplace
RUN python manage.py migrate
RUN python populate_ourplace.py

CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
