import requests
from requests.structures import CaseInsensitiveDict
import json
import cx_Oracle

"""
Limitações
 # Requisições por minuto.
 # Creditos
---------------------------------------------------------------
Parametros para defininições da consulta
 # MaxAge -- Controla a idade máxima que um dado em cache é aceite, pode ser utilizado em conjunto com as estratégias CACHE_IF_FRESH ou CACHE_IF_ERROR.
  Configure o valor no formato nD, nM ou nY, sendo n variável
    # 17D: Aceita dado em cache se mais recente que 17 dias.
    # 2M:  Aceita dado em cache se mais recente que 2 meses.
    # 1Y:  Aceita dado em cache se mais recente que 1 ano.
 # Strategy -- Determina a estratégia de aquisição do dado, os valores possíveis são:
    # ONLINE:         Consulta a fonte online ignorando qualquer cache. Não recomendado.
    # CACHE_IF_FRESH: Retorna o dado em cache obedecendo à idade máxima fornecida em maxAge, se não, busca na fonte online.
    # CACHE_IF_ERROR: Idem ao CACHE_IF_FRESH, porém se a consulta online falhar, retorna o dado em cache desde que obedeça à idade máxima fornecida em maxStale.
    # CACHE:          Retorna o dado mais recente em cache evitando qualquer consulta online, em caso de inexistência resultará em erro 404.
 #MaxStale -- Na ocasião de uma consulta online falhar, controla a idade máxima que um dado em cache é aceite.
  Pode ser utilizado em conjunto apenas com a estratégia CACHE_IF_ERROR, e também considera o valor de maxAge.
  Configure o valor no mesmo formato de maxAge, o comportamento irá variar de acordo com ambas propriedades. Exemplos:
    # maxAge=17D&maxStale=1M: Retorna do cache se mais recente que 17 dias, se não, consulta online. Em caso de exceção, retorna do cache se mais recente que 1 mês.
    # maxAge=2M&maxStale=1Y: Retorna do cache se mais recente que 2 meses, se não, consulta online. Em caso de exceção, retorna do cache se mais recente que 1 ano.
---------------------------------------------------------------
"""

Url = 'https://api.cnpja.com/'
Key = ''
MaxAge = '1D'
Strategy = 'CACHE_IF_FRESH'
MaxStale = '1M'
limitador = 500
#cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_3")

def fila():
    conn = cx_Oracle.connect('')
    cursor = conn.cursor()
    query  = "" # Consulta no banco
    cursor.execute(query)
    consulta = cursor.fetchall();
    cursor.close()
    conn.close()
    return consulta

def header(Key):
    headers = CaseInsensitiveDict()
    headers["Authorization"] = Key
    return headers

def EndPoint(EndPoint,Identifier,Type):
    if Type  == 1: #  Consulta estabelecimento
        #url = f'{EndPoint}{"office/:"}{Identifier}{"?"}{"strategy="}{Strategy}{"&"}{"maxAge="}{MaxAge}{"&"}{"maxStale="}{MaxStale}'
        url = f'{EndPoint}{"office/:"}{Identifier}{"?"}{"strategy="}{Strategy}{"&"}{"maxAge="}{MaxAge}'
    elif Type == 2 : # Mapa arredores
        url = f'{EndPoint}{"office/:"}{Identifier}{"/map"}{"?width=640&heigth=640&scale=2&zoom=17"}'
    elif Type == 3 : # Visão da Rua
        url = f'{EndPoint}{"office/:"}{Identifier}{"/street"}{"?width=640&heigth=640&fov=90"}'
    elif Type == 4 : #Contribuintes
        url = f'{EndPoint}{"ccc?taxId="}{Identifier}{"&states=BR&status=false&maxAge="}{MaxAge}{"&strategy="}{Strategy}'
    elif Type == 5 : # Creditos restantes
        url = f'{EndPoint}{"me/credit"}'
    elif Type == 6 : # Simples e Mei
        url = f'{EndPoint}{"simples?taxId="}{Identifier}'
    return url

def consultar():
    fila_consulta = fila()
    Header = header(Key)
    for reg in fila_consulta:
        EndPoints = EndPoint(Url,reg[0],1)
        get_estabelecimento = requests.get(EndPoints,headers=Header)
        EndPoints = EndPoint(Url,reg[0],4)
        get_contribuintes = requests.get(EndPoints,headers=Header)
        EndPoints = EndPoint(Url,reg[0],6)
        get_simplesMei = requests.get(EndPoints,headers=Header)
        if get_estabelecimento.status_code and get_contribuintes.status_code == 200:
            #Faz a requisicão
            json_estabelecimento = json.loads(get_estabelecimento.content)
            json_contribuintes   = json.loads(get_contribuintes.content)
            json_simplesMei      = json.loads(get_simplesMei.content)
            #Armazena o Json
            r_estabelecimento    = json.dumps(json_estabelecimento)
            r_contribuintes      = json.dumps(json_contribuintes)
            r_simplesMei         = json.dumps(json_simplesMei)
            #Grava o retorno
            cursor = conn.cursor()
            cursor.callproc('',[reg[1],r_estabelecimento,r_contribuintes,r_simplesMei])
            cursor.close()
        elif get_estabelecimento.status_code  == 400 or get_contribuintes.status_code == 400:
            cursor = conn.cursor()
            cursor.callproc('',[reg[1],"Parâmetro de consulta mal formatado ou faltante"])
            cursor.close()
        elif get_estabelecimento.status_code  == 404 or get_contribuintes.status_code == 404:
            cursor = conn.cursor()
            cursor.callproc('',[reg[1],"CNPJ não registrado na Receita Federal"])
            cursor.close()
        elif get_estabelecimento.status_code  == 429 or get_contribuintes.status_code == 429:
            cursor = conn.cursor()
            cursor.callproc('',[reg[1],"Créditos esgotados ou limite por minuto excedido"])
            cursor.close()
        i = 1
        vRet = i + 1
        if vRet+1 >= limitador:
            break;
        
def consulta_creditos():
    EndPoints = EndPoint(Url,None,5)
    Header = header(Key)
    get_EndPoint = requests.get(EndPoints,headers=Header)
    json_ret = json.loads(get_EndPoint.content)
    creditos   = json_ret['transient']
    creditos_acumulado = json_ret['perpetual']
    cursor = conn.cursor()
    cursor.callproc('',["CNPJA",creditos,creditos_acumulado])
    cursor.close();

consultar()
consulta_creditos()


