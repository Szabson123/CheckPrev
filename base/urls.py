from django.urls import path
from . import views

urlpatterns = [
    # Functional
    path('', views.redi, name='red'),
    path('generate/', views.generate_page, name='generate_page'),
    path('base/', views.base_page, name='base_page'),
    path('choose_form/', views.choose_form, name='choose_form'),
    
    # Function_to_generate
    path('prepare-serials/', views.prepare_serials, name='prepare_serials'),
    path('send-one-serial/',   views.send_one_serial, name='send_one_serial'),
    
    # Formularze
    path('dodaj-familie/', views.add_famili, name='add_famili'),
    path('dodaj-produkt/', views.add_product, name='add_product'),
    path('dodaj-kompozycje/', views.add_composition, name='add_composition'),
    
    path('api/products/',   views.products_for_family, name='api_products'),
    path('api/compositions/', views.compositions_for_product, name='api_compositions'),
    path('api/product-dimensions/', views.get_product_dimensions, name='product_dimensions'),
]