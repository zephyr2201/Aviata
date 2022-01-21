FROM python:3.8-slim-buster

ENV PIPENV_NOSPIN true
ENV PYTHONUNBUFFERED 1

# install packages
RUN apt-get -y update \
    && apt-get install -y build-essential gettext libpq-dev\
    && apt-get install -y wkhtmltopdf\
    && apt-get install -y gdal-bin\
    && apt-get install -y libgdal-dev\
    && apt-get install -y --no-install-recommends software-properties-common\
    && apt-add-repository contrib\
    && apt-get update

RUN pip install --upgrade pip pipenv

# Set volume for database and static files.
RUN mkdir -p /static /media

WORKDIR /app

# install requirements
COPY Pipfile* ./
RUN pipenv install --system --ignore-pipfile --dev

COPY . /app

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
