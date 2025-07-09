include .env
export $(shell sed 's/=.*//' .env)
.PHONY: run stop

run:
	uvicorn app.main:app --host $(HOST) --port $(PORT) --reload --env-file .dev.env

install:
	@echo "Installing deppendency $(LIBRARY)"
	uv add $(LIBRARY)

uninstall:
	@echo "Uninstalling deppendency $(LIBRARY)"
	uv remove $(LIBRARY)

format:
	./format.sh

stop:
	@echo "Stopping server"
	@taskkill /F /IM python.exe /T > nul 2>&1 || echo "No processes found"
	@echo "Server stopped"