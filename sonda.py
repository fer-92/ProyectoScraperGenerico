# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import render_template, request, make_response, redirect
from selenium import webdriver
import datetime
import pickle
import requests
from flask_cors import CORS, cross_origin

#from gestionDialogo import get, post, delete
#from GestionDialogoV2 import gd

import json

import time





chats = {

    'nro':'123456789',
    'chat':[{'p':'Pregunra','r':'Respuesta'}]


}





def getConfig(vdato):  # configuracion.json
    try:
        arch_config = open("./Configuracion/configuracion.json", 'r')
        r = eval(arch_config.read())[vdato]
        return r
    except:
        return "none"


## constantes ---------------------------------------------------------

#vurlapi = getConfig('URLAPI')

vurlapi = "http://167.86.120.98:5002/"

global URLAPI
URLAPI = vurlapi if vurlapi != 'none' else "http://127.0.0.1:5002/"


URLAPI_TG = 'http://chatbot-v2-api.baitsoftware.com/api/'

arr_chat = []

env = {'rta': 'none'}

## -----------------------------------------------------------------------


app = Flask(__name__)
CORS(app)
api = Api(app)

db_pad2 = {}

pad_store = {'key1': 'valor'}

comando = ['none']

arreglo_qr = ['none']

json_pr = {}

json_sonda_x = {
    'idProyecto': '1013',
    'vinit_mode': 'auto',
    'categoria_contactos': 'none',
    'nombrePrueba': 'np1',
    'varchivo_nro_cat': ''
}


###
json_grupo_terminos = {}

json_sonda_sb = {

    "grupo_001":{
    "nombre":"Perotti 2021",
    "telegram":"-000000000001",
    "mail":"unmail@gmail.com",
    "medios":["lacapital","clarin"]
    },
    "grupo_003":{
        "nombre":"Perotti 2021",
        "telegram":"-000000000001",
        "mail":"unmail@gmail.com",
        "medios":["lacapital","clarin"]
    },
    "grupo_004":{
        "nombre":"Perotti 2021",
        "telegram":"-000000000001",
        "mail":"unmail@gmail.com",
        "medios":["lacapital","clarin"]
    }

}

##


json_sonda = {
    'id': '1013',
    'vinit_mode': 'auto',
    'categoria_contactos': 'none',
    'nombrePrueba': 'np1',
    'varchivo_nro_cat': ''
}




TODOS = {
    'init': {'valor': 'init_chat', 'descp': 'Inicia el script de scrap'},
    'menu': {'valor': '0', 'descript': "0=no iniciado 1=cargando contactos 2="},
    'todo3': {'valor': 'valor'},
    'help': {'get': "curl http://localhost:5002/pad  -- curl http://localhost:5002/pad/help",
             'post': "curl http://localhost:5002/todos -d valor=1 -X POST -v",
             'put': "curl http://localhost:5002/todos/d1 -d valor=1 -X PUT -v"},
    'api': {'http://127.0.0.1:5002/IniciarChat/': 'Api de iniciación de conversaciones',
            '/pad/<todo_id>': 'help, api, init, menu',
            '/pad/contactosAiniciar/': 'api que devuelve los nros que inicialiaron el chat', '/pad/getContactos/': '',
            '/addcontact2/<contact>': '', '/addcontact/': ''}
}


contacto_mensaje_manual = {}

contacto_estado = {}

Contactos2 = {'nro': 'estado'}

contactosToAdd = {'a': '12345'}

contacto_estado_manual = {'456':True, '123':False}


@app.route('/pad/analizador222/', methods=['POST', 'GET'])
# lo tengo que llamar con /pad/analizador22/?id=

def analizador222():
    print('*********************************')

    if request.method == 'GET':
        file_name = request.args.get('file_name')
        vformat = request.args.get('format')

        # tomar el contenido del archivo file name
        f = open(file_name, 'r')
        j = f.read()

        print('*********************************')

        return render_template("pivote2.html", json=j, format=vformat)




class waapi(Resource):

    def get(self, json_waapi):
        # tomar el contenido del archivo file name

        j = eval(json_waapi)

        print(j['a'],json_waapi['a'])

        print("1",json_waapi)


        return 200

    def post(self, json_waapi):
        # tomar el contenido del archivo file name
        print("2",json_waapi)
        return 200


class analizador2(Resource):

    def get(self, file_name):
        # tomar el contenido del archivo file name
        f = open(file_name, 'r')
        j = json.load(f)

        return render_template("pivote2.html", json=j)

        # generar in json
        # pasarlor a pivot2.htm


def get2(id, num):
    # devuelve el mensaje correspondiente al id y num

    url = "http://chatbot-gd-api-v2.baitsoftware.com/api/experiences"

    url2 = url + '/' + str(id) + "/messages/" + str(num)

    r = requests.get(url2)

    r2 = r.text.replace('null', '"nulo"')

    try:
        json = eval(r2)

        vcomando = json["data"]

        rr = vcomando['message']

        return rr, vcomando


    except Exception as e:

        return 'error', 'error'


def post2(num, id, message, actor):
    url = "http://chatbot-gd-api-v2.baitsoftware.com/api/DialogMessages"

    vdata = {"numReceptor": num, "idProject": int(id), "message": message, "actor": actor}

    r = requests.post(url, json=vdata)
    print(r)


def delete2(num, id):
    try:

        url = "http://chatbot-gd-api-v2.baitsoftware.com/api/DialogChat"

        url = url + '/' + str(id) + '/' + num

        # vdata = {"numReceptor": num,"idProject": int(id)}

        r = requests.delete(url)

    except Exception as e:
        print(" Exception: ", e)


def getConfig(vdato):  # configuracion.json
    try:
        arch_config = open("./Configuracion/configuracion.json", 'r')
        r = eval(arch_config.read())[vdato]
        return r
    except:
        return "none"


def getComando():
    #
    rr = ""

    try:
        url = URLAPI + "pad/cualquiercosa"
        rr = getApi(url)
    except:
        rr = "error"

    return rr


def buscar_idProyecto(id_experiencia):
    try:

        if len(id_experiencia) < 10:
            return id_experiencia
        else:

            url = URLAPI_TG + 'experiences/' + id_experiencia
            r = getApi(url)
            jr = json.loads(r)

            vidProyecto = jr['data']['projectId']

            return vidProyecto

    except:

        return -1



def getApi(part_url, vgd=None, tipo='exp'):
    # en tipo, si la llamo para una experiencia va exp, si la llamo para el gd va gd
    try:

        if vgd!=None:
            if vgd.get_activa():
                #
                url = vgd.vurl_expe_v2 + "/" +  part_url
                req = vgd.api_gd_call(url,'get')
            else:
                #
                url = vgd.vurl_gd + part_url
                req = requests.get(url)

        else:
            url = part_url

            req = requests.get(url)

        if type(req)==dict:
            return json.dumps(req)
        else:
            return req.text
    except Exception as ee:
        print(ee)
        return 'error'



def getProjectId(id_exp, vgd):
    try:

        #url = 'http://chatbot-v2-api.baitsoftware.com/api/experiences/' + id_exp

        part_url = "experiences/" + id_exp

        r = getApi(part_url, vgd)

        j = json.loads(r)

        c = j['data']['projectId']

        return c
    except Exception as ee:
        print(ee)
        return 0



def comandosonda(key, value):
    if key == "starting":
        # todo: ir  a buscar el id
        vidProyecto = buscar_idProyecto(key)
        json_sonda['idProyecto'] = vidProyecto

    else:
        pass


class setsonda(Resource):

    def put(self, valorsonda):
        global json_sonda

        temp = valorsonda.split(':')

        key = temp[0]
        value = temp[1]

        comandosonda(key, value)

        json_sonda = load_persist('json_sonda')

        json_sonda[key] = value

        save_persist('json_sonda')

        return 201


class sonda(Resource):
    def get(self):
        global json_sonda

        return json_sonda


class dropContactos2(Resource):
    def get(self):
        global Contactos2
        Contactos2 = {}
        save_persist('Contactos2')

        return Contactos2


class initChat(Resource):
    def get(self):

        result = []

        global Contactos2
        Contactos2 = load_persist('Contactos2')

        for r in Contactos2:
            print(r)

            vtopic = Contactos2[r]['topic']

            if vtopic == 'Iniciar':
                Contactos2[r]['topic'] = 'iniciado'

                print('60 > ', r, ' cambiado: ', Contactos2[r])

                result.append(r)

        print("***", Contactos2)
        save_persist('Contactos2')

        return result


def save_persist(elem):
    try:
        vpath = "./persist/"
        vpath = ""
        varchivo = vpath + elem + ".bin"
        with open(varchivo, "bw") as archivo:
            pickle.dump(eval(elem), archivo)
    except Exception as e:
        print("Exp save_persist ", e)


def load_persist(elem, ob=None):
    try:

        vpath = "./persist/"
        vpath = ""
        varchivo = vpath + elem + ".bin"
        print(varchivo)
        with open(varchivo, "br") as archivo:
            # print(pickle.load(archivo))
            return pickle.load(archivo)

    except Exception as e:
        print(e)
        return ob


def getApi2(url):
    print("Entrando a getApi ", url)
    req = requests.get(url)
    return req.text


def setApi(url):
    req = requests.put(url)
    return req.status_code


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()

# parser.add_argument('contact')
parser.add_argument('valor')
parser.add_argument('v2')
parser.add_argument('contact2')
parser.add_argument('vcomando')
parser.add_argument('vcomando2')
parser.add_argument('key_value')
parser.add_argument('valorsonda')
parser.add_argument('luis_value')
parser.add_argument('vexpnro')
parser.add_argument('setvexpnro')
parser.add_argument('vnueva_experiencia')
parser.add_argument('vid_exp')
parser.add_argument('vid_nueva_exp')
parser.add_argument('getsonda_value')
parser.add_argument('file_name')
parser.add_argument('json_waapi')


# Todo
# shows a single todo item and lets you delete a todo item


class getContactos(Resource):
    def get(self, vnro):
        # abort_if_todo_doesnt_exist(vnro)
        vContactos2 = load_persist('Contactos2')
        return vContactos2[vnro]


class listContactos(Resource):
    def get(self):
        # abort_if_todo_doesnt_exist(nro)
        Contactos2 = load_persist('Contactos2')
        return Contactos2


def luis_api_metodo(luis_value):
    vdato = luis_value.split(':')

    vid = vdato[0]
    vpregunta = vdato[1]

    url1 = "https://raw.githubusercontent.com/Funpei/chatBot/master/IA/pr" + vid + ".json"
    r = getApi(url1)

    json_pr = eval(r)

    global json_sonda

    json_sonda = load_persist('json_sonda', json_sonda)

    url = eval(json_sonda['luis'])[vid]
    url += '=' + vpregunta

    result = getApi(url)

    jr = eval(result)

    jr1 = (jr['topScoringIntent'])

    vcategoria = jr1['intent']

    # vmax = jr1['score']

    vrespuesta = json_pr[vcategoria]

    print("log 219", vrespuesta)

    return vrespuesta


class luis_api(Resource):
    def get(self, luis_value):
        vdato = luis_value.split(':')

        vid = vdato[0]
        vpregunta = vdato[1]

        url1 = "https://raw.githubusercontent.com/Funpei/chatBot/master/IA/pr" + vid + ".json"
        r = getApi(url1)

        json_pr = eval(r)

        json_sonda = load_persist('json_sonda')

        url = eval(json_sonda['luis'])[vid]
        url += '=' + vpregunta

        result = getApi(url)

        jr = eval(result)

        jr1 = (jr['topScoringIntent'])

        vcategoria = jr1['intent']

        # vmax = jr1['score']

        vrespuesta = json_pr[vcategoria]

        print("log 219", vrespuesta)

        return vrespuesta


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        # task = {'valor': args['valor']}
        task = {'valor': todo_id}
        print(task, todo_id)
        TODOS[todo_id] = task
        print(TODOS)
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'valor': args['valor']}
        return TODOS[todo_id], 201


class AddContact(Resource):
    def post(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()
        vcontact = args['contact']
        contactosToAdd[vcontact] = datetime.datetime.now()
        return 201

    def put(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()
        vcontact = args['contact']
        contactosToAdd[vcontact] = datetime.datetime.now()
        return 201

    def get(self):
        return contactosToAdd


class ContactAdd(Resource):

    def get(self):
        print("** pasando por get")
        return contactosToAdd

    def post(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()
        vcontact = args['contact']
        contactosToAdd[vcontact] = datetime.datetime.now()
        print(" _____________ ", vcontact, "  ", contactosToAdd[vcontact])
        return 201

    def put(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()

        vvalor = args['valor']

        votro = args['v2']

        print(" _____________ ", contact, ' ', vvalor, ' ', votro)
        contactosToAdd[contact] = vvalor

        print(" _____________ ", contact, "  ", contactosToAdd[contact])

        return 201


# -----------------------------------------------

class command(Resource):

    def get(self, vcomando):
        print("**")
        return comando[0].strip()

    def put(self, vcomando):
        args = parser.parse_args()

        comando[0] = vcomando

        save_persist('comando')

        return 201


class command2(Resource):

    def put(self, vcomando2):
        temp = vcomando2.split(':')

        t1 = temp[0]
        t2 = temp[1]

        return 201


def getdb_contact(vidProyecto):
    db_pad2 = load_persist('db_pad2')

    key = 'exp_' + vidProyecto

    j1 = []

    j1 = db_pad2[key]

    arr_contacts = j1['contact']

    return arr_contacts


db_expriencias = {}


class nueva_experiencia(Resource):  # devuelven los contactos que hay en la db_pad2

    def put(self, vid_nueva_exp):
        try:
            try:
                db_pad2 = load_persist('vid_nueva_exp')
            except:
                pass

            key = vid_nueva_exp.split(',')[0]
            value = vid_nueva_exp.split(',')[1]

            db_expriencias[key] = value

            save_persist('db_expriencias')

        except:
            pass


class viewexp(Resource):  # devuelven los contactos que hay en la db_pad2
    def get(self, vid_exp):
        try:

            url1 = 'http://chatbot-v2-api.baitsoftware.com/api/experiences/' + vid_exp

            r = getApi(url1)

            jr = json.loads(r)

            c = jr['data']['conversation']['dialogUnits']

            ll = ""
            arr = []
            i = 0
            j = {}

            for cc in c:

                for ccc in cc['dialogMessages']:
                    i += 1
                    l = '{:<30}'.format(ccc['category']) + " - " + '{:<60}'.format(
                        ccc['message']) + " - " + '{:<30}'.format(ccc['nextDialog'])
                    j[i] = l
                    ll += l
                    arr.append(l)

            j = {'1': '11', '2': '21', '3': '31', '4': '41'}
            j = 'hola'
            print(j)

            return render_template("vexp.html", result=j)



        except Exception as e:
            print("Excepción en viewconversa")
            return 'none'


@app.route('/pad/viewexp2/', methods=['GET'])
def viewexp2():  # devuelven los contactos que hay en la db_pad2
    if request.method == 'GET':
        try:
            vid_exp = request.args.get('id')

            url1 = 'http://chatbot-v2-api.baitsoftware.com/api/experiences/' + vid_exp

            r = getApi(url1)

            jr = json.loads(r)

            c = jr['data']['conversation']['dialogUnits']

            ll = ""
            arr = []
            i = 0
            ii = 0
            j = {}
            jj = {}
            jjj = {}

            for cc in c:
                ii += 1
                i = 0
                j = {}

                ud = cc['alias']

                for ccc in cc['dialogMessages']:
                    i += 1
                    jj = {}
                    jj['alias'] = ud
                    jj['cat'] = ccc['category']
                    jj['men'] = ccc['message']
                    jj['proximo'] = ccc['nextDialog']

                    j[str(i)] = jj

                jjj[str(ii)] = j

            print(jjj)

            # jjj='none'

            return render_template("vexp.html", result=jjj)



        except Exception as e:
            print("Excepción en viewconversa   ", e)
            return 'none'


class getdb_contact_sonda(Resource):  # devuelven los contactos que hay en la db_pad2
    def get(self, vexpnro):
        try:
            db_pad2 = load_persist('db_pad2')

            key = 'exp_' + vexpnro

            j1 = []

            j1 = db_pad2[key]

            # arr_contacts = j1['contact']

            return j1

        except:
            return 'none'

    def put(self, vexpnro):
        try:
            db_pad2 = load_persist('db_pad2')

            if type(getsonda_value) == dict:
                for key in getsonda_value:
                    k = key
                    v = getsonda_value[k]
            else:
                temp = getsonda_value.split(':')

                k = temp[0]
                v = eval(temp[1])

            db_pad2[k] = v

            save_persist('db_pad2')


        except:
            return 'none'


class getsonda(Resource):
    def get(self, getsonda_value):
        try:
            json_sonda = load_persist('json_sonda')
            return json_sonda[getsonda_value]
        except:
            return 'none'


class store(Resource):

    def get(self, key_value):

        try:
            return pad_store[key_value]
        except:
            return "error"

    def put(self, key_value):

        dato = key_value

        dato1 = dato.split(':')

        if dato1[0] == 'qr':
            arreglo_qr[0] = dato1[1]
        else:
            pad_store[dato1[0]] = dato1[1]

        arreglo_qr[0] = dato1[1]

        save_persist('pad_store')

        return 201


# api 1 -
class apiContactos(Resource):

    def get(self):
        print("** pasando por get")
        return contactosToAdd

    def post(self, contact2):
        print(" **  post IniciarChat")
        args = parser.parse_args()
        vcontact = args['contact2']

        global Contactos2
        Contactos2[vcontact['nro']] = eval(contact2)

        return 201

    def put(self, contact2):
        print(" **  put IniciarChat")
        args = parser.parse_args()

        vjson = eval(contact2)

        # vcontact = args['contact2']

        global Contactos2

        Contactos2 = load_persist('Contactos2')

        Contactos2[vjson['nro']] = vjson

        save_persist('Contactos2')

        return 201


# api 2 -
class ContactGet(Resource):

    def get(self):
        print("** pasando por get")
        return contactosToAdd


###################################################
# Apis Apis
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/pad')  # curl http://localhost:5002/todos
api.add_resource(Todo, '/pad/<todo_id>')  # cu0/todos/todo3

# api.add_resource(Contactos, '/pad/getContacto/<vnro>') # Contactos2

# api.add_resource(contactosAiniciar,'/pad/contactosAiniciar/') # Contactos2

# api.add_resource(Contactos, '/pad/setContacto/<vnro>') # Contactos2

# api.add_resource(ContactosTodos, '/pad/getContactos/') #  Contactos2

api.add_resource(ContactAdd, '/addcontact2/<contact>')  # cu0/todos/todo3

api.add_resource(ContactGet, '/addcontact/')  # cu0/todos/todo3

## api para pad2 ###################################################
api.add_resource(apiContactos,
                 '/pad/apiContactos/<contact2>')  # put, post para agregar contentido a Contactos2. Ej: {'nro':'1111,'name':'Ale','topic':'Iniciar'}

api.add_resource(getContactos, '/pad/getContacto/<vnro>')  # Muestra el valor que tiene Contactos[vnro]

api.add_resource(listContactos,
                 '/pad/listContactos/')  # Devuelve Contactos2. Es listado completo de todos los contactos
api.add_resource(initChat, '/pad/initChat/')  # devuelve los nros de contacto que deben ser iniciados
api.add_resource(dropContactos2, '/pad/dropContactos2/') #borra el arreglo que contiene los contactos
api.add_resource(command, '/pad/command/<vcomando>') # no se usa
api.add_resource(command2, '/pad/command2/<vcomando2>') # no se usa
api.add_resource(sonda, '/pad/sonda/')# Muesta todos los valores que tiene guardado la SONDA
api.add_resource(setsonda, '/pad/setsonda/<valorsonda>')  #ingrea un valor a la Sonda. valorsonda = key:valor
api.add_resource(getsonda, '/pad/getsonda/<getsonda_value>') #devuelve el valor que tiene almacenado la sonda para la clave del dict referenciada en getsonda_value
api.add_resource(store, '/pad/store/<key_value>')# guarda datos en la Sonsa, hace lo mismo que setsonda
api.add_resource(luis_api, '/pad/luis_api/<luis_value>') # se usaba para tomar el link de la IA de LUIS MICROSOFT
api.add_resource(getdb_contact_sonda, '/pad/getdb_contact_sonda/<vexpnro>')# no se usa
api.add_resource(viewexp, '/pad/viewexp/<vid_exp>')# devuelve la experiencia (o el nombre de la experiencia) del idproject
api.add_resource(nueva_experiencia, '/pad/nueva_experiencia/<vid_nueva_exp>') # ver que hace
api.add_resource(analizador2, '/pad/analizador2/<file_name>')# Ejecuta el probador de una experiencia. File_name puede ser el idproject o nombre de una exp.
api.add_resource(waapi, '/waapi/<json_waapi>') # ver que hace
#####################################################################



@app.route("/hello1")
def hello1():
    return "Hello World para /hello1!"



# se utiliza para hacer los post y get al DG desde el probador que tiene la vista en: chatprove.html
@app.route("/pad/chatprove2/", methods=['POST', 'GET'])
def chatprove2():
    tel = 1010

    if request.method == 'GET':

        vid_exp = request.args.get('id')
        texto = request.args.get('texto')

        idProject = buscar_idProyecto(vid_exp)

        if texto == None or texto == "" or texto.replace('""', '') == '':
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            global arr_chat
            arr_chat = []
            arr_chat = ["*" + rta]
            env['rta'] = rta
            return render_template("chatprove.html", result=arr_chat, id_exp=vid_exp)


    if request.method == 'POST':

        result = request.form

        vid_exp = result['id_exp']
        vtexto = result['texto']

        idProject = buscar_idProyecto(vid_exp)

        if vtexto == "reiniciar":
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove.html", result=arr_chat, id_exp=vid_exp)

    # hacer post

    # post1  - todo: mando ultima pregunta

    arr_chat.append("................ " + vtexto)
    # arr_chat.append("*"+  rta)

    rta = env['rta']
    post(tel, idProject, rta, "s")

    # post2 - todo: mando respuesta del contacto

    respuesta_contacto = vtexto
    post(tel, idProject, respuesta_contacto, "c")

    # get - todo: obtengo respuesta del DG
    r = get(idProject, tel)
    rta = r[0]

    r1 = rta

    arr_chat.append("**" + rta)

    # mando al GD el mensaje de la regla
    post(tel, idProject, rta, "s")

    # Obtengo del GD el mensaje de la regla siguiente
    r = get(idProject, tel)
    rta = r[0]

    if rta != r1:
        arr_chat.append("*" + rta)
        arr_chat.append(".")

    env['rta'] = rta

    return render_template("chatprove.html", result=arr_chat, id_exp=vid_exp)

# todo todo todo - Este era el probador anterior con las API viejas del GD
@app.route("/pad/anterior_chatprove/", methods=['POST', 'GET'])
def anterior_chatprove_public():
    if request.method == 'GET':

        vid_exp = request.args.get('id')
        texto = request.args.get('texto')
        vnro = request.args.get('nro')

        if vnro == None:
            tiempo = str(time.time())[-4:]
            tel = int(tiempo)
        else:
            tel = int(vnro)

        idProject = buscar_idProyecto(vid_exp)

        if texto == None or texto == "" or texto.replace('""', '') == '':
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            global arr_chat
            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)

    if request.method == 'POST':

        result = request.form

        vid_exp = result['id_exp']
        vtexto = result['texto']
        tel = int(result['nro'])

        idProject = buscar_idProyecto(vid_exp)

        if vtexto == "reiniciar":
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)

        # hacer post

        # post1  - todo: mando ultima pregunta

        if len(vtexto.split()) > 1:
            temp = intention(vtexto)

            if temp != vtexto:
                vtexto = '[' + temp + ']'
            else:
                vtexto = temp

        arr_chat.append(vtexto)
        # arr_chat.append("*"+  rta)

        rta = env['rta']
        post(tel, idProject, rta, "s")

        # post2 - todo: mando respuesta del contacto

        respuesta_contacto = vtexto
        post(tel, idProject, respuesta_contacto, "c")

        # get - todo: obtengo respuesta del DG
        r = get(idProject, tel)
        rta = r[0]

        r1 = rta

        arr_chat.append("**" + rta.ljust(30, ' '))

        # mando al GD el mensaje de la regla
        post(tel, idProject, rta, "s")

        # Obtengo del GD el mensaje de la regla siguiente
        r = get(idProject, tel)
        rta = r[0]

        if rta != r1:
            arr_chat.append("*" + rta.ljust(30, ' '))
            # arr_chat.append(".")

        env['rta'] = rta

        return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)



## intervención manual 1
@app.route("/set_contacto_estado2/", methods=['GET'])
def set_contacto_estado2():
    try:

        dato = request.args.get( 'estado' ).split( ":" )
        contacto = dato[0]
        estado = dato[1]

        contacto_estado[contacto]=estado

        return jsonify(result='ok'),200



    except Exception as e:
        print("Except 1166 ",e)
        return jsonify(result='error'), 400



## intervención manual 2
@app.route("/set_contacto_mensaje_manual/", methods=['GET'])
def set_contacto_mensaje_manual():

    try:

        dato  = request.args.get( 'dato').split(":")

        contacto = dato[0]
        mensaje =  dato[1]


        contacto_mensaje_manual[contacto] = mensaje


        return jsonify(result='ok'),200
    except Exception as e:
        return jsonify(result='error'), 400


## intervención manual 3
## Devuelve True si está en modo manual
@app.route("/get_contacto_mensaje_manual/", methods=['GET'])
def get_contacto_mensaje_manual():

    try:

        vcontacto  = request.args.get( 'contacto')


        if vcontacto in contacto_mensaje_manual.keys():
            r = contacto_mensaje_manual[vcontacto]
        else:
            r = ""


        return jsonify(result=r),200
    except Exception as e:
        return jsonify(result=""), 400

## intervención manual 4
@app.route("/get_modo_manual/", methods=['GET'])
def get_modo_auto():

    try:

        vcontacto  = request.args.get( 'contacto')


        if vcontacto in contacto_estado_manual.keys():
            r = contacto_estado_manual[vcontacto]
        else:
            r = False


        return jsonify(result=r),200
    except Exception as e:
        return jsonify(result=False), 400








## intervención manual 5
@app.route("/modo_manual/", methods=['GET'])
def modo_auto():


    vmodo = "auto"
    vcontacto = "123456789"

    try:

        param = request.args.get('comando')

        valor = param.split(",")

        for v in valor:
            vv = v.split(':')

            if vv[0] == 'modo':
                vmodo = vv[1]

            if vv[0] == 'contacto':
                vcontacto = vv[1]

            if vv[0] == 'mensaje':
                vmensaje = vv[1]


        ###
        # Si el contacto no está chateando con esta SC entonces no tiene
        # que hacer nada
        ##

        if vcontacto in contacto_estado.keys():
            if contacto_estado[vcontacto] != "STOP":

                if vmodo == 'manual':
                    contacto_estado_manual[vcontacto] = True

                    ## aquí se guarda el mansaje que se tiene que devolver de forma manual
                    contacto_mensaje_manual[vcontacto] = vmensaje
                else:
                    contacto_estado_manual[vcontacto] = False
                    contacto_mensaje_manual[vcontacto] = ""

                return jsonify(result=True),200

            else:
                # no está chateando porque está en stop
                return jsonify(result=False), 200
        else:
            # no está en el contacto_estado_manual
            return jsonify(result=False), 200

    except Exception as e:
        print("Except 1180 ", e)
        return jsonify(result=False),400







# todo todo  todo v2chatprove - Provador con la versión2 de las API del GD
@app.route("/pad/chatprove/", methods=['POST', 'GET'])
def chatprove_public():
    global vgd

    if request.method == 'GET':

        vid_exp = request.args.get('id')
        texto = request.args.get('texto')
        vnro = request.args.get('nro')

        if vnro == None:
            tiempo = str(time.time())[-4:]
            tel = int(tiempo)
        else:
            tel = int(vnro)

        idProject = getProjectId(vid_exp, vgd)

        if texto == None or texto == "" or texto.replace('""', '') == '':
            delete(str(tel), idProject,vgd)

            r = get(idProject, tel, vgd)

            rta = r[0]

            global arr_chat
            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)

    if request.method == 'POST':

        result = request.form

        vid_exp = result['id_exp']
        vtexto = result['texto']
        tel = int(result['nro'])

        #idProject = buscar_idProyecto(vid_exp)


        idProject = getProjectId(vid_exp, vgd)

        if vtexto == "reiniciar":
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)

        # hacer post

        # post1  - todo: mando ultima pregunta

        if len(vtexto.split()) > 1:
            #temp = intention(vtexto)

            temp = vtexto

            if temp != vtexto:
                vtexto = '[' + temp + ']'
            else:
                vtexto = temp

        arr_chat.append(vtexto)
        # arr_chat.append("*"+  rta)

        rta = env['rta']
        post(tel, idProject, rta, "s", vgd)

        # post2 - todo: mando respuesta del contacto

        respuesta_contacto = vtexto
        post(tel, idProject, respuesta_contacto, "c", vgd)

        # get - todo: obtengo respuesta del DG
        r = get(idProject, tel, vgd)
        rta = r[0]

        r1 = rta

        arr_chat.append("**" + rta.ljust(30, ' '))

        # mando al GD el mensaje de la regla
        post(tel, idProject, rta, "s", vgd)

        # Obtengo del GD el mensaje de la regla siguiente
        r = get(idProject, tel, vgd)
        rta = r[0]

        if rta != r1:
            arr_chat.append("*" + rta.ljust(30, ' '))
            # arr_chat.append(".")

        env['rta'] = rta

        return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)



@app.route("/luis2", methods=['POST', 'GET'])
def luis2():
    if request.method == 'POST' or request.method == 'GET':

        try:

            url = URL_API + "pad/luis_api/"

            result = request.form

            vidp10 = result['nroexperiencia']
            vpregunta = result['vdato']

            url += vidp10 + ":" + vpregunta

            print("en luis2 getApi() : ", url)

            print(" luis_metodo ", luis_api_metodo(vidp10 + ":" + vpregunta))

            vrespuesta = luis_api_metodo(vidp10 + ":" + vpregunta)

            # vrespuesta = getApi(url).strip().replace('"','')

            rr = [vrespuesta, 0]
        except:
            rr = ["No hay respuesta", 0]

    return render_template("luis.html", result=rr)


# Muestra el contenido de la Sando en sonda.html
# Esta página se muestra cuando es invocada desde el menú de la sonda a travésd el link ABM Sonda.
@app.route("/abmsonda1/")
def abmsonda():
    global json_grupo_terminos
    json_grupo_terminos = load_persist('json_grupo_terminos')


    return render_template("sonda.html", result=json_grupo_terminos)


# Menú general de la sonda
@app.route("/")
def index():
    return render_template("index.html")


# student - esto está de pruena no se usa.
# se puede sacar.
@app.route('/student/')
def student():
    return render_template('student.html')


# resultado2 es llamado dede la página anterior: student.html
# se puede sacar
@app.route('/result2', methods=['POST', 'GET'])
def result2():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


# resultado2 es llamado dede la página anterior: student.html
# se puede sacar
@app.route('/List_nroEstados', methods=['POST', 'GET'])
def List_nroEstados():
    url = 'http://localhost:5002' + '/pad/contactosAiniciar/'

    # result1 = getApi(url)

    global Contactos2
    Contactos2 = load_persist('Contactos2')

    return render_template("List_nroEstados.html", result=Contactos2)


# función auxiliar para guardar un valor
# ver si se usa
def pad_store(valor):
    try:
        if valor == 'qr':
            return arreglo_qr[0]
        else:

            return pad_store[valor]
    except:
        return "error"



# devuelve el qr curado y lo guarda en pad_store
@app.route('/getqr_api', methods=['POST', 'GET'])
def getqr_api():
    if request.method == 'GET':
        qr = pad_store('qr').replace('--', ':').replace('*', '/').replace('"', '')

        # print(" 613 ",qr)

        return qr


# muestra el qr en lapágina qr2.html
@app.route('/getqr', methods=['POST', 'GET'])
def getqr():
    if request.method == 'GET':

        if json_sonda['vinit_mode'] == 'getqr_experience':

            url = URLAPI + "pad/store/qr"

            # url = url.replace('--',':')
            # qr = getApi(url).replace('--',':').replace('*','/').replace('"','')

            qr = pad_store('qr').replace('--', ':').replace('*', '/').replace('"', '')

            if qr == 'none':
                qr = 'https://cdn.shopify.com/growth-tools-assets/qr-code/shopify-faae7065b7b351d28495b345ed76096c03de28bac346deb1e85db632862fd0e4.png'

            # print(" 613 ",qr)
        else:

            qr = 'https://store-images.s-microsoft.com/image/apps.15933.14374624288247235.7037ab92-5a5a-4529-b5af-025b76357642.493a34ee-eb48-40a5-b536-c3f141dce92a?mode=scale&q=90&h=300&w=300'

        return render_template("qr2.html", result=qr)



# Ver si se está usando
@app.route('/analizador', methods=['POST', 'GET'])
def analizador():
    if request.method == 'GET':
        return render_template("vista.html")



# api para guardar datos en la sonda desde la vista sonda.html
@app.route('/putsonda11', methods=['POST', 'GET', 'PUT'])
def putsonda11():
    if request.method == 'POST':
        result = request.form

        key = result['key']
        valor = result['valor']

        global json_sonda


        json_sonda = load_persist('json_sonda')

        json_sonda[key] = valor

        save_persist('json_sonda')

        print(json_sonda)

        return render_template("sonda.html", result=json_sonda)

    if request.method == 'PUT':
        result = str(request.data).replace("b'", '').replace('\\', '')[:-1].split(':')

        key = result[0]
        valor = result[1]

        json_sonda = load_persist('json_sonda')

        json_sonda[key] = valor

        save_persist('json_sonda')

        return ""


# ver si se usa
@app.route('/lanzamiento_init', methods=['POST', 'GET'])
def lanzamiento_init():
    if request.method == 'POST':
        result = request.form

        nombre_contacto = result['nombre_contacto']
        idProyecto = result['idProyecto']
        categorias = result['categorias']
        accion = result['accion']
        nombre_prueba = result['nombre_prueba']

        # global json_sonda

        json_sonda['idProyecto'] = idProyecto
        json_sonda['vinit_mode'] = accion
        json_sonda['varchivo_nro_cat'] = nombre_contacto
        json_sonda['nombrePrueba'] = nombre_prueba
        json_sonda['categoria_contactos'] = categorias

        setApi(URL_API + "pad/command/" + accion)

        save_persist('json_sonda')

        print(json_sonda)

        return render_template("index.html")


# se usaba  para debug y test de la api oficial
# ahora no se usa más
@app.route('/wa_iniciar', methods=['POST', 'GET'])
def wa_iniciar():
    if request.method == 'POST':
        result = request.form
        print("Result: ", result['nro'])

        vnro = result['nro']
        vtema = result['tema']
        vnombre = result['nombre']
        vcomentario = result['comentario']

        vinit = {'nro': vnro, 'name': vnombre, 'topic': vtema, 'comment': vcomentario}

        global Contactos2
        Contactos2 = load_persist('Contactos2')

        Contactos2[vnro] = vinit

        save_persist('Contactos2')

        print(Contactos2)

        vurl = "https://wa.me/5492473466788?text=" + vinit['nro']

        print(vurl)

        return render_template("waIniciado.html")


# API para agregar contacto desde la vista lanzamiento.html
@app.route('/cargarcontactos2', methods=['PUT', 'POST', 'GET'])
def cargar_contactos2():
    if request.method == 'POST':
        result = request.form

        vidProyecto = result['vidProyecto']
        vexp_contactos = result['expcontactos']

        global db_pad2
        db_pad2 = load_persist('db_pad2')

        # if es_formato correcto

        db_pad2["exp_" + vidProyecto] = eval(vexp_contactos)

        save_persist('db_pad2')

        return render_template("lanzamiento.html")

    if request.method == 'PUT':  # and request.headers['Content-Type'] == 'application/json':

        temp = str(request.data).replace("b'", "").replace('\\', '')[:-1]
        j = eval(temp)

        # ----------------------------
        for i in j.keys():
            k = i
        key = k
        value = j[k]
        # -----------------------------

        try:

            # global db_pad2
            db_pad2 = load_persist('db_pad2')

            db_pad2["exp_" + key] = value

            save_persist('db_pad2')

            return "200"

        except:

            return "500 DB read-only"

# abre la vista lanzamiento
@app.route('/admincontactos/')
def lanzamiento():
    # show the user profile for that user
    # todo - acá tengo que que persistir para que desde pad2 lo capte
    return render_template("lanzamiento.html")


# abre la vista sonda.html
@app.route('/putsonda1/')
def putsonda1():
    # show the user profile for that user

    # todo - acá tengo que que persistir para que desde pad2 lo capte

    return render_template("sonda.html")


# no se usa
@app.route('/wa/')
def wa():
    # show the user profile for that user

    # todo - acá tengo que que persistir para que desde pad2 lo capte

    return render_template("wa.html")


# no se usa
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

# no se usa
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    p = post_id + 100
    return 'Post %d' % p


# no se usa
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# no se usa
@app.route('/result')
def result():
    dict = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('result.html', result=dict)

# no se usa
@app.route('/index3')
def inde3():
    return render_template('index2.html')

# no se usa
@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)

    return resp



# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
## intervención manual 1
@app.route("/sb_update_telegram/", methods=['GET'])
def set_contacto_estado():
    try:

        dato = request.args.get( 'param' ).split( ":" )
        grupo_telegram = dato[0]
        terminos_busquedas = dato[1].split(",")

        json_grupo_terminos[grupo_telegram]=terminos_busquedas
        print(json_grupo_terminos)

        # persistir grupo_telegram
        save_persist("json_grupo_terminos")


        return jsonify(result=json_grupo_terminos),200

    except Exception as e:
        print("Except 1166 ",e)
        return jsonify(result='error'), 400


@app.route("/sb_get_tema/", methods=['GET'])
def sb_get_tema():
    try:

        grupo_telegram = request.args.get( 'grupo' )

        if grupo_telegram == "*":
            r = json_grupo_terminos
        else:
            r =  json_grupo_terminos[grupo_telegram]
        #print(r)
        return str(r),200

    except Exception as e:
        print("Except 1166 ",e)
        return "error", 400




@app.route("/sb_get_sonda2t/", methods=['GET'])
def sb_get_sonda2t():
    try:

        r = json_grupo_terminos
        return str(r),200

    except Exception as e:
        print("Except 1166 ",e)
        return "error", 400


@app.route("/sb_get_sonda2j/", methods=['GET'])
def sb_get_sonda2j():
    try:
        r = jsonify(json_grupo_terminos)
        return str(r),200

    except Exception as e:
        print("Except 1166 ",e)
        return "error", 400



# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------


def init():
    global json_grupo_terminos
    json_grupo_terminos = load_persist("json_grupo_terminos")
    print(json_grupo_terminos)

init()


global vgd
vf = True

#vgd = gd(vf)  # i pass a value True if i want use api v2

# loguear

#vgd.params_gd_log = {"Email": "pad2funpei@gmail.com", "Password": "Wsf.2018"}
#vgd.api_gd_login('login')


if __name__ == '__main__':

    #app.run(debug=True)
    print(URLAPI[7:-6])
    app.run(host='0.0.0.0', port=5002)
