import threading
from typing import Protocol

from google.cloud import tasks_v2

from .task import Task


class Backend(Protocol):
    def run(self, task: Task):
        ...


class ThreadingBackend:
    def run(self, task: Task):
        thread = threading.Thread(target=task.run)
        thread.start()


class CloudTasksBackend:
    def __init__(self, project, location, queue, base_url, service_account, audience):
        self.project = project
        self.location = location
        self.queue = queue
        self.base_url = base_url
        self.service_account = service_account
        self.audience = audience

    def run(self, task: Task):
        client = tasks_v2.CloudTasksClient()
        parent = client.queue_path(
            self.project,
            self.location,
            self.queue,
        )
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": self.base_url + task.fully_qualified_name,
                "oidc_token": {
                    "service_account_email": self.service_account,
                    "audience": self.audience,
                },
                "body": task.params.json(),
            }
        }
        client.create_task(request={"parent": parent, "task": task})
