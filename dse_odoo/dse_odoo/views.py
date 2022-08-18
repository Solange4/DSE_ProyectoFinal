from django.http import HttpResponse

from django.template import Template, Context, loader
from django.shortcuts import render
from models.prediction import plotear, prediccion, get_products
import matplotlib.pyplot as plt


obtener_productos = get_products()
name_productos = []
for i in get_products():
    name_productos.append(i[1])


def saludo(request):
    return render(request, 'home.html', {"productos": name_productos})


def prediction(request):
    producto = request.GET["producto"]
    mes = request.GET["mes"]

    code = obtener_productos[int(producto)-1][0]
    mes = mes + " 2022"

    cantidad = prediccion(code, mes)
    plotear()
    plt.close()
    return render(request, 'results.html', {"producto": producto, "mes":mes, "cantidad":cantidad, "code": code})


