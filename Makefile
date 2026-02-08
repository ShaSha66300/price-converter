# Variables
PYTHON = python
PIP = pip

# Default Image for the "make run" demo
IMAGE ?= images/mcdonalds.jpg
TARGET ?= EUR

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run unit tests"
	@echo "  make run        - Run the static image demo"
	@echo "  make webcam     - Run the webcam demo"
	@echo "  make clean      - Remove temporary files"
	@echo "  make docker     - Build the Docker image"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: test
test:
	export PYTHONPATH=$PYTHONPATH:$(PWD)/src; \
	$(PYTHON) -m unittest discover -s tests

.PHONY: run
run:
	$(PYTHON) src/static_image.py $(IMAGE) --target $(TARGET)

.PHONY: webcam
webcam:
	$(PYTHON) src/webcam.py --target $(TARGET)

.PHONY: docker
docker:
	docker build -t ocr-price-converter .

# Clean up bytecode and cache
.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
