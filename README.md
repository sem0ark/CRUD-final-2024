# EPAM AI-Driven XStack: Python/Cloud Final project

## Description
Theme: Project management/profiles dashboard - a service to  create, update, share, and delete projects information (logo, details, attached documents)

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
1. GUEST - not logged in entity
2. USER - logged in entity
3. PARTICIPANT - USER, invited to the project, can modify, cannot delete.
4. OWNER - USER, creator of the project, can do anything.

### API Endpoints

#### Permissions

`POST /auth { login: string, password: string }` - Create user (login, password, repeat password) 
- Access: GUEST
- Success: `200 { login: string }`
- Failure:
	- `400 { error: string }` User error: bad JSON format or missing fields

`POST /login { login: string, password: string }` - Login into service
- Access: GUEST
- Success: `200 { token: JWT }`
- Failure:
	- `400 { error: string }` User error: bad JSON format or missing fields

`POST /project/<project_id>/invite?user=<login>` - Grant project access to specific user.
- Access: OWNER
- Success: `201 { message: string }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields

#### Project

`POST /projects { name: string, description: string }` - Create project from details
- Access: USER
- NOTE: Automatically gives access to created project to user, making him the owner (admin of the project).
- Success: `201 { id: UUID, name: string }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields

`GET /projects` - Get all projects, _accessible for a user_
- Access: USER
- Success: `200 { projects: []{ name: string, id: UUID, description: string, documents: []UUID }}`
- Failure:
	- `403 {}` Permission denied

`GET /project/<project_id>/info` - Return project's details
- Access: PARTICIPANT, OWNER
- Success: `200 { id: UUID, name: string, description: name }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields

`PUT /project/<project_id>/info { name?: string, description?: string }` - Update projects details.
- Access: PARTICIPANT, OWNER
- Success: `200 { id: UUID, name: string, description: name }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields

`DELETE /project/<project_id>` - Delete project.
- Access: OWNER
- Success: `204 {}`
- NOTE: Deletes corresponding logo and documents.
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields

#### Documents

`GET /project/<project_id>/documents` - Return all of the project's documents
- Access: PARTICIPANT, OWNER
- Success: `200 { documents: []UUID }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields


`POST /project/<project_id>/documents` - Upload document/documents for a specific project
- Body: `file: DOCX, PDF`
- Access: PARTICIPANT, OWNER
- Success: `201 { id: UUID }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found
	- `400 { error: string }` User error: bad JSON format or missing fields


`GET /document/<document_id>` - Download document, if the user has access to the corresponding project
- Access: PARTICIPANT, OWNER
- Success: `file: DOCX, PDF` 
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Document was not found
	- `400 { error: string }` User error: bad JSON format or missing fields


`PUT /document/<document_id>` - Update document
- Body: `file: DOCX, PDF`
- Access: PARTICIPANT, OWNER
- Success: `200 { id: UUID }`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Document was not found
	- `400 { error: string }` User error

`DELETE /document/<document_id>` - Delete document and remove from the project.
- Success: `204 {}`
- Access: OWNER
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Document was not found

#### Logo

`GET /project/<project_id>/logo` - Download project's logo.
- Success: `file: PNG, JPEG`
- Access: USER
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Project was not found

`PUT /project/<project_id>/logo { file: PNG, JPEG }` - Upsert project's logo.
- Access: PARTICIPANT
- NOTE: Later to be tied to AWS Lambda for post-processing
- Success: `200 {}`
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Document was not found
	- `400 { error: string }` User error: bad JSON format or missing fields

`DELETE /project/<project_id>/logo` - Delete project's logo.
- Success: `204 {}`
- Access: PARTICIPANT
- Failure:
	- `403 {}` Permission denied
	- `404 {}` Document was not found
	- `400 { error: string }` User error: bad JSON format or missing fields


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

