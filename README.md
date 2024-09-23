# Nilasoft
## Getting Started

To get started with each project:

1. **Clone the Project:**

   - Clone via HTTPS:
     ```bash
      git clone https://github.com/a-sharifi/Nilasoft.git
     ```
## Run security project
   - Change directory to the `security_service` folder:
     ```bash
     cd security_service
     ```
   - Fill the `.env` file with your own values.
    - Install required dependencies:
      ```bash
      pip install -r requirements.txt
      ```
   - Run FastAPI using uvicorn:
    ```bash
         uvicorn src.main:app --reload
    ```
- Build docker image:
 ```bash
docker build -t nila_secure:v1
```


   - Run FastAPI using docker:
     ```bash
        docker run --env-file .env -p 8000:8000 nila_secure:v1 uvicorn src.main:app --host 0.0.0.0 --port 8000
     ```

### With Docker
    docker build -t nila_secure:v1 .

## Run auth_service project
   - Change directory to the `auth_service` folder:
     ```bash
     cd auth_service
     ```
   - Fill the `.env` file with your own values.
    - Install required dependencies:
      ```bash
      pip install -r requirements.txt
      ```
   - Run FastAPI using uvicorn:
     ```bash
     uvicorn src.main:app --reload
     ```


## Swagger
- Swagger UI is available at `/docs` and the OpenAPI schema is available at `/openapi.json`.


## Run tests
   - Change directory to the `security_service` folder:
     ```bash
     cd security_service
     ```
   - Run tests:
     ```bash
     pytest src/security/tests/*
     ```
   - Run tests with docker
     ```bash
      docker run --env-file .env nila_secure:v1 pytest src/security/tests/*
     ```

   - Change directory to the `auth_service` folder:
     ```bash
     cd auth_service
     ```
   - Run tests:
     ```bash
     pytest
     ```