# CipherCore Datei Vergleichs-Tool - Professionelle README

![CipherCore Logo](assets/ciphercore_logo_standard.png)

## Übersicht

Das CipherCore Datei Vergleichs-Tool ist eine hochentwickelte Anwendung zum detaillierten Vergleich von zwei Dateien unterschiedlicher Formate (.csv, .txt, .xls, .xlsx). Es generiert umfassende Vergleichsberichte im PDF-Format, inklusive statistischer Auswertungen und grafischer Diagramme. Entwickelt von CipherCore GmbH, bietet dieses Tool eine benutzerfreundliche Oberfläche (GUI) sowie einen Kommandozeilenmodus (CLI) für maximale Flexibilität.

**Wichtige Merkmale:**

*   **Umfassender Dateivergleich:**  Vergleicht Dateien in den Formaten CSV, TXT, XLS und XLSX.
*   **Detaillierte Metriken:** Berechnet wichtige Vergleichsmetriken wie Anzahl der Einträge, übereinstimmende Namen und prozentuale Unterschiede.
*   **Visuelle Diagramme:** Erstellt aussagekräftige Balken- oder Kreisdiagramme zur Visualisierung der Vergleichsergebnisse.
*   **Professionelle PDF-Berichte:** Generiert Berichte mit Logo, Statistiken, Diagrammen und Firmendetails von CipherCore.
*   **Benutzerfreundliche GUI:** Intuitive grafische Oberfläche für einfache Bedienung.
*   **Kommandozeilenmodus:** CLI für automatisierte Prozesse und Integration in Skripte.
*   **Datenpersistenz:** Speichert Vergleichsergebnisse wahlweise in SQLite-Datenbank oder JSON-Dateien für spätere Einsicht und Analyse.
*   **Umfassendes Logging:** Detaillierte Protokollierung aller Vorgänge für Nachverfolgbarkeit und Fehleranalyse.
*   **Sicherheitsfokus:**  Implementiert Sicherheitsmaßnahmen wie Pfadsicherheitsprüfungen und Prepared Statements zum Schutz vor Angriffen.
*   **Testphasen-Management und Lizenzprüfung:** Integriertes Lizenzsystem und Testphasenüberwachung.

## Inhaltsverzeichnis

1.  [Erste Schritte](#erste-schritte)
    *   [Voraussetzungen](#voraussetzungen)
    *   [Installation](#installation)
    *   [Konfiguration](#konfiguration)
2.  [Benutzung](#benutzung)
    *   [Grafische Benutzeroberfläche (GUI)](#grafische-benutzeroberfläche-gui)
        *   [Lizenzvereinbarung](#lizenzvereinbarung)
        *   [Hauptfenster und Funktionen](#hauptfenster-und-funktionen)
        *   [Vergleich starten und Bericht erstellen](#vergleich-starten-und-bericht-erstellen)
        *   [Vergleichsverlauf anzeigen](#vergleichsverlauf-anzeigen)
    *   [Kommandozeilenmodus (CLI)](#kommandozeilenmodus-cli)
        *   [CLI-Argumente](#cli-argumente)
        *   [Beispiele für die CLI-Nutzung](#beispiele-für-die-cli-nutzung)
3.  [Konfiguration im Detail](#konfiguration-im-detail)
    *   [`config.json` Datei](#configjson-datei)
    *   [Konfigurationsparameter](#konfigurationsparameter)
4.  [Datenpersistenz](#datenpersistenz)
    *   [SQLite Datenbank](#sqlite-datenbank)
    *   [JSON Dateien](#json-dateien)
    *   [Auswahl des Datenmanagers](#auswahl-des-datenmanagers)
5.  [Fehlerbehandlung und Logging](#fehlerbehandlung-und-logging)
    *   [Benutzerdefinierte Exceptions](#benutzerdefinierte-exceptions)
    *   [Logging-System](#logging-system)
6.  [Lizenzbedingungen und Urheberrecht](#lizenzbedingungen-und-urheberrecht)
7.  [Sicherheitshinweise](#sicherheitshinweise)
8.  [Unit Tests](#unit-tests)
9.  [Support und Kontakt](#support-und-kontakt)

---

## 1. Erste Schritte

### Voraussetzungen

Bevor Sie das CipherCore Datei Vergleichs-Tool verwenden, stellen Sie sicher, dass folgende Voraussetzungen erfüllt sind:

*   **Python:** Python 3.8 oder höher muss auf Ihrem System installiert sein. Sie können Python von der offiziellen Website [python.org](https://www.python.org) herunterladen.
*   **Python Bibliotheken:**  Die folgenden Python Bibliotheken sind erforderlich. Diese können einfach mit `pip` installiert werden (siehe [Installation](#installation)).
    *   `pandas`
    *   `matplotlib`
    *   `fpdf`
    *   `Pillow` (PIL Fork)
    *   `tkinter` (in der Regel in Python Standardinstallation enthalten)
    *   `openpyxl` oder `xlrd` und `xlsxwriter` (optional, für Excel-Dateien)

### Installation

1.  **Repository Klonen (oder ZIP herunterladen):** Laden Sie das Repository des CipherCore Datei Vergleichs-Tools herunter oder klonen Sie es mit Git:
    ```bash
    git clone [Repository URL hier einfügen]
    cd CipherCore-DateiVergleichs-Tool
    ```
2.  **Python Bibliotheken installieren:**  Navigieren Sie im Terminal in das heruntergeladene Verzeichnis und installieren Sie die benötigten Python Bibliotheken mit pip:
    ```bash
    pip install -r requirements.txt
    ```
    *(Erstellen Sie eine `requirements.txt` Datei im Projektverzeichnis mit folgendem Inhalt, falls diese nicht existiert)*:
    ```
    pandas
    matplotlib
    fpdf2
    Pillow
    openpyxl
    xlrd
    xlsxwriter
    ```

### Konfiguration

Die Konfiguration des Tools erfolgt über die `config.json` Datei im Hauptverzeichnis. Details zur Konfiguration finden Sie im Abschnitt [Konfiguration im Detail](#konfiguration-im-detail). Standardmäßig werden sinnvolle Voreinstellungen verwendet, die in den meisten Fällen keine Anpassung erfordern.

---

## 2. Benutzung

Das CipherCore Datei Vergleichs-Tool kann auf zwei Arten verwendet werden: über die grafische Benutzeroberfläche (GUI) oder über die Kommandozeile (CLI).

### Grafische Benutzeroberfläche (GUI)

Um die GUI zu starten, führen Sie das Hauptskript `[Name des Hauptskripts].py` ohne zusätzliche Argumente aus:

```bash
python [Name des Hauptskripts].py
```

Sollten Sie das Hauptskript nicht direkt ausführbar haben, stellen Sie sicher, dass der korrekte Pfad zum Skript angegeben ist.

#### Lizenzvereinbarung

Beim ersten Start der GUI wird die CipherCore Lizenzvereinbarung angezeigt. Sie müssen diese akzeptieren, um die Software nutzen zu können. Die Lizenzbedingungen werden im Dialogfenster vollständig angezeigt. Nach Akzeptanz wird die Lizenz in der `config.json` Datei gespeichert und der Dialog wird bei zukünftigen Starts nicht mehr angezeigt, solange die Lizenzbedingungen akzeptiert bleiben.

#### Hauptfenster und Funktionen

Nach dem Start und der Lizenzakzeptanz öffnet sich das Hauptfenster der Anwendung. Dieses ist intuitiv gestaltet und bietet folgende Funktionen:

1.  **Datei 1 (Benutzereingaben) auswählen:** Klicken Sie auf "Datei 1 auswählen", um die erste Datei für den Vergleich auszuwählen. Dies ist typischerweise die Datei mit Ihren Benutzereingaben. Es öffnet sich ein Dateiauswahldialog, der auf das Basisverzeichnis beschränkt ist (konfigurierbar in `config.json`). Unterstützte Dateiformate sind CSV, TXT, XLS und XLSX.
2.  **Datei 2 (Hauptliste) auswählen:** Klicken Sie auf "Datei 2 auswählen", um die zweite Datei für den Vergleich auszuwählen. Dies ist in der Regel Ihre Hauptliste oder Referenzdatei. Der Dateiauswahldialog funktioniert analog zu Datei 1.
3.  **Vergleichsspalte Datei 1 & Datei 2:** Geben Sie die Spaltennamen ein, die für den Vergleich in Datei 1 und Datei 2 verwendet werden sollen. Standardmäßig ist "Name" voreingestellt. Stellen Sie sicher, dass die eingegebenen Spaltennamen in den ausgewählten Dateien existieren.
4.  **Diagrammtyp:** Wählen Sie den gewünschten Diagrammtyp für die visuelle Darstellung der Ergebnisse aus dem Dropdown-Menü. Verfügbare Optionen sind "Balken" und "Kreis". Beachten Sie, dass der Kreisdiagrammtyp sich noch in der Optimierungsphase befindet und in manchen Fällen ein Balkendiagramm eine bessere Übersichtlichkeit bieten kann.
5.  **Vergleich starten & PDF-Bericht erstellen:** Klicken Sie auf diesen Button, um den Dateivergleich zu starten und einen PDF-Bericht zu generieren. Der Prozess kann je nach Dateigröße und Systemleistung einige Zeit in Anspruch nehmen. Der Fortschritt wird in der Statusmeldung unterhalb der Buttons angezeigt.
6.  **Statusmeldung:**  Zeigt aktuelle Statusmeldungen an, wie z.B. "Vergleich gestartet...", "Daten erfolgreich geladen...", "PDF-Bericht erfolgreich erstellt..." oder Fehlermeldungen.
7.  **Vergleichsergebnisse:** Ein Textfeld, das die numerischen Vergleichsergebnisse in übersichtlicher Form nach Abschluss des Vergleichs anzeigt.
8.  **Verlauf anzeigen:** Klicken Sie auf diesen Button, um den Vergleichsverlauf anzuzeigen. Dies lädt frühere Vergleichsergebnisse, die entweder in einer SQLite-Datenbank oder als JSON-Dateien gespeichert wurden (abhängig von Ihrer Konfiguration).
9.  **Vergleichsverlauf:** Ein Textfeld, das den geladenen Vergleichsverlauf anzeigt. Jeder Eintrag enthält den Vergleichszeitpunkt, die verglichenen Dateien und die wichtigsten Metriken.

#### Vergleich starten und Bericht erstellen

Nachdem Sie beide Dateien ausgewählt, die Vergleichsspalten (optional) angepasst und den Diagrammtyp gewählt haben, klicken Sie auf den Button "Vergleich starten & PDF-Bericht erstellen".

*   Das Tool lädt die ausgewählten Dateien.
*   Es führt den Dateivergleich basierend auf den angegebenen Spalten durch.
*   Ein Diagramm wird erstellt, das die Vergleichsergebnisse visualisiert.
*   Ein detaillierter PDF-Bericht wird generiert und im konfigurierten Ausgabepfad gespeichert (Standard: `berichte/datei_vergleichsbericht.pdf`).
*   Die Vergleichsergebnisse werden im Textfeld "Vergleichsergebnisse" angezeigt.
*   Je nach Konfiguration werden die Vergleichsergebnisse persistent gespeichert (SQLite oder JSON-Datei).

Im Fehlerfall wird eine Fehlermeldung in der Statusleiste angezeigt und gegebenenfalls ein Dialogfenster mit detaillierteren Informationen eingeblendet.

#### Vergleichsverlauf anzeigen

Klicken Sie auf den Button "Verlauf anzeigen", um frühere Vergleichsergebnisse zu laden und im Textfeld "Vergleichsverlauf" anzuzeigen. Der Verlauf wird in umgekehrt chronologischer Reihenfolge angezeigt, wobei die neuesten Vergleiche zuerst erscheinen.  Sollte ein Fehler beim Laden des Verlaufs auftreten, wird eine entsprechende Fehlermeldung im Textfeld und gegebenenfalls als Dialogfenster angezeigt.

### Kommandozeilenmodus (CLI)

Für automatisierte Prozesse oder die Integration in Skripte kann das CipherCore Datei Vergleichs-Tool auch im Kommandozeilenmodus (CLI) verwendet werden.

Um den CLI-Modus zu nutzen, führen Sie das Hauptskript mit den entsprechenden Argumenten aus.

#### CLI-Argumente

Die folgenden Argumente sind für den CLI-Modus verfügbar:

```
python [Name des Hauptskripts].py <datei_pfad1> <datei_pfad2> [--logo_pfad <logo_pfad>] [--ausgabe_pfad <ausgabe_pfad>] [--diagramm_typ <diagramm_typ>] [--daten_manager_typ <daten_manager_typ>] [--spalte_datei1 <spalte_datei1>] [--spalte_datei2 <spalte_datei2>]
```

*   `<datei_pfad1>`: Pfad zur ersten Datei (Benutzereingaben). **Erforderlich im CLI-Modus.**
*   `<datei_pfad2>`: Pfad zur zweiten Datei (Hauptliste). **Erforderlich im CLI-Modus.**
*   `--logo_pfad <logo_pfad>`: Pfad zum Logo für den PDF-Bericht. *(Optional. Standardwert aus `config.json`)*
*   `--ausgabe_pfad <ausgabe_pfad>`: Pfad für den PDF-Bericht. *(Optional. Standardwert aus `config.json`)*
*   `--diagramm_typ <diagramm_typ>`: Diagrammtyp (`balken` oder `kreis`). *(Optional. Standardwert ist `balken`)*
*   `--daten_manager_typ <daten_manager_typ>`: Typ des Datenmanagers (`sqlite` oder `file`). *(Optional. Standardwert ist `file`)*
*   `--spalte_datei1 <spalte_datei1>`: Spalte für den Vergleich in Datei 1. *(Optional. Standardwert ist `Name`)*
*   `--spalte_datei2 <spalte_datei2>`: Spalte für den Vergleich in Datei 2. *(Optional. Standardwert ist `Name`)*
*   `--cli`:  Flag, um den expliziten CLI-Modus zu erzwingen (nützlich, wenn Dateipfade als Argumente übergeben werden sollen, aber die GUI nicht gestartet werden soll). *(Optional. Implizit aktiv, wenn Dateipfade als Argumente übergeben werden)*

#### Beispiele für die CLI-Nutzung

1.  **Einfacher Dateivergleich mit Standardeinstellungen:**

    ```bash
    python [Name des Hauptskripts].py benutzereingaben.csv hauptliste.xlsx
    ```
    Dies vergleicht die Dateien `benutzereingaben.csv` und `hauptliste.xlsx`, verwendet Standardeinstellungen für Logo, Ausgabepfad, Diagrammtyp und Datenmanager und erstellt den Bericht im Standardausgabepfad.

2.  **Dateivergleich mit benutzerdefiniertem Ausgabepfad und Diagrammtyp:**

    ```bash
    python [Name des Hauptskripts].py benutzereingaben.csv hauptliste.xlsx --ausgabe_pfad berichte/mein_vergleichsbericht.pdf --diagramm_typ kreis
    ```
    Erstellt einen PDF-Bericht im Pfad `berichte/mein_vergleichsbericht.pdf` und verwendet ein Kreisdiagramm.

3.  **Dateivergleich mit SQLite-Datenmanager und benutzerdefinierten Vergleichsspalten:**

    ```bash
    python [Name des Hauptskripts].py benutzereingaben.csv hauptliste.xlsx --daten_manager_typ sqlite --spalte_datei1 Kundenname --spalte_datei2 Name
    ```
    Verwendet SQLite für die Datenpersistenz und vergleicht die Spalte "Kundenname" aus `benutzereingaben.csv` mit der Spalte "Name" aus `hauptliste.xlsx`.

4.  **Expliziter CLI-Modus Start erzwingen:**

    ```bash
    python [Name des Hauptskripts].py --cli --datei_pfad1 benutzereingaben.csv --datei_pfad2 hauptliste.xlsx
    ```
    Startet im CLI-Modus, selbst wenn keine Dateipfade direkt als erste Argumente angegeben werden. Nützlich, wenn Argumente in anderer Reihenfolge oder über Flags übergeben werden sollen.

---

## 3. Konfiguration im Detail

### `config.json` Datei

Die `config.json` Datei im Hauptverzeichnis des Projekts dient zur Konfiguration des CipherCore Datei Vergleichs-Tools. Diese Datei ist im JSON-Format aufgebaut und erlaubt die Anpassung verschiedener Parameter.

**Beispiel `config.json` Datei:**

```json
{
  "basis_verzeichnis": ".",
  "logo_pfad": "assets/ciphercore_logo_standard.png",
  "ausgabe_pfad": "berichte/datei_vergleichsbericht.pdf",
  "erster_start_datum": "2024-01-01",
  "lizenz_akzeptiert": true,
  "datenbank_pfad": "ciphercore_datei_vergleich.db",
  "daten_verzeichnis": "ciphercore_vergleichsdaten"
}
```

### Konfigurationsparameter

*   **`basis_verzeichnis`**: Das Basisverzeichnis für sichere Dateipfade. Dateiauswahldialoge und Dateizugriffe sind auf dieses Verzeichnis beschränkt. Standardwert ist `"."` (aktuelles Verzeichnis).
*   **`logo_pfad`**: Pfad zum Logo, das im PDF-Bericht in der Kopfzeile angezeigt wird. Standardwert ist `"assets/ciphercore_logo_standard.png"`. Wenn kein Pfad angegeben oder die Datei nicht gefunden wird, wird der Bericht ohne Logo erstellt.
*   **`ausgabe_pfad`**: Standardpfad für den generierten PDF-Bericht. Standardwert ist `"berichte/datei_vergleichsbericht.pdf"`.
*   **`erster_start_datum`**: Datum des ersten Programmstarts. Wird automatisch beim ersten Start gesetzt und für die Testphasenüberwachung verwendet. **Nicht manuell ändern.**
*   **`lizenz_akzeptiert`**: Status der Lizenzakzeptanz. `true`, wenn die Lizenz akzeptiert wurde, `false` sonst. Wird durch den Lizenzdialog in der GUI gesteuert. **Nicht manuell ändern.**
*   **`datenbank_pfad`**: Pfad zur SQLite-Datenbankdatei, wenn der SQLite-Datenmanager verwendet wird. Standardwert ist `"ciphercore_datei_vergleich.db"`.
*   **`daten_verzeichnis`**: Pfad zum Verzeichnis, in dem JSON-Dateien für den File-Datenmanager gespeichert werden. Standardwert ist `"ciphercore_vergleichsdaten"`.

**Wichtige Hinweise zur Konfiguration:**

*   Änderungen in der `config.json` Datei werden beim nächsten Start der Anwendung wirksam.
*   Falsche oder ungültige Konfigurationen können zu Fehlern führen oder dazu, dass die Standardkonfiguration verwendet wird. Die Anwendung validiert die Konfiguration beim Laden und protokolliert Warnungen oder Fehler im Log-File, falls Probleme auftreten.

---

## 4. Datenpersistenz

Das CipherCore Datei Vergleichs-Tool bietet zwei Optionen zur persistenten Speicherung der Vergleichsergebnisse: SQLite Datenbank oder JSON Dateien. Die Wahl des Datenmanagers kann über den CLI-Parameter `--daten_manager_typ` oder indirekt durch die Konfiguration in `config.json` (für GUI-Nutzung und Standardwerte) gesteuert werden.

### SQLite Datenbank

Der SQLite Datenmanager (`SQLiteDataManager`) speichert die Vergleichsergebnisse in einer SQLite Datenbankdatei.

*   **Vorteile:**
    *   Strukturierte Datenspeicherung.
    *   Effiziente Abfrage und Verwaltung von Vergleichsdaten.
    *   Geeignet für größere Datenmengen und häufige Verlaufsabfragen.
*   **Konfiguration:**
    *   Datenbankpfad wird in `config.json` unter dem Schlüssel `"datenbank_pfad"` konfiguriert.
    *   Datenmanager-Typ wird im CLI mit `--daten_manager_typ sqlite` oder implizit durch die Konfiguration in `config.json` ausgewählt.

### JSON Dateien

Der File Datenmanager (`FileDataManager`) speichert die Vergleichsergebnisse in einzelnen JSON Dateien in einem dedizierten Verzeichnis.

*   **Vorteile:**
    *   Einfache Dateibasierte Speicherung.
    *   Keine externe Datenbank erforderlich.
    *   Geeignet für kleinere Datenmengen und einfachere Verlaufsanzeige.
*   **Konfiguration:**
    *   Datenverzeichnis wird in `config.json` unter dem Schlüssel `"daten_verzeichnis"` konfiguriert.
    *   Datenmanager-Typ wird im CLI mit `--daten_manager_typ file` oder implizit durch die Konfiguration in `config.json` ausgewählt.

### Auswahl des Datenmanagers

*   **GUI-Modus:** Der verwendete Datenmanager-Typ wird implizit durch die Konfiguration in `config.json` bestimmt (Standard ist `file`).
*   **CLI-Modus:** Der Datenmanager-Typ kann explizit mit dem Parameter `--daten_manager_typ` beim Aufruf des Skripts angegeben werden (`sqlite` oder `file`). Wenn der Parameter nicht angegeben wird, wird der in `config.json` konfigurierte Typ verwendet (Standard ist `file`).

---

## 5. Fehlerbehandlung und Logging

Das CipherCore Datei Vergleichs-Tool verfügt über ein robustes Fehlerbehandlungs- und Logging-System, um die Stabilität und Nachverfolgbarkeit der Anwendung zu gewährleisten.

### Benutzerdefinierte Exceptions

Zur präzisen Fehlerbehandlung verwendet das Tool benutzerdefinierte Exception-Klassen, die im Modul `[Name des Hauptskripts].py` definiert sind. Diese Exceptions sind von der Basisklasse `CipherCoreDatenFehler` abgeleitet und ermöglichen eine detaillierte Fehlerkategorisierung:

*   `CipherCoreDatenFehler`: Basisklasse für alle Datenfehler.
*   `CipherCoreDatenbankFehler`: Basisklasse für Datenbankfehler.
    *   `CipherCoreDatenbankSchemaFehler`: Fehler beim Erstellen des Datenbank-Schemas.
    *   `CipherCoreDatenbankSpeicherFehler`: Fehler beim Speichern in die Datenbank.
    *   `CipherCoreDatenbankLadeFehler`: Fehler beim Laden aus der Datenbank.
*   `CipherCoreDateiFehler`: Basisklasse für Dateifehler.
    *   `CipherCoreDateiSpeicherFehler`: Fehler beim Speichern in Datei.
    *   `CipherCoreDateiLadeFehler`: Fehler beim Laden aus Datei.
    *   `CipherCoreDateiSchemaFehler`: Fehler beim Erstellen des Datei-Schemas (z.B. Verzeichnis).
*   `CipherCoreDatenValidierungsFehler`: Fehler bei der Validierung der Daten.
*   `CipherCoreUngültigerDiagrammTypFehler`: Fehler aufgrund eines ungültigen Diagrammtyps.

Diese spezifischen Exception-Klassen ermöglichen eine differenzierte Fehlerbehandlung im Code und in der UI, was zu klareren Fehlermeldungen und einer verbesserten Benutzererfahrung beiträgt.

### Logging-System

Das Tool verwendet das Python `logging` Modul, um detaillierte Protokolle aller wichtigen Vorgänge zu erstellen. Das Logging ist standardmäßig konfiguriert, um Informationen, Warnungen, Fehler und kritische Ereignisse in einer Log-Datei zu speichern.

*   **Log-Datei:** Die Log-Datei wird im Verzeichnis `log/` unter dem Namen `ciphercore_datei_vergleich.log` gespeichert. Das Log-Verzeichnis wird automatisch erstellt, falls es nicht existiert.
*   **Log-Format:** Das Log-Format beinhaltet Zeitstempel, Log-Level, Modulname, Funktionsname und die Log-Nachricht.
*   **Log-Level:** Standardmäßig ist das Log-Level auf `INFO` gesetzt, was bedeutet, dass `INFO`, `WARNING`, `ERROR` und `CRITICAL` Nachrichten protokolliert werden.
*   **Konfiguration:** Die Logging-Konfiguration ist im Code fest hinterlegt und in der aktuellen Version nicht über `config.json` anpassbar.

Das Logging-System ist ein wichtiges Werkzeug für:

*   **Fehlerdiagnose:** Bei Problemen oder Fehlern kann die Log-Datei detaillierte Informationen liefern, um die Ursache zu finden und zu beheben.
*   **Nachverfolgbarkeit:** Das Log protokolliert alle wichtigen Schritte des Programms, was die Nachverfolgung von Abläufen und die Analyse des Programmverhaltens erleichtert.
*   **Sicherheitsaudits:** Das Log kann für Sicherheitsaudits verwendet werden, um verdächtige Aktivitäten oder Fehler zu erkennen, die auf Sicherheitslücken hinweisen könnten.

Es wird empfohlen, bei Problemen zuerst die Log-Datei zu konsultieren, bevor Support angefragt wird.

---

## 6. Lizenzbedingungen und Urheberrecht

**Urheberrecht:** Copyright (c) 2024 CipherCore GmbH

**Lizenz:** Proprietär - Alle Rechte vorbehalten

Dieses CipherCore Datei Vergleichs-Tool ist urheberrechtlich geschützt und wird unter einer **proprietären Lizenz** vertrieben. **Alle Rechte sind vorbehalten.**

*   Die Software darf **nicht** ohne ausdrückliche schriftliche Genehmigung der CipherCore GmbH kopiert, verändert, verbreitet, verkauft oder für kommerzielle Zwecke genutzt werden.
*   Die Software wird als **Testversion** bereitgestellt und ist für **Evaluierungszwecke** gedacht.
*   Die Nutzung der Software nach Ablauf der Testphase oder für kommerzielle Zwecke erfordert den Erwerb einer **Vollversion** oder einer entsprechenden **Lizenzvereinbarung** mit der CipherCore GmbH.

**Bitte beachten Sie die vollständigen Lizenzbedingungen, die beim ersten Start der GUI im Lizenzdialog angezeigt werden.**

---

## 7. Sicherheitshinweise

Das CipherCore Datei Vergleichs-Tool wurde mit Fokus auf Sicherheit entwickelt. Dennoch ist es wichtig, die folgenden Sicherheitshinweise zu beachten:

*   **Pfadsicherheitsprüfungen:** Das Tool implementiert Pfadsicherheitsprüfungen, um sicherzustellen, dass Dateizugriffe auf das konfigurierte Basisverzeichnis beschränkt sind. Dies soll Path-Traversal-Angriffe verhindern. Es wird jedoch empfohlen, das Basisverzeichnis sorgfältig zu wählen und sicherzustellen, dass es keine sensiblen Daten außerhalb dieses Verzeichnisses gibt, auf die das Tool unbeabsichtigt zugreifen könnte.
*   **Prepared Statements (SQLite):** Bei Verwendung des SQLite Datenmanagers werden Prepared Statements verwendet, um SQL-Injection-Angriffe zu verhindern.
*   **Datenvalidierung:** Das Tool führt grundlegende Datenvalidierungen durch, um sicherzustellen, dass die geladenen Daten dem erwarteten Format entsprechen. Es wird jedoch empfohlen, die Eingabedateien vor der Verwendung des Tools sorgfältig zu prüfen und sicherzustellen, dass sie keine schädlichen Inhalte enthalten.
*   **Logging:** Das Logging-System protokolliert sensible Informationen (wie Dateipfade) in der Log-Datei. Stellen Sie sicher, dass der Zugriff auf die Log-Dateien entsprechend geschützt ist, um unbefugten Zugriff auf diese Informationen zu verhindern.
*   **Testversion "wie besehen":** Diese Software wird "wie besehen" und ohne jegliche Gewährleistung bereitgestellt. CipherCore GmbH übernimmt keine Haftung für Schäden, die durch die Nutzung dieser Software entstehen könnten, insbesondere Datenverlust oder Sicherheitsverletzungen. Die Nutzung erfolgt auf eigene Gefahr.

Es wird empfohlen, die Software in einer sicheren Umgebung zu betreiben und die Sicherheitshinweise sorgfältig zu beachten.

---

## 8. Unit Tests

Zur Qualitätssicherung sind Unit Tests implementiert, die die Funktionalität der DataManager-Klassen (SQLiteDataManager und FileDataManager) überprüfen. Die Unit Tests sind im Modul `[Name des Hauptskripts].py` im Abschnitt `Unit-Tests` definiert und nutzen das Python `unittest` Framework.

**Um die Unit Tests auszuführen:**

1.  Stellen Sie sicher, dass Sie das Projekt in Ihrer Python Umgebung installiert haben (siehe [Installation](#installation)).
2.  Führen Sie das Hauptskript `[Name des Hauptskripts].py` über die Kommandozeile aus, **ohne** Dateipfade als Argumente und **ohne** das `--cli` Flag.
3.  Setzen Sie die Variable `ausfuehren_unit_tests = True` im `if __name__ == "__main__":` Block des Hauptskripts.
4.  Starten Sie das Skript. Die Unit Tests werden vor dem Start der GUI ausgeführt und die Ergebnisse in der Konsole angezeigt.

**Hinweis:** Standardmäßig sind die Unit Tests deaktiviert (`ausfuehren_unit_tests = False`), um den normalen GUI-Start zu ermöglichen.

---

## 9. Support und Kontakt

Für Supportanfragen, Feedback oder den Erwerb einer Vollversion des CipherCore Datei Vergleichs-Tools kontaktieren Sie bitte das Vertriebsteam der CipherCore GmbH:

**CipherCore GmbH**

[Ihre Adresse]

[Ihre Website]

[Ihre E-Mail-Adresse für Support/Vertrieb]

Wir sind bestrebt, Ihnen eine hochwertige Software und einen exzellenten Kundenservice zu bieten.

---

**Dokument erstellt von CipherCore GmbH.**
