# Ourplace - A Collaborative Canvas
Ourplace is a collaborative canvas that can be used to relax with friends and let our your creative spirit.
## Using Docker To Deploy
1. Follow the install guide for your system on the [Docker Website](https://docs.docker.com/install/), if you are running Linux you will also need to install [Docker Compose](https://docs.docker.com/compose/install/).
2. Clone this repository (into a sensible directory) with `git clone https://github.com/2400757n/ourplace_project.git`
   - For now you also need to do `git checkout backend-working` because we haven't merged this into master yet.
3. Run `docker-compose build` to create a docker image.
4. Run `docker-compose up -d` and head to http://localhost:8000/

## Manual Deployment
If you are too cool for docker then you will need to set up a Redis server. If you are running Linux then install it from your preferred package manager and start it from your preferred service manager(?).

If you are running windows then you can either:
1. Use Docker (it _just_ works)
2. Install Ubuntu WSL from the [Microsoft Store](https://www.microsoft.com/en-gb/p/ubuntu/9nblggh4msv6) and `apt install redis-server` then `sudo service redis-server start`.
3. Install [Memurai](https://www.memurai.com/get-memurai) and follow the setup.

## Acknowledgements
This project would not work without [Bootstrap](https://getbootstrap.com/) - in particular the Yeti them from [Bootswatch](https://bootswatch.com/), [JQuery](https://jquery.com/) and [Django](https://www.djangoproject.com/).
