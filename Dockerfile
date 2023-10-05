FROM python:3.11.5-alpine3.18
LABEL maintainer='Sheldon Allen <shel@shelsoloa.com>'

USER root

WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
