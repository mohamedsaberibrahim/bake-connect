FROM python:3.11.4-slim-bullseye as prod
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  gcc \
  curl \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/

EXPOSE 8000

CMD ["/usr/local/bin/python", "-m", "app"]
