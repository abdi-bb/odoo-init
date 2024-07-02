# Makefile for managing ownership in local and Docker environments

# Variables
LOCAL_USER := $(shell id -u):$(shell id -g)
DOCKER_EXEC := docker exec -it -u root odoo_app

# Targets
local-chown:
	sudo chown -R $(LOCAL_USER) extra-addons

docker-chown:
	$(DOCKER_EXEC) chown -R odoo:odoo /mnt/extra-addons

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  local-chown    : Change ownership of 'extra-addons' locally"
	@echo "  docker-chown   : Change ownership of '/mnt/extra-addons' inside Docker container"
	@echo "  help           : Show this help message"