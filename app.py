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
        props = feature['properties']
        lat = props.get("Latitude")
        lon = props.get("Longitude")

        # Se não houver coordenadas, ignorar
        if lat is None or lon is None:
            continue

        natureza = props.get("Natureza", "Sem natureza")
        estado = props.get("EstadoOcorrencia", "Desconhecido")
        concelho = props.get("Concelho", "")
        freguesia = props.get("Freguesia", "")
        data_inicio = props.get("DataInicioOcorrencia", "")
        operacionais = props.get("Operacionais", 0)
        meios_terrestres = props.get("NumeroMeiosTerrestresEnvolvidos", 0)
        meios_aereos = props.get("NumeroMeiosAereosEnvolvidos", 0)

        descricao = f"""<![CDATA[
        <b>{natureza}</b><br/>
        Estado: {estado}<br/>
        Concelho: {concelho}<br/>
        Freguesia: {freguesia}<br/>
        Data/Hora Início: {data_inicio}<br/>
        Operacionais: {operacionais}<br/>
        Meios Terrestres: {meios_terrestres}<br/>
        Meios Aéreos: {meios_aereos}
        ]]>"""

        pnt = kml.newpoint(name=natureza, coords=[(lon, lat)])
        pnt.description = descricao
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/firedept.png"

    return Response(kml.kml(), mimetype='application/vnd.google-earth.kml+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
