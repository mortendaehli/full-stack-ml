from app.core.celery_app import celery_app


@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    return f"test task returns {word}"


def test_example_task():
    task_output = example_task("Hello World")
    assert task_output == "test task returns Hello World"
