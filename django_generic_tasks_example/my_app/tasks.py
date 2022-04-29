from django.core.mail import send_mail
from pydantic import BaseModel

import django_generic_tasks as tasks


# define task params as a Pydantic BaseModel
class EmailNotificationParams(BaseModel):
    subject: str
    content: str
    recipients: list[str]


# subclass Task and specify params type as a generic type argument and implement the run method
class EmailNotificationTask(tasks.Task[EmailNotificationParams]):
    def run(self):
        send_mail(
            subject=self.params.subject,
            message=self.params.content,
            from_email=None,
            recipient_list=self.params.recipients,
        )


if __name__ == "__main__":
    params = EmailNotificationParams(
        subject="Hello",
        content="Have a nice day",
        recipients=["alice@example.com", "bob@example.com"],
    )
    task = EmailNotificationTask(params)

    # run a task synchronously
    task.run()

    # run a task asynchronously using settings.TASKS_BACKEND
    task.start()
