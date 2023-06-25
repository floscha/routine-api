![logo](logo.png)

# Routine Python API

An unofficial Python API for the [Routine](https://routine.co) planner app.

## Installation

`pip install routine-api`

## Usage

### Prerequisites

First, you have to obtain your Routine token.
For this, go to https://app.routine.co/ and log into the web application.
Then, open the Chrome DevTools and under the **network** tab, find the `renew` request.
(If it doesn't show, try reloading the page without cache, by typing shift + cmd + r on Mac.)
From the `renew` request, find the **Authorization** header and copy the text after **Basic**.
Finally, store the token (i.e. the copied text), either into an *.env* file or an environment variable using `export ROUTINE_TOKEN=<your_token>`.

### Python API

```python
import routine
```

**List all tasks:**

```python
for t in routine.get_all_tasks():
    print(t.title)
```

**Get a single task by its ID:**

```python
t = Task.from_id("<some-task-id")
    print(t.title,
```

**Create a new task with a due date**

```python
new_task = Task("My New Task", [2024, 1, 30])
new_task.create()
```
