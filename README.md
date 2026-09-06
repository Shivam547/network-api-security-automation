# Network & API Security Automation Framework

A Python-based API automation and security testing framework built with
**FastAPI, Pytest, Requests, JWT, SQLAlchemy, Docker, and GitHub
Actions**.

The project demonstrates how an SDET can build an automation framework
that covers functional API testing, authentication and authorization,
negative testing, API contract validation, security scenarios, rate
limiting, network connectivity, concurrency/locking, containerized
execution, and CI reporting.

------------------------------------------------------------------------

## CI Status & Test Report

Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` below with
your GitHub username and repository name.

[![API Security Automation
CI](https://github.com/shivam547/network-api-security-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/shivam547/network-api-security-automation/actions/workflows/ci.yml)

**Latest CI Test Report:**\
[View Pytest HTML
Report](https://shivam547.github.io/network-api-security-automation//)

> The GitHub Pages report URL becomes available after the GitHub Actions
> workflow successfully deploys the report. The repository's Pages
> source should be configured as **GitHub Actions** under **Settings →
> Pages**.

------------------------------------------------------------------------

# 1. Project Overview

This project implements a complete API automation environment where:

``` text
                    API Automation Framework
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
    Functional API       Security Testing    Negative Testing
          |                   |                   |
          +-------------------+-------------------+
                              |
                         Pytest + Requests
                              |
                              v
                         FastAPI API
                              |
                         SQLAlchemy
                              |
                            SQLite
```

The application under test is a local FastAPI service created
specifically to provide realistic endpoints for automation and security
testing.

The automation framework communicates with the API using HTTP requests
and validates status codes, response payloads, authentication behavior,
authorization, schemas, error handling, rate limiting, network
connectivity, and concurrent access behavior.

------------------------------------------------------------------------

# 2. Technology Stack

  Area                   Technology
  ---------------------- ---------------------------------------
  Programming Language   Python 3.12
  API Framework          FastAPI
  API Server             Uvicorn
  API Automation         Requests
  Test Framework         Pytest
  Authentication         JWT / Bearer Token
  Authorization          Role-Based Access Control (RBAC)
  ORM                    SQLAlchemy
  Database               SQLite
  Schema Validation      JSON Schema
  Configuration          YAML
  Containerization       Docker
  CI/CD                  GitHub Actions
  Reporting              Pytest HTML + JUnit XML
  Report Hosting         GitHub Pages
  Network Testing        Python socket + curl
  Concurrency            Python ThreadPoolExecutor / threading

------------------------------------------------------------------------

# 3. Features Implemented

## API Functional Testing

The framework validates REST API behavior including:

-   HTTP status codes
-   Request payloads
-   Response payloads
-   Authentication
-   Authorization
-   CRUD-style operations
-   Resource-not-found behavior
-   Unsupported HTTP methods
-   API error responses

------------------------------------------------------------------------

## JWT Authentication

The application uses JWT Bearer authentication.

Implemented scenarios include:

-   Successful login
-   Missing token
-   Invalid JWT
-   Malformed JWT
-   Expired JWT
-   Tampered JWT
-   JWT signed with an incorrect secret
-   Token for a non-existent user
-   Inactive-user validation

The application generates JWT tokens containing user identity and role
information.

Example:

``` text
POST /auth/login
```

Request:

``` json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

``` json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

> OAuth2 is intentionally not part of the current implementation.
> Authentication testing is based on JWT Bearer tokens.

------------------------------------------------------------------------

# 4. RBAC / Authorization Testing

The application implements role-based access control.

Example roles:

``` text
admin
manager
user
readonly
```

Authorization behavior is validated through API tests.

Examples:

-   Admin can access protected resources.
-   Manager can access permitted resources.
-   Normal users have restricted access.
-   Only administrators can delete users.
-   Unauthorized roles receive HTTP `403 Forbidden`.

The framework validates both authentication failures (`401`) and
authorization failures (`403`).

------------------------------------------------------------------------

# 5. BOLA Testing

BOLA testing was implemented for the user-resource flow.

The framework validates that:

-   A user can access their own permitted resource.
-   A normal user cannot access another user's protected resource.

The project deliberately does not add additional BOLA scenarios to the
order flow because the current scope already covers the required
user-resource authorization behavior.

------------------------------------------------------------------------

# 6. Negative Testing

Negative tests verify that invalid requests are rejected correctly.

Implemented scenarios include:

### Authentication failures

``` text
Missing token
Invalid token
Malformed token
Invalid username
Invalid password
```

### Invalid payloads

``` text
Missing required fields
Invalid request data
Missing version field
```

### Invalid parameters

``` text
Non-existent order
Non-existent user
```

### HTTP method validation

Unsupported operations are validated for expected
`405 Method Not Allowed` behavior.

The purpose is to verify that the API fails safely and predictably
instead of accepting invalid requests.

------------------------------------------------------------------------

# 7. API Schema / Contract Validation

JSON Schema validation was added to verify response contracts
independently from the FastAPI/Pydantic implementation.

Example:

``` text
tests/api/test_order_schema.py
```

validates:

``` text
OrderResponse
```

against:

``` text
schemas/order_response.json
```

The schema validates:

-   Required fields
-   Field types
-   Nullable fields
-   Response structure
-   Unexpected additional properties

A similar schema is used for user responses.

This provides an additional API contract validation layer.

------------------------------------------------------------------------

# 8. Rate Limiting

A dedicated rate-limited endpoint was implemented:

``` text
GET /rate-limit/test
```

The current test configuration allows:

``` text
5 requests / 10 seconds
```

The sixth rapid request is expected to return:

``` text
HTTP 429 Too Many Requests
```

The response includes retry information and a:

``` text
Retry-After
```

HTTP header.

Example behavior:

``` text
Request 1 → 200
Request 2 → 200
Request 3 → 200
Request 4 → 200
Request 5 → 200
Request 6 → 429
```

The rate limiter is implemented in memory and is intended for local
testing/demo purposes. A production distributed implementation would
normally use a shared store such as Redis.

------------------------------------------------------------------------

# 9. Network Connectivity Testing

Network-level checks were added separately from API functional tests.

Implemented checks include:

### HTTP connectivity

Validates that the API is reachable over HTTP:

``` text
GET /health
```

Expected:

``` json
{
  "status": "UP"
}
```

### TCP connectivity

Python's `socket` module is used to validate TCP connectivity to the API
host/port.

### DNS resolution

Python socket APIs are used to validate local hostname resolution.

### curl validation

The framework can invoke `curl` through Python's `subprocess` module and
validate the returned HTTP status.

This demonstrates testing beyond application-level assertions.

------------------------------------------------------------------------

# 10. Concurrency and Temporary Locking

The order API contains a temporary resource locking mechanism.

The flow is:

``` text
User A
  |
  | POST /orders/{id}/lock
  v
Order locked for 30 seconds
  |
  +------------------------+
  |                        |
User A                    User B
  |                        |
  | update                 | update
  v                        v
Allowed                  HTTP 429
                         Resource locked
```

The lock acquisition uses an atomic database update so that simultaneous
callers cannot both successfully acquire the same lock.

Implemented behavior includes:

-   Temporary resource locking
-   Lock expiration
-   Lock ownership
-   Rejection of updates from another user while locked
-   `429 Too Many Requests` response
-   Retry information
-   Lock release

Python concurrency tools were used for concurrent test execution.

------------------------------------------------------------------------

# 11. Database Initialization and Test Data Seeding

The application currently uses SQLite.

The database is created automatically when the application starts.

Startup flow:

``` text
Application starts
       |
       v
Create database tables
       |
       v
Seed required users
       |
       v
Start FastAPI
```

The seed operation is designed to avoid creating duplicate users.

This is particularly important for Docker and CI because every new
container can start with a clean database.

------------------------------------------------------------------------

# 12. Configuration Management

Automation configuration is maintained separately from test code.

Example:

``` text
automation/config/config.yaml
```

Example configuration:

``` yaml
base_url: "http://127.0.0.1:8000"
timeout: 10

users:
  admin:
    username: "admin"
    password: "admin123"

  manager:
    username: "manager"
    password: "manager123"

  user:
    username: "user1"
    password: "user123"

  readonly:
    username: "readonly"
    password: "readonly123"
```

This allows the API base URL and test-user credentials to be changed
without modifying individual test cases.

> These example credentials are local/demo credentials only. Real
> projects should store secrets in environment variables or CI secret
> stores.

------------------------------------------------------------------------

# 13. API Client Abstraction

The framework contains a reusable API client:

``` text
automation/clients/api_client.py
```

The client provides reusable methods such as:

``` python
client.get(...)
client.post(...)
client.put(...)
client.delete(...)
```

It also manages the Bearer token:

``` python
client.set_token(token)
client.clear_token()
```

This avoids duplicating HTTP request setup across individual tests.

The resulting test code can focus on business behavior instead of
repeatedly creating sessions and headers.

------------------------------------------------------------------------

# 14. Pytest Fixtures

Common setup is centralized in:

``` text
tests/conftest.py
```

Fixtures include:

``` text
base_url
timeout

admin_token
manager_token
user_token
readonly_token

admin_client
manager_client
user_client
readonly_client

unauthenticated_client
```

The authentication tokens are created at session scope where
appropriate, while API clients are provided to individual tests.

This keeps tests isolated and reduces repetitive login code.

------------------------------------------------------------------------

# 15. Project Structure

The current project is organized approximately as follows:

``` text
network-api-security-automation/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── authorization.py
│   ├── lock.py
│   ├── rate_limiter.py
│   ├── seed.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── rate_limit.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       ├── orders.py
│       └── rate_limit.py
│
├── automation/
│   ├── __init__.py
│   ├── clients/
│   │   ├── __init__.py
│   │   └── api_client.py
│   │
│   ├── utils/
│   │   ├── auth_utils.py
│   │   └── schema_validator.py
│   │
│   └── config/
│       └── config.yaml
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   │
│   ├── api/
│   │   ├── test_authentication.py
│   │   ├── test_order_schema.py
│   │   └── test_user_schema.py
│   │
│   ├── security/
│   │   ├── test_broken_authentication.py
│   │   ├── test_bola.py
│   │   ├── test_rbac.py
│   │   └── test_rate_limiting.py
│   │
│   ├── negative/
│   │   ├── test_authentication_failures.py
│   │   ├── test_invalid_payloads.py
│   │   ├── test_invalid_parameters.py
│   │   └── test_method_validation.py
│   │
│   ├── concurrency/
│   │   ├── test_concurrent_updates.py
│   │   └── test_lock_ownership.py
│   │
│   └── network/
│       ├── test_http_connectivity.py
│       ├── test_tcp_connectivity.py
│       ├── test_dns_resolution.py
│       └── test_network_commands.py
│
├── schemas/
│   ├── order_response.json
│   └── user_response.json
│
├── reports/
│
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── .dockerignore
└── README.md
```

------------------------------------------------------------------------

# 16. Dockerization

The FastAPI application is containerized using Docker.

The Dockerfile:

1.  Uses Python 3.12 slim.
2.  Creates `/app` as the working directory.
3.  Installs Python dependencies.
4.  Copies the project into the image.
5.  Exposes port `8000`.
6.  Starts Uvicorn.

Build the image:

``` bash
docker build -t network-api-security .
```

Run the application:

``` bash
docker run --rm -p 8000:8000 network-api-security
```

Verify:

``` bash
curl http://127.0.0.1:8000/health
```

Expected:

``` json
{
  "status": "UP"
}
```

------------------------------------------------------------------------

# 17. Docker Compose

Docker Compose is used to simplify application startup.

Start the API:

``` bash
docker compose up --build
```

Run in detached mode:

``` bash
docker compose up -d --build
```

Check running services:

``` bash
docker compose ps
```

Stop the environment:

``` bash
docker compose down
```

The current Compose setup manages the FastAPI service while the
automation suite can execute against:

``` text
http://127.0.0.1:8000
```

------------------------------------------------------------------------

# 18. Running the Project Locally

## Prerequisites

Install:

-   Python 3.12+
-   Docker Desktop
-   Git
-   curl

Verify Python:

``` bash
python3 --version
```

Verify Docker:

``` bash
docker --version
```

Verify Docker Compose:

``` bash
docker compose version
```

------------------------------------------------------------------------

## Clone the repository

``` bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

------------------------------------------------------------------------

## Create a virtual environment

macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

``` powershell
python -m venv venv
venv\Scripts\activate
```

------------------------------------------------------------------------

## Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 19. Run the API Locally Without Docker

Start FastAPI:

``` bash
uvicorn app.main:app --reload
```

Verify:

``` bash
curl http://127.0.0.1:8000/health
```

Open Swagger:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 20. Run Tests Locally

With the API running:

``` bash
pytest
```

Because `pytest.ini` contains:

``` ini
addopts = -v
```

verbose output is enabled automatically.

Run a specific test directory:

``` bash
pytest tests/security/
```

Run a specific file:

``` bash
pytest tests/security/test_rbac.py
```

Run a specific test:

``` bash
pytest tests/security/test_rbac.py::test_admin_can_access_users
```

------------------------------------------------------------------------

# 21. Generate Test Reports

Create the reports directory:

``` bash
mkdir -p reports
```

Run:

``` bash
pytest \
  --html=reports/test-report.html \
  --self-contained-html \
  --junitxml=reports/junit-results.xml
```

This generates:

``` text
reports/
├── test-report.html
└── junit-results.xml
```

Open the HTML report on macOS:

``` bash
open reports/test-report.html
```

The HTML report provides detailed human-readable results.

The JUnit XML report is intended for CI systems.

------------------------------------------------------------------------

# 22. GitHub Actions CI

The project uses GitHub Actions for CI.

Workflow:

``` text
Git Push / Pull Request
        |
        v
GitHub Actions
        |
        v
Checkout source
        |
        v
Set up Python
        |
        v
Install dependencies
        |
        v
Build Docker image
        |
        v
Start FastAPI container
        |
        v
Health check
        |
        v
Run Pytest
        |
        +------------------+
        |                  |
        v                  v
   HTML report        JUnit XML
        |                  |
        +------------------+
                 |
                 v
          Upload artifacts
                 |
                 v
          GitHub Pages
```

The workflow file is:

``` text
.github/workflows/ci.yml
```

It is configured to run on pushes and pull requests targeting:

``` text
main
master
```

------------------------------------------------------------------------

# 23. CI Test Reports

The workflow generates two report formats.

### HTML

``` text
reports/test-report.html
```

Uploaded as a GitHub Actions artifact and prepared for GitHub Pages.

### JUnit XML

``` text
reports/junit-results.xml
```

Uploaded as a GitHub Actions artifact for CI consumption.

The report upload steps use:

``` yaml
if: always()
```

so reports remain available even when the test suite fails.

This is important because a failed CI run should still provide
diagnostic test information.

------------------------------------------------------------------------

# 24. GitHub Pages Report

The workflow prepares the HTML report as:

``` text
public/index.html
```

and deploys it through GitHub Pages.

Repository configuration:

``` text
Settings
  → Pages
  → Build and deployment
  → Source: GitHub Actions
```

After deployment, the report can be accessed through:

``` text
https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY_NAME/
```

For security, do not publish secrets, tokens, customer information, or
sensitive test data in a publicly accessible report.

------------------------------------------------------------------------

# 25. CI Status Badge

Add the following to the top of this README:

``` markdown
[![API Security Automation CI](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME/actions/workflows/ci.yml)
```

Replace:

``` text
YOUR_GITHUB_USERNAME
YOUR_REPOSITORY_NAME
```

with your actual GitHub values.

For example:

``` markdown
[![API Security Automation CI](https://github.com/shivam/example/actions/workflows/ci.yml/badge.svg)](https://github.com/shivam/example/actions/workflows/ci.yml)
```

------------------------------------------------------------------------

# 26. Recommended README Report Link

Add:

``` markdown
### Latest Test Report

[View Pytest HTML Report](https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY_NAME/)
```

This gives a reviewer two quick entry points:

``` text
CI Badge
   ↓
GitHub Actions
   ↓
Build/Test status

Test Report Link
   ↓
GitHub Pages
   ↓
Detailed Pytest report
```

------------------------------------------------------------------------

# 27. Complete Local Workflow

### Option A --- Run API locally

Terminal 1:

``` bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2:

``` bash
pytest \
  --html=reports/test-report.html \
  --self-contained-html \
  --junitxml=reports/junit-results.xml
```

------------------------------------------------------------------------

### Option B --- Run API using Docker

Terminal 1:

``` bash
docker build -t network-api-security .
docker run --rm -p 8000:8000 network-api-security
```

Terminal 2:

``` bash
pytest \
  --html=reports/test-report.html \
  --self-contained-html \
  --junitxml=reports/junit-results.xml
```

------------------------------------------------------------------------

### Option C --- Run API using Docker Compose

``` bash
docker compose up -d --build
```

Then:

``` bash
pytest \
  --html=reports/test-report.html \
  --self-contained-html \
  --junitxml=reports/junit-results.xml
```

Finally:

``` bash
docker compose down
```

------------------------------------------------------------------------

# 28. Troubleshooting

## Docker daemon not running

If you see:

``` text
Cannot connect to the Docker daemon
```

start Docker Desktop and verify:

``` bash
docker info
```

------------------------------------------------------------------------

## Authentication tests return 401

The application uses a SQLite database that is initialized and seeded
when the container starts.

Verify login manually:

``` bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

If login fails, inspect the API container logs:

``` bash
docker logs network-api-security-api
```

------------------------------------------------------------------------

## API is not ready

Check:

``` bash
curl http://127.0.0.1:8000/health
```

Expected:

``` json
{
  "status": "UP"
}
```

Also inspect:

``` bash
docker logs network-api-security-api
```

------------------------------------------------------------------------

# 29. Engineering Practices Demonstrated

This project demonstrates the following SDET concepts:

-   API automation
-   REST API testing
-   Python automation
-   Pytest fixtures
-   Reusable API client abstraction
-   Configuration-driven testing
-   Authentication testing
-   JWT validation
-   Authorization/RBAC testing
-   Security testing
-   Negative testing
-   API schema validation
-   Rate-limit validation
-   Network connectivity testing
-   TCP testing
-   DNS testing
-   curl-based validation
-   Concurrent request testing
-   Temporary resource locking
-   SQLite test-data initialization
-   Docker containerization
-   Docker Compose
-   CI/CD with GitHub Actions
-   HTML test reporting
-   JUnit reporting
-   GitHub Pages report deployment

------------------------------------------------------------------------

# 30. Interview Explanation

A concise way to explain the project:

> "I built a Python-based API automation and security testing framework
> using Pytest and Requests. I created a FastAPI application as the
> system under test and implemented JWT authentication, RBAC, negative
> scenarios, API schema validation, rate limiting, network connectivity
> checks, and concurrent resource-locking scenarios. I separated the
> automation layer using reusable API clients and Pytest fixtures. I
> then containerized the API using Docker, generated HTML and JUnit test
> reports, and integrated the suite with GitHub Actions so tests execute
> automatically on pushes and pull requests. The HTML report is also
> deployed through GitHub Pages."

------------------------------------------------------------------------

# 31. Future Enhancements

Possible future improvements include:

-   Replace SQLite with PostgreSQL when realistic database transaction
    testing is required.
-   Replace in-memory rate limiting with Redis for distributed
    environments.
-   Add environment-specific configuration.
-   Store credentials in GitHub Actions Secrets.
-   Run the Pytest framework inside a dedicated Docker test container.
-   Use Docker Compose to orchestrate both API and test services.
-   Add API performance/load testing.
-   Add mutation testing.
-   Add static security scanning.
-   Add dependency vulnerability scanning.
-   Add coverage reporting.
-   Add scheduled CI execution.
-   Add separate smoke, regression, security, and network test suites.

------------------------------------------------------------------------

# 32. Project Goal

The goal of this project is not only to create API tests, but to
demonstrate an end-to-end SDET workflow:

``` text
Design API
    ↓
Build testable application
    ↓
Create reusable automation framework
    ↓
Functional testing
    ↓
Negative testing
    ↓
Security testing
    ↓
Network testing
    ↓
Concurrency testing
    ↓
Containerize application
    ↓
Generate reports
    ↓
Automate CI execution
    ↓
Publish test results
```

This makes the project suitable as a portfolio project for **SDET /
Software Development Engineer in Test / QA Automation Engineer** roles.
