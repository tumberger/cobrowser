import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_instagram_post():
    # Test implementation
    pass 