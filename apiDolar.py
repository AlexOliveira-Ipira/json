import requests 
import json
from flask import Flask , request, jsonify

app = Flask(__name__)

chave = 'Valor absorvido no site HGBrasil, tendo de ser substituida os campos "{chave}" de todas as URLS abaixo'


@app.route('/getdolar', methods = ['GET'])
def get_dolar():
    rDolar = requests.get('https://api.hgbrasil.com/finance?format=json&key={chave}')
    if rDolar.status_code == 200:
        data_dolar = json.loads(rDolar.content)

    dados_real = data_dolar['results']['currencies']
    #dados_dolar = data['results']['currencies']['EUR']

    return jsonify(dados_real)

@app.route('/getacaoh', methods = ['GET'])
def get_acaoh():
    rAcaohigh = requests.get('https://api.hgbrasil.com/finance/stock_price?format=json&key={chave}&symbol=get-high')
    if rAcaohigh.status_code == 200:
        dados_acao_h = json.loads(rAcaohigh.content)  

    acao_high = dados_acao_h['results']
    return jsonify(acao_high)

@app.route('/getacaol', methods = ['GET'])
def get_acaol():
    rAcaolow = requests.get('https://api.hgbrasil.com/finance/stock_price?format=json&key={chave}&symbol=get-low')
    if rAcaolow.status_code == 200:
        dados_acao_l = json.loads(rAcaolow.content)  

    acao_low = dados_acao_l['results']
    return jsonify(acao_low)


if __name__=="__main__":
    app.run(debug=True , port=8880)
