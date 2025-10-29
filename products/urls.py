from django import path
from . import views
app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:categore_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/detail/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
],