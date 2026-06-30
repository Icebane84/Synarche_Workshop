bootstrap:
	docker compose up -d

shutdown:
	docker compose down

lint:
	ruff check .

format:
	ruff format .

test:
	pytest

build:
	docker compose build

logs:
	docker compose logs -f

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +