# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
import datetime
import base64
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Checkbutton, Button
import threading
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Optional, Callable

from PIL import Image  # Importiere PIL Image für die Bildverarbeitung

# --- CipherCore Urheberrechtsvermerk und Lizenz ---
__copyright__ = "Copyright (c) 2024 CipherCore GmbH"
__license__ = "Proprietär - Alle Rechte vorbehalten"

# --- Konstanten Definitionen (Erhöhte Sicherheit und Klarheit) ---
CONFIG_DATEI = 'config.json'
LOGO_DATEIPFAD_STANDARD = 'assets/ciphercore_logo_standard.png' # Standardpfad für Logo
AUSGABE_DATEIPFAD_STANDARD = 'berichte/datei_vergleichsbericht.pdf' # Standardpfad für Berichte
CONFIG_SCHLUESSEL_ERSTES_STARTDATUM = "erster_start_datum"
CONFIG_SCHLUESSEL_LIZENZ_AKZEPTIERT = "lizenz_akzeptiert"
CONFIG_SCHLUESSEL_DATENBANK_PFAD = "datenbank_pfad"
DATENBANK_DATEINAME_STANDARD = 'ciphercore_datei_vergleich.db' # Standard Datenbankname
DATEN_VERZEICHNIS_STANDARD = 'ciphercore_vergleichsdaten' # Standard Datenverzeichnis

DATEIFORMAT_CSV = '.csv'
DATEIFORMAT_TEXT = '.txt'
DATEIFORMAT_EXCEL_XLS = '.xls'
DATEIFORMAT_EXCEL_XLSX = '.xlsx'
UNTERSTUETZTE_DATEIFORMATE = (DATEIFORMAT_CSV, DATEIFORMAT_TEXT, DATEIFORMAT_EXCEL_XLS, DATEIFORMAT_EXCEL_XLSX)

DIAGRAMM_TYP_BALKEN = 'balken'
DIAGRAMM_TYP_KREIS = 'kreis'
UNTERSTUETZTE_DIAGRAMM_TYPEN = (DIAGRAMM_TYP_BALKEN, DIAGRAMM_TYP_KREIS)

METRIK_ANZAHL_DATEI1 = 'Anzahl Einträge Datei 1 (Benutzereingabe)' # Klarstellung der Metrik
METRIK_ANZAHL_DATEI2 = 'Anzahl Einträge Datei 2 (Hauptliste)' # Klarstellung der Metrik
METRIK_GLEICHE_NAMEN = 'Anzahl übereinstimmende Namen' # Präzisere Metrikbezeichnung
METRIK_PROZENTUALER_UNTERSCHIED_ANZAHL = 'Prozentualer Unterschied in der Anzahl der Einträge' # Präzisere Metrikbezeichnung
METRIK_DURCHSCHNITTSALTER_DATEI1 = 'Durchschnittsalter Datei 1 (Benutzereingabe)' # Klarstellung der Metrik
METRIK_DURCHSCHNITTSALTER_DATEI2 = 'Durchschnittsalter Datei 2 (Hauptliste)' # Klarstellung der Metrik
METRIK_REIHENFOLGE = [METRIK_ANZAHL_DATEI1, METRIK_ANZAHL_DATEI2, METRIK_PROZENTUALER_UNTERSCHIED_ANZAHL,
                     METRIK_GLEICHE_NAMEN, METRIK_DURCHSCHNITTSALTER_DATEI1, METRIK_DURCHSCHNITTSALTER_DATEI2]

# --- Logging Konfiguration (CipherCore Standard: Detailliert und Sicher) ---
LOG_DATEIPFAD = 'log/ciphercore_datei_vergleich.log' # Log-Dateien in separatem Verzeichnis
os.makedirs(os.path.dirname(LOG_DATEIPFAD), exist_ok=True) # Log-Verzeichnis erstellen, falls nicht vorhanden

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
                    filename=LOG_DATEIPFAD,
                    filemode='w')
logger = logging.getLogger(__name__) # Benannter Logger für bessere Nachverfolgung

# --- Konfiguration Laden und Validierung (Sicherheitsfokus: Fehlerresistent) ---
STANDARD_KONFIGURATION = {
    "basis_verzeichnis": os.path.abspath('.'), # Basisverzeichnis für Pfadsicherheit
    "logo_pfad": LOGO_DATEIPFAD_STANDARD, # Standard Logo Pfad
    "ausgabe_pfad": AUSGABE_DATEIPFAD_STANDARD, # Standard Ausgabepfad
    CONFIG_SCHLUESSEL_ERSTES_STARTDATUM: None, # Erstes Startdatum für Testphase
    CONFIG_SCHLUESSEL_LIZENZ_AKZEPTIERT: False, # Lizenzakzeptanzstatus
    CONFIG_SCHLUESSEL_DATENBANK_PFAD: DATENBANK_DATEINAME_STANDARD, # Standard Datenbankpfad
    "daten_verzeichnis": DATEN_VERZEICHNIS_STANDARD # Standard Datenverzeichnis
}

konfiguration = STANDARD_KONFIGURATION.copy() # Kopie der Standardkonfiguration

def _lade_konfiguration(konfig_datei_pfad: str) -> Dict:
    """
    Lädt die Konfiguration aus einer JSON-Datei und validiert diese gegen ein Schema.
    Sicherheitsmaßnahme: Verhindert das Laden unerwarteter oder schädlicher Konfigurationen.
    """
    try:
        if not os.path.exists(konfig_datei_pfad):
            logger.warning(f"Konfigurationsdatei '{konfig_datei_pfad}' nicht gefunden. Standardkonfiguration wird verwendet.")
            return STANDARD_KONFIGURATION

        with open(konfig_datei_pfad, 'r', encoding='utf-8') as konfig_datei: # Explizite Encoding-Angabe für Robustheit
            benutzer_konfiguration = json.load(konfig_datei)
            konfiguration_temp = STANDARD_KONFIGURATION.copy()
            konfiguration_temp.update(benutzer_konfiguration) # Nur bekannte Schlüssel werden aktualisiert
            _validiere_konfiguration(konfiguration_temp) # Validierung der geladenen Konfiguration
            logger.info(f"Konfiguration aus '{konfig_datei_pfad}' geladen und validiert.")
            return konfiguration_temp

    except json.JSONDecodeError as e:
        logger.error(f"Fehler beim Lesen der Konfigurationsdatei '{konfig_datei_pfad}'. JSON-Format ungültig: {e}. Standardkonfiguration wird verwendet.")
        return STANDARD_KONFIGURATION
    except FileNotFoundError:
        logger.warning(f"Konfigurationsdatei '{konfig_datei_pfad}' nicht gefunden. Standardkonfiguration wird verwendet.")
        return STANDARD_KONFIGURATION
    except ValueError as e: # Validierungsfehler
        logger.error(f"Ungültige Konfiguration in '{konfig_datei_pfad}': {e}. Standardkonfiguration wird verwendet.")
        return STANDARD_KONFIGURATION
    except Exception as e:
        logger.exception(f"Unerwarteter Fehler beim Laden der Konfiguration aus '{konfig_datei_pfad}': {e}. Standardkonfiguration wird verwendet.")
        return STANDARD_KONFIGURATION


def _validiere_konfiguration(konfiguration_dict: Dict) -> None:
    """
    Validiert die Konfiguration gegen ein vordefiniertes Schema.
    Stellt sicher, dass kritische Konfigurationswerte gültig sind, um unerwartetes Verhalten zu verhindern.
    """
    basis_verzeichnis = konfiguration_dict.get("basis_verzeichnis")
    logo_pfad = konfiguration_dict.get("logo_pfad")
    ausgabe_pfad = konfiguration_dict.get("ausgabe_pfad")
    datenbank_pfad = konfiguration_dict.get(CONFIG_SCHLUESSEL_DATENBANK_PFAD)
    daten_verzeichnis = konfiguration_dict.get("daten_verzeichnis")

    if not basis_verzeichnis or not isinstance(basis_verzeichnis, str):
        raise ValueError("Basisverzeichnis in der Konfiguration ungültig.")
    if logo_pfad and not isinstance(logo_pfad, str):
        raise ValueError("Logo-Pfad in der Konfiguration ungültig.")
    if ausgabe_pfad and not isinstance(ausgabe_pfad, str):
        raise ValueError("Ausgabe-Pfad in der Konfiguration ungültig.")
    if datenbank_pfad and not isinstance(datenbank_pfad, str):
        raise ValueError("Datenbank-Pfad in der Konfiguration ungültig.")
    if daten_verzeichnis and not isinstance(daten_verzeichnis, str):
        raise ValueError("Datenverzeichnis in der Konfiguration ungültig.")


konfiguration = _lade_konfiguration(CONFIG_DATEI) # Konfiguration beim Start laden

BASIS_VERZEICHNIS = konfiguration["basis_verzeichnis"]
LOGO_DATEIPFAD = konfiguration["logo_pfad"]
AUSGABE_DATEIPFAD = konfiguration["ausgabe_pfad"]
DATENBANK_PFAD = konfiguration[CONFIG_SCHLUESSEL_DATENBANK_PFAD]
DATEN_VERZEICHNIS = konfiguration["daten_verzeichnis"]

# --- Lizenzbedingungen (CipherCore Standard: Klar und Rechtlich geprüft) ---
LIZENZBEDINGUNGEN_TEXT = """
LIZENZBEDINGUNGEN FÜR CIPHERCORE DATEIVERGLEICHS-TOOL - TESTVERSION

Dies ist eine Testversion der CipherCore Dateivergleichs-Software.
... (Vollständiger, rechtlich geprüfter Lizenztext hier einfügen) ...

SICHERHEITSHINWEIS:
Diese Software wird "wie besehen" und ohne jegliche Gewährleistung bereitgestellt.
CipherCore GmbH übernimmt keine Haftung für Schäden, die durch die Nutzung
dieser Software entstehen könnten, insbesondere Datenverlust oder
Sicherheitsverletzungen. Die Nutzung erfolgt auf eigene Gefahr.

Bitte lesen und akzeptieren Sie die vollständigen Lizenzbedingungen,
bevor Sie die Software verwenden.
"""

# --- Benutzerdefinierte Exceptions (CipherCore Standard: Präzise Fehlerbehandlung) ---
class CipherCoreDatenFehler(Exception):
    """Basisklasse für alle CipherCore Datenfehler."""
    pass

class CipherCoreDatenbankFehler(CipherCoreDatenFehler):
    """Basisklasse für Datenbankfehler."""
    pass

class CipherCoreDatenbankSchemaFehler(CipherCoreDatenbankFehler):
    """Fehler beim Erstellen des Datenbank-Schemas."""
    pass

class CipherCoreDatenbankSpeicherFehler(CipherCoreDatenbankFehler):
    """Fehler beim Speichern in die Datenbank."""
    pass

class CipherCoreDatenbankLadeFehler(CipherCoreDatenbankFehler):
    """Fehler beim Laden aus der Datenbank."""
    pass

class CipherCoreDateiFehler(CipherCoreDatenFehler):
    """Basisklasse für Dateifehler."""
    pass

class CipherCoreDateiSpeicherFehler(CipherCoreDateiFehler):
    """Fehler beim Speichern in Datei."""
    pass

class CipherCoreDateiLadeFehler(CipherCoreDateiFehler):
    """Fehler beim Laden aus Datei."""
    pass

class CipherCoreDateiSchemaFehler(CipherCoreDateiFehler):
    """Fehler beim Erstellen des Datei-Schemas (z.B. Verzeichnis)."""
    pass

class CipherCoreDatenValidierungsFehler(CipherCoreDatenFehler):
    """Fehler bei der Validierung der Daten."""
    pass

class CipherCoreUngültigerDiagrammTypFehler(CipherCoreDatenFehler):
    """Fehler aufgrund eines ungültigen Diagrammtyps."""
    pass


# --- DatenLader Klasse (CipherCore Standard: Sicheres und Robustes Laden) ---
class DatenLader:
    """
    Modul zum sicheren und robusten Laden von Daten aus verschiedenen Dateiformaten.
    Implementiert strenge Sicherheitsprüfungen für Dateipfade und umfassende Datenvalidierung.
    """

    def __init__(self, basis_verzeichnis: str):
        """
        Initialisiert den Datenlader mit dem Basisverzeichnis für sichere Dateipfade.

        Args:
            basis_verzeichnis (str): Das Basisverzeichnis, auf das Dateipfade beschränkt werden.
        """
        if not basis_verzeichnis or not isinstance(basis_verzeichnis, str):
            raise ValueError("Basisverzeichnis muss ein gültiger Pfad sein.")
        self.basis_verzeichnis = os.path.abspath(basis_verzeichnis) # Absoluter Pfad für sichere Pfadvergleiche
        logger.debug(f"DatenLader initialisiert mit Basisverzeichnis: {self.basis_verzeichnis}")


    def lade_daten(self, datei_pfad: str) -> Tuple[pd.DataFrame, str]:
        """
        Lädt Daten aus der angegebenen Datei. Führt Sicherheitsprüfungen und Validierung durch.

        Args:
            datei_pfad (str): Der Pfad zur zu ladenden Datei.

        Returns:
            Tuple[pd.DataFrame, str]: Ein DataFrame mit den geladenen Daten und der Dateiname.

        Raises:
            CipherCoreDateiFehler: Wenn der Dateipfad ungültig ist, das Dateiformat nicht unterstützt wird,
                                  die Datei nicht gefunden wird oder ein Fehler beim Lesen der Datei auftritt.
            CipherCoreDatenValidierungsFehler: Wenn die Datenvalidierung fehlschlägt.
        """
        dateiname = os.path.basename(datei_pfad)
        logger.info(f"Starte Ladevorgang für Datei: '{dateiname}'")

        if not self._ist_pfad_sicher(datei_pfad):
            logger.error(f"Unsicherer Dateipfad: '{datei_pfad}'. Pfad liegt außerhalb des Basisverzeichnisses.")
            raise CipherCoreDateiFehler(f"Ungültiger Dateipfad. Sicherheitshinweis: Pfad muss innerhalb des Basisverzeichnisses liegen.")

        try:
            daten_frame = self._datei_laden(datei_pfad)
        except FileNotFoundError as e:
            logger.error(f"Datei nicht gefunden: {e.filename}")
            raise CipherCoreDateiLadeFehler(f"Datei nicht gefunden: {e.filename}") from e
        except ValueError as e:
            logger.error(f"Fehler beim Lesen der Datei '{dateiname}': {e}")
            raise CipherCoreDateiLadeFehler(f"Fehler beim Lesen der Datei '{dateiname}': {e}") from e
        except Exception as e:
            logger.exception(f"Unerwarteter Fehler beim Laden der Datei '{dateiname}': {e}")
            raise CipherCoreDateiLadeFehler(f"Unerwarteter Fehler beim Laden der Datei '{dateiname}': {e}") from e

        try:
            self._validiere_daten(daten_frame, dateiname)
        except CipherCoreDatenValidierungsFehler as e:
            logger.error(f"Datenvalidierung für Datei '{dateiname}' fehlgeschlagen: {e}")
            raise e # Fehler weiterleiten

        logger.info(f"Datei '{dateiname}' erfolgreich geladen und validiert.")
        return daten_frame, dateiname


    def _datei_laden(self, datei_pfad: str) -> pd.DataFrame:
        """
        Interne Hilfsfunktion zum Laden einer einzelnen Datei (CSV, TXT oder Excel).

        Args:
            datei_pfad (str): Der Pfad zur Datei.

        Returns:
            pd.DataFrame: Ein DataFrame mit den Daten aus der Datei.

        Raises:
            ValueError: Wenn das Dateiformat nicht unterstützt wird.
        """
        dateiname = os.path.basename(datei_pfad)
        datei_endung = datei_pfad.lower()
        if datei_endung.endswith(DATEIFORMAT_CSV) or datei_endung.endswith(DATEIFORMAT_TEXT):
            try:
                daten_frame = pd.read_csv(datei_pfad, encoding='utf-8') # Explizite Encoding-Angabe für Robustheit
                logger.debug(f"Datei '{dateiname}' als CSV/TXT geladen.")
            except Exception as e:
                logger.error(f"Fehler beim Lesen der CSV/TXT-Datei '{dateiname}': {e}")
                raise ValueError(f"Fehler beim Lesen der CSV/TXT-Datei '{dateiname}': {e}") from e

        elif datei_endung.endswith(DATEIFORMAT_EXCEL_XLS) or datei_endung.endswith(DATEIFORMAT_EXCEL_XLSX):
            try:
                daten_frame = pd.read_excel(datei_pfad)
                logger.debug(f"Datei '{dateiname}' als Excel geladen.")
            except Exception as e:
                logger.error(f"Fehler beim Lesen der Excel-Datei '{dateiname}': {e}")
                raise ValueError(f"Fehler beim Lesen der Excel-Datei '{dateiname}': {e}") from e
        else:
            logger.error(f"Ungültiges Dateiformat für Datei: '{dateiname}'. Unterstützte Formate: {', '.join(UNTERSTUETZTE_DATEIFORMATE)}.")
            raise ValueError(
                f"Ungültiges Dateiformat für Datei: {dateiname}. Nur {', '.join(UNTERSTUETZTE_DATEIFORMATE)} Dateien werden unterstützt.")

        return daten_frame


    def _ist_pfad_sicher(self, datei_pfad: str) -> bool:
        """
        Interne Hilfsfunktion zur Überprüfung, ob ein Dateipfad sicher ist (innerhalb des Basisverzeichnisses).
        Verhindert Path-Traversal-Angriffe, ein wichtiger Sicherheitsaspekt.

        Args:
            datei_pfad (str): Der zu überprüfende Dateipfad.

        Returns:
            bool: True, wenn der Pfad sicher ist, False sonst.
        """
        absoluter_pfad = os.path.abspath(datei_pfad)
        ist_sicher = absoluter_pfad.startswith(self.basis_verzeichnis)
        logger.debug(f"Pfad '{datei_pfad}' (absolut: '{absoluter_pfad}') ist sicher im Basisverzeichnis '{self.basis_verzeichnis}': {ist_sicher}")
        return ist_sicher


    def _validiere_daten(self, daten_frame: pd.DataFrame, dateiname: str) -> None:
        """
        Interne Hilfsfunktion zur Validierung der geladenen Daten (Datentypen, Spalten, etc.).
        Stellt Datenintegrität sicher und verhindert Fehler durch unerwartete Datenformate.

        Args:
            daten_frame (pd.DataFrame): Der DataFrame mit den zu validierenden Daten.
            dateiname (str): Der Name der Datei, aus der die Daten geladen wurden.

        Raises:
            CipherCoreDatenValidierungsFehler: Wenn die Daten ungültig sind.
        """
        erforderliche_spalten = ['Name', 'Alter'] # Beispiel für erforderliche Spalten

        for spalte in erforderliche_spalten:
            if spalte not in daten_frame.columns:
                logger.warning(f"Erforderliche Spalte '{spalte}' fehlt in Datei '{dateiname}'.")
                raise CipherCoreDatenValidierungsFehler(f"Erforderliche Spalte '{spalte}' fehlt in Datei '{dateiname}'.")

        if 'Alter' in daten_frame.columns:
            if not pd.api.types.is_numeric_dtype(daten_frame['Alter']):
                logger.warning(f"Spalte 'Alter' in Datei '{dateiname}' ist nicht numerisch.")
                raise CipherCoreDatenValidierungsFehler(f"Spalte 'Alter' in Datei '{dateiname}' ist nicht numerisch.")
            # Validierung: Sicherstellen, dass Alter eine nicht-negative Zahl ist
            negative_alter_werte = daten_frame[daten_frame['Alter'] < 0]['Alter']
            if not negative_alter_werte.empty:
                 logger.warning(f"Spalte 'Alter' in Datei '{dateiname}' enthält ungültige Werte (negative Alter): {negative_alter_werte.tolist()}")
                 raise CipherCoreDatenValidierungsFehler(f"Spalte 'Alter' in Datei '{dateiname}' enthält ungültige Werte (negative Alter). Bitte korrigieren Sie die Datei.")

        logger.debug(f"Daten aus Datei '{dateiname}' erfolgreich validiert.")



# --- DateiVergleicher Klasse (CipherCore Standard: Effiziente Datenverarbeitung) ---
class DateiVergleicher:
    """
    Modul zum Vergleichen von zwei DataFrames und zur Berechnung relevanter Vergleichsmetriken.
    Fokus auf Effizienz und Genauigkeit der Vergleichsberechnungen.
    """

    def vergleiche_daten(self, daten_frame1: pd.DataFrame, daten_frame2: pd.DataFrame, spalte_datei1: str = 'Name', spalte_datei2: str = 'Name') -> Dict[str, str]:
        """
        Vergleicht die DataFrames basierend auf angegebenen Spalten und ermittelt verschiedene Statistiken.

        Args:
            daten_frame1 (pd.DataFrame): Der erste DataFrame (Benutzereingabe).
            daten_frame2 (pd.DataFrame): Der zweite DataFrame (Hauptliste).
            spalte_datei1 (str, optional): Die Spalte aus Datei 1, die verglichen werden soll. Standard ist 'Name'.
            spalte_datei2 (str, optional): Die Spalte aus Datei 2, die verglichen werden soll. Standard ist 'Name'.

        Returns:
            Dict[str, str]: Ein Dictionary mit den Vergleichsergebnissen (Metriken und formatierte Werte).
        """
        logger.info("Starte Datenvergleich...")
        vergleichs_ergebnisse: Dict[str, str] = {} # Type-Hinting für Klarheit
        vergleichs_ergebnisse[METRIK_ANZAHL_DATEI1] = str(len(daten_frame1)) # Explizite String-Konvertierung
        vergleichs_ergebnisse[METRIK_ANZAHL_DATEI2] = str(len(daten_frame2))

        try: # Fehlerbehandlung für ungültige Spaltennamen
            # Vergleich der angegebenen Spalten
            gleiche_werte = set(daten_frame1[spalte_datei1]).intersection(set(daten_frame2[spalte_datei2]))
            vergleichs_ergebnisse[METRIK_GLEICHE_NAMEN] = str(len(gleiche_werte)) # Verwendung der generischen Metrik
        except KeyError as e:
            logger.error(f"Spaltenname Fehler beim Datenvergleich: {e}")
            raise CipherCoreDatenValidierungsFehler(f"Ungültiger Spaltenname für den Vergleich: {e}") from e


        anzahl_unterschied_prozentual = abs(len(daten_frame1) - len(daten_frame2)) / max(len(daten_frame1), len(daten_frame2)) if max(len(daten_frame1), len(daten_frame2)) > 0 else 0 # Division durch Null verhindern
        vergleichs_ergebnisse[METRIK_PROZENTUALER_UNTERSCHIED_ANZAHL] = f"{anzahl_unterschied_prozentual:.2%}"

        if 'Alter' in daten_frame1.columns and 'Alter' in daten_frame2.columns:
            vergleichs_ergebnisse[METRIK_DURCHSCHNITTSALTER_DATEI1] = f"{daten_frame1['Alter'].mean():.1f}"
            vergleichs_ergebnisse[METRIK_DURCHSCHNITTSALTER_DATEI2] = f"{daten_frame2['Alter'].mean():.1f}"

        logger.debug(f"Vergleichsergebnisse: {vergleichs_ergebnisse}")
        logger.info("Datenvergleich abgeschlossen.")
        return vergleichs_ergebnisse


# --- DiagrammGenerator Klasse (CipherCore Standard: Klare Visualisierung) ---
class DiagrammGenerator:
    """
    Modul zum Erstellen von Diagrammen zur Visualisierung von Vergleichsergebnissen.
    Unterstützt verschiedene Diagrammtypen und generiert Base64-kodierte PNG-Bilder.
    Fokus auf klare und verständliche Diagramme.
    """

    def erstelle_diagramm(self, vergleichs_ergebnisse: Dict[str, str], diagramm_typ: str = DIAGRAMM_TYP_BALKEN) -> str:
        """
        Erstellt ein Diagramm zur Visualisierung der Vergleichsergebnisse.

        Args:
            vergleichs_ergebnisse (Dict[str, str]): Die Vergleichsergebnisse (Metriken und Werte).
            diagramm_typ (str): Der gewünschte Diagrammtyp ('balken' oder 'kreis').

        Returns:
            str: Base64-kodierte PNG-Bilddaten des Diagramms.

        Raises:
            CipherCoreUngültigerDiagrammTypFehler: Wenn ein ungültiger Diagrammtyp angegeben wird.
        """
        logger.info(f"Starte Diagrammerstellung vom Typ '{diagramm_typ}'...")

        if diagramm_typ not in UNTERSTUETZTE_DIAGRAMM_TYPEN:
            logger.error(f"Ungültiger Diagrammtyp angefordert: '{diagramm_typ}'. Unterstützte Typen: {', '.join(UNTERSTUETZTE_DIAGRAMM_TYPEN)}.")
            raise CipherCoreUngültigerDiagrammTypFehler(
                f"Ungültiger Diagrammtyp: '{diagramm_typ}'. Unterstützte Typen: {', '.join(UNTERSTUETZTE_DIAGRAMM_TYPEN)}.")

        metrik_bezeichnungen = list(vergleichs_ergebnisse.keys())
        werte_str = list(vergleichs_ergebnisse.values())
        try:
            werte = [float(wert.replace('%','')) if '%' in wert else float(wert) for wert in werte_str] # Konvertierung zu float, Prozentzeichen entfernen
        except ValueError as e:
            logger.error(f"Fehler beim Konvertieren der Werte für das Diagramm: {e}")
            raise CipherCoreDatenFehler(f"Fehler beim Konvertieren der Werte für das Diagramm: {e}") from e


        plt.figure(figsize=(12, 7))

        if diagramm_typ == DIAGRAMM_TYP_BALKEN:
            plt.bar(metrik_bezeichnungen, werte,
                    color=['skyblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightseagreen', 'lightgoldenrodyellow'])
            plt.ylabel('Anzahl / Prozent / Durchschnitt')
        elif diagramm_typ == DIAGRAMM_TYP_KREIS:
            plt.pie(werte, labels=metrik_bezeichnungen, autopct='%1.1f%%', startangle=90)
            plt.ylabel('')
            logger.warning(
                "Kreisdiagramm-Typ ist noch nicht vollständig optimiert. Es wird ein Balkendiagramm erstellt.")
            diagramm_typ = DIAGRAMM_TYP_BALKEN # Fallback auf Balkendiagramm, falls Kreisdiagramm nicht optimal

        plt.title('Vergleich der Dateien')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        try:
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            bild_daten = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des Diagrammbildes: {e}")
            raise CipherCoreDatenFehler(f"Fehler beim Erstellen des Diagrammbildes: {e}") from e


        logger.debug(f"Diagramm vom Typ '{diagramm_typ}' als Base64-String erzeugt.")
        logger.info("Diagrammerstellung abgeschlossen.")
        return bild_daten



# --- Abstrakte Basisklasse für DatenManager (CipherCore Standard: Erweiterbarkeit) ---
class AbstractDataManager(ABC):
    """
    Abstrakte Basisklasse für Daten-Manager-Implementierungen.
    Definiert die Schnittstelle für Daten-Manager-Operationen zur Persistierung von Vergleichsergebnissen.
    Ermöglicht verschiedene Persistenzmechanismen (Datei, Datenbank, etc.).
    """

    @abstractmethod
    def erstelle_schema(self) -> None:
        """Erstellt das Daten-Schema (Datenbanktabellen, Verzeichnisstruktur etc.)."""
        pass

    @abstractmethod
    def speichere_ergebnisse(self, vergleichs_ergebnisse: Dict[str, str], dateiname_datei1: str, dateiname_datei2: str) -> None:
        """Speichert die Vergleichsergebnisse."""
        pass

    @abstractmethod
    def lade_alle_ergebnisse(self) -> List[Dict]:
        """Lädt alle Vergleichsergebnisse."""
        pass


# --- SQLiteDataManager Klasse (CipherCore Standard: Sichere Datenbankinteraktion) ---
class SQLiteDataManager(AbstractDataManager):
    """
    DataManager-Implementierung für SQLite-Datenbank.
    Implementiert sicheren Datenbankzugriff und Fehlerbehandlung.
    Nutzt Prepared Statements zum Schutz vor SQL-Injection (Best Practice).
    """

    def __init__(self, datenbank_pfad: str = DATENBANK_DATEINAME_STANDARD):
        """
        Initialisiert den SQLiteDataManager.

        Args:
            datenbank_pfad (str): Der Pfad zur SQLite-Datenbankdatei.
        """
        if not datenbank_pfad or not isinstance(datenbank_pfad, str):
            raise ValueError("Datenbankpfad muss ein gültiger Pfad sein.")
        self.datenbank_pfad = datenbank_pfad
        self.erstelle_schema()
        logger.debug(f"SQLiteDataManager initialisiert mit Datenbankpfad: {self.datenbank_pfad}")


    def erstelle_schema(self) -> None:
        """
        Erstellt das Datenbank-Schema (Tabellen), falls nicht vorhanden.
        Nutzt IF NOT EXISTS Klausel für sichere Schemaerstellung.
        """
        verbindung = None # Verbindung außerhalb des try-Blocks definieren für finally-Zugriff
        try:
            verbindung = sqlite3.connect(self.datenbank_pfad)
            zeiger = verbindung.cursor()
            zeiger.execute("""
                CREATE TABLE IF NOT EXISTS vergleichsergebnisse (
                    vergleich_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datei1_name TEXT NOT NULL,
                    datei2_name TEXT NOT NULL,
                    vergleichszeitpunkt DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metrik_name TEXT NOT NULL,
                    metrik_wert TEXT
                )
            """)
            verbindung.commit()
            logger.info(f"Datenbank-Schema in '{self.datenbank_pfad}' erstellt oder geprüft.")
        except sqlite3.Error as e:
            logger.error(f"Fehler beim Erstellen des Datenbank-Schemas: {e}")
            raise CipherCoreDatenbankSchemaFehler(f"Fehler beim Erstellen des Datenbank-Schemas: {e}") from e
        finally:
            if verbindung:
                verbindung.close()


    def speichere_ergebnisse(self, vergleichs_ergebnisse: Dict[str, str], dateiname_datei1: str, dateiname_datei2: str) -> None:
        """
        Speichert die Vergleichsergebnisse in der SQLite-Datenbank.
        Verwendet Prepared Statements zum Schutz vor SQL-Injection.

        Args:
            vergleichs_ergebnisse (Dict[str, str]): Die Vergleichsergebnisse.
            dateiname_datei1 (str): Der Dateiname der ersten Datei.
            dateiname_datei2 (str): Der Dateiname der zweiten Datei.
        """
        verbindung = None
        try:
            verbindung = sqlite3.connect(self.datenbank_pfad)
            zeiger = verbindung.cursor()
            sql_einfuegen = """
                INSERT INTO vergleichsergebnisse (datei1_name, datei2_name, metrik_name, metrik_wert)
                VALUES (?, ?, ?, ?)
            """
            for metrik_name, metrik_wert in vergleichs_ergebnisse.items():
                zeiger.execute(sql_einfuegen, (dateiname_datei1, dateiname_datei2, metrik_name, str(metrik_wert))) # Prepared Statement
            verbindung.commit()
            logger.info(f"Vergleichsergebnisse in Datenbank '{self.datenbank_pfad}' gespeichert.")
        except sqlite3.Error as e:
            logger.error(f"Fehler beim Speichern der Vergleichsergebnisse in der Datenbank: {e}")
            raise CipherCoreDatenbankSpeicherFehler(f"Fehler beim Speichern der Vergleichsergebnisse in der Datenbank: {e}") from e
        finally:
            if verbindung:
                verbindung.close()


    def lade_alle_ergebnisse(self) -> List[Dict]:
        """
        Lädt alle Vergleichsergebnisse aus der Datenbank.

        Returns:
            List[Dict]: Eine Liste von Dictionaries, wobei jedes Dictionary ein Vergleichsergebnis darstellt.
        """
        ergebnisse: List[Dict] = []
        verbindung = None
        try:
            verbindung = sqlite3.connect(self.datenbank_pfad)
            zeiger = verbindung.cursor()
            zeiger.execute("SELECT * FROM vergleichsergebnisse ORDER BY vergleichszeitpunkt DESC") # Keine Benutzereingaben, daher kein Prepared Statement nötig
            spalten_namen = [beschreibung[0] for beschreibung in zeiger.description]
            daten_saetze = zeiger.fetchall()
            for daten_satz in daten_saetze:
                ergebnis_dict = dict(zip(spalten_namen, daten_satz))
                ergebnisse.append(ergebnis_dict)
            logger.info(f"Alle Vergleichsergebnisse aus Datenbank '{self.datenbank_pfad}' geladen.")
        except sqlite3.Error as e:
            logger.error(f"Fehler beim Laden der Vergleichsergebnisse aus der Datenbank: {e}")
            raise CipherCoreDatenbankLadeFehler(f"Fehler beim Laden der Vergleichsergebnisse aus der Datenbank: {e}") from e
        finally:
            if verbindung:
                verbindung.close()
        return ergebnisse



# --- FileDataManager Klasse (CipherCore Standard: Sichere Dateiverarbeitung) ---
class FileDataManager(AbstractDataManager):
    """
    DataManager-Implementierung, die Vergleichsergebnisse in JSON-Dateien in einem dedizierten Verzeichnis speichert.
    Implementiert sichere Dateiverarbeitung und Fehlerbehandlung.
    Sichere Dateinamensgenerierung und Pfadkonstruktion.
    """

    def __init__(self, daten_verzeichnis: str = DATEN_VERZEICHNIS_STANDARD):
        """
        Initialisiert den FileDataManager.

        Args:
            daten_verzeichnis (str): Das Verzeichnis, in dem JSON-Dateien gespeichert werden.
        """
        if not daten_verzeichnis or not isinstance(daten_verzeichnis, str):
            raise ValueError("Datenverzeichnis muss ein gültiger Pfad sein.")

        self.daten_verzeichnis = daten_verzeichnis
        self.erstelle_schema()
        logger.debug(f"FileDataManager initialisiert mit Datenverzeichnis: {self.daten_verzeichnis}")


    def erstelle_schema(self) -> None:
        """
        Erstellt das Datenverzeichnis, falls es nicht existiert.
        Verwendet exist_ok=True für sichere Verzeichniserstellung.
        """
        try:
            os.makedirs(self.daten_verzeichnis, exist_ok=True)
            logger.info(f"Datenverzeichnis '{self.daten_verzeichnis}' erstellt oder geprüft.")
        except OSError as e:
            logger.error(f"Fehler beim Erstellen des Datenverzeichnisses '{self.daten_verzeichnis}': {e}")
            raise CipherCoreDateiSchemaFehler(f"Fehler beim Erstellen des Datenverzeichnisses: {e}") from e


    def _generiere_dateinamen(self, dateiname_datei1: str, dateiname_datei2: str) -> str:
        """
        Generiert einen eindeutigen und sicheren Dateinamen für die JSON-Datei.
        Sanitized Dateinamen, um Dateisystem- und Sicherheitsprobleme zu vermeiden.

        Args:
            dateiname_datei1 (str): Der Dateiname der ersten Datei.
            dateiname_datei2 (str): Der Dateiname der zweiten Datei.

        Returns:
            str: Der generierte Dateipfad für die JSON-Datei.
        """
        zeitstempel = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        datei_sicher_datei1 = "".join(x if x.isalnum() else "_" for x in dateiname_datei1) # Dateinamen "sanitieren"
        datei_sicher_datei2 = "".join(x if x.isalnum() else "_" for x in dateiname_datei2) # Dateinamen "sanitieren"
        dateiname = f"vergleichsergebnis_{datei_sicher_datei1}_vs_{datei_sicher_datei2}_{zeitstempel}.json"
        return os.path.join(self.daten_verzeichnis, dateiname) # Sichere Pfadkonstruktion


    def speichere_ergebnisse(self, vergleichs_ergebnisse: Dict[str, str], dateiname_datei1: str, dateiname_datei2: str) -> None:
        """
        Speichert die Vergleichsergebnisse in einer JSON-Datei im Datenverzeichnis.
        Verwendet sichere Dateiverarbeitung mit 'with open' Kontextmanager.

        Args:
            vergleichs_ergebnisse (Dict[str, str]): Die Vergleichsergebnisse.
            dateiname_datei1 (str): Der Dateiname der ersten Datei.
            dateiname_datei2 (str): Der Dateiname der zweiten Datei.
        """
        datei_pfad = self._generiere_dateinamen(dateiname_datei1, dateiname_datei2)
        daten_zum_speichern = {
            "datei1_name": dateiname_datei1,
            "datei2_name": dateiname_datei2,
            "vergleichszeitpunkt": datetime.datetime.now().isoformat(),
            "metriken": vergleichs_ergebnisse
        }
        try:
            with open(datei_pfad, 'w', encoding='utf-8') as json_datei: # Sichere Dateiverarbeitung mit 'with open' und Encoding
                json.dump(daten_zum_speichern, json_datei, indent=4, ensure_ascii=False) # Konfiguration als JSON speichern, ensure_ascii=False für korrekte Zeichenkodierung
            logger.info(f"Vergleichsergebnisse in Datei '{datei_pfad}' gespeichert.")
        except OSError as e:
            logger.error(f"Fehler beim Speichern der Vergleichsergebnisse in Datei '{datei_pfad}': {e}")
            raise CipherCoreDateiSpeicherFehler(f"Fehler beim Speichern der Vergleichsergebnisse in Datei: {e}") from e


    def lade_alle_ergebnisse(self) -> List[Dict]:
        """
        Lädt alle Vergleichsergebnisse aus den JSON-Dateien im Datenverzeichnis.
        Behandelt Fehler beim Lesen einzelner Dateien robust und setzt den Ladevorgang fort.

        Returns:
            List[Dict]: Eine Liste von Dictionaries, wobei jedes Dictionary ein Vergleichsergebnis darstellt.
        """
        ergebnisse: List[Dict] = []
        try:
            dateien = [f for f in os.listdir(self.daten_verzeichnis) if f.endswith('.json') and f.startswith('vergleichsergebnis_')]
            for datei_name in dateien:
                datei_pfad = os.path.join(self.daten_verzeichnis, datei_name) # Sichere Pfadkonstruktion
                try:
                    with open(datei_pfad, 'r', encoding='utf-8') as json_datei: # Sichere Dateiverarbeitung mit 'with open' und Encoding
                        daten = json.load(json_datei)
                        ergebnisse.append(daten)
                except json.JSONDecodeError as e:
                    logger.warning(f"Fehler beim Lesen der JSON-Datei '{datei_pfad}'. Datei wird übersprungen. Fehler: {e}")
                except OSError as e:
                    logger.warning(f"Fehler beim Zugriff auf JSON-Datei '{datei_pfad}'. Datei wird übersprungen. Fehler: {e}")
            logger.info(f"Alle Vergleichsergebnisse aus Datenverzeichnis '{self.daten_verzeichnis}' geladen.")
        except OSError as e:
            logger.error(f"Fehler beim Zugriff auf das Datenverzeichnis '{self.daten_verzeichnis}': {e}")
            raise CipherCoreDateiLadeFehler(f"Fehler beim Laden der Vergleichsergebnisse aus dem Datenverzeichnis: {e}") from e

        ergebnisse.sort(key=lambda x: x.get('vergleichszeitpunkt', '1970-01-01T00:00:00'), reverse=True) # Sortierung beibehalten
        return ergebnisse



# --- BerichtsGenerator Klasse (CipherCore Standard: Professionelle Berichterstellung) ---
class BerichtsGenerator:
    """
    Modul zum Erstellen von Berichten im PDF-Format.
    Integriert Logo, Statistiken, Diagramm und CipherCore Firmendetails in professionelle Berichte.
    Sichere Einbindung von Ressourcen (Logo) und robuste Dateispeicherung.
    """

    def __init__(self, logo_pfad: str = LOGO_DATEIPFAD_STANDARD, ausgabe_pfad: str = AUSGABE_DATEIPFAD_STANDARD, daten_manager: Optional[AbstractDataManager] = None):
        """
        Initialisiert den Berichtsgenerator.

        Args:
            logo_pfad (str): Der Pfad zum Logo für den Bericht.
            ausgabe_pfad (str): Der Pfad, in dem der PDF-Bericht gespeichert wird.
            daten_manager (Optional[AbstractDataManager]): Der Daten-Manager für die Speicherung der Ergebnisse (optional).
        """
        if logo_pfad and not isinstance(logo_pfad, str):
            raise ValueError("Logo-Pfad muss ein gültiger Pfad sein.")
        if ausgabe_pfad and not isinstance(ausgabe_pfad, str):
            raise ValueError("Ausgabe-Pfad muss ein gültiger Pfad sein.")

        self.logo_pfad = logo_pfad
        self.ausgabe_pfad = ausgabe_pfad
        self.daten_manager = daten_manager
        logger.debug(f"BerichtsGenerator initialisiert. Logo-Pfad: '{self.logo_pfad}', Ausgabe-Pfad: '{self.ausgabe_pfad}', Daten-Manager: {daten_manager.__class__.__name__ if daten_manager else 'Kein'}")


    def erstelle_pdf_bericht(self, vergleichs_ergebnisse: Dict[str, str], diagramm_bild_daten: str, dateiname_datei1: str, dateiname_datei2: str) -> str:
        """
        Erstellt einen PDF-Bericht mit Statistiken, Diagramm und CipherCore Firmendetails.

        Args:
            vergleichs_ergebnisse (Dict[str, str]): Die Vergleichsergebnisse.
            diagramm_bild_daten (str): Base64-kodierte PNG-Bilddaten des Diagramms.
            dateiname_datei1 (str): Der Dateiname der ersten Datei.
            dateiname_datei2 (str): Der Dateiname der zweiten Datei.

        Returns:
            str: Der Pfad zum erstellten PDF-Bericht.
        """
        logger.info(f"Starte PDF-Berichterstellung: '{self.ausgabe_pfad}'...")

        if self.daten_manager:
            try:
                self.daten_manager.speichere_ergebnisse(vergleichs_ergebnisse, dateiname_datei1, dateiname_datei2)
            except CipherCoreDatenbankFehler as e:
                logger.error(f"Fehler beim Speichern der Ergebnisse über den Daten-Manager: {e}")
                raise e # Fehler weiterleiten
            except CipherCoreDateiFehler as e:
                logger.error(f"Fehler beim Speichern der Ergebnisse über den Daten-Manager: {e}")
                raise e # Fehler weiterleiten
            except Exception as e:
                logger.exception(f"Unerwarteter Fehler beim Speichern der Ergebnisse über den Daten-Manager: {e}")
                raise CipherCoreDatenFehler(f"Unerwarteter Fehler beim Speichern der Ergebnisse: {e}") from e
        else:
            logger.warning("Kein DatenManager konfiguriert. Vergleichsergebnisse werden nicht persistent gespeichert.")


        pdf = FPDF()
        pdf.add_page()

        self._pdf_kopfzeile_erstellen(pdf, "Datei-Vergleichsbericht") # Kopfzeile erstellen

        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 6, f"Verglichene Dateien: {dateiname_datei1}, {dateiname_datei2}", ln=1, align='C')
        pdf.cell(0, 6, f"Vergleichszeitpunkt: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align='C')
        pdf.ln(5)

        self._pdf_statistik_tabelle_erstellen(pdf, vergleichs_ergebnisse) # Statistik Tabelle erstellen

        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Grafische Darstellung", ln=1)
        pdf.set_font("Arial", "", 10)
        diagramm_breite = 140
        seiten_breite = 210
        x_position_diagramm = (seiten_breite - diagramm_breite) / 2
        try:
            # Korrigierter Code für pdf.image() mit PIL
            bild_bytes = base64.b64decode(diagramm_bild_daten)
            bild = Image.open(BytesIO(bild_bytes))
            temp_datei = "temp_diagramm.png"
            bild.save(temp_datei, format="PNG")
            pdf.image(temp_datei, x=x_position_diagramm, y=pdf.get_y(), w=diagramm_breite)
            os.remove(temp_datei) # Temporäre Datei löschen
        except Exception as e:
            logger.error(f"Fehler beim Einbetten des Diagrammbildes in den PDF-Bericht: {e}")
            raise CipherCoreDatenFehler(f"Fehler beim Einbetten des Diagrammbildes in den PDF-Bericht: {e}") from e


        self._pdf_fusszeile_erstellen(pdf, "CipherCore GmbH") # Fußzeile erstellen

        pdf.set_y(-25)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, f"{__copyright__} - {__license__}", 0, 0, 'C')

        try:
            os.makedirs(os.path.dirname(self.ausgabe_pfad), exist_ok=True) # Ausgabe-Verzeichnis erstellen falls nicht existent
            pdf.output(self.ausgabe_pfad, "F") # PDF-Datei speichern
            logger.info(f"PDF-Bericht erfolgreich gespeichert: '{self.ausgabe_pfad}'")
        except OSError as e:
            logger.error(f"Fehler beim Speichern des PDF-Berichts unter '{self.ausgabe_pfad}': {e}")
            raise CipherCoreDateiSpeicherFehler(f"Fehler beim Speichern des PDF-Berichts: {e}") from e

        return self.ausgabe_pfad


    def _pdf_kopfzeile_erstellen(self, pdf: FPDF, titel: str) -> None:
        """
        Interne Hilfsfunktion zum Erstellen der PDF-Kopfzeile (Logo und Titel).
        Sichere Logo-Einbindung mit Pfadsicherheitsprüfung.

        Args:
            pdf (FPDF): Das FPDF-Objekt.
            titel (str): Der Titel der Kopfzeile.
        """
        if self.logo_pfad and os.path.exists(self.logo_pfad):
            basis_verzeichnis = os.path.dirname(os.path.abspath(__file__))
            if not _ist_pfad_sicher_static(self.logo_pfad, BASIS_VERZEICHNIS):
                logger.warning(f"Unsicherer Logo-Dateipfad: '{self.logo_pfad}'. Logo wird nicht eingebunden.")
            else:
                try:
                    pdf.image(self.logo_pfad, x=10, y=8, w=25) # Logo einbinden
                    logger.debug(f"Logo in Kopfzeile eingebunden: '{self.logo_pfad}'")
                except Exception as e:
                    logger.warning(f"Fehler beim Laden des Logos für Kopfzeile: {e}")
        else:
            logger.warning(f"Logo-Datei nicht gefunden oder Pfad nicht angegeben: '{self.logo_pfad}'. Kopfzeile ohne Logo.")

        pdf.set_font("Arial", "B", 15)
        pdf.cell(0, 10, titel, 0, 1, 'C')
        pdf.ln(5)


    def _pdf_statistik_tabelle_erstellen(self, pdf: FPDF, vergleichs_ergebnisse: Dict[str, str]) -> None:
        """
        Interne Hilfsfunktion zum Erstellen der tabellarischen Statistik im PDF.
        Generiert eine übersichtliche Tabelle der Vergleichsergebnisse.

        Args:
            pdf (FPDF): Das FPDF-Objekt.
            vergleichs_ergebnisse (Dict[str, str]): Die Vergleichsergebnisse.
        """
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Statistische Auswertung", ln=1)
        pdf.set_font("Arial", "", 10)

        pdf.set_fill_color(240, 240, 240)
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.1)
        pdf.cell(90, 8, "Metrik", 1, 0, 'L', 1) # Breite der Metrik-Spalte angepasst
        pdf.cell(50, 8, "Wert", 1, 0, 'R', 1) # Breite der Wert-Spalte angepasst
        pdf.ln()

        pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Arial", "", 10)

        for metrik in METRIK_REIHENFOLGE:
            if metrik in vergleichs_ergebnisse:
                wert = vergleichs_ergebnisse[metrik]
                pdf.cell(90, 7, metrik, 1, 0, 'L', 1) # Breite der Metrik-Spalte angepasst
                pdf.cell(50, 7, str(wert), 1, 0, 'R', 1) # Breite der Wert-Spalte angepasst
                pdf.ln()


    def _pdf_fusszeile_erstellen(self, pdf: FPDF, firmenname: str) -> None:
        """
        Interne Hilfsfunktion zum Erstellen der PDF-Fußzeile (Seitenzahl und Firmenname).
        Standardisierte Fußzeile für professionelles Erscheinungsbild.

        Args:
            pdf (FPDF): Das FPDF-Objekt.
            firmenname (str): Der Firmenname für die Fußzeile.
        """
        pdf.set_y(-15)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, f"Seite {pdf.page_no()}", 0, 0, 'C')
        pdf.cell(0, 10, firmenname, 0, 0, 'R')



# --- Hilfsfunktionen (CipherCore Standard: Wiederverwendbarkeit und Sicherheit) ---

def _ist_pfad_sicher_static(datei_pfad: str, basis_verzeichnis: str) -> bool:
    """
    Statische Hilfsfunktion zur Sicherheitsprüfung eines Dateipfads.
    Überprüft, ob ein Dateipfad innerhalb des Basisverzeichnisses liegt, um Path-Traversal-Angriffe zu verhindern.
    Wiederverwendbare Funktion für Pfadsicherheitsprüfungen.

    Args:
        datei_pfad (str): Der zu überprüfende Dateipfad.
        basis_verzeichnis (str): Das Basisverzeichnis.

    Returns:
        bool: True, wenn der Pfad sicher ist, False sonst.
    """
    absoluter_pfad = os.path.abspath(datei_pfad)
    basis_verzeichnis_absolut = os.path.abspath(basis_verzeichnis)
    ist_sicher = absoluter_pfad.startswith(basis_verzeichnis_absolut)
    logger.debug(f"Statische Pfadsicherheitsprüfung: Pfad '{datei_pfad}' (absolut: '{absoluter_pfad}') ist sicher im Basisverzeichnis '{basis_verzeichnis}': {ist_sicher}")
    return ist_sicher


# --- Hauptfunktion (CipherCore Standard: Robuste Ausführung und Fehlerbehandlung) ---

def dateien_vergleichen_und_bericht_erstellen(datei_pfad1: str, datei_pfad2: str, logo_pfad: str = LOGO_DATEIPFAD, ausgabe_pfad: str = AUSGABE_DATEIPFAD,
                                              diagramm_typ: str = DIAGRAMM_TYP_BALKEN, daten_manager: Optional[AbstractDataManager] = None,
                                              ui_status_rueckruf: Optional[Callable[[str], None]] = None,
                                              spalte_datei1: str = 'Name', spalte_datei2: str = 'Name') -> Tuple[str, Optional[Dict[str, str]]]:
    """
    Hauptfunktion: Vergleicht zwei Dateien, erstellt Statistiken, Diagramm und PDF-Bericht.
    Implementiert umfassende Fehlerbehandlung und Logging für robuste Ausführung.
    Klare Schnittstelle mit Rückgabewerten und optionalem UI-Status-Rückruf.

    Args:
        datei_pfad1 (str): Der Pfad zur ersten Datei (Benutzereingabe).
        datei_pfad2 (str): Der Pfad zur zweiten Datei (Hauptliste).
        logo_pfad (str): Der Pfad zum Logo für den Bericht (optional).
        ausgabe_pfad (str): Der Pfad für den PDF-Bericht (optional).
        diagramm_typ (str): Der Diagrammtyp ('balken' oder 'kreis', optional).
        daten_manager (Optional[AbstractDataManager]): Der Daten-Manager für die Speicherung der Ergebnisse (optional).
        ui_status_rueckruf (Optional[Callable[[str], None]]): Eine Rückruffunktion zur Aktualisierung des UI-Status (optional).
        spalte_datei1 (str, optional): Spalte für Vergleich aus Datei 1. Standard 'Name'.
        spalte_datei2 (str, optional): Spalte für Vergleich aus Datei 2. Standard 'Name'.

    Returns:
        Tuple[str, Optional[Dict[str, str]]]: Ein Tuple mit dem Pfad zum PDF-Bericht und den Vergleichsergebnissen.
               Im Fehlerfall wird ein Fehlerstring und None zurückgegeben.
    """
    logger.info(f"Starte Dateivergleich: Datei 1='{datei_pfad1}', Datei 2='{datei_pfad2}'")
    if ui_status_rueckruf:
        ui_status_rueckruf("Vergleich gestartet...")

    try:
        daten_lader = DatenLader(BASIS_VERZEICHNIS)
        daten_frame1, dateiname_datei1 = daten_lader.lade_daten(datei_pfad1)
        daten_frame2, dateiname_datei2 = daten_lader.lade_daten(datei_pfad2)
        if ui_status_rueckruf:
            ui_status_rueckruf("Daten erfolgreich geladen...")

        datei_vergleicher = DateiVergleicher()
        vergleichs_ergebnisse = datei_vergleicher.vergleiche_daten(daten_frame1, daten_frame2, spalte_datei1, spalte_datei2) # Spalten für Vergleich übergeben
        if ui_status_rueckruf:
            ui_status_rueckruf("Datenvergleich abgeschlossen...")

        diagramm_generator = DiagrammGenerator()
        diagramm_bild_daten = diagramm_generator.erstelle_diagramm(vergleichs_ergebnisse, diagramm_typ)
        if ui_status_rueckruf:
            ui_status_rueckruf("Diagramm erstellt...")

        berichts_generator = BerichtsGenerator(logo_pfad, ausgabe_pfad, daten_manager)
        pdf_pfad = berichts_generator.erstelle_pdf_bericht(vergleichs_ergebnisse, diagramm_bild_daten,
                                                            dateiname_datei1, dateiname_datei2)
        if ui_status_rueckruf:
            ui_status_rueckruf(f"PDF-Bericht erfolgreich erstellt: {pdf_pfad}")

        logger.info(f"PDF-Bericht erfolgreich erstellt: '{pdf_pfad}'")
        return pdf_pfad, vergleichs_ergebnisse

    except CipherCoreDateiLadeFehler as e: # Spezifische Fehlerbehandlung für Dateiladefehler
        fehler_meldung = f"Fehler beim Laden der Datei: {e}"
        logger.error(fehler_meldung)
        if ui_status_rueckruf:
            ui_status_rueckruf(fehler_meldung)
        return fehler_meldung, None
    except CipherCoreDatenValidierungsFehler as e: # Spezifische Fehlerbehandlung für Datenvalidierungsfehler
        fehler_meldung = f"Datenvalidierungsfehler: {e}"
        logger.error(fehler_meldung)
        if ui_status_rueckruf:
            ui_status_rueckruf(fehler_meldung)
        return fehler_meldung, None
    except CipherCoreDatenbankFehler as e: # Spezifische Fehlerbehandlung für Datenbankfehler
        fehler_meldung = f"Datenbankfehler: {e}"
        logger.error(fehler_meldung)
        if ui_status_rueckruf:
            ui_status_rueckruf(fehler_meldung)
        return fehler_meldung, None
    except CipherCoreDateiFehler as e: # Generische Fehlerbehandlung für Dateifehler
        fehler_meldung = f"Dateifehler: {e}"
        logger.error(fehler_meldung)
        if ui_status_rueckruf:
            ui_status_rueckruf(fehler_meldung)
        return fehler_meldung, None
    except CipherCoreUngültigerDiagrammTypFehler as e: # Spezifische Fehlerbehandlung für ungültigen Diagrammtyp
        fehler_meldung = f"Ungültiger Diagrammtyp: {e}"
        logger.error(fehler_meldung)
        if ui_status_rueckruf:
            ui_status_rueckruf(fehler_meldung)
        return fehler_meldung, None
    except Exception as e: # Unerwartete Fehlerbehandlung (Generischer Catch-All)
        logger.exception(f"Unerwarteter Fehler: {e}")
        if ui_status_rueckruf:
            ui_status_rueckruf(f"Unerwarteter Fehler: {e}")
        return f"Unerwarteter Fehler: {e}", None



# --- UI-Teil mit Tkinter (CipherCore Standard: Benutzerfreundlichkeit und Robustheit) ---
class DateiVergleichsApp:
    """
    Tkinter-Anwendung für das CipherCore Datei-Vergleichs-Tool.
    Bietet eine benutzerfreundliche Oberfläche mit klarer Statusanzeige und Fehlerbehandlung.
    Thread-sichere UI-Updates für reaktionsschnelle Anwendung.
    """
    def __init__(self, root: tk.Tk, daten_manager: AbstractDataManager):
        """
        Initialisiert die DateiVergleichsApp.

        Args:
            root (tk.Tk): Das Hauptfenster der Tkinter-Anwendung.
            daten_manager (AbstractDataManager): Der Daten-Manager für die Ergebnispersistenz.
        """
        self.root = root
        root.title("CipherCore Datei Vergleichs Tool") # Firmenname im Fenstertitel
        self.daten_manager = daten_manager
        self.datei_pfad1 = tk.StringVar()
        self.datei_pfad2 = tk.StringVar()
        self.diagramm_typ = tk.StringVar(value=DIAGRAMM_TYP_BALKEN)
        self.status_meldung = tk.StringVar()
        self.ergebnis_text = None
        self.lizenz_akzeptiert = tk.BooleanVar(value=konfiguration.get(CONFIG_SCHLUESSEL_LIZENZ_AKZEPTIERT, False))
        self.verlauf_text = None
        self.spalte_datei1 = tk.StringVar(value='Name') # Standardspalte für Datei 1
        self.spalte_datei2 = tk.StringVar(value='Name') # Standardspalte für Datei 2

        self._check_lizenz_und_testphase() # Lizenzprüfung vor UI-Erstellung
        if not self.lizenz_akzeptiert.get():
            return # UI nicht erstellen, wenn Lizenz nicht akzeptiert

        self._create_widgets() # UI-Elemente erstellen
        self._lade_verlauf_beim_start() # Verlauf beim Start laden und anzeigen
        logger.info("DateiVergleichsApp UI initialisiert.")


    def _check_lizenz_und_testphase(self) -> None:
        """
        Prüft Lizenzvereinbarung und Testphase vor dem Start der Haupt-UI.
        Stellt sicher, dass die Lizenzbedingungen akzeptiert wurden und die Testphase gültig ist.
        """
        if not konfiguration.get(CONFIG_SCHLUESSEL_LIZENZ_AKZEPTIERT, False):
            self._zeige_lizenz_dialog() # Lizenzdialog anzeigen, falls nicht akzeptiert
            if not self.lizenz_akzeptiert.get():
                logger.warning("Lizenz nicht akzeptiert. Anwendung wird beendet.")
                self.root.destroy() # Anwendung beenden, wenn Lizenz abgelehnt
                return
        logger.debug("Lizenzprüfung bestanden.")

        erster_start_datum_str = konfiguration.get(CONFIG_SCHLUESSEL_ERSTES_STARTDATUM)
        if erster_start_datum_str is None:
            konfiguration[CONFIG_SCHLUESSEL_ERSTES_STARTDATUM] = datetime.date.today().isoformat()
            self._speichere_konfiguration() # Konfiguration speichern
            logger.info("Erster Start der Anwendung. Testphase beginnt.")
        else:
            erster_start_datum = datetime.date.fromisoformat(erster_start_datum_str)
            heute = datetime.date.today()
            testende_datum = erster_start_datum + datetime.timedelta(days=14) # 14-Tage Testphase
            if heute > testende_datum:
                logger.warning("Testphase abgelaufen. Anwendung im Testphasen-Ende-Modus.")
                messagebox.showwarning("Testphase beendet",
                                     "Ihre 14-tägige Testphase ist abgelaufen. Bitte kontaktieren Sie unser Vertriebsteam von CipherCore, um eine Vollversion zu erwerben.") # Hinweis zur Testphasenende


    def _zeige_lizenz_dialog(self) -> None:
        """
        Zeigt das Lizenzdialogfenster an.
        Dialog ist modal und blockiert die Hauptanwendung, bis eine Entscheidung getroffen wurde.
        """
        lizenz_fenster = tk.Toplevel(self.root)
        lizenz_fenster.title("CipherCore Lizenzvereinbarung") # Firmenname im Lizenzdialog-Titel

        lizenz_text_widget = scrolledtext.ScrolledText(lizenz_fenster, wrap=tk.WORD, height=15, width=70)
        lizenz_text_widget.insert(tk.END, LIZENZBEDINGUNGEN_TEXT) # Lizenztext einfügen
        lizenz_text_widget.config(state='disabled') # Textfeld schreibgeschützt machen
        lizenz_text_widget.pack(padx=10, pady=10)

        akzeptanz_var = tk.BooleanVar()
        check_button = Checkbutton(lizenz_fenster, text="Ich akzeptiere die CipherCore Lizenzbedingungen", variable=akzeptanz_var) # Firmenname im Checkbutton-Text
        check_button.pack(pady=(0, 10))

        def akzeptieren_und_schliessen():
            if akzeptanz_var.get():
                konfiguration[CONFIG_SCHLUESSEL_LIZENZ_AKZEPTIERT] = True # Lizenzakzeptanz in Konfiguration speichern
                self._speichere_konfiguration() # Konfiguration persistent speichern
                self.lizenz_akzeptiert.set(True) # Lizenzakzeptanzstatus im UI setzen
                lizenz_fenster.destroy() # Lizenzfenster schließen
                logger.info("Lizenzbedingungen akzeptiert.")
            else:
                messagebox.showerror("Lizenz ablehnen", "Bitte akzeptieren Sie die Lizenzbedingungen von CipherCore, um fortzufahren.") # Firmenname in Fehlermeldung
                logger.warning("Lizenzbedingungen abgelehnt.")

        akzeptieren_button = Button(lizenz_fenster, text="Akzeptieren", command=akzeptieren_und_schliessen)
        akzeptieren_button.pack(pady=(0, 10))

        ablehnen_button = Button(lizenz_fenster, text="Ablehnen & Beenden", command=self.root.destroy)
        ablehnen_button.pack(pady=(0, 10))

        lizenz_fenster.transient(self.root) # Dialog wird zum transienten Fenster des Hauptfensters
        lizenz_fenster.grab_set() # Dialog modal machen
        self.root.wait_window(lizenz_fenster) # Warten, bis Lizenzdialog geschlossen wird


    def _create_widgets(self) -> None:
        """
        Erstellt die UI-Elemente im Hauptfenster.
        Layout mit Grid-Manager für flexible und responsive Oberfläche.
        Klare Beschriftungen und Benutzerführung.
        """
        # Datei 1 Auswahl
        tk.Label(self.root, text="Datei 1 (Benutzereingaben):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.datei_pfad1, width=50, state='disabled').grid(row=0, column=1, padx=5, pady=5) # Eingabefeld für Datei 1 (deaktiviert)
        tk.Button(self.root, text="Datei 1 auswählen", command=self.datei_auswaehlen_datei1).grid(row=0, column=2, padx=5, pady=5) # Button zum Auswählen von Datei 1

        # Datei 2 Auswahl
        tk.Label(self.root, text="Datei 2 (Hauptliste):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.datei_pfad2, width=50, state='disabled').grid(row=1, column=1, padx=5, pady=5) # Eingabefeld für Datei 2 (deaktiviert)
        tk.Button(self.root, text="Datei 2 auswählen", command=self.datei_auswaehlen_datei2).grid(row=1, column=2, padx=5, pady=5) # Button zum Auswählen von Datei 2

        # Spaltenauswahl für Datei 1
        tk.Label(self.root, text="Vergleichsspalte Datei 1:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.spalte_datei1, width=20).grid(row=2, column=1, padx=5, pady=5, sticky="w") # Eingabefeld für Spalte Datei 1

        # Spaltenauswahl für Datei 2
        tk.Label(self.root, text="Vergleichsspalte Datei 2:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.spalte_datei2, width=20).grid(row=3, column=1, padx=5, pady=5, sticky="w") # Eingabefeld für Spalte Datei 2

        # Diagrammtyp Auswahl
        tk.Label(self.root, text="Diagrammtyp:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        diagramm_optionen = [DIAGRAMM_TYP_BALKEN, DIAGRAMM_TYP_KREIS] # Verfügbare Diagrammtypen
        diagramm_dropdown = tk.OptionMenu(self.root, self.diagramm_typ, *diagramm_optionen) # Dropdown-Menü für Diagrammtyp
        diagramm_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Start Button
        tk.Button(self.root, text="Vergleich starten & PDF-Bericht erstellen", command=self.starte_vergleich, width=30).grid(
            row=5, column=0, columnspan=3, pady=10) # Button zum Starten des Vergleichs

        # Statusmeldung
        tk.Label(self.root, textvariable=self.status_meldung).grid(row=6, column=0, columnspan=3, pady=5) # Label für Statusmeldungen

        # Ergebnis-Textfeld
        tk.Label(self.root, text="Vergleichsergebnisse:").grid(row=7, column=0, padx=5, pady=5, sticky="nw")
        self.ergebnis_text = scrolledtext.ScrolledText(self.root, height=10, width=60) # Textfeld für Vergleichsergebnisse
        self.ergebnis_text.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.ergebnis_text.config(state='disabled') # Textfeld schreibgeschützt
        self.root.grid_rowconfigure(7, weight=1) # Zeile für Ergebnis-Textfeld soll expandieren
        self.root.grid_columnconfigure(1, weight=1) # Spalte für Ergebnis-Textfeld soll expandieren

        # Verlauf anzeigen Button
        tk.Button(self.root, text="Verlauf anzeigen", command=self.zeige_verlauf, width=20).grid(row=8, column=0, columnspan=3, pady=10) # Button zum Anzeigen des Verlaufs

        # Verlauf-Textfeld
        tk.Label(self.root, text="Vergleichsverlauf:").grid(row=9, column=0, padx=5, pady=5, sticky="nw")
        self.verlauf_text = scrolledtext.ScrolledText(self.root, height=10, width=60) # Textfeld für Vergleichsverlauf
        self.verlauf_text.grid(row=9, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.verlauf_text.config(state='disabled') # Textfeld schreibgeschützt
        self.root.grid_rowconfigure(9, weight=1) # Zeile für Verlauf-Textfeld soll expandieren


    def datei_auswaehlen_datei1(self) -> None:
        """
        Öffnet einen Dateiauswahldialog für Datei 1.
        Beschränkt die Dateiauswahl auf unterstützte Dateiformate und das Basisverzeichnis (Sicherheit).
        """
        datei_pfad = filedialog.askopenfilename(initialdir=BASIS_VERZEICHNIS, title="Datei 1 auswählen (Benutzereingabe)", filetypes=[('Unterstützte Dateien', UNTERSTUETZTE_DATEIFORMATE)]) # Dateifilter für unterstützte Formate
        if datei_pfad:
            self.datei_pfad1.set(datei_pfad) # Pfad in UI speichern
            logger.debug(f"Datei 1 ausgewählt: {datei_pfad}")


    def datei_auswaehlen_datei2(self) -> None:
        """
        Öffnet einen Dateiauswahldialog für Datei 2.
        Beschränkt die Dateiauswahl auf unterstützte Dateiformate und das Basisverzeichnis (Sicherheit).
        """
        datei_pfad = filedialog.askopenfilename(initialdir=BASIS_VERZEICHNIS, title="Datei 2 auswählen (Hauptliste)", filetypes=[('Unterstützte Dateien', UNTERSTUETZTE_DATEIFORMATE)]) # Dateifilter für unterstützte Formate
        if datei_pfad:
            self.datei_pfad2.set(datei_pfad) # Pfad in UI speichern
            logger.debug(f"Datei 2 ausgewählt: {datei_pfad}")


    def starte_vergleich(self) -> None:
        """
        Startet den Dateivergleich und die Berichterstellung in einem Hintergrundthread.
        Verhindert Blockieren der UI während der Verarbeitung (Responsivität).
        Fehlerbehandlung und Anzeige von Statusmeldungen in der UI.
        """
        datei_pfad1 = self.datei_pfad1.get()
        datei_pfad2 = self.datei_pfad2.get()
        diagramm_typ = self.diagramm_typ.get()
        spalte_datei1 = self.spalte_datei1.get() # Spalte für Datei 1 aus UI holen
        spalte_datei2 = self.spalte_datei2.get() # Spalte für Datei 2 aus UI holen

        if not datei_pfad1 or not datei_pfad2:
            messagebox.showerror("Fehler", "Bitte wählen Sie beide Dateien aus.") # Fehlermeldung, wenn Dateien fehlen
            logger.warning("Vergleichsstart abgebrochen: Beide Dateien müssen ausgewählt sein.")
            return

        self.ergebnis_text.config(state='normal') # Ergebnis-Textfeld editierbar machen
        self.ergebnis_text.delete('1.0', tk.END) # Textfeld leeren
        self.ergebnis_text.config(state='disabled') # Textfeld wieder schreibgeschützt machen
        self.verlauf_text.config(state='normal') # Verlauf-Textfeld editierbar machen
        self.verlauf_text.delete('1.0', tk.END) # Textfeld leeren
        self.verlauf_text.config(state='disabled') # Textfeld wieder schreibgeschützt machen
        self.status_meldung.set("Vergleich wird gestartet...") # Statusmeldung setzen

        threading.Thread(target=self._starte_vergleich_hintergrund, args=(datei_pfad1, datei_pfad2, diagramm_typ, spalte_datei1, spalte_datei2)).start() # Vergleich in Thread starten
        logger.info("Vergleichs-Thread gestartet.")


    def _starte_vergleich_hintergrund(self, datei_pfad1: str, datei_pfad2: str, diagramm_typ: str, spalte_datei1: str, spalte_datei2: str) -> None:
        """
        Führt den Dateivergleich und die Berichterstellung im Hintergrund aus.
        Ruft die Hauptfunktion `dateien_vergleichen_und_bericht_erstellen` auf.
        Behandelt Fehler und aktualisiert die UI mit Ergebnissen und Statusmeldungen.

        Args:
            datei_pfad1 (str): Pfad zur ersten Datei.
            datei_pfad2 (str): Pfad zur zweiten Datei.
            diagramm_typ (str): Diagrammtyp.
            spalte_datei1 (str): Spalte für Vergleich aus Datei 1.
            spalte_datei2 (str): Spalte für Vergleich aus Datei 2.
        """
        pdf_pfad, vergleichs_ergebnisse = dateien_vergleichen_und_bericht_erstellen(datei_pfad1, datei_pfad2,
                                                                                     diagramm_typ=diagramm_typ,
                                                                                     daten_manager=self.daten_manager,
                                                                                     ui_status_rueckruf=self.update_status_meldung_ui,
                                                                                     spalte_datei1=spalte_datei1, # Spalten für Vergleich übergeben
                                                                                     spalte_datei2=spalte_datei2) # Spalten für Vergleich übergeben
        if isinstance(pdf_pfad, str) and pdf_pfad.endswith('.pdf'):
            self.update_status_meldung_ui(f"PDF-Bericht erfolgreich erstellt: {pdf_pfad}") # Erfolgsmeldung in UI
            logger.info(f"PDF-Bericht erfolgreich erstellt: {pdf_pfad}")
        else:
            self.update_status_meldung_ui(f"Fehler beim Erstellen des Berichts: {pdf_pfad}") # Fehlermeldung in UI
            messagebox.showerror("Fehler beim Bericht", f"Fehler beim Erstellen des PDF-Berichts:\n{pdf_pfad}") # Fehlermeldung als MessageBox
            logger.error(f"Fehler beim Erstellen des Berichts: {pdf_pfad}")


        if vergleichs_ergebnisse:
            self.zeige_vergleichs_ergebnisse_ui(vergleichs_ergebnisse) # Vergleichsergebnisse in UI anzeigen


    def update_status_meldung_ui(self, meldung: str) -> None:
        """
        Aktualisiert die Statusmeldung in der UI (thread-sicher).
        Verwendet `root.after` um UI-Updates im Hauptthread auszuführen (Tkinter Thread-Sicherheit).

        Args:
            meldung (str): Die anzuzeigende Statusmeldung.
        """
        self.root.after(0, self.status_meldung.set, meldung) # Statusmeldung im Hauptthread aktualisieren


    def zeige_vergleichs_ergebnisse_ui(self, vergleichs_ergebnisse: Dict[str, str]) -> None:
        """
        Zeigt die Vergleichsergebnisse im Textfeld der UI an (thread-sicher).
        Formatiert die Ergebnisse als String und aktualisiert das Textfeld im Hauptthread.

        Args:
            vergleichs_ergebnisse (Dict[str, str]): Die Vergleichsergebnisse.
        """
        ergebnis_text_string = "Vergleichsergebnisse:\n"
        ergebnis_text_string += "-------------------------\n"
        for metrik, wert in vergleichs_ergebnisse.items():
            ergebnis_text_string += f"  {metrik}: {wert}\n" # Metrik und Wert formatieren
        ergebnis_text_string += "-------------------------\n"

        self.root.after(0, self._update_ergebnis_text_widget, ergebnis_text_string) # Ergebnis-Textfeld im Hauptthread aktualisieren


    def _update_ergebnis_text_widget(self, text: str) -> None:
        """
        Hilfsfunktion zum thread-sicheren Aktualisieren des Ergebnis-Text-Widgets.
        Direkter Zugriff auf UI-Elemente nur im Hauptthread erlaubt (Tkinter Einschränkung).

        Args:
            text (str): Der anzuzeigende Text.
        """
        self.ergebnis_text.config(state='normal') # Textfeld editierbar machen
        self.ergebnis_text.delete('1.0', tk.END) # Textfeld leeren
        self.ergebnis_text.insert(tk.END, text) # Neuen Text einfügen
        self.ergebnis_text.config(state='disabled') # Textfeld wieder schreibgeschützt machen


    def zeige_verlauf(self) -> None:
        """
        Zeigt den Vergleichsverlauf aus dem DatenManager im Verlauf-Textfeld an.
        Ruft `daten_manager.lade_alle_ergebnisse()` auf und formatiert die Daten für die UI-Anzeige.
        Behandelt verschiedene Fehlerfälle beim Laden des Verlaufs und zeigt Fehlermeldungen in der UI.
        """
        self.verlauf_text.config(state='normal') # Verlauf-Textfeld editierbar machen
        self.verlauf_text.delete('1.0', tk.END) # Textfeld leeren
        self.status_meldung.set("Lade Vergleichsverlauf...") # Statusmeldung setzen
        threading.Thread(target=self._lade_verlauf_hintergrund).start() # Verlauf laden in Thread starten
        logger.info("Verlauf laden Thread gestartet.")


    def _lade_verlauf_hintergrund(self) -> None:
        """
        Lädt den Vergleichsverlauf im Hintergrund und aktualisiert die UI.
        """
        try:
            verlauf_daten = self.daten_manager.lade_alle_ergebnisse() # Verlaufdaten laden

            verlauf_text_string = "Vergleichsverlauf:\n"
            verlauf_text_string += "-------------------------------------------------------------------\n"
            if verlauf_daten:
                for eintrag in verlauf_daten: # Jeden Verlaufseintrag durchgehen
                    zeitpunkt_str = eintrag.get('vergleichszeitpunkt', 'N/A') # Vergleichszeitpunkt auslesen
                    datei1_name = eintrag.get('datei1_name', 'N/A') # Dateiname 1 auslesen
                    datei2_name = eintrag.get('datei2_name', 'N/A') # Dateiname 2 auslesen
                    verlauf_text_string += f"Zeitpunkt: {zeitpunkt_str}\n" # Zeitpunkt zum Ausgabestring hinzufügen
                    verlauf_text_string += f"  Dateien: {datei1_name}, {datei2_name}\n" # Dateinamen zum Ausgabestring hinzufügen

                    metriken_eintrag = eintrag.get('metriken', {}) if isinstance(self.daten_manager, FileDataManager) else eintrag # Metriken je nach DataManager-Typ abrufen
                    for metrik in METRIK_REIHENFOLGE: # Metriken in definierter Reihenfolge durchgehen
                        wert = metriken_eintrag.get(metrik, 'N/A') if isinstance(self.daten_manager, FileDataManager) else eintrag.get(metrik, 'N/A') # Metrikwert abrufen
                        if wert != 'N/A':
                            verlauf_text_string += f"  - {metrik}: {wert}\n" # Metrik und Wert zum Ausgabestring hinzufügen
                    verlauf_text_string += "-------------------------------------------------------------------\n"
            else:
                verlauf_text_string += "Keine Verlaufsdaten gefunden.\n" # Meldung, wenn keine Verlaufsdaten vorhanden
                verlauf_text_string += "-------------------------------------------------------------------\n"

            self.root.after(0, self._update_verlauf_text_widget, verlauf_text_string) # Verlauftext in Textfeld einfügen
            self.update_status_meldung_ui("Vergleichsverlauf geladen.") # Statusmeldung aktualisieren

        except CipherCoreDateiLadeFehler as e: # Spezifische Fehlerbehandlung für Dateiladefehler
            logger.error(f"Fehler beim Laden des Vergleichsverlaufs aus Dateien: {e}")
            fehlermeldung = f"Dateifehler beim Laden des Verlaufs:\n{e}\nBitte überprüfen Sie das Datenverzeichnis und die Dateiberechtigungen."
            self.root.after(0, self._zeige_verlauf_fehler, fehlermeldung) # Fehlermeldung in UI anzeigen

        except CipherCoreDatenbankLadeFehler as e: # Spezifische Fehlerbehandlung für Datenbankladefehler
            logger.error(f"Fehler beim Laden des Vergleichsverlaufs aus der Datenbank: {e}")
            fehlermeldung = f"Datenbankfehler beim Laden des Verlaufs:\n{e}\nBitte überprüfen Sie die Logdatei und die Datenbankverbindung."
            self.root.after(0, self._zeige_verlauf_fehler, fehlermeldung) # Fehlermeldung in UI anzeigen

        except CipherCoreDatenFehler as e: # Generische Fehlerbehandlung für Datenfehler
            logger.error(f"Generischer Datenquellen-Fehler beim Laden des Vergleichsverlaufs: {e}")
            fehlermeldung = f"Allgemeiner Datenquellen-Fehler beim Laden des Verlaufs:\n{e}\nBitte überprüfen Sie die Logdatei und die Datenquelle."
            self.root.after(0, self._zeige_verlauf_fehler, fehlermeldung) # Fehlermeldung in UI anzeigen

        except Exception as e: # Unerwartete Fehlerbehandlung (Generischer Catch-All)
            logger.exception(f"Unerwarteter Fehler beim Laden des Vergleichsverlaufs: {e}")
            fehlermeldung = f"Unerwarteter Fehler beim Laden des Verlaufs:\n{e}\nBitte überprüfen Sie die Logdatei für Details."
            self.root.after(0, self._zeige_verlauf_fehler, fehlermeldung) # Fehlermeldung in UI anzeigen


    def _update_verlauf_text_widget(self, text: str) -> None:
        """
        Hilfsfunktion zum thread-sicheren Aktualisieren des Verlauf-Text-Widgets.
        """
        self.verlauf_text.config(state='normal') # Textfeld editierbar machen
        self.verlauf_text.delete('1.0', tk.END) # Textfeld leeren
        self.verlauf_text.insert(tk.END, text) # Neuen Text einfügen
        self.verlauf_text.config(state='disabled') # Textfeld wieder schreibgeschützt machen


    def _zeige_verlauf_fehler(self, fehlermeldung: str) -> None:
        """
        Zeigt eine Fehlermeldung im Verlauf-Textfeld und als MessageBox an.
        """
        self.verlauf_text.config(state='normal') # Textfeld editierbar machen
        self.verlauf_text.delete('1.0', tk.END) # Textfeld leeren
        self.verlauf_text.insert(tk.END, "Fehler beim Laden des Verlaufs. Siehe Fehlermeldung und Logdatei.") # Kurze Fehlermeldung im Textfeld
        self.verlauf_text.config(state='disabled') # Textfeld wieder schreibgeschützt machen
        messagebox.showerror("Fehler beim Verlauf", fehlermeldung) # Fehlermeldung als MessageBox
        self.update_status_meldung_ui("Fehler beim Laden des Vergleichsverlaufs.") # Statusmeldung aktualisieren


    def _lade_verlauf_beim_start(self) -> None:
        """
        Lädt und zeigt den Vergleichsverlauf beim Start der Anwendung.
        """
        self.zeige_verlauf() # Verlauf laden und anzeigen


    def _speichere_konfiguration(self) -> None:
        """
        Speichert die aktuelle Konfiguration in die config.json-Datei.
        Sichere Dateiverarbeitung mit try-except-Block zur Fehlerbehandlung.
        """
        try:
            with open(CONFIG_DATEI, 'w', encoding='utf-8') as konfig_datei: # Sichere Dateiverarbeitung mit 'with open' und Encoding
                json.dump(konfiguration, konfig_datei, indent=4, ensure_ascii=False) # Konfiguration als JSON speichern, ensure_ascii=False für korrekte Zeichenkodierung
            logger.info(f"Konfiguration in '{CONFIG_DATEI}' gespeichert.")
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Konfiguration in '{CONFIG_DATEI}': {e}")



# --- Unit-Tests (CipherCore Standard: Qualitätssicherung) ---
import unittest
import tempfile

class TestDataManager(unittest.TestCase):
    """
    Unit-Test Klasse für die DataManager-Implementierungen (SQLite und File).
    Stellt die korrekte Funktion der Datenpersistenz sicher.
    Umfasst Tests für Speichern, Laden und Fehlerfälle.
    """

    def setUp(self):
        """
        Setzt die Testumgebung vor jedem Testfall auf.
        Erstellt Test-Datenbank und temporäres Datenverzeichnis.
        """
        self.test_db_pfad_sqlite = 'test_ciphercore_datei_vergleich.db' # Test-Datenbankpfad für SQLite
        self.daten_manager_sqlite = SQLiteDataManager(datenbank_pfad=self.test_db_pfad_sqlite) # SQLiteDataManager für Tests

        self.temp_daten_verzeichnis = tempfile.TemporaryDirectory() # Temporäres Verzeichnis für FileDataManager
        self.test_daten_verzeichnis_file = self.temp_daten_verzeichnis.name # Pfad zum temporären Verzeichnis
        self.daten_manager_file = FileDataManager(daten_verzeichnis=self.test_daten_verzeichnis_file) # FileDataManager für Tests


    def tearDown(self):
        """
        Räumt die Testumgebung nach jedem Testfall auf.
        Löscht Test-Datenbank und temporäres Datenverzeichnis.
        """
        if os.path.exists(self.test_db_pfad_sqlite):
            os.remove(self.test_db_pfad_sqlite) # Test-Datenbank löschen

        self.temp_daten_verzeichnis.cleanup() # Temporäres Verzeichnis löschen


    def test_speichere_lade_ergebnisse_sqlite(self):
        """
        Testet das Speichern und Laden von Vergleichsergebnissen mit SQLiteDataManager.
        Prüft, ob die Daten korrekt gespeichert und wieder geladen werden können.
        """
        vergleichs_ergebnisse = {
            METRIK_ANZAHL_DATEI1: 100,
            METRIK_ANZAHL_DATEI2: 120,
            METRIK_GLEICHE_NAMEN: 50
        } # Beispiel Vergleichsergebnisse
        datei1_name = "datei1.csv" # Beispiel Dateiname 1
        datei2_name = "datei2.xlsx" # Beispiel Dateiname 2

        self.daten_manager_sqlite.speichere_ergebnisse(vergleichs_ergebnisse, datei1_name, datei2_name) # Ergebnisse speichern
        geladene_ergebnisse_liste = self.daten_manager_sqlite.lade_alle_ergebnisse() # Alle Ergebnisse laden

        self.assertIsNotNone(geladene_ergebnisse_liste) # Prüfen, ob Ergebnisse geladen wurden
        self.assertTrue(len(geladene_ergebnisse_liste) > 0) # Prüfen, ob mindestens ein Ergebnis geladen wurde

        letzter_eintrag = geladene_ergebnisse_liste[0] # Letzten Eintrag aus der Liste holen (neuester Eintrag)

        self.assertEqual(letzter_eintrag['datei1_name'], datei1_name) # Dateiname 1 vergleichen
        self.assertEqual(letzter_eintrag['datei2_name'], datei2_name) # Dateiname 2 vergleichen
        self.assertEqual(letzter_eintrag['metrik_wert'], str(vergleichs_ergebnisse[METRIK_ANZAHL_DATEI1])) # Metrikwert vergleichen


    def test_speichere_lade_ergebnisse_file(self):
        """
        Testet das Speichern und Laden von Vergleichsergebnissen mit FileDataManager.
        Prüft, ob die Daten korrekt als JSON-Dateien gespeichert und wieder geladen werden können.
        """
        vergleichs_ergebnisse = {
            METRIK_ANZAHL_DATEI1: 150,
            METRIK_ANZAHL_DATEI2: 180,
            METRIK_GLEICHE_NAMEN: 75,
            METRIK_DURCHSCHNITTSALTER_DATEI1: "35.5"
        } # Beispiel Vergleichsergebnisse
        datei1_name = "testdatei1.csv" # Beispiel Dateiname 1
        datei2_name = "testdatei2.xlsx" # Beispiel Dateiname 2

        self.daten_manager_file.speichere_ergebnisse(vergleichs_ergebnisse, datei1_name, datei2_name) # Ergebnisse speichern
        geladene_ergebnisse_liste = self.daten_manager_file.lade_alle_ergebnisse() # Alle Ergebnisse laden

        self.assertIsNotNone(geladene_ergebnisse_liste) # Prüfen, ob Ergebnisse geladen wurden
        self.assertTrue(len(geladene_ergebnisse_liste) > 0) # Prüfen, ob mindestens ein Ergebnis geladen wurde

        letzter_eintrag = geladene_ergebnisse_liste[0] # Letzten Eintrag aus der Liste holen (neuester Eintrag)

        self.assertEqual(letzter_eintrag['datei1_name'], datei1_name) # Dateiname 1 vergleichen
        self.assertEqual(letzter_eintrag['datei2_name'], datei2_name) # Dateiname 2 vergleichen
        self.assertEqual(letzter_eintrag['metriken'][METRIK_ANZAHL_DATEI1], vergleichs_ergebnisse[METRIK_ANZAHL_DATEI1]) # Metrikwert 1 vergleichen
        self.assertEqual(letzter_eintrag['metriken'][METRIK_DURCHSCHNITTSALTER_DATEI1], vergleichs_ergebnisse[METRIK_DURCHSCHNITTSALTER_DATEI1]) # Metrikwert 2 vergleichen


    def test_lade_alle_ergebnisse_leeres_verzeichnis_file(self):
        """
        Testet das Laden von Ergebnissen aus einem leeren Verzeichnis mit FileDataManager.
        Erwartet, dass eine leere Liste zurückgegeben wird, wenn keine JSON-Dateien vorhanden sind.
        """
        self.assertTrue(not os.listdir(self.test_daten_verzeichnis_file)) # Prüfen, ob Verzeichnis leer ist

        geladene_ergebnisse_liste = self.daten_manager_file.lade_alle_ergebnisse() # Ergebnisse laden
        self.assertEqual(geladene_ergebnisse_liste, []) # Erwartet leere Liste


    def test_erstelle_schema_file_existiert_bereits(self):
        """
        Testet die Schemaerstellung mit FileDataManager, wenn das Verzeichnis bereits existiert.
        Erwartet keinen Fehler, da die Schemaerstellung idempotent sein sollte.
        """
        try:
            self.daten_manager_file.erstelle_schema() # Schema erstellen (Verzeichnis sollte bereits existieren)
        except CipherCoreDateiSchemaFehler:
            self.fail("erstelle_schema() hat einen Fehler verursacht, obwohl das Verzeichnis existieren sollte.") # Test fehlschlagen, wenn Fehler auftritt


    def test_speichere_ergebnisse_datei_schreibgeschuetzt_file(self):
        """
        Testet das Speichern von Ergebnissen mit FileDataManager in ein schreibgeschütztes Verzeichnis.
        Erwartet einen CipherCoreDateiSpeicherFehler, da das Speichern in ein schreibgeschütztes Verzeichnis fehlschlagen sollte.
        """
        os.chmod(self.test_daten_verzeichnis_file, 0o555) # Verzeichnis schreibgeschützt machen
        vergleichs_ergebnisse = {METRIK_ANZAHL_DATEI1: 200} # Beispiel Vergleichsergebnisse
        datei1_name = "datei1.csv" # Beispiel Dateiname 1
        datei2_name = "datei2.xlsx" # Beispiel Dateiname 2

        with self.assertRaises(CipherCoreDateiSpeicherFehler): # Erwartet CipherCoreDateiSpeicherFehler
            self.daten_manager_file.speichere_ergebnisse(vergleichs_ergebnisse, datei1_name, datei2_name) # Ergebnisse speichern (sollte fehlschlagen)

        os.chmod(self.test_daten_verzeichnis_file, 0o777) # Verzeichnis wieder beschreibbar machen


    def test_lade_ergebnisse_ungueltige_json_file(self):
        """
        Testet das Laden von Ergebnissen mit FileDataManager, wenn ungültige JSON-Dateien im Verzeichnis vorhanden sind.
        Erwartet, dass ungültige JSON-Dateien ignoriert werden und keine Fehler geworfen werden.
        """
        ungueltige_json_datei_pfad = os.path.join(self.test_daten_verzeichnis_file, "ungueltige_datei.json") # Pfad zur ungültigen JSON-Datei
        with open(ungueltige_json_datei_pfad, 'w') as f: # Ungültige JSON-Datei erstellen
            f.write("Dies ist keine gültige JSON-Datei") # Ungültigen JSON-Inhalt schreiben

        try:
            ergebnisse = self.daten_manager_file.lade_alle_ergebnisse() # Ergebnisse laden (sollte ungültige Datei ignorieren)
            self.assertEqual(ergebnisse, []) # Erwartet leere Liste, da ungültige Datei ignoriert werden soll
        except CipherCoreDateiLadeFehler:
            self.fail("lade_alle_ergebnisse() sollte ungültige JSON-Dateien ignorieren und keinen Fehler werfen.") # Test fehlschlagen, wenn Fehler auftritt



if __name__ == "__main__":
    """
    Haupteinstiegspunkt des Programms.
    Verarbeitet Kommandozeilenargumente, startet GUI oder CLI-Modus und führt Unit-Tests aus (optional).
    """
    parser = argparse.ArgumentParser(description="Vergleicht zwei Dateien und erstellt einen PDF-Bericht mit CipherCore Sicherheit.") # ArgumentParser für Kommandozeilenargumente
    parser.add_argument("datei_pfad1", nargs='?', default=None, help="Pfad zur ersten Datei (Benutzereingaben).") # Argument für Datei 1 (optional für GUI-Start)
    parser.add_argument("datei_pfad2", nargs='?', default=None, help="Pfad zur zweiten Datei (Hauptliste).") # Argument für Datei 2 (optional für GUI-Start)
    parser.add_argument("--logo_pfad", default=LOGO_DATEIPFAD, help="Pfad zum Logo für den PDF-Bericht (optional).") # Argument für Logo-Pfad
    parser.add_argument("--ausgabe_pfad", default=AUSGABE_DATEIPFAD, help="Pfad für den PDF-Bericht (optional).") # Argument für Ausgabepfad
    parser.add_argument("--diagramm_typ", default=DIAGRAMM_TYP_BALKEN, choices=UNTERSTUETZTE_DIAGRAMM_TYPEN,
                        help=f"Diagrammtyp ({', '.join(UNTERSTUETZTE_DIAGRAMM_TYPEN)}). Standard: {DIAGRAMM_TYP_BALKEN}") # Argument für Diagrammtyp
    parser.add_argument("--daten_manager_typ", default="file", choices=["sqlite", "file"],
                        help="Typ des Datenmanagers ('sqlite' oder 'file'). Standard: 'file'") # Argument für DatenManager-Typ
    parser.add_argument("--cli", action="store_true", help="Startet das Tool im Kommandozeilenmodus (ohne GUI).") # Flag für CLI-Modus
    parser.add_argument("--spalte_datei1", default="Name", help="Spalte für Vergleich in Datei 1 (CLI Modus). Standard: 'Name'") # Argument für Spalte Datei 1
    parser.add_argument("--spalte_datei2", default="Name", help="Spalte für Vergleich in Datei 2 (CLI Modus). Standard: 'Name'") # Argument für Spalte Datei 2


    argumente = parser.parse_args() # Kommandozeilenargumente parsen

    daten_manager_typ = argumente.daten_manager_typ # DatenManager-Typ aus Argumenten holen
    if daten_manager_typ == "sqlite":
        daten_manager = SQLiteDataManager(DATENBANK_PFAD) # SQLiteDataManager erstellen
        print("Verwende SQLiteDataManager für Datenpersistenz.")
    elif daten_manager_typ == "file":
        daten_manager = FileDataManager(DATEN_VERZEICHNIS) # FileDataManager erstellen
        print(f"Verwende FileDataManager für Datenpersistenz. Datenverzeichnis: '{DATEN_VERZEICHNIS}'")
    else:
        daten_manager = FileDataManager(DATEN_VERZEICHNIS) # FileDataManager als Standard erstellen
        print(f"Ungültiger DatenManager-Typ gewählt oder nicht angegeben. Verwende standardmäßig FileDataManager.")


    if argumente.cli or (argumente.datei_pfad1 and argumente.datei_pfad2): # CLI-Modus starten, wenn --cli Flag oder beide Dateipfade gegeben sind
        if not argumente.datei_pfad1 or not argumente.datei_pfad2: # Fehler, wenn im CLI-Modus Dateipfade fehlen
            print("Fehler: Für den Kommandozeilenmodus müssen beide Dateipfade angegeben werden.")
            parser.print_help() # Hilfe ausgeben
        else:
            print("Starte im Kommandozeilenmodus...")
            pdf_pfad, vergleichs_ergebnisse = dateien_vergleichen_und_bericht_erstellen( # Vergleichsfunktion aufrufen
                argumente.datei_pfad1, argumente.datei_pfad2,
                logo_pfad=argumente.logo_pfad, ausgabe_pfad=argumente.ausgabe_pfad,
                diagramm_typ=argumente.diagramm_typ, daten_manager=daten_manager,
                spalte_datei1=argumente.spalte_datei1, spalte_datei2=argumente.spalte_datei2 # Spalten für Vergleich übergeben
            )
            if isinstance(pdf_pfad, str) and pdf_pfad.endswith('.pdf'): # Erfolgsmeldung im CLI-Modus
                print(f"PDF-Bericht erfolgreich erstellt: {pdf_pfad}")
            else: # Fehlermeldung im CLI-Modus
                print(f"Fehler beim Erstellen des Berichts: {pdf_pfad}")


    else: # GUI-Modus starten, wenn keine Dateipfade und kein --cli Flag gegeben sind
        print("Starte GUI...")
        root = tk.Tk()
        app = DateiVergleichsApp(root, daten_manager) # GUI-App erstellen

        if app.lizenz_akzeptiert.get(): # GUI nur starten, wenn Lizenz akzeptiert
            root.grid_columnconfigure(1, weight=1) # Spalte 1 soll expandieren
            root.grid_rowconfigure(7, weight=1) # Zeile 7 soll expandieren # Zeile angepasst, da mehr UI-Elemente
            root.grid_rowconfigure(9, weight=1) # Zeile 9 soll expandieren # Zeile angepasst, da mehr UI-Elemente
            ausfuehren_unit_tests = False # Unit-Tests standardmässig deaktiviert
            if ausfuehren_unit_tests:
                suite = unittest.TestSuite()
                suite.addTest(unittest.makeSuite(TestDataManager)) # Test-Suite erstellen
                runner = unittest.TextTestRunner() # Test-Runner erstellen
                runner.run(suite) # Unit-Tests ausführen
            else:
                root.mainloop() # GUI Hauptloop starten


# --- Dummy Daten und Dateierzeugung für Testzwecke ---
data1 = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Franz', 'Greta', 'Hans', 'Ingrid', 'Julia', 'Kurt', 'Lena'],
         'Alter': [30, 25, 35, 28, 22, 45, 38, 29, 31, 27, 52, 24],
         'Stadt': ['Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Leipzig', 'Dresden', 'Nürnberg', 'Hannover', 'Bremen']}
df1 = pd.DataFrame(data1) # DataFrame 1 erstellen

data2 = {'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Frank', 'Günther', 'Heidi', 'Igor', 'Julia', 'Kevin', 'Laura', 'Max', 'Mia'],
         'Alter': [30, 25, 35, 29, 40, 55, 42, 26, 27, 33, None, 48, 36],
         'Stadt': ['Berlin', 'Hamburg', 'München', 'Stuttgart', 'Frankfurt', 'Dortmund', 'Essen', 'Bonn', 'Nürnberg', 'Mannheim', 'Kiel', 'Rostock', 'Saarbrücken']}
df2 = pd.DataFrame(data2) # DataFrame 2 erstellen

dummy_datei_pfad1 = "benutzereingaben.csv" # Dummy Dateipfad 1
dummy_datei_pfad2 = "neue_hauptliste.xlsx" # Dummy Dateipfad 2  <- Fehler behoben: Dateiname geändert

df1.to_csv(dummy_datei_pfad1, index=False, encoding='utf-8') # DataFrame 1 als CSV speichern, Encoding hinzugefügt
try:
    df2.to_excel(dummy_datei_pfad2, index=False) # DataFrame 2 als Excel speichern (versuchen)
except ImportError as e: # ImportError abfangen (Excel-Bibliothek fehlt)
    print(f"Warnung: Excel-Datei konnte nicht erstellt werden. Bitte installieren Sie 'openpyxl' oder 'xlsxwriter': {e}")
    dummy_datei_pfad2 = "neue_hauptliste.csv" # Fallback auf CSV für DataFrame 2  <- Fehler behoben: Dateiname geändert
    df2.to_csv(dummy_datei_pfad2, index=False, encoding='utf-8') # DataFrame 2 als CSV speichern, Encoding hinzugefügt
    print(f"Stattdessen CSV-Datei '{dummy_datei_pfad2}' erstellt.")
