# Proyecto Final - DSE
## Integrantes
Jim Leonardo Huertas Canaza

Dennis Pumaraime Espinoza

Solange Aracely Romero Chacón

Luisa Villanueva Guerrero

## Propuesta
La propuesta del trabajo consiste en crear una aplicación que aproveche los datos provenientes de los informes de ventas de productos de Odoo. A ellos se les aplica un modelo de machine learning a fin de predecr la demanda de un producto en específico para un período de tiempo indicado por el usuario.

## Herramientas
**Frotend:** html, css

**Backend:** django

## How To Run
Requisitos:
- python 3.10
- django 4.1
- pip install
    - py -m pip install matplotlib-venn
    - py -m pip install hvplot holoviews
    - py -m pip install seaborn
    - py -m pip install pandas
    - py -m pip install openpyxl
    - py -m pip install sklearn

To Run:
- python manage.py migrate(si es la primera ves que corres el projecto en tu PC)
- python manage.py runserver(dentro de la carpeta dse_odoo)

Another facts:
- Para que funcione correctamente, tienes que cambiar 2 directorios en
    - dse_odoo/settings.py line 58
    - dse_odoo/models/prediction.py line 16 (path a los .xlsx inputs) 

## Prototipo
https://www.figma.com/file/Crinn4ilJwxREZiEF6xmmy/DSE

## Planificación
https://trello.com/invite/b/VJiAQ1sl/987c7ddc59645f62f83a915470bf0798/dse-proyecto
