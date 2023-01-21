"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Nom: projet_globales_pc
# Quelques fonctions globales
#
###########################################################################
"""

from time import sleep

sujet = "TOUCAN"
etat_rouler = True

def quitter():
    global etat_rouler
    etat_rouler = False

def rouler():
    global etat_rouler
    return etat_rouler

def attente(limite = 10):
    """
    Fournit un service d'attente
    La variable "limite" est en secondes
    """
    while rouler() and limite > 0:
        limite -= 1
        sleep(1) # on attend une seconde
