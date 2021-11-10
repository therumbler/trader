FROM python:3.10.0
RUN apt-get update && apt-get install -y wait-for-it
RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv sync

COPY . .

ENTRYPOINT [ "./docker-entrypoint.sh" ]
