from django.urls import path
from . import views

urlpatterns= [
    path('list/', views.ListBook.as_view(), name='list_book'),
    path('create/',views.CreateBook.as_view(), name='create_book'),
    path('detail/<int:pk>', views.BookDetail.as_view(), name='book_detail'),
    path('update/<int:pk>',views.UpdateBook.as_view(),name='update_book'),
    path('delete/<int:pk>', views.DeleteBook.as_view(),name ='delete_book'),
    path('index/', views.index, name='index'),
    path('create_author', views.CreateAuthor.as_view(),name='create_author'),
    path('search/', views.SearchBook.as_view(), name='search_book'), 
]