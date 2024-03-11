# Python/Cloud Final project

## How to run

Run tests: `make test`
Run as a container locally: `make dev-container`

## Description

Theme: Project management/profiles dashboard - a service to create, update, share, and delete projects information (logo, details, attached documents)

**Desired functionality:**

- User login/auth
- Create/Delete projects
- Add/Update project's info/details - name, description
- Add/Update/Remove project's logo (image) (+ resizing/cropping on backend)
- Add/Update/Remove projects documents (docx, pdf)
- Share project with other users to access

## API Documentation

### Authorization and authentication

Access model: Authorization via JWT, issued by POST /login. _JWT should last 1 hour._

1. GUEST - non-authenticated user
2. USER - authenticated user
3. PARTICIPANT - USER, invited to the project. Can modify, cannot delete.
4. OWNER - USER, creator of the project. Can do anything.

### API Endpoints

#### Healthcheck

`GET /test`

- Access: GUEST
- Success: `200 "Success"`

#### Authentication

`POST /login { login: string, password: string }` - Login into service

- Access: GUEST
- Success: `200 { access_token: string, token_type: string }`
- Failure:
  - `422 { error: message }` User error: bad JSON format or missing fields
  - `403 { error: message }` Forbidden, incorrect username or password

`POST /auth { login: string, password: string }` - Create user (login, password, repeat password)

- Access: GUEST
- Success: `201 { login: string }`
- Failure:
  - `422 { error: message }` User error: bad JSON format or user was already defined

#### Project

`POST /project { name: string, description: string }` - Create project from details

- Access: USER
- NOTE: Automatically gives access to created project to user, making him the owner of the project.
- Success: `201 { id: int, name: string, description: string }`
- Failure:
  - `422 { error: message }` User error: bad JSON format or missing fields

`GET /projects?limit=int&offset=int` - Get all projects _accessible to the user_

- Access: USER
- Success: `200 []{ id: int, name: string, description: string, created_at: datetime, updated_at: datetime }`
- Failure:
  - `422 {}` Format error

`GET /project/<project_id:int>/info` - Return project's details

- Access: PARTICIPANT, OWNER
- Success: `200 { id: int, name: string, description: string, created_at: datetime, updated_at: datetime }`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`PUT /project/<project_id:int>/info { name?: string, description?: string }` - Update projects details.

- Access: PARTICIPANT, OWNER
- Success: `200 { id: int, name: string, description: string, created_at: datetime, updated_at: datetime }`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`DELETE /project/<project_id:int>` - Delete project.

- Access: OWNER
- Success: `204 {}`
- NOTE: Deletes corresponding logo and documents.
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`POST /project/<project_id:int>/invite?login=<login:string>` - Grant project access to specific user.

- Access: OWNER
- Success: `201 { string }`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

#### Documents

`GET /project/<project_id:int>/documents?limit=int&offset=int` - Return all of the project's documents

- Access: PARTICIPANT, OWNER
- Success: `200 []{ id: UUID, name: string, created_at: datetime, updated_at: datetime }`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`POST /project/<project_id:int>/documents` - Upload document/documents for a specific project

- Body: `file: DOCX, PDF`
- Access: PARTICIPANT, OWNER
- Success: `201 { id: UUID, name: string, created_at: datetime, updated_at: datetime }`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`GET /document/<document_id:UUID>` - Download document, if user has access to the corresponding project

- Access: PARTICIPANT, OWNER
- Success: `file: DOCX, PDF`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Document was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`PUT /document/<document_id:UUID>` - Update document

- Body: `file: DOCX, PDF`
- Access: PARTICIPANT, OWNER
- Success: `200 { id: UUID, name: string, created_at: datetime, updated_at: datetime }`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Document was not found
  - `422 { error: message }` User error

`DELETE /document/<document_id:UUID>` - Delete document and remove from the project.

- Success: `204 {}`
- Access: OWNER
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Document was not found

#### Logo

`GET /project/<project_id:int>/logo` - Download project's logo.

- Success: `file: PNG, JPEG`
- Access: USER
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Project was not found

`PUT /project/<project_id:int>/logo { file: PNG, JPEG }` - Upsert project's logo.

- Access: PARTICIPANT
- NOTE: Later to be tied to AWS Lambda for post-processing
- Success: `200 {}`
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Document was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

`DELETE /project/<project_id:int>/logo` - Delete project's logo.

- Success: `204 {}`
- Access: OWNER
- Failure:
  - `403 {}` Permission denied
  - `404 {}` Document was not found
  - `422 { error: message }` User error: bad JSON format or missing fields

## Implementation Structure

### Used technologies

Programming language: `Python3.10`

- Libraries:
  - `FastAPI`
  - `SQLAlchemy` + `alembic` for migrations
- Linting:
  - `ruff` <- `flake8, black`
  - `mypy`
- Testing:
  - `pytest` + `httpx` for integration testing

Storage:

- PostgreSQL - local for the server, metadata
- AWS S3 - logos and documents

Environment management:

- Local:
  - `poetry` -> `venv` and project configuration
  - githooks -> linting + testing
- Docker
- AWS Lambda functions (for image processing on S3 event)
- CI/CD: GitHub Actions
  - testing/linting/building
  - pushing to registry & deploy to cloud on merge request approval

### Database

[See the structure in dbdiagram.io](https://dbdiagram.io/d/65ce6aa7ac844320ae3f471a)

```dbml
Table users {
  login varchar pk // use as a PK for searching and indexing
  password_hash varchar
}

Table projects {
  id integer pk
  name varchar
  description text
  logo_id varchar // UUID for AWS later
}

Table documents {
  id varchar pk // UUID for AWS later
  project_id integer
}

Table permissions {
  login varchar pk
  project_id integer pk
  permission varchar // used as string for simplicity, less joins
}

Ref: documents.project_id > projects.id
Ref: permissions.login > users.login
Ref: permissions.project_id > projects.id
```
