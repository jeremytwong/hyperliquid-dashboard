.PHONY: help install test lint format clean docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install all dependencies"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code"
	@echo "  clean       - Clean up generated files"
	@echo "  docker-build- Build Docker images"
	@echo "  docker-run  - Run with Docker Compose"
	@echo "  dev         - Start development servers"

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installation complete!"

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	cd backend && pip install -r requirements-dev.txt
	@echo "Development dependencies installed!"

# Run tests
test:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && npm test -- --watchAll=false

# Run linting
lint:
	@echo "Linting backend code..."
	cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "Linting frontend code..."
	cd frontend && npm run lint

# Format code
format:
	@echo "Formatting backend code..."
	cd backend && black . && isort .
	@echo "Formatting frontend code..."
	cd frontend && npm run format

# Clean up
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "Cleanup complete!"

# Build Docker images
docker-build:
	@echo "Building Docker images..."
	docker-compose build

# Run with Docker Compose
docker-run:
	@echo "Starting services with Docker Compose..."
	docker-compose up -d

# Stop Docker services
docker-stop:
	@echo "Stopping Docker services..."
	docker-compose down

# Development mode
dev:
	@echo "Starting development servers..."
	@echo "Backend will be available at http://localhost:8000"
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Press Ctrl+C to stop all servers"
	@make -j2 dev-backend dev-frontend

# Start backend in development mode
dev-backend:
	cd backend && python run.py

# Start frontend in development mode
dev-frontend:
	cd frontend && npm start 