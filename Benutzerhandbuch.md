# Benutzeranleitung für CipherCore Datei Vergleichs Tool Pro

## 1. Einführung in CipherCore Datei Vergleichs Tool Pro

Willkommen beim CipherCore Datei Vergleichs Tool Pro! Dieses Werkzeug wurde entwickelt, um Ihnen einen präzisen und effizienten Vergleich zwischen zwei Dateien zu ermöglichen. Es identifiziert Unterschiede und Gemeinsamkeiten und präsentiert diese in einem übersichtlichen PDF-Bericht mit Diagrammen. Die Pro-Version bietet erweiterte Funktionen wie Kreisdiagramme und die Speicherung von Vergleichsverläufen, um Ihre Analysen noch umfassender zu gestalten.

**Hauptmerkmale der Pro Version:**

*   **Umfassende Dateiformatunterstützung:** Verarbeitet CSV-, TXT-, XLS- und XLSX-Dateien.
*   **Detaillierte Vergleichsmetriken:**  Berechnet wichtige Statistiken wie Anzahl der Einträge, übereinstimmende Namen und prozentuale Unterschiede.
*   **Visuelle Diagramme:** Erstellt Balken- und Kreisdiagramme (exklusiv in der Pro-Version) zur anschaulichen Darstellung der Ergebnisse.
*   **Professionelle PDF-Berichte:** Generiert detaillierte Berichte mit Logo, Statistiken, Diagrammen und Firmeninformationen.
*   **Verlaufsspeicherung:** Speichert Vergleichsergebnisse in einer Datenbank oder JSON-Dateien für spätere Einsicht und Analyse (exklusiv in der Pro-Version).
*   **Lizenzschlüsselaktivierung:**  Nutzt einen Lizenzschlüssel zur Freischaltung der Pro-Funktionen und zur Validierung der Softwarelizenz.
*   **Sicherheit und Datenschutz:** Entwickelt mit Fokus auf Datensicherheit und Einhaltung von Datenschutzrichtlinien.

## 2. Schlüsselkonzepte und Lizenzierung

### 2.1 Was sind Schlüssel im Kontext von CipherCore Pro?

Im CipherCore Datei Vergleichs Tool Pro spielen **Lizenzschlüssel** eine zentrale Rolle. Diese Schlüssel sind digitale Codes, die Ihre **Berechtigung zur Nutzung der Pro-Version** bestätigen und freischalten.  Sie stellen sicher, dass Sie die erweiterten Funktionen und den vollen Umfang des Tools gemäß den Lizenzbedingungen von CipherCore GmbH nutzen können.

**Arten von Schlüsseln in dieser Software:**

*   **Lizenzschlüssel (Pro Version):**  Ein eindeutiger, alphanumerischer Code, den Sie beim Erwerb der Pro-Version erhalten. Dieser Schlüssel wird in der Software eingegeben, um die Pro-Funktionen zu aktivieren und die Testversionsbeschränkungen aufzuheben.
*   **Öffentlicher Schlüssel (für Lizenzvalidierung):** Ein kryptographischer Schlüssel, der fest in der Software integriert ist (`public_key.pem`). Dieser Schlüssel wird von der Software verwendet, um die **Echtheit und Gültigkeit Ihres Lizenzschlüssels zu überprüfen**.  Sie interagieren nicht direkt mit diesem Schlüssel, er arbeitet im Hintergrund.

**Wichtiger Hinweis:** Der öffentliche Schlüssel ist **nur zum Überprüfen** von Signaturen gedacht. Er kann **nicht** verwendet werden, um Lizenzschlüssel zu erstellen oder zu entschlüsseln. Die **Erstellung und Signierung von Lizenzschlüsseln ist ein sicherer Prozess**, der außerhalb dieser Software von CipherCore durchgeführt wird.

### 2.2 Warum werden Schlüssel verwendet?

*   **Lizenzmanagement:** Schlüssel ermöglichen es CipherCore GmbH, die Nutzung der Pro-Version zu verwalten und sicherzustellen, dass nur lizenzierte Benutzer die erweiterten Funktionen nutzen können.
*   **Schutz vor Softwarepiraterie:** Die Lizenzschlüsselvalidierung hilft, unautorisierte Kopien der Pro-Software zu erkennen und deren Nutzung einzuschränken.
*   **Sicherstellung der Softwareintegrität:** Durch die kryptographische Signatur der Lizenzschlüssel (mit dem privaten Schlüssel von CipherCore und Überprüfung mit dem öffentlichen Schlüssel in der Software) wird sichergestellt, dass der Lizenzschlüssel **nicht manipuliert** wurde und **von CipherCore stammt**.
*   **Freischaltung erweiterter Funktionen:**  Die Pro-Version bietet zusätzliche Features (Kreisdiagramme, Verlaufsspeicherung), die durch den Lizenzschlüssel freigeschaltet werden. Die Testversion ist in diesen Funktionen eingeschränkt.

### 2.3 Testversion vs. Pro Version und Schlüssel

*   **Testversion:** Nach dem ersten Start des Tools beginnt automatisch eine 14-tägige Testphase. In dieser Zeit können Sie die grundlegenden Funktionen des Datei Vergleichs Tools nutzen.  **Die Testversion benötigt keinen Lizenzschlüssel für die grundlegenden Funktionen**.  Allerdings sind bestimmte Pro-Funktionen (wie Kreisdiagramme und Verlaufsspeicherung) in der Testversion **deaktiviert**.
*   **Pro Version:** Um die **vollen Funktionen** des CipherCore Datei Vergleichs Tools Pro freizuschalten, benötigen Sie einen **gültigen Lizenzschlüssel**. Diesen erhalten Sie beim Kauf der Pro-Version von CipherCore GmbH.  Durch die Eingabe und Aktivierung des Lizenzschlüssels wird die Software in die Pro-Version umgewandelt, und alle Features werden zugänglich.

**Zusammenfassend:**

*   **Kein Schlüssel für Testversion (Grundfunktionen).**
*   **Lizenzschlüssel erforderlich für Pro Version (volle Funktionalität).**

## 3. Nutzung von Schlüsseln im CipherCore Datei Vergleichs Tool Pro

### 3.1 Lizenzschlüssel eingeben und aktivieren

1.  **Starten Sie das CipherCore Datei Vergleichs Tool Pro.**
2.  **Lizenzschlüssel-Feld:**  Im oberen Bereich der Benutzeroberfläche finden Sie ein Feld mit der Beschriftung "Lizenzschlüssel (Pro Version):".
3.  **Lizenzschlüssel eingeben:** Geben Sie Ihren **gültigen Lizenzschlüssel** in dieses Feld ein. Achten Sie genau auf die **Groß- und Kleinschreibung** und alle Zeichen. Es empfiehlt sich, den Lizenzschlüssel zu **kopieren und einzufügen**, um Tippfehler zu vermeiden.
4.  **"Schlüssel aktivieren" Button:** Klicken Sie auf den Button **"Schlüssel aktivieren"** direkt neben dem Lizenzschlüssel-Feld.
5.  **Lizenzvalidierung:** Das Tool **überprüft nun automatisch die Gültigkeit Ihres Lizenzschlüssels** im Hintergrund. Dieser Prozess kann einen kurzen Moment dauern.
6.  **Statusanzeige:** Unterhalb des Lizenzschlüsselfelds wird eine **Statusmeldung** angezeigt, die den **Lizenzstatus** wiedergibt:
    *   **"Lizenzstatus: Pro Version" (Grün):**  Zeigt an, dass Ihr Lizenzschlüssel **erfolgreich aktiviert** wurde und Sie die Pro-Version nutzen. Alle Pro-Funktionen sind nun freigeschaltet.
    *   **"Lizenzstatus: Test Version" (Rot):**  Zeigt an, dass **kein gültiger Lizenzschlüssel aktiviert** ist oder die **Validierung fehlgeschlagen** ist. Sie nutzen weiterhin die Testversion mit eingeschränkten Funktionen.

**Hinweis:**

*   **Internetverbindung:**  Für die Lizenzvalidierung ist **keine ständige Internetverbindung erforderlich**. Die Validierung erfolgt primär anhand des öffentlichen Schlüssels, der in der Software enthalten ist. In bestimmten Fällen (z.B. bei komplexeren Lizenzmodellen) kann jedoch eine gelegentliche Online-Validierung erfolgen.
*   **Lizenzschlüssel speichern:**  Der eingegebene Lizenzschlüssel wird in der Konfigurationsdatei des Tools gespeichert, sodass Sie ihn **nicht bei jedem Start erneut eingeben** müssen.

### 3.2 Was passiert nach der Aktivierung des Lizenzschlüssels?

Nachdem Sie einen gültigen Lizenzschlüssel erfolgreich aktiviert haben, ändert sich das Verhalten des CipherCore Datei Vergleichs Tools Pro wie folgt:

*   **Pro-Funktionen freigeschaltet:**
    *   **Kreisdiagramm-Option:**  Im Dropdown-Menü "Diagrammtyp" ist nun die Option **"Kreisdiagramm" aktiv und auswählbar**. In der Testversion ist diese Option ausgegraut und nicht nutzbar.
    *   **Verlaufsspeicherung:**  Die Vergleichsergebnisse werden nun **persistent gespeichert**, entweder in einer SQLite-Datenbank oder als JSON-Dateien, je nach Ihrer Konfiguration. Dies ermöglicht Ihnen, frühere Vergleiche über den Button **"Verlauf anzeigen"** einzusehen. In der Testversion werden die Ergebnisse nicht gespeichert.
    *   **Keine Testphasen-Einschränkungen:**  Hinweise zur ablaufenden Testphase werden nicht mehr angezeigt.
*   **Lizenzstatusanzeige:** Die Lizenzstatusanzeige bleibt auf **"Lizenzstatus: Pro Version" (Grün)**, solange der Lizenzschlüssel gültig ist.
*   **Voller Funktionsumfang:** Sie können nun den **vollen Funktionsumfang** des CipherCore Datei Vergleichs Tools Pro nutzen und von allen Vorteilen der Pro-Version profitieren.

### 3.3 Was tun, wenn die Lizenzschlüsselaktivierung fehlschlägt?

Es kann verschiedene Gründe geben, warum die Lizenzschlüsselaktivierung fehlschlägt. Hier sind einige häufige Probleme und Lösungsansätze:

1.  **Falscher Lizenzschlüssel:**
    *   **Überprüfen Sie die Eingabe:** Stellen Sie sicher, dass Sie den Lizenzschlüssel **korrekt eingegeben** haben. Achten Sie auf Groß- und Kleinschreibung, Ziffern und Sonderzeichen.
    *   **Kopieren und Einfügen:** Verwenden Sie **Kopieren und Einfügen**, um Tippfehler zu vermeiden.
    *   **Lizenzschlüsselquelle prüfen:**  Vergewissern Sie sich, dass Sie den **richtigen Lizenzschlüssel** verwenden, den Sie beim Kauf der Pro-Version erhalten haben.
2.  **Ungültiger Lizenzschlüssel:**
    *   **Lizenzschlüsselgültigkeit:**  Überprüfen Sie, ob Ihr Lizenzschlüssel **noch gültig** ist.  Einige Lizenzen sind zeitlich begrenzt.
    *   **Lizenztyp:** Stellen Sie sicher, dass der Lizenzschlüssel **für die Pro-Version** des CipherCore Datei Vergleichs Tools bestimmt ist.
3.  **Technische Probleme (selten):**
    *   **Neustart der Software:**  **Starten Sie das CipherCore Datei Vergleichs Tool Pro neu** und versuchen Sie die Lizenzaktivierung erneut.
    *   **Kontaktieren Sie den Support:** Wenn das Problem weiterhin besteht, **kontaktieren Sie den CipherCore GmbH Support** (support@ciphercore.de) mit Ihrem Lizenzschlüssel und einer Beschreibung des Problems.

**Fehlermeldungen:**

Bei einer fehlgeschlagenen Lizenzschlüsselaktivierung kann eine **Fehlermeldung** im Tool angezeigt werden.  Achten Sie auf diese Meldung, da sie oft Hinweise auf die Ursache des Problems gibt.  Typische Fehlermeldungen sind:

*   **"Ungültiger Lizenzschlüssel. Bitte überprüfen Sie Ihren Lizenzschlüssel."** (Deutet auf einen fehlerhaften oder ungültigen Schlüssel hin).
*   **"Fehler bei der Lizenzschlüsselvalidierung: ... (Details zum Fehler)"** (Kann auf technische Probleme hinweisen).

**In jedem Fall:**  Wenn Sie Probleme bei der Lizenzschlüsselaktivierung haben, zögern Sie nicht, den **CipherCore GmbH Support** zu kontaktieren.  Wir helfen Ihnen gerne weiter!

## 4. Umgang mit Schlüsseln und Sicherheitshinweise

### 4.1 Sicherer Umgang mit Ihrem Lizenzschlüssel

Ihr Lizenzschlüssel ist vertraulich und sollte **sicher behandelt** werden.  Hier einige Empfehlungen:

*   **Nicht weitergeben:** Geben Sie Ihren Lizenzschlüssel **nicht an unbefugte Dritte weiter**. Er ist personengebunden oder für Ihr Unternehmen bestimmt.
*   **Sicher aufbewahren:** Bewahren Sie den Lizenzschlüssel an einem **sicheren Ort** auf, z.B. in Ihren E-Mails (Kaufbestätigung) oder in einem Passwort-Manager.
*   **Bei Bedarf erneut eingeben:**  Sollten Sie die Software auf einem neuen Computer installieren oder die Konfiguration zurücksetzen, benötigen Sie den Lizenzschlüssel erneut zur Aktivierung.

### 4.2 Sicherheit der Lizenzschlüsselvalidierung

*   **RSA-basierte Validierung:** Die Lizenzschlüsselvalidierung im CipherCore Datei Vergleichs Tool Pro verwendet **moderne kryptographische Verfahren (RSA)**. Dies bietet ein **hohes Maß an Sicherheit** gegen Fälschungen und Manipulationen.
*   **Öffentlicher Schlüssel in Software:** Der **öffentliche Schlüssel** für die Validierung ist **fest in der Software integriert** und wird nicht extern abgefragt. Dies minimiert das Risiko von Man-in-the-Middle-Angriffen.
*   **Kein privater Schlüssel in Software:** Der **private Schlüssel**, der zum Erstellen und Signieren der Lizenzschlüssel verwendet wird, **befindet sich NICHT in der Software**. Er wird **sicher von CipherCore GmbH verwaltet**.
*   **Regelmäßige Software-Updates:** CipherCore GmbH empfiehlt, die Software **regelmäßig auf Updates zu prüfen** und zu installieren. Updates können Sicherheitsverbesserungen und Fehlerbehebungen enthalten, die auch die Lizenzschlüsselvalidierung betreffen können.

**Wichtiger Hinweis:**  Obwohl die Lizenzschlüsselvalidierung sicher gestaltet ist, ist es wichtig, dass Sie Ihren **Lizenzschlüssel selbst schützen** und die oben genannten Sicherheitshinweise beachten.

## 5. Zusammenfassung und Support

Der Lizenzschlüssel ist Ihr **Schlüssel zur vollen Funktionalität** des CipherCore Datei Vergleichs Tools Pro.  Durch die korrekte Eingabe und Aktivierung schalten Sie die erweiterten Pro-Funktionen frei und nutzen das Tool in seinem vollen Umfang.

**Bei Fragen oder Problemen rund um Lizenzschlüssel oder die Software im Allgemeinen:**

*   **Lesen Sie diese Benutzeranleitung sorgfältig durch.**
*   **Besuchen Sie die CipherCore GmbH Webseite:** [www.ciphercore.de](www.ciphercore.de) (Beispielwebseite)
*   **Kontaktieren Sie den CipherCore GmbH Support:** [support@ciphercore.de](mailto:support@ciphercore.de)

Wir wünschen Ihnen viel Erfolg bei der Nutzung des CipherCore Datei Vergleichs Tools Pro!
