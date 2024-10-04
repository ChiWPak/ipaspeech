build.%:
	docker build -f src/Dockerfile -t ipaspeech:$* src

up:
	docker run --rm --name ipaspeech -p 8080:8080 -v /Users/cp/.aws:/root/.aws -v /Users/cp/cpak/ipaspeech/src/data:/app/data -t ipaspeech:latest

clean:
	docker volume prune -f
	docker image prune -f
	docker container prune -f
