from textblob import TextBlob
from elastic import els
from mi_time import mi_time
from translators import translator
import random
import datetime
from datetime import datetime
mugre = ["rdquo;","&amp;","&gt",".ar",".com",";>>",";>","<br","&quot;","xmlns=http://www.w3.org/1999/>","<\n", "\n>","<<p>","<p>","</p","xmlns=http://www.w3.org/1999/>","xmlns=http://www.w3.org/1999/>","<br />","CDATA", "</div>>", "<div>", "</div>","%>", "<iframe>", "</iframe>", "100%", "<div", "http://w3.org/","xmlms","xhtml", ";>","]",'"',"'"]
from db2 import db2


# ---
# funciones auxiliares

vels = els()
vdb2 = db2()


def sentimiento(texto):


    # Realizar el análisis de sentimiento de los tweets descargados
    # Crear las listas de polaridad polarity_list y frecuencia de polaridad numbers_list    polarity_list = []

    negativo = 0
    positivo = 0
    t = ""

    for tweet in texto.split(" "):

        tweet = limpiar( tweet, mugre )
        c ="DATA" in tweet.upper() or "http" in tweet or "html" in tweet or "%" in tweet or '#' in tweet or "=" in tweet or len(tweet) < 5



        if not c:
            t += " " + tweet


    text = TextBlob( t )
    #text_traducido = str(text.translate( to='en' ))

    text_traducido = translator.translate( t )

    analysis = TextBlob( (text_traducido) )
    #analysis = TextBlob( tweet )

    analysis = analysis.sentiment
    # Guardar la polaridad
    polarity = analysis.polarity


    if polarity < 0:
        return -1

    if polarity > 0:
        return  1

    if polarity ==  0:
        return 0



def json2sql_q(j):

    campos = ""
    valores = ""

    for e in j.keys():
        campos += e + ","

        if type(j[e]) == int:
            valores += str(j[e]) + ","
        else:
            valores += "'" + j[e] + "'" + ","

    campos = campos[:-1]
    valores = valores[:-1]

    return campos, valores




def fgeolocation2():
    f = open( "geolocaciones.csv" )
    arr = []

    for l in f:
        ll = l.split( "," )
        lan = ll[6]
        lon = ll[7]

        arr.append( lan + "," + lon )

    rr = random.choice( arr )
    return rr

def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m,"")
    return texto



def multiple_replace(texto, lista):
    try:

        for e in lista:
            texto = texto.replace(e,"")
        return texto

    except Exception:
        return texto
# --


#####
##########################################################
#####


class store:


    def store(titulo, fecha, texto, link, medio, grupo):


        # grabar en elastic y mysql
        store.add2elastic(titulo,fecha,link,texto, medio, grupo)

        # grabar en elastic para la nube
        store.add2els_nube(texto, fecha, medio, grupo )


    def add2elastic(titulo, fecha, link, texto, medio, grupo = ""):
        # graba los datos en elastic de contabo 98
        # si no exite o es falso
        try:
            # todo: hay que encodear todo bien para que no guarde basura.

            titulo = multiple_replace(titulo, "'[]<>!*,\@" ).replace( '"', '' )
            titulo = limpiar( titulo, mugre )

            link = multiple_replace(link[:200], "'[]<>!*,\@" ).replace( '"', '' )
            #
            # desc = multiple_replace(j_i['desc']  ,"'[]<>!*,\@").replace('"','')

            ddd = multiple_replace(texto, "'[]!*,\@" ).replace( '"', '' )
            # desc = str( re.search( '><div>(.*)<\/div>', ddd ) ).replace( "<div>", "" ).replace( "</div>", "" )
            #
            d1 = ddd[ddd.find( ";>" ):]

            # si el parser anterior no cauda efecto, lo dejo como está
            if len( d1 ) > 3:
                ddd = d1

            #vsentimiento = sentimiento(texto)

            # desc = ddd[ddd.find("100%"):len(ddd)].replace( "<div>", "" ).replace( "100%;", "" )
            desc = limpiar( ddd, mugre )

            # desc = str(re.search('<div>(.*)<\/div>',desc)).replace("<div>","").replace("</div>","")

            date = multiple_replace(fecha, "[']<>!*\@," ).replace( '"', '' )

            fecha2 = mi_time()[0]

            # armo el json para grabar en elastic

            # vgeolocation = fgeolocation(j_i["medio"])
            vgeolocation = fgeolocation2()

            # vsentimiento = sentimiento(desc)

            arr = ['😡', '😏', '😁']

            vlocation10 = "0,0"
            vlocation20 = "0,0"
            vlocation30 = "0,0"

            vsentimiento = random.choice( [-1, 0, 1] )

            if vsentimiento == -1:
                vlocation10 = vgeolocation

            if vsentimiento == 0:
                vlocation20 = vgeolocation

            if vsentimiento == 1:
                vlocation30 = vgeolocation

            date = limpiar( date, mugre )

            print( vgeolocation )

            date = datetime.utcnow().isoformat()
            fecha2 = date

            imagen = random.choice( [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )
            sentimiento = random.choice( [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )
            seguridad = random.choice( [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )
            salud = random.choice( [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )
            trabajo = random.choice( [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )
            educacion = random.choice( [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )

            j_els = {

                "titulo": titulo,
                "link": link,
                "texto": desc,
                "fecha": fecha2,
                "medio": medio,
                "fecha2": fecha2,
                "location3": vgeolocation,
                "location100": vlocation10,
                "location200": vlocation20,
                "location300": vlocation30,
                "sentimiento": ["Negativo", "Neutro", "Positivo"][vsentimiento],
                "imagen": imagen,
                "salud": salud,
                "trabajo": trabajo,
                "educacion": educacion,
                "sentiminto": sentimiento,
                "grupo":grupo
            }

             ## grabo en el elastic
            r = vels.post( "noticias", "politica", j_els )
            print("vels.post ",r)



            ### guardo los datos en la base de dastos mysql
            r = json2sql_q(j_els)
            valores = r[1]
            campos = r[0]

            vsql = "insert into noticias ("+campos+") values ("+ valores + ")"
            vdb2.exect(vsql )





        except Exception as e:
            print( "add_rss_db ", e )


    ## --------------------------------------------------------

    def add2els_nube(texto, fecha, medio, grupo = ""):

        # pongo todo el texto
        j = {
            "palabra": texto,
            "fecha": fecha,
            "medio": medio,
            "grupo":grupo

        }

        r = vels.post( "noticias_nube", "palabras", j )

        # ahoro pongo las palabras

        texto = texto


        for e in texto.split( " " ):
            if len( e ) > 4:

                try:
                    j = {
                        "palabra": e,
                        "fecha": fecha,
                        "medio": medio,
                        "grupo":grupo
                    }
                    r = vels.post( "noticias_nube", "palabras", j )
                except Exception as e:
                    print( "19 - ", e )

        pass