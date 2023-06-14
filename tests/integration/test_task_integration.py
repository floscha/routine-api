from routine import Task


def test_setting_starred():
    test_task = Task.from_id("task:dZLzodNYs38tQ5EXtpyaa")
    assert test_task.title == "Test Task"

    test_task.title = "New Title"
    assert test_task.title == "New Title"

    test_task.title = "Test Task"
