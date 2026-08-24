.PHONY: test check-architecture validate

test:
	python -m unittest discover -s tests -v

check-architecture:
	python scripts/check_architecture.py

validate: test check-architecture
