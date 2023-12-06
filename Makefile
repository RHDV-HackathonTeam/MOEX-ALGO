docker_clean:
	sudo docker stop $$(sudo docker ps -a -q) || true
	sudo docker rm $$(sudo docker ps -a -q) || true

docker_up:
	docker-compose -f docker-compose.yaml up

docker_upD:
	docker compose -f docker-compose.yaml up -d

docker_down:
	docker compose -f docker-compose.yaml down && docker network prune --force

server_up:
	uvicorn API.main:app --workers 4 --host 0.0.0.0 --port 9878

# Clean cache
clean:
	find . -name __pycache__ -type d -print0|xargs -0 rm -r --
	rm -rf .idea/

test:
	pytest app/TaLib/Test/MomentumIndicatorsTest.py

alembic_init:
	alembic init migrations

alembic_rev:
	alembic revision --autogenerate -m 'init'

alembic_upgrade:
	alembic upgrade heads

pre_commit:
	pre-commit run flake8 --all-files

pylint:
	pylint $(git ls-files '*.py')
