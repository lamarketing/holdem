from django.urls import path

from dev.views import TableView, TablesViews

urlpatterns = [
    path('table/<int:id>', TableView.as_view()),
    path('tables/', TablesViews.as_view()),
]