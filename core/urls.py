from dongle.urls.conf import include, build_routers

urlpatterns = [
    include("api.users.urls"),
]


routes = build_routers(urlpatterns)
