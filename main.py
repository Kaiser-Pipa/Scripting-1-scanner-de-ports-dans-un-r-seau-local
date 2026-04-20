# main.py - Programme principal (interface utilisateur)
# Fichier à exécuter

import sys
import time
import argparse
from utils import (
    valider_ip,
    est_dans_reseau_local,
    afficher_infos_reseau,
    obtenir_reseau_local,
    nom_service
)
from scanner import scanner_port



def afficher_banniere():
    """Affiche une bannière améliorée sans emojis"""
    bleu = "\033[94m"
    vert = "\033[92m"
    jaune = "\033[93m"
    reset = "\033[0m"

    print()
    print(bleu + "╔" + "═" * 58 + "╗" + reset)
    print(bleu + "║" + vert + "   SCANNER DE PORTS - Réseau Local ".center(58) + bleu + "║" + reset)
    print(bleu + "╠" + "═" * 58 + "╣" + reset)
    print(bleu + "║" + jaune + "   Version sécurisée - uniquement LAN ".center(58) + bleu + "║" + reset)
    print(bleu + "╚" + "═" * 58 + "╝" + reset)
    print()


def afficher_barre_progression(current, total, largeur=40):
    """Affiche une barre de progression améliorée sans emojis"""
    pourcentage = (current / total)
    rempli = int(pourcentage * largeur)
    vide = largeur - rempli
    barre = "█" * rempli + "─" * vide
    return f"\r[{barre}] {pourcentage*100:6.2f}% ({current}/{total})"


def demander_ip():
    """Demande et valide une IP locale"""
    while True:
        ip = input("Adresse IP à scanner : ").strip()
        if not valider_ip(ip):
            print("Format d'IP invalide (ex: 192.168.1.1)\n")
            continue
        if not est_dans_reseau_local(ip):
            mon_reseau = obtenir_reseau_local()
            print("\n" + "═" * 60)
            print("ACCÈS REFUSÉ : IP hors réseau local")
            print("═" * 60)
            print(f"Votre réseau autorisé : {mon_reseau}xxx")
            print(f"IP saisie : {ip}\n")
            continue
        return ip


def demander_plage_ports():
    """Demande et valide une plage de ports"""
    while True:
        plage = input("Plage de ports (ex: 20-100) : ").strip()
        try:
            debut, fin = map(int, plage.split('-'))
            if debut < 1 or fin > 65535 or debut > fin:
                raise ValueError
            return debut, fin
        except ValueError:
            print("Plage invalide. Format attendu : début-fin (ex: 20-100)\n")


def main():
    """Programme principal"""
    afficher_banniere()
    afficher_infos_reseau()

    # Saisie IP et ports
    ip = demander_ip()
    print(f"\nIP valide et autorisée : {ip}\n")

    debut, fin = demander_plage_ports()
    total_ports = fin - debut + 1

    print("\n" + "═" * 60)
    print("RÉCAPITULATIF DU SCAN")
    print("═" * 60)
    print(f"   Cible : {ip}")
    print(f"   Plage : {debut} → {fin}")
    print(f"   Nombre de ports : {total_ports}")
    print("═" * 60)

    if input("\nLancer le scan ? (o/n) : ").strip().lower() != 'o':
        print("\nScan annulé. Au revoir !")
        sys.exit(0)

    # Scan
    print("\n" + "═" * 60)
    print("SCAN EN COURS...")
    print("═" * 60 + "\n")

    ports_ouverts = []
    for index, port in enumerate(range(debut, fin + 1), 1):
        progression = afficher_barre_progression(index, total_ports)
        print(f"{progression} | Test port {port}...", end=" ")

        if scanner_port(ip, port):
            service = nom_service(port)
            print(f"OUVERT → {service}")
            ports_ouverts.append(port)
        else:
            print("Fermé")

        time.sleep(0.05)

    # Résultats
    print("\n" + "═" * 60)
    print("RÉSULTATS DU SCAN")
    print("═" * 60)

    if ports_ouverts:
        print(f"\n{len(ports_ouverts)} port(s) ouvert(s) trouvé(s) :\n")
        for port in sorted(ports_ouverts):
            print(f"   Port {port} : {nom_service(port)}")
    else:
        print("\nAucun port ouvert trouvé.")
        print("Conseil : Essayez une plage plus large (ex: 1-1000)")

    print("\n" + "═" * 60)
    print("Scan terminé.")
    print("═" * 60 + "\n")

    print("\n" + "═" * 60)
    print("Scan terminé.")
    print("═" * 60 + "\n")

    # === Option de sauvegarde des résultats ===
    choix = input("Souhaitez-vous sauvegarder les résultats dans un fichier texte ? (o/n) : ").strip().lower()

    if choix == "o":
        nom_fichier = input("Entrez le nom du fichier (ex: resultats.txt) : ").strip()

        # Ajout automatique de l'extension .txt si oubliée
        if not nom_fichier.endswith(".txt"):
            nom_fichier += ".txt"

        try:
            with open(nom_fichier, "w", encoding="utf-8") as f:
                f.write("RÉSULTATS DU SCAN\n")
                f.write("=" * 60 + "\n")
                f.write(f"Cible : {ip}\n")
                f.write(f"Plage : {debut} → {fin}\n")
                f.write(f"Nombre de ports testés : {total_ports}\n\n")

                if ports_ouverts:
                    f.write(f"{len(ports_ouverts)} port(s) ouvert(s) trouvé(s) :\n")
                    for port in sorted(ports_ouverts):
                        f.write(f"   Port {port} : {nom_service(port)}\n")
                else:
                    f.write("Aucun port ouvert trouvé.\n")
                    f.write("Conseil : Essayez une plage plus large (ex: 1-1000)\n")

            print(f"Les résultats ont été sauvegardés dans le fichier '{nom_fichier}'.\n")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des résultats : {e}")
    else:
        print("Les résultats n'ont pas été sauvegardés.\n")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Scanner de ports (réseau local uniquement)")
        parser.add_argument("--ip", help="Adresse IP cible")
        parser.add_argument("--ports", help="Plage de ports ex: 20-100")
        args = parser.parse_args()

        if args.ip and args.ports:
            ip = args.ip if valider_ip(args.ip) and est_dans_reseau_local(args.ip) else demander_ip()
            try:
                debut, fin = map(int, args.ports.split('-'))
            except ValueError:
                debut, fin = demander_plage_ports()
            main()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\nScan interrompu par l'utilisateur. Au revoir !\n")
        sys.exit(0)