build.%:
	@echo "Building ipaspeech.$* Docker image"
	docker buildx build --platform linux/amd64 -f src/Dockerfile -t ipaspeech:$* src

up.%: build.%
	@echo "Running ipaspeech.$*"
	docker run --rm --name ipaspeech -p 8080:8080 -v /Users/cp/.aws:/root/.aws -v /Users/cp/cpak/ipaspeech/src/data:/app/data -t ipaspeech:$*

clean:
	@echo "Clean up Docker assets"
	docker volume prune -f
	docker image prune -f
	docker container prune -f
