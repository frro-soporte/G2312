from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
from datetime import datetime
import database as dbase  
from bson import ObjectId
from product import Product
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random

db = dbase.dbConnection()

app = Flask(__name__)
#Method get
@app.route('/', methods=['POST', 'GET'])
def get_item():
    if request.method == 'POST':
        item = request.form["it"].lower()
        r = requests.get('https://listado.mercadolibre.com.ar/nuevo/'+item)
        r.status_code

        fecha = str(datetime.now())
        fecha = fecha[:10]

        soup = BeautifulSoup(r.content, 'html.parser')
        titulos = soup.find_all('h2', attrs={"class":"ui-search-item__title"})
        titulos = [i.text for i in titulos]
        urls = soup.find_all('a', attrs={"class":"ui-search-item__group__element ui-search-link"})
        urls = [i.get('href') for i in urls]
        dom = etree.HTML(str(soup))
        precios = dom.xpath('//li[@class="ui-search-layout__item"]//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]//span[@class="andes-money-amount__fraction"]')
        precios = [i.text.replace('.','') for i in precios]
        imgs = soup.find_all('img', attrs={"class": "ui-search-result-image__element"})

        imgs = [i['data-src'] for i in imgs]

        d = [{'Item_buscado': item, 'Titulo': x, 'Precio': y, 'URL': z, 'Fecha': fecha, 'Img': img}
             for x, y, z, img in zip(titulos[:10], precios[:10], urls[:10], imgs[:10])]
        pretty_json = json.dumps(d, sort_keys=True, indent=4)
        collection = db["Grupo12Collection"]

        # Convierte el JSON en un objeto Python
        data = json.loads(pretty_json)

        # Inserta los datos en la colección
        collection.insert_many(data)
        return redirect(url_for("item", product_name=item, search_date=fecha))
    else:
        return render_template('index.html')
    

@app.route("/<product_name>/<search_date>")
def item(product_name, search_date):
    products = db["Grupo12Collection"]
    valores = products.find({"Item_buscado": product_name, "Fecha": search_date})
    acum = 0
    bajo2 = 9999999999999999
    alto2 = 0
    #suma de precios
    for i in valores:
        acum += int(i["Precio"])
        if(int(i["Precio"])< bajo2):
            bajo2 = int(i["Precio"])
        if(int(i["Precio"])> alto2):
            alto2 = int(i["Precio"])
    acumulado = str(int(acum/products.count_documents({"Item_buscado": product_name})))
    minItem = products.find_one({ "$and":[{"Item_buscado": product_name}, {"Precio": str(bajo2)}]})
    maxItem = products.find_one({ "$and":[{"Item_buscado": product_name}, {"Precio": str(alto2)}]})
    return render_template('index2.html', acumulado=acumulado, bajo2=bajo2, alto2=alto2, product_name=product_name.upper(), minItem=minItem, maxItem=maxItem)

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/plot.png/<product_name>')
def plot_png(product_name):
    fig = createGraph(product_name.lower())
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def createGraph(product_name):
    products = db["Grupo12Collection"]
    valores = products.find({"Item_buscado": product_name.lower()}).sort("Fecha")
    fechas=[]
    for i in valores:
        fecha = i["Fecha"]
        if fecha not in fechas:
            fechas.append(fecha)
    proms =[]
    altos=[]
    bajos=[]
    for f in fechas:
        acum = 0
        bajo2 = 99999999999999
        alto2 = 0
        count = 0
        valores = products.find({"Item_buscado": product_name.lower()})
        for i in valores:
            if (f==i["Fecha"]):
                acum += int(i["Precio"])
                count = count+1
                if(int(i["Precio"])< bajo2):
                    bajo2 = int(i["Precio"])
                if(int(i["Precio"])> alto2):
                    alto2 = int(i["Precio"])
        if (count!=0):
            proms.append(acum/count)
            altos.append(alto2)
            bajos.append(bajo2)
        else:
            fechas.remove(f)


    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(fechas, proms, color="green", label="Promedio",marker='o')
    axis.plot(fechas, altos, color="blue", label="Altos",marker='o')
    axis.plot(fechas, bajos, color="red", label="Bajos",marker='o')
    axis.legend()
    return fig


if __name__ == '__main__':
    app.run(debug=True, port=4000)