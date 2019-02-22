01:04 21.07.2009

Programm "rad2krl" Version 1.4
-------------------------------

Readme zum Programm "rad2krl"(geschrieben in Python3 - Version 3.0.1)

Auf dieser CD befinden sich 4 Verzeichnisse.

documentation - Beinhaltet Dokumentation und Hinweise über das Programm "rad2krl"
kukaconfigs - Konfigurationsdateien, die nur bei einem KUKA-Roboter-Reset oder einem fabrikneuen Roboter eingespielt werden müssen, damit das Programm korrekt ablaufen kann.
pyinstaller - Installationsdatei von Python 3 und Installationshinweise für andere Betriebssysteme als Windows. (Damit das Programm "rad2krl" läuft, ist vorher Python3 zu installieren!)
pyprogram - RAD2KRL_v1_3 - eigentliches Programm (zum Starten einfach doppelklicken)
ppt - Projekt-/Diplomarbeitstatus - Zwischen- u. Endpräsentation

------------------------------

Dieses Tool erzeugt KRL(KUKA Roboter Language) Code bzw. Bewegungsanweisungen,
damit Prüffeldlinien von Prüffeldern wie Phase I, II und ENCAP automatisiert
auf eine beliebige Fahrzeugfront übertragen werden können.
Es dient als Schnittstelle zwischen dem Programm Hypermesh v9 von Altair am Rechner
und der Robotersteuerung (KRC2), die die zu zeichnenden Prüffeldlinien als Bewegungsanweisungen
für den verwendeten KUKA-Roboter interpretieren muss.

Ausgehend von den .rad-Dateien (= Export aus Hypermesh v9 einer Punkteliste XYZ - liegend auf Prueffeldlinien) werden
diese in .src Dateien (Lauffähige KUKA/KRL Programme mit Bewegungsanweisungen für einen KUKA-Roboter) konvertiert.

Der KUKA-Roboter führt nach korrekter Einmessung in Fahrzeug und Werkzeug (Lackstift-Halterung) nun die Bewegungsanweisungen durch und
zeichnet die Linien mittels am Roboterarm angebrachten Lackstift ein.

(Näheres in der Doku bzw Diplomarbeit "Roboterprogrammierung für die automatisierte Übertragung von Prüffeldern im Fussgängerschutz")

Die Entwicklung fand im Rahmen dieser Diplomarbeit im Zeitraum von Jan. 09 - Jul 09 statt.

Author: Pucher Alfred

-------------------------------
Neuerungen in der v1.4:

-Programm nimmt als Dateicache nur mehr Home-Verzeichnisse des Users
-Verbesserte Dialogführung



