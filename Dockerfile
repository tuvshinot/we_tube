FROM python:3.7-alpine
MAINTAINER Tuvshin-dev


ENV PYTHONNUNBUFFERED 1 
# apk package management from python alpine
COPY ./requirements.txt /requirements.txt
# that needs for container running in container postgresql, pillow package
RUN apk add --update --no-cache postgresql-client jpeg-dev
# those are all temporary dependencies for installing python packages
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
# after install del temp-requirements
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# static folders ### -p means if theres no vol will create
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# that creates another user with name user and docker swtiches to user
# if do not do that we person who clones this image will manipulates root access
RUN adduser -D user

# ownership of files to user we created !!! important it should be before changing user
RUN chown -R user:user /vol/
# permission user can do everything with directory
RUN chmod -R 755 /vol/web

USER user