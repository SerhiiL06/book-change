from rest_framework.routers import SimpleRouter
from .views import NewsViewset

routers = SimpleRouter()


routers.register("news", NewsViewset)


urlpatterns = []

urlpatterns += routers.urls
