from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user,name='register'),
    path('', views.login_user,name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('test/', views.Test.as_view(),name='test'),
    path('book/', views.ListBook.as_view(),name='user_list_book'),
    path('list_users/',views.ListUser.as_view(), name='list_user'),
    path('update_user/<pk>/',views.update_user,name='update_user'),
    path('delete/user/<pk>/',views.DeleteUser.as_view(),name = 'delete_user'),
    path('book_detail/<int:pk>/', views.BookDetail.as_view(), name = 'user_book_detail'),
    path('add_to_cart_list/<book_id>', views.add_to_cart_from_list,name='add_to_cart_from_list'),
    path('add_to_cart_detail/<pk>', views.add_to_cart_from_details,name='add_to_cart_from_details'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('increase_quantity/<item_id>', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<item_id>', views.decrease_quantity, name='decrease_quantity'),
    path('remove_cart_item/<item_id>', views.remove_item, name='remove_item'),
    path('create_checkout_session/', views.create_checkout_session, name = 'create_checkout_session'),
    path('payment_success/', views.success, name='success'),
    path('payment_cancel/', views.cancel, name='cancel'),
    path('search_book/', views.SearchBook.as_view(), name='user_search_book'),
]