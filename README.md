# 🚀 Taskify - FastAPI + MongoDB Task Manager

A modern, RESTful API for managing tasks built with FastAPI and MongoDB. Features full CRUD functionality, comprehensive test suite, automatic documentation via Swagger UI, and robust async architecture.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Docker Setup](#docker-setup)
- [Development](#development)
- [Contributing](#contributing)

## ✨ Features

- ✅ **Create Tasks** - Add new tasks with title, description, and status
- 📥 **Get Tasks** - Retrieve all tasks or filter by specific criteria
- 📄 **Get Task by ID** - Fetch individual task details
- ✏️ **Update Tasks** - Modify existing tasks with PATCH support (partial updates)
- 🔄 **Update Status** - Dedicated endpoint for status-only updates
- ❌ **Delete Tasks** - Remove tasks from the system
- 🔍 **Filter by Status** - Find tasks by their status (pending, in_progress, completed, cancelled)
- 📚 **Auto Documentation** - Interactive Swagger UI at `/docs`
- 🧪 **Comprehensive Testing** - 30 unit tests with 100% pass rate
- ⚡ **Async Support** - Built with async/await for high performance
- 🛡️ **Error Handling** - Comprehensive error responses with proper HTTP status codes
- 🎯 **Status Validation** - Enum-based status validation with Pydantic
- 🐳 **Docker Ready** - Containerization support (implementation pending)

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.13+)
- **Database**: MongoDB with Motor (async driver)
- **Validation**: Pydantic v2 models with enum validation
- **Testing**: pytest + pytest-asyncio with comprehensive mocking
- **Documentation**: Automatic OpenAPI/Swagger
- **HTTP Client**: httpx for async API testing
- **Environment**: python-dotenv for configuration

## 📁 Project Structure

```
taskify/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── routes.py        # API endpoints and route handlers
│   ├── schemas.py       # Pydantic models with TaskStatus enum
│   └── database.py      # MongoDB connection and configuration
├── tests/               # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py      # Test fixtures and mocking utilities
│   ├── test_routes.py   # API endpoint tests (17 test classes)
│   └── test_schemas.py  # Pydantic model validation tests
├── env/                 # Virtual environment
├── requirements.txt     # Python dependencies
├── pytest.ini          # Pytest configuration
├── Dockerfile          # Docker container configuration (pending)
├── docker-compose.yml  # Multi-container setup (pending)
├── .env               # Environment variables
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+ (tested with Python 3.13.5)
- MongoDB (local installation or Docker)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd taskify
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "MONGO_URI=mongodb://localhost:27017" > .env
   echo "DATABASE_NAME=taskify_db" >> .env
   ```

5. **Start MongoDB** (if running locally)
   ```bash
   mongod
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Documentation: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

## 🧪 Testing

This project includes a comprehensive test suite with **30 unit tests** covering all API endpoints and edge cases.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_routes.py

# Run tests with coverage (if coverage installed)
pytest --cov=app

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

### Test Coverage

- ✅ **API Endpoints**: All CRUD operations with success and error scenarios
- ✅ **Status Validation**: TaskStatus enum validation with invalid inputs
- ✅ **Error Handling**: 400, 404, 422 HTTP status code responses
- ✅ **Database Operations**: Mocked MongoDB operations with async iteration
- ✅ **Schema Validation**: Pydantic model validation with edge cases

### Test Structure

```
tests/
├── conftest.py          # Fixtures, AsyncClient, MockTasksCollection
├── test_routes.py       # 17 test classes covering all endpoints
└── test_schemas.py      # Pydantic model validation tests
```

### Key Testing Features

- **AsyncClient**: httpx-based async API testing
- **Database Mocking**: Custom MockTasksCollection with async iterator support  
- **Fixture Management**: Comprehensive test data fixtures
- **Async Testing**: Full pytest-asyncio integration

## 📚 API Endpoints

### Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/task/` | Create a new task | `201`, `400`, `422` |
| `GET` | `/task/` | Get all tasks | `200` |
| `GET` | `/task/{id}` | Get task by ID | `200`, `400`, `404` |
| `PATCH` | `/task/{id}` | Update task by ID (partial) | `200`, `400`, `404`, `422` |
| `PATCH` | `/task/{id}/status` | Update task status only | `200`, `400`, `404`, `422` |
| `DELETE` | `/task/{id}` | Delete task by ID | `204`, `400`, `404` |
| `GET` | `/task/filter/{status}` | Filter tasks by status | `200`, `400` |

### Task Schema

```json
{
  "id": "string (ObjectId)",
  "title": "string (required, max 100 chars)",
  "description": "string (optional, max 500 chars)",
  "status": "enum (pending|in_progress|completed|cancelled)",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Status Enum Values

- `pending` - Task is created but not started
- `in_progress` - Task is currently being worked on  
- `completed` - Task has been finished
- `cancelled` - Task has been cancelled

## 💡 Usage Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/task/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "status": "pending"
  }'
```

### Get All Tasks
```bash
curl -X GET "http://localhost:8000/api/v1/task/"
```

### Get Task by ID
```bash
curl -X GET "http://localhost:8000/api/v1/task/6507c7f4e1234567890abcde"
```

### Update a Task (Partial Update)
```bash
curl -X PATCH "http://localhost:8000/api/v1/task/6507c7f4e1234567890abcde" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "description": "Updated description"
  }'
```

### Update Task Status Only
```bash
curl -X PATCH "http://localhost:8000/api/v1/task/6507c7f4e1234567890abcde/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/api/v1/task/6507c7f4e1234567890abcde"
```

### Filter Tasks by Status
```bash
# Valid status values: pending, in_progress, completed, cancelled
curl -X GET "http://localhost:8000/api/v1/task/filter/completed"
```

## 🐳 Docker Setup

> **Note**: Docker configuration is planned for future implementation.

### Using Docker Compose (Coming Soon)

1. **Build and start services**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - API: `http://localhost:8000`
   - Docs: `http://localhost:8000/docs`

3. **Stop services**
   ```bash
   docker-compose down
   ```

### Using Docker Only (Coming Soon)

1. **Start MongoDB**
   ```bash
   docker run -d --name taskify-mongo -p 27017:27017 mongo:latest
   ```

2. **Build and run the app**
   ```bash
   docker build -t taskify-api .
   docker run -d --name taskify-app -p 8000:8000 --link taskify-mongo:mongo taskify-api
   ```

## 🔧 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code documentation
- Write descriptive commit messages
- Maintain 100% test coverage for new features

### Testing Standards
- Write tests for all new endpoints
- Include both success and error scenarios
- Use descriptive test names and docstrings
- Mock external dependencies (database, APIs)

### Adding New Features

1. Create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your changes
3. Write comprehensive tests
   ```bash
   pytest tests/ -v
   ```
4. Ensure all tests pass
5. Commit and push
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

### Running Tests
```bash
# Run all tests (30 tests)
pytest

# Run with verbose output
pytest -v

# Run specific test categories
pytest tests/test_routes.py    # API endpoint tests
pytest tests/test_schemas.py   # Schema validation tests

# Check test coverage
pytest --cov=app --cov-report=html
```

## 🌟 Future Enhancements

- [ ] Docker containerization with docker-compose
- [ ] User authentication with JWT tokens
- [ ] Task pagination for large datasets
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] Task priority levels
- [ ] Bulk operations
- [ ] Search functionality
- [ ] API rate limiting
- [ ] CI/CD pipeline
- [ ] Performance monitoring
- [ ] Database indexes for optimization

## ✅ Completed Features

- [x] Full CRUD API with FastAPI
- [x] MongoDB integration with Motor
- [x] Pydantic v2 models with enum validation
- [x] Comprehensive test suite (30 tests, 100% pass rate)
- [x] Async/await architecture
- [x] PATCH endpoints for partial updates
- [x] Status-specific update endpoint
- [x] Error handling with proper HTTP status codes
- [x] Automatic API documentation
- [x] Environment configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- MongoDB team for the robust database
- Python community for excellent tooling

---

**Happy Coding! 🚀**

