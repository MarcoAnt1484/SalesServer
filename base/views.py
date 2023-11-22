from django.shortcuts import render
from .forms import SalesForm, InventoryForm, ProductsForm, FilterForm, FilterFormTable
from .models import Sales, Inventory
import plotly.express as px

import random
from datetime import datetime, date, timedelta
from django.http import JsonResponse, FileResponse, HttpResponse
# Create your views here.

def home(request):
	# RUDIMENTARY RESET SWITCH
	if 1 == False:
		Resetdbs()
		""


	# sales = 
	context = {}
	return render(request, 'base/home.html', context)

def makeSale(request):
	form = SalesForm

	if request.method == 'POST':
		# print(request.POST)
		pID = request.POST.get("ProductID")
		tSaleTime = request.POST.get("SaleTime")
		tAmount = request.POST.get("Amount")

		if Inventory.objects.filter(ProductID=pID).exists():
			tempSales = Sales(ProductID = pID, SaleTime = tSaleTime, Amount = tAmount)
			tempSales.save()

			tempInventory = Inventory.objects.get(ProductID = pID)
			tempInventory.Amount -= tAmount
			tempInventory.save()




	context = {'form': form}
	return render(request, 'base/sales_form.html', context)

def addInventory(request):
	form = InventoryForm

	if request.method == 'POST':
		pID = request.POST.get("ProductID")

		if Inventory.objects.filter(id=pID).exists():
			Amount = request.POST.get("Amount")

			temp = Inventory.objects.get(ProductID = pID)
			temp.Amount += Amount
			temp.save()

	InventoryData = Inventory.objects.only('Name', 'Amount').values()

	fig = px.pie(InventoryData, values='Amount', names='Name', title='Total Inventory')
	fig.update_layout(title={
		'font_size':22,
		'xanchor': 'center',
		'x': 0.5
	})

	chart = fig.to_html

	context = {'form': form, 'chart': chart}
	return render(request, 'base/inventory-form.html', context)

def addProduct(request):
	# if request.method == 'POST':

	# 	# CHECKS IF THE PRODUCT NAME DOESN'T EXIST, IF SO IT IS SAVED TO THE DATABASE AND ITS ID RECORDED TO ADD THE PRODUCT TO INVENTORY
	# 	tname = request.POST.get("name")

	# 	if not Products.objects.filter(name=tname).exists():
	# 		tdescription = request.POST.get("description")

	# 		tempProduct = Products(name = tname, description = tdescription)
	# 		tempProduct.save()


	# 		pID = tempProduct.id
	# 		tAmount = 0

	# 		tempInventory = Inventory(ProductID = pID, Amount = tAmount)
	# 		tempInventory.save()


	form = ProductsForm
	context = {'form': form}

	return render(request, 'base/products-form.html', context)

Products = {
	1:"Donitas Bimbo",
	2:"Pan",
	3:"Carne",
	4:"Especias",
	5:"Ropa",
	6:"Electrodomesticos",
	7:"Juegos",
	8:"Limpiadores",
	9:"Utencilios",
	10:"Lacteos"
}

def Resetdbs(request):

	# ADDS THE PRODUCTS TO INVENTORY
	BimboProduct = Inventory(Name = "Donitas Bimbo", Description = "Donitas marca bimbo", Amount = "55", Price = 15, ProductID = 1)
	BimboProduct.save()

	PanProduct = Inventory(Name = "Pan", Description = "Pan blanco", Amount = "90", Price = 23, ProductID = 2)
	PanProduct.save()

	CarneProduct = Inventory(Name = "Carne", Description = "carne roja", Amount = "57", Price = 45, ProductID = 3)
	CarneProduct.save()

	EspeciasProduct = Inventory(Name = "Especias", Description = "Especias mixtas", Amount = "90", Price = 17, ProductID = 4)
	EspeciasProduct.save()

	RopaProduct = Inventory(Name = "Ropa", Description = "Ropa unisex", Amount = "21", Price = 46, ProductID = 5)
	RopaProduct.save()

	ElectroProduct = Inventory(Name = "Electrodomesticos", Description = "Electrodomesticos varios", Amount = "64", Price = 80, ProductID = 6)
	ElectroProduct.save()

	JuegosProduct = Inventory(Name = "Juegos", Description = "Juegos infantiles", Amount = "96", Price = 10, ProductID = 7)
	JuegosProduct.save()

	LimpiadoresProduct = Inventory(Name = "Limpiadores", Description = "Limpiadores para hogar", Amount = "17", Price = 19, ProductID = 8)
	LimpiadoresProduct.save()

	UtenciliosProduct = Inventory(Name = "Utencilios", Description = "Utencilios para comida", Amount = "44", Price = 9, ProductID = 9)
	UtenciliosProduct.save()

	LacteosProduct = Inventory(Name = "Lacteos", Description = "Productos lacteos", Amount = "83", Price = 14, ProductID = 10)
	LacteosProduct.save()


	# SIMPLE EMULATION OF DAILY SALES BY CHANCE

	SalesList = []
	# DailySales = [ [ [pID, Amount], [pID, Amount], [pID, Amount] ], Date]


	start_date = date(2023, 1, 1)
	end_date = date(2024, 1, 1)
	for n in range(int((end_date - start_date).days)):

		current_date = start_date + timedelta(n)
		tempSales = {}

		while True:

			Product = random.randint(1,10)

			if Product not in tempSales:
				tempSales[Product] = 1
			else:
				tempSales[Product] += 1


			if random.randint(0,10) == 10:
				break

		DailySales = []
		for i in tempSales:
			DailySales.append([i,tempSales[i]])

		SalesList.append([DailySales, current_date])

	# SAVES THE SALES TO THE DB
	for DailySales in SalesList:
		# print("Date: ", DailySales[1])
		for Sale in DailySales[0]:
			# print("pID:", Sale[0], "Amount:", Sale[1])
			tempSale = Sales(ProductID=Sale[0], Amount=Sale[1], SaleDate=DailySales[1])
			tempSale.save()

	# RETURNS TO HOME
	context = {}
	return render(request, 'base/home.html', context)

def chartsView(request):

	start = request.GET.get('startDate')
	end = request.GET.get('endDate')

	ProductID = request.GET.get('ProductID')
	ChartType = request.GET.get('Type')

	if not ChartType:
		ChartType = "Income"

	if not start:
		start = '2023-01-01'
	
	if not end:
		end = '2024-01-01'
	
	start = datetime.strptime(start, r'%Y-%m-%d').date()
	end = datetime.strptime(end, r'%Y-%m-%d').date()

	xDates = [start + timedelta(n) for n in range(int((end - start).days))]
	ySales = []

	for date in xDates:

		Total = 0
		DailySales = Sales.objects.filter(SaleDate__contains=date)
		Total = 0

		for sale in DailySales:

			if not ProductID or int(sale.ProductID) == int(ProductID):
				Amount = sale.Amount
				if ChartType == "Income":
					Cost = Inventory.objects.get(ProductID=sale.ProductID).Price
					Total += Amount * Cost
				else:
					Total += Amount
			# else:
			# 	print(sale.ProductID, ProductID)
		
		ySales.append(Total)

	if ChartType == "Income":
		fig = px.line(x=xDates,y=ySales,title="INCOME",labels={'x':'Date', 'y': 'Daily Income'})
	else:
		fig = px.line(x=xDates,y=ySales,title="SALES",labels={'x':'Date', 'y': 'Daily Sales'})


	fig.update_layout(title={
		'font_size':22,
		'xanchor': 'center',
		'x': 0.5
	})

	chart = fig.to_html
	form = FilterForm
	context = {'chart': chart, 'form':form}

	return render(request, 'base/charts.html', context)

def tablesView(request):
	start = request.GET.get('startDate')
	end = request.GET.get('endDate')

	pID = request.GET.get('ProductID')

	salesData = Sales.objects.values()

	if start:
		salesData = salesData.filter(SaleDate__gte=start)
	if end:
		salesData = salesData.filter(SaleDate__lte=end)
	if pID:
		salesData = salesData.filter(ProductID=pID)

	print(type(salesData))

	OldDate = salesData.first()["SaleDate"].strftime(r"%d %B %Y")
	SalesDict = []
	# SalesDict[OldDate] = []
	DayTotal = 0
	Day = OldDate
	x = 0
	for sale in salesData:
		NewDate = sale['SaleDate'].strftime(r"%d %B %Y")

		if NewDate != OldDate:
			SalesDict.append(['', 'Total','','','','',DayTotal])
			SalesDict.append(['.','',''])
			DayTotal = 0
			# SalesDict[NewDate] = []
			Day = NewDate

		ID = sale["id"]
		pID = sale["ProductID"]
		Name = Inventory.objects.get(ProductID=pID).Name
		Amount = sale["Amount"]
		Cost = Inventory.objects.get(ProductID=pID).Price
		Total = Amount * Cost
		DayTotal+=Total

		SalesDict.append([Day, ID,pID,Name,Amount,Cost,Total])
		OldDate = NewDate
		Day = ''

	form = FilterFormTable

	context = {'data':SalesDict, "form":form}
	return render(request, 'base/tables.html', context)
	""

def DownloadSalesJSON(request):
	data = list(Sales.objects.values()) 
	JSONData = JsonResponse(data,safe = False) 


	response = HttpResponse(JSONData, content_type='application/force-download')
	response['Content-Disposition'] = f'attachment; filename={"Sales_Report.json"}'
	return response

def DownloadInventoryJSON(request):
	data = list(Inventory.objects.values()) 
	JSONData = JsonResponse(data,safe = False) 


	response = HttpResponse(JSONData, content_type='application/force-download')
	response['Content-Disposition'] = f'attachment; filename={"Inventory_Report.json"}'
	return response