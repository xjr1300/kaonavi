lint:
	flake8 kaonavi
	isort kaonavi --diff
	black --check kaonavi

fmt:
	isort kaonavi
	black kaonavi
