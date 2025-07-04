from flask import Flask, Response
import requests
import simplekml

app = Flask(__name__)

@app.route('/')
def gerar_kml():
    url = "https://prociv-agserver.geomai.mai.gov.pt/arcgis/rest/services/Ocorrencias_Base/FeatureServer/0/query"
    params = {
        "f": "geojson",
        "where": "0=0",
        "outFields": "*"
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    kml = simplekml.Kml()

    for feature in data['features']:
        coords = feature['geometry']['coordinates']
        props = feature['properties']
        nome = props.get("NOME", "Sem nome")
        tipo = props.get("TIPO", "Desconhecido")
        datahora = props.get("DATA_HORA_ALERTA", "")
        descricao = f"Tipo: {tipo}\nData/Hora: {datahora}"

        pnt = kml.newpoint(name=nome, coords=[(coords[0], coords[1])])
        pnt.description = descricao
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/firedept.png"

    return Response(kml.kml(), mimetype='application/vnd.google-earth.kml+xml')
