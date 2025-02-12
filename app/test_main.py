from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

TASKS = {
    "A2":[
        "Format /data/format.md with prettier 3.4.2",

    ],
    "A3":[
        "The file /data/dates.txt contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to /data/dates-wednesdays.txt"
    ],
    "A4":[
        "Sort the array of contacts in /data/contacts.json by last_name, then first_name, and write the result to /data/contacts-sorted.json"
    ]
}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
#    {"message": "Welcome to the LLM Automation Agent!","token": AIPROXY_TOKEN} 
    assert response.json()["message"] == "Welcome to the LLM Automation Agent!"

def test_readme_format():
    # format_readme_task1 = "Format+/data/format.md+with+prettier+3.4.2"
    format_readme_task1 = "Format /data/format.md with prettier 3.4.2"
    format_readme_task1_http_encoded = format_readme_task1.replace(" ", "+")

    response = client.post(f"https://localhost:8000/run?task={format_readme_task1_http_encoded}")

    assert response.status_code == 200


def test_all_tasks():
    for task, task_list in TASKS.items():
        print(f"Testing task: {task}")
        for task_item in task_list:
            task_http_encoded = task_item.replace(" ", "+")
            response = client.post(f"https://localhost:8000/run?task={task_http_encoded}")
            assert response.status_code == 200

