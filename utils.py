# utils.py - Validation des entrées et détection du réseau local
# Ce fichier contient toutes les fonctions de vérification

import socket
import os
import ipaddress

def valider_ip(ip: str) -> bool:
    """
    Vérifie si une adresse IP est valide (format IPv4).

    """
    try:
        # ipaddress gère directement la validation IPv4
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def obtenir_ip_locale():
    """
    Récupère l'adresse IP réelle de ta machine sur le réseau local
    
    """
    try:
        # Crée une connexion temporaire pour connaître notre IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        # Si ça échoue, on essaie une autre méthode
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except:
            return "127.0.0.1"

def obtenir_reseau_local():
    """
    Détecte le réseau local réel de ta machine
    Exemple: si ton IP est 192.168.1.45 -> retourne "192.168.1."
    """
    ip_locale = obtenir_ip_locale()
    parties = ip_locale.split('.')
    if len(parties) >= 3:
        return parties[0] + '.' + parties[1] + '.' + parties[2] + '.'
    

def est_dans_reseau_local(ip):
    """
    Vérifie si une IP appartient au MÊME réseau local que ta machine
    C'est la fonction clé qui filtre les adresses hors réseau
    """
    mon_reseau = obtenir_reseau_local()
    return ip.startswith(mon_reseau)

def afficher_infos_reseau():
    """
    Affiche les informations réseau de ta machine (interface utilisateur)
    """
    ip_locale = obtenir_ip_locale()
    reseau = obtenir_reseau_local()
    print("┌" + "─" * 58 + "┐")
    print("│ " + " INFORMATIONS RÉSEAU".ljust(56) + "│")
    print("├" + "─" * 58 + "┤")
    print(f"│  Votre IP locale     : {ip_locale.ljust(36)}│")
    print(f"│ Votre réseau        : {reseau + 'xxx'.ljust(36)}│")
    print(f"│  Plage autorisée     : {reseau + '1 à ' + reseau + '254'.ljust(31)}│")
    print("└" + "─" * 58 + "┘")
    print()

# ports.py - Correspondance entre ports et services standards
# Pour rendre le scan plus intelligent et informatif

def nom_service(port):
    """
    Retourne le nom du service associé à un port
    """
    services = {
        20: " FTP (transfert fichiers)",
        21: " FTP (commandes)",
        22: " SSH (connexion sécurisée)",
        23: " Telnet (non sécurisé)",
        25: " SMTP (envoi emails)",
        53: " DNS (résolution noms)",
        67: " DHCP (serveur)",
        68: " DHCP (client)",
        80: " HTTP (sites web classiques)",
        110: " POP3 (réception emails)",
        111: " RPC (appels distants)",
        135: " RPC (Windows)",
        137: " NetBIOS (noms)",
        138: " NetBIOS (datagrammes)",
        139: " NetBIOS (session)",
        143: " IMAP (emails)",
        161: " SNMP (supervision)",
        389: " LDAP (annuaire)",
        443: " HTTPS (sites sécurisés)",
        445: " SMB (partage Windows)",
        993: " IMAPS (emails sécurisés)",
        995: " POP3S (emails sécurisés)",
        1433: " SQL Server",
        3306: " MySQL",
        3389: " RDP (bureau distant)",
        5432: " PostgreSQL",
        5900: " VNC (bureau distant)",
        6379: " Redis",
        27017: " MongoDB",
    }
    
    if port in services:
        return services[port]
    else:
        return " Service inconnu"