# Ourplace - A Collaborative Canvas
Ourplace is a collaborative canvas that can be used to relax with friends and let our your creative spirit.

## Deploying
**Requirements:** Python 3.7
1. Clone this repository using `git clone https://github.com/2400757n/ourplace_project.git` and navigate into the new directory.
2. Make a virtual environment with your method of choice and activate it, we suggest [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
3. Run `pip install -r requirements.txt`
4. Once pip has finished, run:
```
python manage.py makemigrations ourplace
python manage.py migrate
python populate_ourplace.py
python manage.py runserver
```
5. Go to http://localhost/


## Using Docker
If you already have Docker (and optionally compose) installed this method will be faster and easier. If you don't, you can get it [here](https://docs.docker.com/install/).

1. Clone this repository with `git clone https://github.com/2400757n/ourplace_project.git` and navigate to it.
2. Run `docker build -t ourplace .` to create a docker image.
3. Run `docker run -dp 8000:8000 ourplace` and head to http://localhost:8000/

If you have `docker-compose` [installed](https://docs.docker.com/compose/install/) you can skip steps 2 & 3, instead do `docker-compose build` and `docker-compose up -d`.

## Acknowledgements
This project would not work without [Bootstrap](https://getbootstrap.com/) - in particular the Yeti theme from [Bootswatch](https://bootswatch.com/), [JQuery](https://jquery.com/) and [Django](https://www.djangoproject.com/).
