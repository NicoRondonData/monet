# base image
FROM python:3.9.6 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV POETRY_VIRTUALENVS_CREATE false

RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client && \
    apt-get install -y netcat && \
    rm -rf /var/lib/apt/lists/*
# install poetry
RUN curl -sSL https://install.python-poetry.org | python - --version 1.3.2
ENV PATH="/root/.local/bin:$PATH"
RUN poetry self add poetry-plugin-export
RUN poetry --version



# poetry dependencies
COPY poetry.lock pyproject.toml ./

FROM base as development
RUN poetry install --without test,linters,customlinters --no-root
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# linters image
FROM base as linters

RUN poetry install --only dev,linters --no-root

COPY . ./

CMD ["bash"]

# test image
FROM base as test
ARG JUNIT_PATH=./reports/junit.xml
ARG COVERAGE_PATH=./reports/coverage.xml

RUN poetry install --with test --no-root

COPY . ./

CMD ["./test.sh"]
