from django.urls import path
from .views import Question1,Question2,Question3
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api_1/',Question1,name='Question1'),
    path('api_2/',Question2,name='Question2'),
    path('api_3/',Question3,name='Question3'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
