# 🚀 Taskify - FastAPI + MongoDB Task Manager

A modern, high-performance RESTful API for managing tasks built with FastAPI and MongoDB. Features comprehensive CRUD functionality, advanced search with regex pattern matching, 40 unit tests with 100% pass rate, automatic documentation via Swagger UI, and production-ready async architecture.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack) 
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Contributing](#contributing)

## ✨ Features

- ✅ **Create Tasks** - Add new tasks with title, description, and status validation
- 📥 **Get Tasks** - Retrieve all tasks with comprehensive filtering capabilities
- 📄 **Get Task by ID** - Fetch individual task details
- ✏️ **Update Tasks** - Modify existing tasks with PATCH support (partial updates)
- 🔄 **Update Status** - Dedicated endpoint for status-only updates
- ❌ **Delete Tasks** - Remove tasks from the system
- 🔍 **Filter by Status** - Find tasks by their status (pending, in_progress, completed, cancelled)
- 🔎 **Search Tasks** - Advanced search by title and description with regex support
- 📚 **Auto Documentation** - Interactive Swagger UI at `/docs`
- 🧪 **Comprehensive Testing** - **40 unit tests** with 100% pass rate
- ⚡ **Async Support** - Built with async/await for high performance
- 🛡️ **Error Handling** - Comprehensive error responses with proper HTTP status codes
- 🎯 **Status Validation** - Enum-based status validation with Pydantic
- 🌐 **RESTful Design** - Follows REST conventions with semantic HTTP status codes

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
├── tests/               # Comprehensive test suite (40 tests)
│   ├── __init__.py
│   ├── conftest.py      # Test fixtures and mocking utilities
│   ├── test_routes.py   # API endpoint tests (27 tests across 7 test classes)
│   └── test_schemas.py  # Pydantic model validation tests (13 tests)
├── env/                 # Virtual environment
├── requirements.txt     # Python dependencies
├── pytest.ini          # Pytest configuration
├── .env               # Environment variables
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+ (tested with Python 3.13.5)
- MongoDB (local installation or Docker)
- Git
- Docker (optional, for MongoDB container)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/anand-808/Taskify.git
   cd Taskify
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

5. **Start MongoDB**
   
   **Option A: Local MongoDB**
   ```bash
   mongod
   ```
   
   **Option B: Docker MongoDB (Recommended)**
   ```bash
   # Run MongoDB in Docker container
   docker run -d --name taskify-mongo -p 27017:27017 mongo:latest
   
   # Check if container is running
   docker ps | grep taskify-mongo
   
   # Stop container when done
   docker stop taskify-mongo
   
   # Start existing container
   docker start taskify-mongo
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

This project includes a comprehensive test suite with **40 unit tests** covering all API endpoints, search functionality, and edge cases.

### Running Tests

```bash
# Run all tests (40 tests)
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_routes.py    # 27 API endpoint tests
pytest tests/test_schemas.py   # 13 schema validation tests

# Run tests with coverage (if coverage installed)
pytest --cov=app

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

### Test Coverage

- ✅ **API Endpoints**: All CRUD operations with success and error scenarios
- ✅ **Search Functionality**: Text search with case-insensitive regex matching
- ✅ **Status Validation**: TaskStatus enum validation with invalid inputs
- ✅ **Error Handling**: 400, 404, 422 HTTP status code responses
- ✅ **Database Operations**: Mocked MongoDB operations with async iteration
- ✅ **Schema Validation**: Pydantic model validation with edge cases
- ✅ **Query Parameters**: Search query validation and error handling

### Test Structure

```
tests/
├── conftest.py          # Fixtures, AsyncClient, MockTasksCollection
├── test_routes.py       # 27 tests across 7 test classes
│   ├── TestCreateTask          # Task creation tests
│   ├── TestGetTasks           # Retrieve all tasks tests  
│   ├── TestGetTaskById        # Individual task retrieval tests
│   ├── TestUpdateTask         # Task update tests
│   ├── TestUpdateTaskStatus   # Status-only update tests
│   ├── TestDeleteTask         # Task deletion tests
│   └── TestSearchTasks        # Search functionality tests (10 tests)
└── test_schemas.py      # 13 Pydantic model validation tests
```

### Key Testing Features

- **AsyncClient**: httpx-based async API testing
- **Database Mocking**: Custom MockTasksCollection with async iterator support  
- **Search Testing**: Comprehensive search functionality validation
- **Fixture Management**: Comprehensive test data fixtures
- **Async Testing**: Full pytest-asyncio integration
- **Error Scenarios**: Complete error handling validation

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
| `GET` | `/task/filter/{status}` | Filter tasks by status | `200`, `422` |
| `GET` | `/task/search?q={query}` | Search tasks by title/description | `200`, `404`, `422` |

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

### Search Tasks
```bash
# Search by title or description (case-insensitive)
curl -X GET "http://localhost:8000/api/v1/task/search?q=documentation"

# Search with special characters (URL encoded)
curl -X GET "http://localhost:8000/api/v1/task/search?q=bug%20%23123"

# Partial matching (searches both title and description)
curl -X GET "http://localhost:8000/api/v1/task/search?q=fastapi"
```

### Response Examples

#### Successful Task Creation (201)
```json
{
  "id": "6507c7f4e1234567890abcde",
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "status": "pending",
  "created_at": "2025-08-07T10:30:00Z",
  "updated_at": "2025-08-07T10:30:00Z"
}
```

#### Search Results (200)
```json
[
  {
    "id": "6507c7f4e1234567890abcde",
    "title": "API Documentation",
    "description": "Write FastAPI documentation",
    "status": "pending",
    "created_at": "2025-08-07T10:30:00Z",
    "updated_at": "2025-08-07T10:30:00Z"
  }
]
```

#### No Search Results (404)
```json
{
  "detail": "No tasks found matching search query: 'nonexistent'"
}
```

#### Error Response (422)
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["query", "q"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

##  Development

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
# Run all tests (40 tests total)
pytest

# Run with verbose output
pytest -v

# Run specific test categories
pytest tests/test_routes.py    # 27 API endpoint tests
pytest tests/test_schemas.py   # 13 schema validation tests

# Run specific test classes
pytest tests/test_routes.py::TestSearchTasks -v  # Search functionality tests

# Check test coverage
pytest --cov=app --cov-report=html
```

## 🌟 Recent Updates & Achievements

### ✅ Latest Enhancements (August 2025)
- **Search Functionality**: Added comprehensive search endpoint with regex support
- **Improved Error Handling**: Search returns 404 when no results found (better than empty array)
- **Enhanced Testing**: Expanded test suite from 30 to 40 tests
- **Search Tests**: Added 10 comprehensive search tests covering all scenarios
- **Better Validation**: Enhanced query parameter validation with proper error messages
- **Documentation**: Updated README with complete API documentation and examples

### 🎯 Quality Metrics
- **Test Coverage**: 40 comprehensive unit tests with 100% pass rate
- **API Endpoints**: 8 fully documented REST endpoints  
- **Error Handling**: Complete HTTP status code coverage (200, 201, 204, 400, 404, 422)
- **Async Architecture**: Full async/await implementation for optimal performance
- **Code Quality**: Type hints, proper exception handling, and comprehensive docstrings

## 🌟 Future Enhancements

- [ ] Docker containerization with docker-compose
- [ ] User authentication with JWT tokens
- [ ] Task pagination for large datasets
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] Task priority levels
- [ ] Bulk operations (bulk create, update, delete)
- [ ] Advanced search filters (date range, status combination)
- [ ] API rate limiting
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Performance monitoring and logging
- [ ] Database indexes for optimization
- [ ] WebSocket real-time updates
- [ ] Task assignment to users
- [ ] Task comments and history

## ✅ Completed Features

- [x] Full CRUD API with FastAPI
- [x] MongoDB integration with Motor async driver
- [x] Pydantic v2 models with enum validation
- [x] **Comprehensive test suite (40 tests, 100% pass rate)**
- [x] **Advanced search functionality with regex support**
- [x] **Case-insensitive text search across title and description**
- [x] **Proper HTTP status codes (404 for no search results)**
- [x] Async/await architecture throughout
- [x] PATCH endpoints for partial updates
- [x] Status-specific update endpoint
- [x] Comprehensive error handling with descriptive messages
- [x] Automatic API documentation with OpenAPI/Swagger
- [x] Environment configuration with python-dotenv
- [x] Query parameter validation
- [x] ObjectId validation for MongoDB documents
- [x] **Enhanced test coverage with search functionality validation**

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

