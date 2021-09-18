FROM python:3.8-alpine

# copy project
COPY app app

WORKDIR app

# install python dependencies
RUN \
	apk add --no-cache postgresql-libs && \
	apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev postgresql-dev && \
	pip install --no-cache-dir -r requirements.txt && \
	apk --purge del .build-deps


EXPOSE 8080

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# key has to be 32 bit length (you can generate it by cryptography.Fernet.generate_key())
ENV SECURITY_KEY key

ENV DATABASE_URL database_url

ENV FLASK_ENV production

CMD ["gunicorn", "-b", "0.0.0.0:8080", "--log-file=-", "app:app"]