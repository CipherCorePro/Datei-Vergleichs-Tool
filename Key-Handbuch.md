# Benutzeranleitung für CipherCore Lizenzschlüssel-Generator (Pro Version)

**Version:** 1.0 (basierend auf dem Python-Skript vom 2024)

**Urheberrecht:** Copyright (c) 2024 CipherCore GmbH
**Lizenz:** Proprietär - Alle Rechte vorbehalten

## 1. Einleitung

Dieses Dokument ist eine umfassende Anleitung zur Verwendung des CipherCore Lizenzschlüssel-Generators. Mit diesem Tool können Sie RSA-Schlüsselpaare erstellen, diese Schlüssel serialisieren und signierte Lizenzschlüssel für die "Pro"-Version Ihrer Software generieren.  Diese Anleitung richtet sich an Systemadministratoren, Softwareentwickler und alle, die für die Lizenzierung und den Schutz der CipherCore "Pro"-Software verantwortlich sind.

**Wichtige Konzepte:**

*   **RSA-Schlüsselpaar:**  Besteht aus einem privaten Schlüssel und einem öffentlichen Schlüssel.
    *   **Privater Schlüssel:**  Wird verwendet, um Lizenzschlüssel **zu signieren**.  Er muss **absolut geheim und sicher** aufbewahrt werden. Der Besitzer des privaten Schlüssels kann gültige Lizenzen erstellen.
    *   **Öffentlicher Schlüssel:** Wird verwendet, um die **Signaturen von Lizenzschlüsseln zu überprüfen**. Er kann sicher verteilt werden, da er nur zum Validieren und nicht zum Erstellen von Lizenzen verwendet werden kann.
*   **PEM-Format:**  Ein gängiges Format zum Speichern von kryptografischen Schlüsseln.
*   **Base64-Kodierung:**  Eine Methode, um Binärdaten in ein ASCII-String-Format zu konvertieren, das leicht über Textkanäle übertragen werden kann. Im Kontext von Lizenzschlüsseln wird es verwendet, um die Lizenzdaten und Signaturen in einem textbasierten Format darzustellen.
*   **Signatur:** Ein kryptografischer "Fingerabdruck" der Lizenzdaten, der mit dem privaten Schlüssel erstellt wird. Er beweist, dass die Lizenzdaten authentisch sind und nicht manipuliert wurden und vom Besitzer des privaten Schlüssels stammen.
*   **Payload:**  Die eigentlichen Daten der Lizenz, wie z.B. die Version, das Ablaufdatum und optional die Hardware-ID.
*   **Hardware-ID (optional):**  Eine eindeutige Kennung eines Computers.  Lizenzen können optional an eine bestimmte Hardware-ID gebunden werden, um die Verwendung der Lizenz auf ein bestimmtes Gerät zu beschränken.

## 2. Voraussetzungen

Bevor Sie den Lizenzschlüssel-Generator verwenden, stellen Sie sicher, dass folgende Voraussetzungen erfüllt sind:

*   **Python 3.6 oder höher:**  Python muss auf Ihrem System installiert sein. Sie können Python von der offiziellen Webseite herunterladen: [https://www.python.org/downloads/](https://www.python.org/downloads/)

*   **PyCryptodome Bibliothek:**  Diese Bibliothek wird für die kryptografischen Operationen (RSA-Schlüssel, Signatur) benötigt. Sie können sie mit pip installieren:

    ```bash
    pip install pycryptodome
    ```

    **Hinweis:**  In einigen älteren Systemen kann es sein, dass Sie `cryptography` anstelle von `pycryptodome` installieren müssen. Das Skript verwendet `cryptography`. Installieren Sie es mit:

    ```bash
    pip install cryptography
    ```

*   **Zugriff auf die Python-Skriptdatei:**  Stellen Sie sicher, dass Sie Zugriff auf die Python-Datei `lizenzschluessel_generator.py` (oder wie auch immer Sie sie benannt haben) haben und dass Sie sie in Ihrem Terminal/Ihrer Kommandozeile ausführen können.

## 3. Installation (der Python-Bibliotheken)

Falls Sie die `cryptography` Bibliothek noch nicht installiert haben, öffnen Sie Ihr Terminal (oder die Eingabeaufforderung unter Windows) und führen Sie den folgenden Befehl aus:

```bash
pip install cryptography
```

Pip ist der Paketmanager für Python und wird verwendet, um externe Bibliotheken zu installieren.  Nachdem Sie diesen Befehl ausgeführt haben, sollte pip die `cryptography` Bibliothek herunterladen und installieren.  Sie können überprüfen, ob die Installation erfolgreich war, indem Sie versuchen, die Bibliothek in einer Python-Shell zu importieren:

```python
python
>>> from cryptography.hazmat.primitives.asymmetric import rsa
>>> exit()
```

Wenn keine Fehlermeldung angezeigt wird, ist die Bibliothek korrekt installiert.

## 4. Verwendung des Lizenzschlüssel-Generators

Das Python-Skript wird über die Befehlszeile (Terminal/Eingabeaufforderung) gesteuert. Es bietet verschiedene Aktionen, die Sie ausführen können.

### 4.1. Schlüsselpaar generieren (`generieren`)

Diese Aktion erstellt ein neues RSA-Schlüsselpaar (privater und öffentlicher Schlüssel). Dies ist der erste Schritt, den Sie ausführen müssen, wenn Sie noch kein Schlüsselpaar haben.

**Befehl:**

```bash
python lizenzschluessel_generator.py --schluessel_aktion generieren
```

**Optionale Parameter:**

*   `--privater_schluessel_pfad`:  Legt den Dateipfad für den privaten Schlüssel fest (Standard: `private_key.pem`).
*   `--oeffentlicher_schluessel_pfad`: Legt den Dateipfad für den öffentlichen Schlüssel fest (Standard: `public_key.pem`).

**Beispiel:**

Um ein Schlüsselpaar zu generieren und die Schlüssel in den Dateien `mein_privater_schluessel.pem` und `mein_oeffentlicher_schluessel.pem` zu speichern, verwenden Sie:

```bash
python lizenzschluessel_generator.py --schluessel_aktion generieren --privater_schluessel_pfad mein_privater_schluessel.pem --oeffentlicher_schluessel_pfad mein_oeffentlicher_schluessel.pem
```

**Ausgabe:**

Nach erfolgreicher Ausführung sehen Sie eine Ausgabe ähnlich der folgenden:

```
RSA Schlüsselpaar generiert und gespeichert:
- Privater Schlüssel: mein_privater_schluessel.pem
- Öffentlicher Schlüssel: mein_oeffentlicher_schluessel.pem

Pro-Lizenzschlüssel (signiert, RSA, Base64-kodiert):
[Hier wird der generierte Lizenzschlüssel angezeigt...]
```

**Erläuterung:**

*   Das Skript generiert ein 2048-Bit RSA-Schlüsselpaar.
*   Der private Schlüssel wird im PEM-Format ohne Passwortverschlüsselung in der Datei `private_key.pem` (oder dem angegebenen Pfad) gespeichert. **Achtung:** In Produktionsumgebungen sollten Sie den privaten Schlüssel **immer mit einem starken Passwort verschlüsseln** (siehe Abschnitt 4.2).
*   Der öffentliche Schlüssel wird im PEM-Format in der Datei `public_key.pem` (oder dem angegebenen Pfad) gespeichert.
*   Zusätzlich wird **ein Beispiel-Pro-Lizenzschlüssel generiert und in der Konsole ausgegeben**. Dieser Schlüssel wurde mit dem gerade generierten privaten Schlüssel signiert und ist für 365 Tage gültig (Standardwert).

**Wichtiger Hinweis zur Sicherheit:**

*   **Sichern Sie den privaten Schlüssel `private_key.pem` unbedingt!**  Verlieren Sie ihn nicht und geben Sie ihn niemals an Unbefugte weiter.  Der private Schlüssel ist der Schlüssel zur Erstellung gültiger Lizenzen.
*   Der öffentliche Schlüssel `public_key.pem` kann weitergegeben werden, da er nur zur Validierung von Lizenzen dient.

### 4.2. Schlüssel serialisieren (`serialisieren`)

Diese Aktion demonstriert, wie Sie ein bestehendes RSA-Schlüsselpaar serialisieren können.  Im Skript wird zwar ein *neues* Schlüsselpaar generiert, aber im realen Anwendungsfall würden Sie wahrscheinlich Ihre bereits existierenden Schlüssel laden und serialisieren, um sie z.B. in unterschiedlichen Formaten zu speichern oder zu exportieren.  **Besonders wichtig ist die Verschlüsselung des privaten Schlüssels mit einem Passwort für die sichere Speicherung!**

**Befehl:**

```bash
python lizenzschluessel_generator.py --schluessel_aktion serialisieren
```

**Optionale Parameter:**

*   `--privater_schluessel_pfad`:  Pfad zum privaten Schlüssel (wird hier zum Speichern der *serialisierten* Version verwendet, Standard: `private_key.pem`).
*   `--oeffentlicher_schluessel_pfad`: Pfad zum öffentlichen Schlüssel (wird hier zum Speichern der *serialisierten* Version verwendet, Standard: `public_key.pem`).

**Beispiel:**

```bash
python lizenzschluessel_generator.py --schluessel_aktion serialisieren
```

**Ausgabe:**

```
Serialisierter privater Schlüssel (PEM, verschlüsselt):
-----BEGIN ENCRYPTED PRIVATE KEY-----
[Hier wird der verschlüsselte private Schlüssel im PEM-Format angezeigt...]
-----END ENCRYPTED PRIVATE KEY-----

Serialisierter öffentlicher Schlüssel (PEM):
-----BEGIN PUBLIC KEY-----
[Hier wird der öffentliche Schlüssel im PEM-Format angezeigt...]
-----END PUBLIC KEY-----
```

**Erläuterung:**

*   Das Skript generiert **für Demonstrationszwecke ein neues Schlüsselpaar** (in der Praxis würden Sie Ihre vorhandenen Schlüssel laden).
*   Der private Schlüssel wird **mit dem Passwort `mein_geheimes_passwort` verschlüsselt** und im PEM-Format in der Konsole ausgegeben.  **Wichtig:**  Dieses Passwort ist nur ein Beispiel.  Verwenden Sie **immer ein starkes und einzigartiges Passwort** in realen Anwendungen.
*   Der öffentliche Schlüssel wird im PEM-Format (nicht verschlüsselt) in der Konsole ausgegeben.

**Wichtiger Hinweis zur Sicherheit:**

*   **Verschlüsseln Sie private Schlüssel immer mit einem starken Passwort**, wenn Sie sie auf der Festplatte speichern oder übertragen.  Das Beispiel im Skript verwendet `serialization.BestAvailableEncryption(passwort)`, was eine gute Wahl für die Verschlüsselung ist.
*   **Passwortmanagement:**  Denken Sie sorgfältig über die sichere Speicherung und Verwaltung des Passworts nach, das zum Verschlüsseln des privaten Schlüssels verwendet wird.  Ein verlorenes Passwort bedeutet, dass der private Schlüssel unbrauchbar wird.

### 4.3. Lizenzschlüssel validieren (`validieren`)

Diese Aktion verwendet den öffentlichen Schlüssel, um einen gegebenen Lizenzschlüssel zu validieren.  Dies ist der Schritt, der in Ihrer Software implementiert wird, um zu überprüfen, ob ein Benutzer eine gültige Lizenz besitzt.

**Befehl:**

```bash
python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "[Ihr_Lizenzschlüssel_hier]"
```

**Benötigte Parameter:**

*   `--lizenzschluessel`: Der Base64-kodierte Lizenzschlüssel, der validiert werden soll.  **Ersetzen Sie `[Ihr_Lizenzschlüssel_hier]` durch den tatsächlichen Lizenzschlüssel.**

**Optionale Parameter:**

*   `--oeffentlicher_schluessel_pfad`:  Pfad zum öffentlichen Schlüssel (Standard: `public_key.pem`).
*   `--hardware_id`:  Hardware-ID, gegen die die Lizenz validiert werden soll (optional).

**Beispiele:**

**1. Lizenzschlüssel validieren (einfach):**

Angenommen, Sie haben einen Lizenzschlüssel und möchten ihn mit dem öffentlichen Schlüssel `public_key.pem` validieren:

```bash
python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "IhrLizenzschlüssel..."
```

**2. Lizenzschlüssel validieren mit Hardware-ID-Prüfung:**

Wenn der Lizenzschlüssel an eine bestimmte Hardware-ID gebunden sein soll (z.B. `ABC-123-DEF-456`), verwenden Sie:

```bash
python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "IhrLizenzschlüssel..." --hardware_id ABC-123-DEF-456
```

**3. Lizenzschlüssel validieren mit einem anderen öffentlichen Schlüsselpfad:**

Wenn Ihr öffentlicher Schlüssel nicht in `public_key.pem` gespeichert ist, sondern z.B. in `oeffentlich.pem`:

```bash
python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "IhrLizenzschlüssel..." --oeffentlicher_schluessel_pfad oeffentlich.pem
```

**Ausgabe (gültige Lizenz):**

```
Lizenzschlüssel ist GÜLTIG.
Payload Daten:
{
    "version": "Pro",
    "ablaufdatum": "2025-02-28",
    "hardware_id": "ABC-123-DEF-456",
    "ausgestellt_am": "2024-03-01"
}
```

**Ausgabe (ungültige Lizenz):**

```
Lizenzschlüssel ist UNGÜLTIG.
```

**Mögliche Gründe für eine ungültige Lizenz:**

*   **Falsche Signatur:** Der Lizenzschlüssel wurde nicht mit dem passenden privaten Schlüssel signiert oder wurde manipuliert.
*   **Abgelaufen:** Das Ablaufdatum der Lizenz liegt in der Vergangenheit.
*   **Falsche Version:** Die Lizenz ist nicht für die erwartete Version ("Pro") ausgestellt.
*   **Hardware-ID stimmt nicht überein:** Wenn eine Hardware-ID-Prüfung durchgeführt wird, stimmt die im Lizenzschlüssel gespeicherte Hardware-ID nicht mit der angegebenen Hardware-ID überein.
*   **Fehler beim Dekodieren:**  Der Lizenzschlüssel ist kein gültiger Base64-String oder hat ein ungültiges JSON-Format.

**Erläuterung:**

*   Das Skript liest den öffentlichen Schlüssel aus der angegebenen Datei (oder `public_key.pem` standardmäßig).
*   Es dekodiert den Base64-kodierten Lizenzschlüssel.
*   Es extrahiert die Signatur und die Payload aus dem Lizenzschlüssel.
*   Es verwendet den öffentlichen Schlüssel, um die Signatur der Payload zu überprüfen.  Dies stellt sicher, dass die Payload nicht manipuliert wurde und vom Besitzer des privaten Schlüssels stammt.
*   Es überprüft, ob die Lizenz für die erwartete Version ("Pro") ausgestellt ist.
*   Es überprüft, ob das Ablaufdatum noch in der Zukunft liegt.
*   Wenn eine Hardware-ID angegeben wurde, überprüft es, ob die Hardware-ID im Lizenzschlüssel mit der angegebenen Hardware-ID übereinstimmt.
*   Wenn alle Prüfungen erfolgreich sind, wird die Lizenz als gültig betrachtet und die Payload-Daten (Version, Ablaufdatum, Hardware-ID, Ausstellungsdatum) werden ausgegeben. Andernfalls wird die Lizenz als ungültig markiert.

### 4.4. Pro-Lizenzschlüssel generieren (`generieren` mit Parametern)

Obwohl die Aktion `generieren` bereits einen Beispiel-Lizenzschlüssel ausgibt, können Sie die Lizenzschlüsselgenerierung auch direkt steuern, um spezifische Gültigkeitsdauern und Hardware-IDs festzulegen.

**Befehl (im Prinzip die `generieren` Aktion, aber mit zusätzlichen Parametern):**

```bash
python lizenzschluessel_generator.py --schluessel_aktion generieren --tage_gueltig [Anzahl_Tage] --hardware_id [Hardware_ID]
```

**Optionale Parameter (zusätzlich zu denen der `generieren` Aktion):**

*   `--tage_gueltig`:  Anzahl der Tage, für die der Lizenzschlüssel gültig sein soll (Standard: 365 Tage).
*   `--hardware_id`:  Hardware-ID, an die der Lizenzschlüssel gebunden werden soll (optional).

**Beispiele:**

**1. Pro-Lizenzschlüssel für 90 Tage gültig generieren:**

```bash
python lizenzschluessel_generator.py --schluessel_aktion generieren --tage_gueltig 90
```

**2. Pro-Lizenzschlüssel für 1 Jahr gültig und an Hardware-ID `XYZ-789-UVW-012` binden:**

```bash
python lizenzschluessel_generator.py --schluessel_aktion generieren --tage_gueltig 365 --hardware_id XYZ-789-UVW-012
```

**Ausgabe:**

Die Ausgabe ist ähnlich der Ausgabe der einfachen `generieren` Aktion, aber der generierte Lizenzschlüssel wird nun die angegebene Gültigkeitsdauer und Hardware-ID (falls angegeben) berücksichtigen.

```
RSA Schlüsselpaar generiert und gespeichert:
- Privater Schlüssel: private_key.pem
- Öffentlicher Schlüssel: public_key.pem

Pro-Lizenzschlüssel (signiert, RSA, Base64-kodiert):
[Hier wird der generierte Lizenzschlüssel angezeigt, der die angegebene Gültigkeitsdauer und Hardware-ID enthält...]
```

**Erläuterung:**

*   Wenn Sie die Parameter `--tage_gueltig` und/oder `--hardware_id` bei der `generieren` Aktion angeben, werden diese Werte in die Payload des generierten Lizenzschlüssels aufgenommen.
*   Die Gültigkeitsdauer wird als Ablaufdatum im Format `YYYY-MM-DD` im Lizenzschlüssel gespeichert.
*   Die Hardware-ID wird (falls angegeben) ebenfalls in der Payload gespeichert.
*   Der generierte Lizenzschlüssel ist weiterhin Base64-kodiert und signiert.

## 5. Anwendungsbeispiele (Zusammenfassung)

Hier sind einige typische Anwendungsfälle und die entsprechenden Befehle:

*   **Neues RSA-Schlüsselpaar generieren und in Standarddateien speichern:**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion generieren
    ```

*   **Neues RSA-Schlüsselpaar generieren und in benutzerdefinierten Dateien speichern:**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion generieren --privater_schluessel_pfad mein_firma_privat.pem --oeffentlicher_schluessel_pfad mein_firma_oeffentlich.pem
    ```

*   **Pro-Lizenzschlüssel für 6 Monate (180 Tage) generieren:**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion generieren --tage_gueltig 180
    ```

*   **Pro-Lizenzschlüssel für 1 Jahr gültig und an Hardware-ID `SERVER-ID-42` binden:**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion generieren --tage_gueltig 365 --hardware_id SERVER-ID-42
    ```

*   **Einen bestimmten Lizenzschlüssel validieren (mit Standard-öffentlichem Schlüsselpfad):**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "IhrSehrLangerLizenzschlüsselStringHier..."
    ```

*   **Einen Lizenzschlüssel validieren und die Hardware-ID `WORKSTATION-7` überprüfen:**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "IhrSehrLangerLizenzschlüsselStringHier..." --hardware_id WORKSTATION-7
    ```

*   **Einen Lizenzschlüssel validieren mit einem öffentlichen Schlüssel, der in `lizenz_oeffentlich.pem` gespeichert ist:**

    ```bash
    python lizenzschluessel_generator.py --schluessel_aktion validieren --lizenzschluessel "IhrSehrLangerLizenzschlüsselStringHier..." --oeffentlicher_schluessel_pfad lizenz_oeffentlich.pem
    ```

## 6. Fehlerbehebung

*   **`ModuleNotFoundError: No module named 'cryptography'` oder `ModuleNotFoundError: No module named 'Crypto'`:**  Stellen Sie sicher, dass Sie die `cryptography` Bibliothek (oder `pycryptodome`) korrekt mit `pip install cryptography` installiert haben. Überprüfen Sie die Schreibweise und stellen Sie sicher, dass Sie pip für die richtige Python-Installation verwenden (falls Sie mehrere Python-Versionen installiert haben).
*   **`FileNotFoundError: [Errno 2] No such file or directory: 'public_key.pem'`:**  Der öffentliche Schlüssel konnte nicht unter dem angegebenen Pfad gefunden werden. Stellen Sie sicher, dass der Pfad korrekt ist und die Datei existiert, besonders wenn Sie `--oeffentlicher_schluessel_pfad` verwenden.  Wenn Sie die Aktion `validieren` verwenden und noch kein Schlüsselpaar generiert haben, müssen Sie zuerst ein Schlüsselpaar mit der Aktion `generieren` erstellen.
*   **`Fehler bei der Lizenzvalidierung: InvalidSignature`:** Die Signatur des Lizenzschlüssels ist ungültig. Dies kann folgende Gründe haben:
    *   Der Lizenzschlüssel wurde manipuliert.
    *   Der Lizenzschlüssel wurde mit einem anderen privaten Schlüssel signiert als dem, zu dem der verwendete öffentliche Schlüssel gehört.
    *   Es gibt ein Problem mit der Implementierung der Signaturprüfung (weniger wahrscheinlich, wenn Sie das bereitgestellte Skript unverändert verwenden).
*   **`Lizenzschlüssel ist UNGÜLTIG.` (ohne detailliertere Fehlermeldung):**  In diesem Fall kann es verschiedene Gründe geben (abgelaufen, falsche Version, Hardware-ID-Fehler).  Überprüfen Sie die Payload-Daten des Lizenzschlüssels (falls Sie Zugriff darauf haben) und stellen Sie sicher, dass die erwarteten Bedingungen erfüllt sind.  Führen Sie das Validierungskommando ggf. erneut aus und prüfen Sie die Konsolenausgabe auf detailliertere Fehlermeldungen (z.B. durch Hinzufügen von `print` Anweisungen im `validiere_lizenzschluessel_pro` Funktionsteil zur Fehlerbehebung).
*   **Allgemeine Probleme mit Base64- oder JSON-Dekodierung:**  Fehler beim Dekodieren von Base64 oder JSON deuten darauf hin, dass der Lizenzschlüsselstring möglicherweise beschädigt oder kein gültiges Format hat. Stellen Sie sicher, dass der Lizenzschlüssel korrekt kopiert und eingefügt wurde und keine Zeichen fehlen oder hinzugefügt wurden.

## 7. Sicherheitshinweise

*   **Schutz des privaten Schlüssels ist entscheidend:** Der private Schlüssel ist das wertvollste Gut in diesem Lizenzsystem.  Er muss **absolut geheim und sicher** aufbewahrt werden.  Verlieren Sie ihn nicht, geben Sie ihn niemals an Unbefugte weiter und speichern Sie ihn sicher (idealerweise verschlüsselt und mit Zugriffskontrolle).
*   **Verwenden Sie starke Passwörter für die private Schlüsselverschlüsselung:**  Wenn Sie den privaten Schlüssel verschlüsseln (was dringend empfohlen wird), verwenden Sie ein starkes, zufälliges und einzigartiges Passwort.  Verwalten Sie dieses Passwort sicher.
*   **Öffentliche Schlüssel können sicher verteilt werden:** Der öffentliche Schlüssel dient nur zur Validierung und kann ohne Sicherheitsrisiko verteilt werden (z.B. in Ihrer Software enthalten sein).
*   **Regelmäßige Schlüsselrotation (optional, aber empfehlenswert für langfristige Sicherheit):**  Für langfristige Sicherheit sollten Sie in Erwägung ziehen, Schlüsselpaare in regelmäßigen Abständen zu rotieren (neue Schlüsselpaare generieren und alte Schlüssel nach einer Übergangszeit ausser Betrieb nehmen).  Dies minimiert das Risiko, falls ein privater Schlüssel kompromittiert wird.
*   **Sichere Übertragung von Lizenzschlüsseln:**  Übertragen Sie Lizenzschlüssel sicher, insbesondere wenn sie sensible Informationen enthalten (wie z.B. Hardware-IDs).  Verwenden Sie HTTPS oder andere sichere Kanäle, um die Übertragung zu schützen.

## 8. Zusammenfassung

Dieses Dokument hat Ihnen eine detaillierte Anleitung zur Verwendung des CipherCore Lizenzschlüssel-Generators gegeben. Sie haben gelernt, wie Sie:

*   RSA-Schlüsselpaare generieren.
*   Private und öffentliche Schlüssel serialisieren und speichern.
*   Pro-Lizenzschlüssel mit konfigurierbarer Gültigkeitsdauer und optionaler Hardware-ID generieren.
*   Lizenzschlüssel mit dem öffentlichen Schlüssel validieren (inklusive optionaler Hardware-ID-Prüfung).

Durch die Befolgung dieser Anleitung und die Beachtung der Sicherheitshinweise können Sie das Lizenzsystem effektiv nutzen, um Ihre CipherCore "Pro"-Software zu schützen und zu lizenzieren.

---

**Urheberrechtsvermerk und Lizenz (Wiederholung):**

__copyright__ = "Copyright (c) 2024 CipherCore GmbH"
__license__ = "Proprietär - Alle Rechte vorbehalten"

Bitte beachten Sie, dass dieses Dokument und das zugehörige Python-Skript urheberrechtlich geschützt sind und unter einer proprietären Lizenz stehen.  Die Verwendung ist nur gemäß den Bedingungen dieser Lizenz gestattet.
