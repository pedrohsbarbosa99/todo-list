from dongle.urls.conf import build_routers, include

urlpatterns = [
    include("api.users.urls"),
    include("api.auth.urls"),
    include("api.tasks.urls"),
]


routes = build_routers(urlpatterns)
