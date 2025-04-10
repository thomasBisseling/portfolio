FROM registry.gitlab.com/vitaleey/docker-registry/django-base-image:312 AS builder
ARG USER_UID=1000

WORKDIR /home/userapp/src

COPY --chown=userapp src/requirements /home/userapp/requirements

RUN --mount=type=secret,id=gitlab_pip_index_url,uid=$USER_UID \
    pip install -r /home/userapp/requirements/private.in  \
      --index-url=$(cat /run/secrets/gitlab_pip_index_url)

FROM builder AS development
ENV RELEASE_VERSION=development
ENV DJANGO_DEBUG=True
ENV LOG_LEVEL=DEBUG
ENV ALLOWED_HOSTS="*"
ENV DJANGO_SETTINGS_MODULE=service.settings.dev
ENV IPYTHONDIR=/home/userapp/.home/ipython
ENV HISTFILE=/home/userapp/.home/bash_history
ENV PYTHONBREAKPOINT=ipdb.set_trace
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@vitaleey.com

RUN mkdir -p /home/userapp/.home

RUN pip install --upgrade pip && pip install --no-deps -r /home/userapp/requirements/development.txt

CMD ["gunicorn", "service.wsgi:application", "--reload", "--timeout=0"]

FROM builder AS production
ENV DJANGO_SETTINGS_MODULE=service.settings.prd
# We only want one worker per pod
ENV GUNICORN_WORKERS=1
# Disable worker restart after x requests, if there is a memory leak k8s have limits and restart pod
ENV GUNICORN_MAX_REQUESTS=0

COPY --chown=userapp src /home/userapp/src
COPY --chown=userapp deploy.sh /home/userapp/deploy.sh

RUN pip install --upgrade pip && pip install --no-deps -r /home/userapp/requirements/production.txt
RUN make compilemessages

CMD ["gunicorn", "service.wsgi:application", "--timeout=600"]