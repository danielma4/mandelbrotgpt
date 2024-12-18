from rest_framework import routers
from .views import MathematicianViewSet, EquationViewSet, LlamaViewSet
from django.urls import path, include

#here, we map views to urls to allow users (or postman) to access the crud operations via http requests

router = routers.DefaultRouter() #automatically generates necessary urls for viewsets
router.register(r'mathematicians', MathematicianViewSet, basename='mathematician') #url for mathematicians
router.register('equations', EquationViewSet)
router.register('llama', LlamaViewSet, basename='llama')


urlpatterns = router.urls #/api/mathematicians, etc