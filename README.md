# 🚀 Taskify - FastAPI + MongoDB Task Manager

A modern, RESTful API for managing tasks built with FastAPI and MongoDB. Features full CRUD functionality, automatic documentation via Swagger UI, and Docker containerization.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Docker Setup](#docker-setup)
- [Development](#development)
- [Contributing](#contributing)

## ✨ Features

- ✅ **Create Tasks** - Add new tasks with title, description, and status
- 📥 **Get Tasks** - Retrieve all tasks or filter by specific criteria
- 📄 **Get Task by ID** - Fetch individual task details
- ✏️ **Update Tasks** - Modify existing tasks (partial updates supported)
- ❌ **Delete Tasks** - Remove tasks from the system
- 🔍 **Filter by Status** - Find tasks by their status (pending, completed, etc.)
- 📚 **Auto Documentation** - Interactive Swagger UI at `/docs`
- 🐳 **Dockerized** - Easy deployment with Docker and docker-compose
- ⚡ **Async Support** - Built with async/await for high performance
- 🛡️ **Error Handling** - Comprehensive error responses with proper HTTP status codes

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: MongoDB with Motor (async driver)
- **Validation**: Pydantic models
- **Documentation**: Automatic OpenAPI/Swagger
- **Containerization**: Docker & Docker Compose
- **Environment**: python-dotenv for configuration

## 📁 Project Structure

```
taskify/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── routes.py        # API endpoints and route handlers
│   ├── schemas.py       # Pydantic models for request/response
│   └── database.py      # MongoDB connection and configuration
├── env/                 # Virtual environment
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Multi-container setup
├── .env               # Environment variables
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
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

## 📚 API Endpoints

### Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/task/` | Create a new task | `201`, `400`, `422` |
| `GET` | `/task/` | Get all tasks | `200` |
| `GET` | `/task/{id}` | Get task by ID | `200`, `400`, `404` |
| `PUT` | `/task/{id}` | Update task by ID | `200`, `400`, `404`, `422` |
| `DELETE` | `/task/{id}` | Delete task by ID | `204`, `400`, `404` |
| `GET` | `/task/filter/{status}` | Filter tasks by status | `200` |

### Task Schema

```json
{
  "id": "string",
  "title": "string (required, max 100 chars)",
  "description": "string (optional, max 500 chars)",
  "status": "string (default: 'pending')",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

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

### Update a Task
```bash
curl -X PUT "http://localhost:8000/api/v1/task/6507c7f4e1234567890abcde" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/api/v1/task/6507c7f4e1234567890abcde"
```

### Filter Tasks by Status
```bash
curl -X GET "http://localhost:8000/api/v1/task/filter/completed"
```

## 🐳 Docker Setup

### Using Docker Compose (Recommended)

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

### Using Docker Only

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

### Adding New Features

1. Create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Test your changes
4. Commit and push
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

### Running Tests
```bash
# Add when tests are implemented
pytest
```

## 🌟 Future Enhancements

- [ ] User authentication with JWT tokens
- [ ] Task pagination for large datasets
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] Task priority levels
- [ ] Bulk operations
- [ ] Search functionality
- [ ] API rate limiting
- [ ] Unit and integration tests
- [ ] CI/CD pipeline

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

