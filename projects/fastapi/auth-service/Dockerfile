ARG IMAGE_TAG=312
FROM registry.gitlab.com/vitaleey/docker-registry/fastapi-base-image:${IMAGE_TAG} AS base
ARG USER_UID=1000

WORKDIR /home/userapp/src

COPY --chown=userapp src/requirements /home/userapp/requirements

#RUN --mount=type=secret,id=gitlab_pip_index_url,uid=$USER_UID \
#    pip install --upgrade pip &&  \
#    pip install --no-cache-dir --no-deps -r /home/userapp/requirements/private.in  \
#      --index-url=$(cat /run/secrets/gitlab_pip_index_url)

FROM base AS development

ENV RELEASE_VERSION=development \
    LOG_LEVEL=DEBUG \
    ALLOWED_HOSTS="*" \
    IPYTHONDIR=/home/userapp/.home/ipython \
    HISTFILE=/home/userapp/.home/bash_history \
    PYTHONBREAKPOINT=ipdb.set_trace \
    API_SETTINGS_MODULE=service.settings.development

RUN mkdir /home/userapp/.home && pip install --no-deps -r /home/userapp/requirements/development.txt

CMD ["python3", "./main.py", "runserver", "--host", "0.0.0.0", "--reload"]

FROM base AS production

ENV API_SETTINGS_MODULE=service.settings.production

COPY --chown=userapp src /home/userapp/src
COPY --chown=userapp deploy.sh /home/userapp/deploy.sh

RUN pip install --user --no-deps -r /home/userapp/requirements/production.txt

CMD ["python3", "./main.py", "runserver", "--host", "0.0.0.0", "--proxy-headers"]
