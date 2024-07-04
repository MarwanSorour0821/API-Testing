import requests
import uuid
from helperFunctions import create_task, updateTask,delete_task,newTaskPayload, get_task, listTasks

#API enpoint https://todo.pixegami.io/docs
ENDPOINT = "https://todo.pixegami.io/"


def test_canCreateTask():
    #Request body that the endpoint needs
    payload = newTaskPayload()
    create_task_response = create_task(payload, ENDPOINT)
    assert create_task_response.status_code == 200
    data = create_task_response.json()

    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id, ENDPOINT)
    
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    

def test_canUpdateTask():
    #create task
    payload = newTaskPayload()
    create_task_reponse = create_task(payload, ENDPOINT)
    assert create_task_reponse.status_code == 200
    task_id = create_task_reponse.json()["task"]["task_id"]
    
    #update task
    new_payload = {
        "content": "my update content",
        "user_id" : payload["user_id"],
        "task_id" : task_id,
        "is_done": True
    }

    update_task_response = updateTask(new_payload, ENDPOINT)
    assert update_task_response.status_code == 200


    #get and validate changes
    get_task_response = get_task(task_id, ENDPOINT)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


def test_canListTasks():
    #Create N tasks
    n = 3
    payload = newTaskPayload()
    for _ in range(n):
        create_task_response = create_task(payload, ENDPOINT)
        assert create_task_response.status_code == 200
    
    user_id = payload["user_id"]
    list_task_response = listTasks(user_id, ENDPOINT)
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data["tasks"]
    assert len(tasks) == n
    
    

def test_canDeleteTask():
    #Create
    payload = newTaskPayload()
    create_task_reponse = create_task(payload, ENDPOINT)
    assert create_task_reponse.status_code == 200
    task_id = create_task_reponse.json()["task"]["task_id"]
    
    #delete
    delete_task_response = delete_task(task_id, ENDPOINT)
    assert delete_task_response.status_code == 200


    #get
    get_task_response = get_task(task_id, ENDPOINT)
    assert get_task_response.status_code == 404
