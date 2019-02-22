01:04 21.07.2009

Programm "rad2krl" Version 1.4
-------------------------------

Readme zum Programm "rad2krl"(geschrieben in Python3 - Version 3.0.1)

Auf dieser CD befinden sich 4 Verzeichnisse.

documentation - Beinhaltet Dokumentation und Hinweise �ber das Programm "rad2krl"
kukaconfigs - Konfigurationsdateien, die nur bei einem KUKA-Roboter-Reset oder einem fabrikneuen Roboter eingespielt werden m�ssen, damit das Programm korrekt ablaufen kann.
pyinstaller - Installationsdatei von Python 3 und Installationshinweise f�r andere Betriebssysteme als Windows. (Damit das Programm "rad2krl" l�uft, ist vorher Python3 zu installieren!)
pyprogram - RAD2KRL_v1_3 - eigentliches Programm (zum Starten einfach doppelklicken)
ppt - Projekt-/Diplomarbeitstatus - Zwischen- u. Endpr�sentation

------------------------------

Dieses Tool erzeugt KRL(KUKA Roboter Language) Code bzw. Bewegungsanweisungen,
damit Pr�ffeldlinien von Pr�ffeldern wie Phase I, II und ENCAP automatisiert
auf eine beliebige Fahrzeugfront �bertragen werden k�nnen.
Es dient als Schnittstelle zwischen dem Programm Hypermesh v9 von Altair am Rechner
und der Robotersteuerung (KRC2), die die zu zeichnenden Pr�ffeldlinien als Bewegungsanweisungen
f�r den verwendeten KUKA-Roboter interpretieren muss.

Ausgehend von den .rad-Dateien (= Export aus Hypermesh v9 einer Punkteliste XYZ - liegend auf Prueffeldlinien) werden
diese in .src Dateien (Lauff�hige KUKA/KRL Programme mit Bewegungsanweisungen f�r einen KUKA-Roboter) konvertiert.

Der KUKA-Roboter f�hrt nach korrekter Einmessung in Fahrzeug und Werkzeug (Lackstift-Halterung) nun die Bewegungsanweisungen durch und
zeichnet die Linien mittels am Roboterarm angebrachten Lackstift ein.

(N�heres in der Doku bzw Diplomarbeit "Roboterprogrammierung f�r die automatisierte �bertragung von Pr�ffeldern im Fussg�ngerschutz")

Die Entwicklung fand im Rahmen dieser Diplomarbeit im Zeitraum von Jan. 09 - Jul 09 statt.

Author: Pucher Alfred

-------------------------------
Neuerungen in der v1.4:

-Programm nimmt als Dateicache nur mehr Home-Verzeichnisse des Users
-Verbesserte Dialogf�hrung



