FROM python:3.7

WORKDIR /

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ourplace_project/ ./ourplace_project/
COPY ourplace/ ./ourplace/
COPY manage.py ./
COPY static/ ./static/
COPY populate_ourplace.py ./
RUN python manage.py makemigrations ourplace
RUN python manage.py migrate
RUN python populate_ourplace.py

COPY . .

CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
