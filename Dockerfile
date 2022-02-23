# Using Debian slim-buster to reduce Docker image size
FROM debian:bullseye-slim

WORKDIR /home/app

RUN mkdir -p /home/app

ARG DEVELOPMENT

# Install expensive things
# Installing postgresql-client-12 needs extra step (https://www.postgresql.org/download/linux/debian/)
# Install latest nginx from mainline (http://nginx.org/en/linux_packages.html)
# libpython3.9 needed for uwsgi to work
RUN \
  BUILD_DEPS='g++ python3-dev git gnupg2' \
  && apt-get update \
  && apt-get install -y wget less git vim-tiny python3 python3-pip python-is-python3 libpython3.9 \
  && apt-get install -y --no-install-recommends $BUILD_DEPS \
  && pip install pipenv \
  && echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && apt-get update \
  && apt-get install -y postgresql-client-12 \
  && apt-get install -y locales \
  && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && apt-get purge --autoremove -y $BUILD_DEPS \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Optimization trick to cache pip libraries if not changed
# COPY requirements.txt requirements-dev.txt ./
COPY Pipfile Pipfile.lock ./

RUN \
  BUILD_DEPS='g++ python3-dev libffi-dev libpq-dev git' \
  && apt-get update \
  && apt-get install -y --no-install-recommends $BUILD_DEPS \
#  && pip install --no-deps -r requirements.txt \
  && pipenv install --system --dev \
  && apt-get purge --autoremove -y $BUILD_DEPS \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy rest of files
COPY . /home/app

CMD "/home/app/entrypoint/run-web.sh"
