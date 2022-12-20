.DEFAULT_GOAL := docker

docker:
	docker build -t kim .

docker-run:
	docker run --rm -eDATABASE_URL=${DATABASE_URL} -eSECURITY_KEY=${SECURITY_KEY} kim

docker-save:
	docker save kim | gzip > kim.tar.gz

docker-clean:
	-docker image rm kim
	-rm kim.tar.gz