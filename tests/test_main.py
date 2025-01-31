import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session


# Use an sqlite in-memory DB for these, just to mitigate having a separate test postgres instance running for tests
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_movies(client: TestClient):
    response = client.get("movies/")
    assert response.status_code == 200


def test_create_movie(client: TestClient):
    response = client.post(
        "/movies/", json={"movie": "Big Ant", "genre": "Action-Adventure"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["movie"] == "Big Ant"
    assert data["genre"] == "action adventure"


def test_get_movie(client: TestClient):
    # create data
    client.post(
        "/movies/", json={"movie": "Big Ant 2", "genre": "Action-Adventure"}
    )

    # Get
    get_response = client.get("/movies/1")
    data = get_response.json()

    assert get_response.status_code == 200
    assert data["movie"] == "Big Ant 2"
    assert data["genre"] == "action adventure"


def test_get_movie_invalid(client: TestClient):
    # create data
    client.post("/movies/", json={"movie": "Big Ant 3", "genre": "Comedy"})

    # Get
    get_response = client.get("/movies/2")

    assert get_response.status_code == 404


def test_update_movie(client: TestClient):
    # create data
    client.post("/movies/", json={"movie": "Big Ant 4", "genre": "Crime"})

    get_response = client.put(
        "/movies/1", json={"movie": "Big Ant 4", "genre": "Comedy"}
    )
    data = get_response.json()

    assert get_response.status_code == 200
    assert data["movie"] == "Big Ant 4"
    assert data["genre"] == "comedy"


def test_delete_movie(client: TestClient):
    # create data
    client.post("/movies/", json={"movie": "Big Ant 5", "genre": "Animation"})

    # Delete
    get_response = client.delete("/movies/1")
    data = get_response.json()

    assert get_response.status_code == 200
    assert data == ["Deleted"]
