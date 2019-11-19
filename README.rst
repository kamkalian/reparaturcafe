"""""""""""""""""""""""""""""
Webtool für ein Reparaturcafe
"""""""""""""""""""""""""""""
.....................................................................
Zur Digitalisierung und Dokumentation von Reparaturen defekter Geräte
.....................................................................

.. contents:: Inhalt
   :depth: 3


Wofür ist dieses Webtool gut?
=============================
Mit diesem Webtool kannst Du eine Datenbank aufbauen,
in der alle reparierten Geräte dokumentiert werden.

Folgende Features stehen zur verfügung:

- Es können Anfragen, sogenannte Onlinechecks erstellt werden
- Eine Übersicht zeigt alle Onlinechecks in einer filterbaren Liste an
- Mit dem Statuskonzept kannst Du den aktuellen Status eines Onlinechecks
  setzen und ändern
- Der Telegram Bot meldet in Echtzeit aktuelle Statusänderungen.

Was wird benötigt?
==================
- Umgebung in der Python3.7 oder höher läuft
  (z.B. ein Virtueller Server mit Ubuntu)
- MySQL Datenbank
- Dieses Repo von github.com
- Weitere Pakete aus der requirements.txt
- nginx Webserver


Schritt für Schritt Anleitung
=============================

Vorraussetzungen
----------------
Es wird vorrausgesetzt das eine Maschine mit Ubuntu oder
einem anderen Linux System vorhanden ist.
Die Maschine sollte soweit abgesichert sein das z.B:

Grundlegende Software installieren
----------------------------------
Zu aller erst installieren wir Python, MySQL Datenbank und den Nginx Webserver

.. code-block:: sh

    sudo apt-get install python3 mysql nginx

MySQL Datenbank einrichten
--------------------------
In der MySQL Datenbank brauchen wir einen User und eine Datenbank, 
in der später die Tabellen angelegt werden.
Zum Einrichten benutzen wir das Kommandozeilentool ``mysql``.
Dazu gehen wir per Terminal in mysql rein:

.. code-block:: sh

    sudo mysql

User anlegen
^^^^^^^^^^^^
Der User wird mit folgendem Befehl angelegt:

.. code-block:: mysql

    create user 'USERNAME'@'localhost' identified by 'PASSWORD';

Datenbank erstellen
^^^^^^^^^^^^^^^^^^^
Erstelle eine Datenbank mit dem Namen "reparaturcafe".

.. code-block:: mysql

    create database reparaturcafe;

User für Datebank berechtigen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Damit der User auch auf die Datenbank zugreifen kann muss er noch
berechtigt werden.

.. code-block:: mysql

    grant all privileges on reparaturcafe.* to 'USERNAME'@'localhost';


.. hint::

    Diese Seite ist gerade im Aufbau, bald geht es hier weiter.
