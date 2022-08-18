from django.http import HttpResponse

from django.template import Template, Context, loader
from django.shortcuts import render
from models.prediction import plotear, prediccion
import matplotlib.pyplot as plt

def saludo(request):
    return render(request, 'home.html')


def prediction(request):
    producto = request.GET["producto"]
    mes = request.GET["mes"]

    cantidad = prediccion('[FURN_6666]','setiembre 2022')
    plotear()
    plt.close()
    return render(request, 'results.html', {"producto": producto, "mes":mes, "cantidad":cantidad})


