import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import hvplot.pandas
import sklearn
from sklearn.linear_model import LinearRegression





# matplotlib inline
pd.options.mode.chained_assignment = None  # default='warn'

path = 'C:/Users/Jim/Documents/py_DSE/DSE_ProyectoFinal/dse_odoo/data/reporte2.xlsx'
sheet_name='Análisis de ventas'

df = pd.read_excel(path, sheet_name, header = 2)
df_prod = pd.DataFrame()

meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
         'julio', 'agosto', 'setiembre', 'octubre', 'noviembre', 'diciembre']

mes_ini = anio_ini = mes_fin = anio_fin = X = y = reg_pred = None

# TRATAMIENTO DE DATOS

df.columns = ['Productos', 'Total']

lista_productos = df['Productos']

#print(df['Productos'])
# borra espacios vacios en los string de productos
df['Productos'] = df['Productos'].str.strip()



# cambiar nombre de producto por su codigo
for i in df.index:
    
    if( df['Productos'][i][0] == "[" ):
        indice_i = df['Productos'][i].index('[')
        indice_f = df['Productos'][i].index(']')
        df['Productos'][i] = df['Productos'][i][indice_i:indice_f + 1]
        
#print(df)



# devuelve el indice de la primera aparicion de un producto a partir de una posicion 
def indice_producto(pos_ini = 0):
    size_df = len(df.index)
    
    if(pos_ini < (size_df - 1)):
        for i in range(pos_ini, size_df):
            if df['Productos'][i][0] == '[':
                return i
        return (size_df)
    return -1

# crea el dataframe para un producto específico según su código
def crear_df_producto(producto): 
    pos_ini = pos_fin = count = 0
    
    for i in df.index:
        if(df['Productos'][i] == producto):
            pos_ini = i
            pos_fin = indice_producto(pos_ini+1)
            
    if(pos_fin != -1):
        df_copy = df.iloc[pos_ini+1:pos_fin]
        df_copy = df_copy.rename(columns = {'Productos':'Periodo'})
        
        # reestablecer los indices del dataframe 
        df_copy.reset_index(drop=True, inplace=True)
        
        return df_copy


def get_mes_df(indice):
    fecha = df_prod['Periodo'][indice].split(' ')
    return meses.index(fecha[0])

def get_anio_df(indice):
    fecha = df_prod['Periodo'][indice].split(' ')
    return int(fecha[1])

def calcular_cant_periodos(mes_ini, anio_ini, mes_fin, anio_fin):
    if anio_ini == anio_fin: 
        cant_periodos = mes_fin - mes_ini + 1
    elif anio_fin - anio_ini == 1:
        cant_periodos = 12 - mes_ini + mes_fin + 1
    else:
        cant_periodos = ((anio_fin - anio_ini - 1)*12) + (12 - mes_ini + mes_fin + 1)
        
    return cant_periodos

def completar_df_producto():
    global mes_ini, anio_ini, mes_fin, anio_fin
    global df_prod
    
    mes_ini  = get_mes_df(0)
    anio_ini = get_anio_df(0)
    mes_fin  = get_mes_df(len(df_prod.index)-1)
    anio_fin = get_anio_df(len(df_prod.index)-1)

    cant_periodos = calcular_cant_periodos(mes_ini, anio_ini, mes_fin, anio_fin)


    if (len(df_prod.index) != cant_periodos):

        # se crea un nuevo df vacio
        df_tmp = pd.DataFrame(columns = ['Periodo', 'Total'], index = range(cant_periodos))


        # se completan las fechas para todos los periodos

        it_mes = mes_ini # iteradores para mes y anio en el nuevo df
        it_anio = anio_ini

        it_df_prod = 0 # iterador para periodo en el df original del producto

        # se copian los totales del df_prod en el nuevo df_tmp
        for i in df_tmp.index:

            per = str(meses[it_mes]) + " " + str(it_anio)
            df_tmp['Periodo'][i] = per

            if df_prod['Periodo'][it_df_prod] == per:
                df_tmp['Total'][i] = df_prod['Total'][it_df_prod]
                it_df_prod += 1
            else:
                df_tmp['Total'][i] = 0

            it_mes = (it_mes + 1) % 12
            if it_mes == 0:  # iteracion pasó al siguiente anio
                it_anio += 1

        df_prod = df_tmp
    
    # conversion variables categoricas de período a numericas
    cont = 1
    for i in df_prod.index:
        df_prod['Periodo'][i] = cont
        cont += 1
    df_prod


# PREDICCION con fecha arbitraria
# Entrada: (cod_producto, periodo) . Ej. prediccion('[FURN_7777]','setiembre 2022')
# Salida : (pred) entero con la predicción de pedidos de compra para esa fecha. Ej. 10 (unidades - redondeado)

def periodo_a_valor(periodo):
    arr_periodo = periodo.split(' ')
    mes_pred  = meses.index(arr_periodo[0])
    anio_pred = int(arr_periodo[1])
    
    valor =  calcular_cant_periodos(mes_ini, anio_ini, mes_pred, anio_pred)
    return valor
    
def prediccion(cod_producto, periodo):
    global df_prod, X, y, reg_pred
    df_prod = crear_df_producto(cod_producto)
    completar_df_producto()
    
    # se aplica regresión lineal
    X=df_prod[['Periodo']]
    y=df_prod['Total']
    reg = LinearRegression().fit(X.values, y)
    
    # predicciones para los valores de X, para crear la línea de la grafica
    reg_pred = reg.predict(X.values)
    
    val_periodo = periodo_a_valor(periodo)
    # print(val_periodo)
    pred = int( reg.predict([[val_periodo]]) )
    if pred < 0:
        pred = 0
    return pred


def plotear():
    plt.switch_backend('AGG')
    plt.scatter(X, y, color="black")
    plt.plot(X, reg_pred, color="blue", linewidth=3)
    plt.ylim(0,)
    plt.savefig('static/foo.png')
    plt.close()
    #plt.show()

#prediccion('[FURN_6666]','setiembre 2022')




def separar_codigo_nombre(txt):
    code = txt.split("]")
    code[0] = code[0] + "]"
    code[1] = code[1][1:]
    return code

def get_products():
    products = []
    cont = 0
    for i in lista_productos:
        i = i.strip()
        if i[0] == '[':
            products.append(separar_codigo_nombre(i))
        cont=cont+1
    return products


