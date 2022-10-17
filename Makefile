lint:
	flake8 kaonavi
	black --check kaonavi

fmt:
	isort kaonavi
	black kaonavi
