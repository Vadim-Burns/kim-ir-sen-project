FROM python:3.8-alpine

RUN \
	apk add --no-cache postgresql-libs && \
	apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev postgresql-dev && \
	pip install --no-cache-dir -r requirements.txt && \
	apk --purge del .build-deps
COPY . .

EXPOSE 80
ENV SECURITY_KEY=cWXO0G3BdlKyvpupgQ-zDwcjIdqvjE54FdfXyoNSuYk\=
ENV DATABASE_URL=postgres://qyyalecpgjsmkp:53dd92dfd1e5ed4ee1f8e2a04d9fc66a497da23d41a9d3234e6234cfe0cee348@ec2-54-247-125-38.eu-west-1.compute.amazonaws.com:5432/dbfrpdo59f277v

CMD ["python", "app.py"]