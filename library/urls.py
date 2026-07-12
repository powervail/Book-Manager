from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name="book_detail"),
    path('books/add/', views.create_book, name='create_book'),
    path("books/<int:pk>/edit/", views.update_book, name="update_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
    path('books/<int:book_id>/notes/add/', views.create_note, name="create_note",),
    path('notes/<int:pk>/edit/', views.update_note, name="update_note"),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    path("books/<int:book_id>/quotes/add/", views.create_quote, name='create_quote',),
    path("quotes/<int:pk>/edit/", views.update_quote, name="update_quote"),
    path("quotes/<int:pk>/delete/", views.delete_quote, name="delete_quote"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("books/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite",),
    
]