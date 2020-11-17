from django.urls import path

from .views import bbs
from .views import BbDetailView
from .views import comments

urlpatterns = [
	path('bbs/', bbs),
	path('bbs/<int:pk>/', BbDetailView.as_view()),
	path('bbs/<int:pk>/comments/', comments)
]