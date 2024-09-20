from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.common.database import sessionmanager
from src.common.exceptions import ExceptionMiddleware
from src.common.response import ResponseMessages, response_error_schema_generator
from src.security.presentation.routers.security_http_router import router as security_router
from src.security.domain.models.entities import security_sql_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    # Startup event
    # Create tables
    async with sessionmanager.connect() as connection:
        await connection.run_sync(security_sql_model.Base.metadata.create_all)
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Security Backend",
    description="Security backend project",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    redirect_slashes=True,
)

origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
security_response_messages = ResponseMessages(object_name="Security Data")
ExceptionMiddleware(app)

app.include_router(
    security_router, responses=response_error_schema_generator(
        "Security Data", security_response_messages
    ),
)
