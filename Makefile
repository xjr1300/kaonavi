lint:
	flake8 kaonavi
	isort kaonavi --diff
	mypy kaonavi
	black --check kaonavi

fmt:
	isort kaonavi
	black kaonavi
