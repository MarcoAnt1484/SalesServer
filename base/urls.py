from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('sales-form/', views.makeSale, name="sales-form"),
	path('inventory-form/', views.addInventory, name="inventory-form"),
	path('products-form/', views.addProduct, name="products-form"),
	path('charts/', views.chartsView, name="chartsview"),
	path('tables/', views.tablesView, name="tablesview"),
	path('resetDB/', views.Resetdbs, name="resetButton"),
	path('downloadSalesReport/', views.DownloadSalesJSON, name="dSalesReport"),
	path('downloadInventoryReport/', views.DownloadInventoryJSON, name="dInventoryReport"),
]

