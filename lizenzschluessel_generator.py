# -*- coding: utf-8 -*-
import argparse
import secrets
import base64
import datetime
import json  # Für die Payload-Struktur
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# --- CipherCore Urheberrechtsvermerk und Lizenz ---
__copyright__ = "Copyright (c) 2024 CipherCore GmbH"
__license__ = "Proprietär - Alle Rechte vorbehalten"


def generiere_rsa_schluesselpaar():
    """
    Generiert ein RSA-Schlüsselpaar für die Lizenzsignierung.

    Returns:
        tuple: (RSAPrivateKey, RSAPublicKey) - Privater und öffentlicher Schlüssel.
    """
    privater_schluessel = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    oeffentlicher_schluessel = privater_schluessel.public_key()
    return privater_schluessel, oeffentlicher_schluessel


def serialisiere_privaten_schluessel(privater_schluessel, passwort=None):
    """
    Serialisiert einen privaten RSA-Schlüssel in PEM-Format.

    Args:
        privater_schluessel (RSAPrivateKey): Der zu serialisierende private Schlüssel.
        passwort (bytes, optional): Ein Passwort zum Verschlüsseln des privaten Schlüssels.

    Returns:
        bytes: Serialisierter privater Schlüssel im PEM-Format.
    """
    verschluesselung = serialization.NoEncryption()
    if passwort:
        verschluesselung = serialization.BestAvailableEncryption(passwort)

    pem_privat = privater_schluessel.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=verschluesselung
    )
    return pem_privat


def serialisiere_oeffentlichen_schluessel(oeffentlicher_schluessel):
    """
    Serialisiert einen öffentlichen RSA-Schlüssel im PEM-Format.

    Args:
        oeffentlicher_schluessel (RSAPublicKey): Der zu serialisierende öffentliche Schlüssel.

    Returns:
        bytes: Serialisierter öffentlicher Schlüssel im PEM-Format.
    """
    pem_oeffentlich = oeffentlicher_schluessel.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem_oeffentlich


def signiere_daten_rsa(privater_schluessel, daten):
    """
    Signiert Daten mit einem privaten RSA-Schlüssel.

    Args:
        privater_schluessel (RSAPrivateKey): Der private Schlüssel zum Signieren.
        daten (bytes): Die zu signierenden Daten (Bytes).

    Returns:
        bytes: Die Signatur (Bytes).
    """
    signatur = privater_schluessel.sign(
        daten,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signatur


def generiere_lizenzschluessel_pro(privater_schluessel, tage_gueltig=365, hardware_id=None, version="Pro"):
    """
    Generiert einen signierten Lizenzschlüssel für die Pro-Version mit RSA.

    Args:
        privater_schluessel (RSAPrivateKey): Der private RSA-Schlüssel zum Signieren.
        tage_gueltig (int): Anzahl der Tage, die der Schlüssel gültig ist. Standard ist 365 Tage (1 Jahr).
        hardware_id (str, optional): Hardware-ID, an die der Schlüssel gebunden werden soll.
        version (str): Versionstyp der Lizenz (Standard: "Pro").

    Returns:
        str: Ein Base64-kodierter, signierter Lizenzschlüssel.
    """
    ablaufdatum = datetime.date.today() + datetime.timedelta(days=tage_gueltig)
    ablaufdatum_str = ablaufdatum.strftime("%Y-%m-%d")

    payload_daten = {
        "version": version,
        "ablaufdatum": ablaufdatum_str,
        "hardware_id": hardware_id if hardware_id else None, # Hardware-ID optional
        "ausgestellt_am": datetime.date.today().strftime("%Y-%m-%d")
    }
    payload_json_bytes = json.dumps(payload_daten, sort_keys=True).encode('utf-8') # JSON Payload erstellen und sortieren für deterministische Signatur

    signatur_bytes = signiere_daten_rsa(privater_schluessel, payload_json_bytes)
    lizenz_daten = {
        "payload": base64.urlsafe_b64encode(payload_json_bytes).decode('utf-8'), # Payload Base64-kodiert
        "signatur": base64.urlsafe_b64encode(signatur_bytes).decode('utf-8')   # Signatur Base64-kodiert
    }
    lizenzschluessel_base64 = base64.urlsafe_b64encode(json.dumps(lizenz_daten).encode('utf-8')).decode('utf-8') # Komplettes Lizenz-JSON Base64-kodiert
    return lizenzschluessel_base64


def validiere_lizenzschluessel_pro(oeffentlicher_schluessel, lizenzschluessel_base64, erwartete_version="Pro", hardware_id_pruefen=None):
    """
    Validiert einen signierten Pro-Lizenzschlüssel mit RSA und optionaler Hardware-ID-Prüfung.

    Args:
        oeffentlicher_schluessel (RSAPublicKey): Der öffentliche RSA-Schlüssel zum Validieren.
        lizenzschluessel_base64 (str): Der Base64-kodierte Lizenzschlüssel.
        erwartete_version (str): Die erwartete Lizenzversion (Standard: "Pro").
        hardware_id_pruefen (str, optional): Die Hardware-ID, gegen die geprüft werden soll.

    Returns:
        tuple: (bool, dict oder None) - True und Payload-Daten (dict) bei gültiger Lizenz, False und None bei ungültiger Lizenz.
    """
    try:
        lizenz_json_bytes = base64.urlsafe_b64decode(lizenzschluessel_base64)
        lizenz_daten = json.loads(lizenz_json_bytes.decode('utf-8'))

        payload_base64 = lizenz_daten.get("payload")
        signatur_base64 = lizenz_daten.get("signatur")

        if not payload_base64 or not signatur_base64:
            return False, None # Ungültiges Lizenzformat

        payload_bytes = base64.urlsafe_b64decode(payload_base64)
        signatur_bytes = base64.urlsafe_b64decode(signatur_base64)

        oeffentlicher_schluessel.verify(
            signatur_bytes,
            payload_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        ) # Verify wirft InvalidSignature Exception wenn Signatur ungültig

        payload_daten = json.loads(payload_bytes.decode('utf-8'))

        if payload_daten.get("version") != erwartete_version:
            return False, None # Falsche Version

        ablaufdatum_str = payload_daten.get("ablaufdatum")
        if ablaufdatum_str:
            ablaufdatum = datetime.datetime.strptime(ablaufdatum_str, "%Y-%m-%d").date()
            if datetime.date.today() > ablaufdatum:
                return False, payload_daten # Lizenz abgelaufen

        if hardware_id_pruefen and payload_daten.get("hardware_id") != hardware_id_pruefen:
            return False, None # Hardware-ID stimmt nicht überein

        return True, payload_daten # Lizenz gültig

    except (json.JSONDecodeError, InvalidSignature, ValueError, TypeError, base64.binascii.Error) as e: #  Mehr Exceptions abfangen
        print(f"Fehler bei der Lizenzvalidierung: {e}") #  Für Debugging-Zwecke
        return False, None # Validierung fehlgeschlagen


def main():
    parser = argparse.ArgumentParser(description="CipherCore Lizenzschlüssel Generator (Pro Version)")
    parser.add_argument("--tage_gueltig", type=int, default=365, help="Anzahl der Tage Gültigkeit für Pro-Lizenz (Standard: 365)")
    parser.add_argument("--hardware_id", type=str, default=None, help="Hardware-ID für die Lizenzbindung (optional)")
    parser.add_argument("--schluessel_aktion", choices=['generieren', 'serialisieren', 'validieren'], default='generieren', help="Aktion: Schlüsselpaar generieren, Schlüssel serialisieren oder Lizenz validieren")
    parser.add_argument("--privater_schluessel_pfad", type=str, default="private_key.pem", help="Pfad zum privaten Schlüssel für Serialisierung/Signierung")
    parser.add_argument("--oeffentlicher_schluessel_pfad", type=str, default="public_key.pem", help="Pfad zum öffentlichen Schlüssel für Serialisierung/Validierung")
    parser.add_argument("--lizenzschluessel", type=str, default=None, help="Zu validierender Lizenzschlüssel (Base64-kodiert)")


    argumente = parser.parse_args()

    if argumente.schluessel_aktion == 'generieren':
        privater_schluessel, oeffentlicher_schluessel = generiere_rsa_schluesselpaar()

        pem_privat = serialisiere_privaten_schluessel(privater_schluessel)
        pem_oeffentlich = serialisiere_oeffentlichen_schluessel(oeffentlicher_schluessel)

        with open(argumente.privater_schluessel_pfad, "wb") as f:
            f.write(pem_privat)
        with open(argumente.oeffentlicher_schluessel_pfad, "wb") as f:
            f.write(pem_oeffentlich)

        print(f"RSA Schlüsselpaar generiert und gespeichert:")
        print(f"- Privater Schlüssel: {argumente.privater_schluessel_pfad}")
        print(f"- Öffentlicher Schlüssel: {argumente.oeffentlicher_schluessel_pfad}")

        lizenzschluessel_pro = generiere_lizenzschluessel_pro(privater_schluessel, tage_gueltig=argumente.tage_gueltig, hardware_id=argumente.hardware_id)
        print("\nPro-Lizenzschlüssel (signiert, RSA, Base64-kodiert):")
        print(lizenzschluessel_pro)


    elif argumente.schluessel_aktion == 'serialisieren':
        privater_schluessel, oeffentlicher_schluessel = generiere_rsa_schluesselpaar() # Zum Testen, in echt laden

        pem_privat = serialisiere_privaten_schluessel(privater_schluessel, passwort=b"mein_geheimes_passwort") # Passwort zum Schutz!
        print("\nSerialisierter privater Schlüssel (PEM, verschlüsselt):")
        print(pem_privat.decode('utf-8'))

        pem_oeffentlich = serialisiere_oeffentlichen_schluessel(oeffentlicher_schluessel)
        print("\nSerialisierter öffentlicher Schlüssel (PEM):")
        print(pem_oeffentlich.decode('utf-8'))


    elif argumente.schluessel_aktion == 'validieren':
        if not argumente.lizenzschluessel:
            print("Fehler: Zum Validieren eines Schlüssels muss der Parameter --lizenzschluessel angegeben werden.")
            return

        try:
            with open(argumente.oeffentlicher_schluessel_pfad, "rb") as key_file:
                oeffentlicher_schluessel_pem = key_file.read()
                oeffentlicher_schluessel = serialization.load_pem_public_key(oeffentlicher_schluessel_pem)
        except FileNotFoundError:
            print(f"Fehler: Öffentlicher Schlüssel nicht gefunden unter: {argumente.oeffentlicher_schluessel_pfad}")
            return

        ist_gueltig, payload = validiere_lizenzschluessel_pro(oeffentlicher_schluessel, argumente.lizenzschluessel, hardware_id_pruefen=argumente.hardware_id) # Hardware ID optional zum Testen

        if ist_gueltig:
            print("\nLizenzschlüssel ist GÜLTIG.")
            print("Payload Daten:")
            print(json.dumps(payload, indent=4))
        else:
            print("\nLizenzschlüssel ist UNGÜLTIG.")


if __name__ == "__main__":
    main()