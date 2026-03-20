# API Testing Platform

A backend platform for testing and automating API requests, similar to Postman but focused on execution and test automation.

## Features

- JWT Authentication
- Create and manage API Projects
- Save and organize Endpoints
- Execute real HTTP requests
- Store request history
- Create Test Suites
- Define Test Cases with expected results
- Run automated API tests
- Get structured test reports (pass/fail + success rate)
- Pagination, filtering, and ordering
- Swagger API documentation

## Tech Stack

- Python
- Django
- Django REST Framework
- JWT Authentication
- SQLite (can be upgraded to PostgreSQL)

## How it works

1. Create a Project
2. Add API Endpoints
3. Group tests into a Test Suite
4. Define Test Cases (expected status codes)
5. Run the Test Suite
6. Get a detailed report of passed/failed tests

## Example Test Report

```
{
  "summary": {
    "total": 3,
    "passed": 2,
    "failed": 1,
    "success_rate": "66%"
  }
}
```

## Why this project?

This project demonstrates:

- Real-world backend architecture
- API design with Django REST Framework
- Automated API testing logic
- Handling external HTTP requests
- Data modeling and relationships
- Professional API features (filters, pagination, docs)

## Future Improvements

- Docker support
- Async execution (Celery)
- Frontend dashboard
- Test scheduling
- CI/CD integration

---

Built by Moisés 🚀
