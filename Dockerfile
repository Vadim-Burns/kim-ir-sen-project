FROM python:3.10-alpine

# copy project
COPY app app
COPY requirements.txt app/

WORKDIR app

# install python dependencies
RUN \
	apk add --no-cache postgresql-libs && \
	apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev postgresql-dev && \
	pip install --no-cache-dir -r requirements.txt && \
	apk --purge del .build-deps

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

ENV FLASK_ENV production

CMD ["python", "main.py"]