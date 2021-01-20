aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $DOCKER_REGISTRY

docker build -t django/app .
docker tag django/app:latest $DOCKER_REGISTRY/django/app:latest
docker push $DOCKER_REGISTRY/django/app:latest

docker build -t django/proxy .
docker tag django/proxy:latest $DOCKER_REGISTRY/django/proxy:latest
docker push $DOCKER_REGISTRY/django/proxy:latest

CMD="docker stack deploy -c $DOCKER_COMPOSE_YML ec2 --with-registry-auth"
DOCKER_HOST="ssh://$HOST" $CMD