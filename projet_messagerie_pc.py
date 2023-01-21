"""
###########################################################################
#                              Projet Intégrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 17/01/2023
#
# Nom: projet_messagerie_pc
# Gère la connexion à MQTT
#
###########################################################################
"""
from projet_prive_pc import host, port, client_id, username, password
from projet_globales_pc import attente, sujet, quitter
import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, response_code):

    response_message = ""

    if response_code == 0:
        response_message = "connecté"
    elif response_code == 1:
        response_message = "connection refused: protocol version not accepted"
    elif response_code == 2:
        response_message = "connection refused: incorrect client ID"
    elif response_code == 3:
        response_message = "connection made but service is not vailable"
    elif response_code == 4:
        response_message = "connection refused: invalid credentials"
    elif response_code == 5:
        response_message = "connection refused: unauthorized access"
    else:
        response_message = "unknown"

    print( userdata.nom + ": " + response_message )


def on_message(client, userdata, message):
    contenu = str(message.payload.decode("utf-8"))
    #print( userdata.nom + ": reçu: ", contenu )  # Verification 1

    if contenu == "FIN": # condition de sortie de la boucle d'attente
        quitter()
        print(userdata.nom + ": condition de fin rencontrée")
    else:
        userdata.inscrireDocument( contenu )  # Verification 2


class Messagerie():

    def __init__( self, parent, sujets: list ):

        self.nom = "MQTT"
        self.sujets = sujets  # liste de sujets à écouter
        self.inscrit = False

        # on obtient une interface à mosquitto
        try:
            self.client = None
            self.client = mqtt.Client( client_id = client_id, clean_session = True )
            print(self.nom + ": client OK" )
        except:
            print(self.nom + ": ERREUR (1) : le client n'a pu être instancié" )
            return

        # on établit quelques paramètres
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.user_data_set(parent) # on passe le parent au callbacks
        self.client.username_pw_set(username, password) # pour l'authentification

        # on tente de se connecter au serveur
        try:
            # host = MQTT_BROKER (lorsque local)
            self.client.connect( host = host, keepalive = 60 ) # port = port,
        except:
            print(self.nom + ": ERREUR (2) : la connexion n'a pu se faire" )
            return

        # on se souscrit aux sujets à écouter et on démarre le fil
        self.inscrire(sujets)
        self.inscrit = True
        self.client.loop_start()
        print(self.nom + ": à l'écoute..." )


    def inscrire(self, sujets: list): # s_inscrir
        for sujet in self.sujets:
            # ce serait bien de vérifier si le sujet existe déjà
            # donc de nous faire une liste de sujets auxquels on est inscrits
            self.client.subscribe( sujet )


    def desinscrire(self, sujets: list = None):
        if sujets is None:
            sujets = self.sujets
        for sujet in sujets:
            self.client.unsubscribe(sujet)


    def publieMessages(self, sujet, valeur):
        self.client.publish( sujet, valeur )
        print(self.nom + ": Publié: ", valeur, "au sujet " + sujet )


    def deconnexion(self):
        if self.client is not None:
            self.client.loop_stop()
            # on se désinscrit des sujets et on se déconnecte

            if self.inscrit:
                self.desinscrire() # attention aux paramètre
                self.inscrit = False
                print(self.nom + ": désinscrit")

            self.client.disconnect()
            print(self.nom + ": déconnecté")


    def __del__(self):
        #print(self.nom + ": destructeur() MQTT")
        pass


# -------------------------------- TESTS -------------------------------------


# objet pour tests ci-bas
class Obj():

    def __init__(self, nom):
        self.nom = nom

    def traiteMessages(self, contenu):
        print("pc reçoit: ", contenu)

    def inscrireDocument(self, contenu):
        print("pc reçoit: ", contenu)


#-----------------------------------TESTS--------------------------------------


def main():
    from projet_globales_pc import attente, sujet

    print("début du test")
    obj = Obj("MQTT")
    messagerie = Messagerie( obj, [sujet] ) # le sujet d'inscription est Bonjour
    attente()
    messagerie.deconnexion()
    print("test terminée")


if __name__ == '__main__':
    main()