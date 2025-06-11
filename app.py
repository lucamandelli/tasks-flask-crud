from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks: list[Task] = []
task_id_control = 0


def get_tasks():
    return jsonify(
        {
            "Tasks": [task.to_dict() for task in tasks],
            "Total tasks": len(tasks),
        }
    )


def create_task(request_data):
    global task_id_control
    new_task = Task(
        id=task_id_control,
        title=request_data["title"],
        description=request_data.get("description", "No description provided"),
    )
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({"message": "Task created successfully"}), 201


def get_task(task_id):
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict()), 200
    return jsonify({"message": "Task not found"}), 404


def update_task_by_id(task_id, request_data):
    for task in tasks:
        if task.id == task_id:
            if "title" in request_data:
                task.title = request_data["title"]
            if "description" in request_data:
                task.description = request_data["description"]
            if "completed" in request_data:
                task.completed = request_data["completed"]
            return jsonify({"message": "Task updated successfully"})
    return jsonify({"message": "Task not found"}), 404


def delete_task_by_id(task_id):
    task_to_delete = None
    for task in tasks:
        if task.id == task_id:
            task_to_delete = task
            break
    if task_to_delete:
        tasks.remove(task_to_delete)
        return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"message": "Task not found"}), 404


@app.route("/tasks", methods=["GET", "POST"])
def tasks_route():
    if request.method == "GET":
        return get_tasks()
    elif request.method == "POST":
        return create_task(request.get_json())


@app.route("/tasks/<int:task_id>", methods=["GET", "PATCH", "DELETE"])
def task_route_by_id(task_id):
    if request.method == "GET":
        return get_task(task_id)
    elif request.method == "PATCH":
        return update_task_by_id(task_id, request.get_json())
    elif request.method == "DELETE":
        return delete_task_by_id(task_id)
    else:
        return jsonify({"message": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(debug=True)
