# Variables
PYTHON = python
PIP = pip

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run unit tests"
	@echo "  make run       - Run the static image demo"
	@echo "  make webcam    - Run the webcam demo"
	@echo "  make clean     - Remove temporary files"
	@echo "  make docker    - Build the Docker image"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: test
test:
	$(PYTHON) -m unittest discover tests

.PHONY: run
run:
	$(PYTHON) static_image.py images/mcdonalds.jpg --target EUR

.PHONY: webcam
webcam:
	$(PYTHON) webcam.py --target EUR

.PHONY: docker
docker:
	docker build -t ocr-price-converter .

# Clean up bytecode and cache
.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
