# scanner.py - Test des ports TCP
# Ce fichier contient la logique de connexion réseau

import socket
import time

def scanner_port(ip, port, delai=0.3):
    """
    Teste si un port est ouvert sur une IP donnée
    Retourne True si ouvert, False sinon
    """
    try:
        # Crée un socket (prise réseau)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Définit un délai d'attente (timeout)
        s.settimeout(delai)
        # Tente la connexion (connect_ex retourne 0 si réussi)
        resultat = s.connect_ex((ip, port))
        # Ferme la connexion
        s.close()
        return resultat == 0
    except:
        return False