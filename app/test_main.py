from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
#    {"message": "Welcome to the LLM Automation Agent!","token": AIPROXY_TOKEN} 
    assert response.json() == {"message": "Welcome to the LLM Automation Agent!","token":"your-secret-token"}

def test_readme_format():
    # format_readme_task1 = "Format+/data/format.md+with+prettier+3.4.2"
    format_readme_task1 = "Format /data/format.md with prettier 3.4.2"
    format_readme_task1_http_encoded = format_readme_task1.replace(" ", "+")

    response = client.post(f"https://localhost:8000/run?task={format_readme_task1_http_encoded}")

    assert response.status_code == 200
    print(response.json())
    assert response.json() == {"result": format_readme_task1}