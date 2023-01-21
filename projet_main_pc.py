"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Nom: projet_main_pc
# Intègre les objets nécéssaires pour constituer et rouler l'application
#
###########################################################################
"""

from projet_basedonnees_pc import BaseDonnees
from projet_messagerie_pc import Messagerie
from projet_globales_pc import attente, sujet
from datetime import datetime


def main():
    print("Programme démarré")
    bdd = BaseDonnees(sujet)
    messagerie = Messagerie(bdd, [sujet])

    print("debut à: ", datetime.now())

    attente(5) # la valeur correspond à la limite d'attente en secondes

    print("fin à:", datetime.now())

    messagerie.deconnexion()
    bdd.deconnexion()
    print("Programme terminé")


if __name__ == '__main__':
    main()
