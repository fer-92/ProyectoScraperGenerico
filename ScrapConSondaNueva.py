"""
Con este diseño el scrip se debería lanzar de esta manera:
python3 scrap.py 1
python3 scrap.py 2
python3 scrap.py 3
python3 scrap.py 4
python3 scrap.py 5
python3 scrap.py 6
python3 scrap.py 7
python3 scrap.py 8
python3 scrap.py 9
"""
import hashlib
import json
import ast
import requests
from jsonmerge import merge
import sys


def corresponde_procesar_id(k, terminacion_id):
    if k[-1] == terminacion_id:
        return True
    else:
        return False

    """
    :param k:
        es el id del grupo de telegram que que devuelve el json que tiene la sonda llamadao json_sonda2.bin
    :secreto:
        Se fija que terminanción de id_telegram tiene asiganada esta asignada esta instancia correr.
        Este dato se lo pasa como parámettro cuando se ejecuta.
        Por ejemplo: si tiene el parámetro 1 quire decir que el k tiene que terminar en 1 para devolver true,
        caso contrario devuelve false. Ejemplo: si el k es -123456789, termina en 9, etonces devuelve false, porque
        el parámetro es 1.
    :return:
        True or False
    """
def carga_portales(provincia):
    f = open("./LinksDeLasProvincias/"+provincia+".json", "r")
    ff = json.loads(f.read())
    return ff
def formar_json_portales(lista_de_provincias):
    base = None
    result = []
    result2 = {}
    for l in lista_de_provincias:
        #with open("./LinksDeLasProvincias/"+l+".json", "r") as infile:
           # links = infile.read().replace("\n","")
            #result.append(links)
        base = merge(base, carga_portales(l))
        result.extend(base["link"])
    return result
j_link_enviado = {}
j_pag_ne = {}
mugre = ["xmlns=http://www.w3.org/1999/>", "<\n", "\n>", "<<p>", "<p>", "</p", "xmlns=http://www.w3.org/1999/>",
         "xmlns=http://www.w3.org/1999/>", "<br />", "CDATA", "</div>>", "<div>", "</div>", "%>", "<iframe>",
         "</iframe>", "100%", "<div", "http://w3.org/", "xmlms", "xhtml", ";>", "<", ">", "'", '"', "\/", "]", "[",
         "/","-","ttp",":","swww"]

def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m, "")
    return texto
def hashear(l):
    l = l.encode('utf-8')
    h = hashlib.new( "sha1",l)
    return h.hexdigest()
def link_enviado(l):

    print("Telegram analiza este link para enviar ",l)
    l = limpiar(l, mugre)
    l = hashear(l)

    if not l in j_link_enviado.keys():
        print(" Enviando a telegram :", l)
        j_link_enviado[l] = 1
        return False
    else:
        print(" !!!!!!!!!!!!!!! ENCONTRO DUPLICADO !!!!!!!!!!!!!!!!!! ")
        return True
def configuracion():


    f = open("configParametrosGenerico.json", "r")

    global j_config
    j_config = {}
    j_config = json.loads(f.read())
    global vtelegram
    global grupo_telegram_fijo
    grupo_telegram_fijo = j_config["grupo_telegram_fijo"]
    global url_api_sonda
    url_api_sonda = j_config["url_api_sonda"]

    try:
        vtelegram = j_config["telegram"]
    except:
        vtelegram = True
    global token
    token = j_config["token"]
    global idchat
    idchat = j_config["id_chat"]
    global Tema
    Tema = j_config["Tema"]
    global NombreGrupo
    NombreGrupo = j_config["NombreGrupo"]
    global directorio
    directorio = j_config["directorio"]
    try:

        global db_noticias2
        db_noticias2 = {}

        #if os.path.isfile(directorio + 'persist'+nrogrupo+'/db_noticias2.bin'):
            #db_noticias2 = load_persist("db_noticias2")
        #else:
            #db_noticias2 = {}
    except:
        db_noticias2 = {}

    try:
        global LinksDePaginasWeb
        LinksDePaginasWeb = {}
        #if os.path.isfile(directorio + 'persist/LinksDePaginasWeb.bin'):
            #LinksDePaginasWeb = load_persist("LinksDePaginasWeb")
        #else:
            #LinksDePaginasWeb = {}
    except:
        LinksDePaginasWeb = {}
def enviar_noticias(idchat,NombreGrupo,provincias,Tema):
    if not vtelegram:
        pass
        # return
    #filtro_repetida

    try:
        url_api = "bot1294708386:AAHCE0tRcq-hqT_b14UbHaArxs9q4XCj5fs" + "/sendMessage"

        # print( "- tema \n", Tema, " \n ",  NombreGrupo )
        men_t = "✔ Noticias referidas al tema %s, enviadas al grupo de télegram %s: " % (Tema, NombreGrupo) + "\n"
        ta = False
        # recorro el arreglo de links y lo imprimos
        men = []
        # print("arr \n",  arr)
        # print( "men_t \n", men_t )
        for a in provincias:
            # print("3- ",a)
            # men += "- " + a + "\n\n"

            # armo la linea
            l = "- " + a + "\n\n"
            men.append(l)
            if a != "":
                ta = True
        if ta:
            # Si tiene información, mando el título.
            requests.post('https://api.telegram.org/' + url_api, data={'chat_id': idchat, 'text': men_t})
            for m in men:

                # todo Eze, fijate que tuve que poner esta función par que controle no mandar repetidos.
                if not link_enviado(m):

                    requests.post('https://api.telegram.org/' + url_api,
                                  data={'chat_id': idchat, 'text': '\n [' + NombreGrupo + ']\n' + m})
                    print(requests.status_codes)
    except Exception as e:
        print(" 279 - enviar ", e)
def procesar_id(k):
    # obtengo el valor de la sonda para el k
    valor_sonda = datos_sonda[k]
    id_telegram = k
    nombre_grupo = valor_sonda[0]
    tema = valor_sonda[1]
    provincias = valor_sonda[2]
    json_donde_estan_los_portales = formar_json_portales(provincias)
    j = open("./persist/configGenerico.json", "r")

    confiTagPage = {}
    confiTagPage = json.loads(j.read())
    for url in json_donde_estan_los_portales:
        if json_donde_estan_los_portales != "":
            # print( "********************************" )
            print("TEMA:\n\n", tema)
            # print( "********************************" )
            print(" Procesando la url:  ", url)
            r = RSSParser().parse(confiTagPage, url, tema)
            #PagNoticiaLink.save('./Excel/' + urlCortada + '-Noticias.xlsx')
            #if r != []:
            enviar_noticias(id_telegram,nombre_grupo,provincias,tema)
    """
    acá va el programa tal cual está en el main original ahora
    
    """


### main ###

## supongamos que tenemos en memoria estos datos en la sonda
datos_sonda = {
    "-123456789": ("sb_019_Presidente", ["termino1,termino2"], ["BsAs", "Catamarca"]),
    "-123456781": ("sb_010_otro", ["termino1,termino2"], ["Neuquen", "Mendoza"]),
    "-123456782": ("sb_020_otro", ["termino1,termino2"], ["Cordoba", "Catamarca"]),
    "-123456783": ("sb_012_X", ["termino1,termino2"], ["Cordoba", "San_Luis"]),
    "-123456784": ("sb_014_Y", ["termino1,termino2"], ["Tierra_Del_Fuego", "La_Rioja"])
}


def verifico_cambios_en_la_sonda():
    # traigo los datos de las sonda

    url = "http://167.86.120.98:5003/sb_get_sonda2t/"
    url2 = "http://167.86.120.98:5003/sb_get_sonda2j/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    dict1 = {}
    # = requests.get(url, headers=headers).text
    datos_sonda_temp = requests.get(url, headers=headers)
    datos_sonda_temp = ast.literal_eval(datos_sonda_temp.content.decode('utf-8'))
    global datos_sonda
    if datos_sonda != datos_sonda_temp:
        datos_sonda = datos_sonda_temp


if __name__ == '__main__':

    # tomo el primer parámetro que se le pasa al scrip cuando se ejecuta
    # en este caso, es el nro de terminación del id de telegram
    terminacion_id = sys.argv[1]

    # tiene que haber un bucle infinito
    while True:

        verifico_cambios_en_la_sonda()

        for k in datos_sonda:

            if corresponde_procesar_id(k, terminacion_id):
                procesar_id(k)
