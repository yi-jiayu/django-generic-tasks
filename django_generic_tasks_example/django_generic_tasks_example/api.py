from ninja import NinjaAPI

import django_generic_tasks.api

api = NinjaAPI()
api.add_router("/tasks/", django_generic_tasks.api.router)
