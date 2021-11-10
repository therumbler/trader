FROM python:3.10.0

RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv sync

COPY . .

ENTRYPOINT [ "./docker-entrypoint.sh" ]
