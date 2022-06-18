# 14100 DWD Unwetter

## Beschreibung 

Der Baustein liest die [JSON-Daten zu aktuellen Unwetterwarnungen des DWD](https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json) aus und stellt die Informationen zur Verfügung.
Bei mehreren Warnungen wird die höchste Unwetterwarnung ausgegeben - unabhängig vom Warnzeitraum.

## Eingänge

| Nr. | Name | Initialisierung | Beschreibung |
| --- | ---  | --- | --- |
| 1   | Trigger | 0 | Bei einem Wert =1 wird die aktuelle DWD-Json datei abgerfen und ausgewertet. |
| 2 | Region Id | | *Id* der Region / Stadt / Landkreis aus der DWD-Json Datei, für die die Unwetterdaten ausgegeben werden sollen. |
| 3 | Region | | *Name* der Region / Stadt / Landkreis aus der DWD-Json Datei, für die die Unwetterdaten ausgegeben werden sollen. Innerhalb der Json-Datei wird nach dem 1. Vorkommen des Namens gesucht. "Frankfurt" liefert die Ergebnisse für Frankfurt am Main oder Frankfurt an der Oder |


## Ausgänge

Hinweis: Alle Textausgänge werden Umlaute und Sonderzeichen mit XML Reference Characters ersetzt nach dem Schema &amp#123;.


| Nr. | Name | Initialisierung | Beschreibung |
| --- | --- | --- | --- |
| 1   |Überschrift | | Überschrift der Unwetterwarnung. |
| 2 | Level | 0 | Level der höchsten Unwetterwarnung für die Gemeinde / Stadt. | 
| 3 | Beschreibung 	| | Beschreibung der Unwetterwarnung | 
| 4 | Hinweise | | Handlungsempfehlungen für die Unwetterwarnung. | 
| 5 | Startzeit | 0 | Start-Zeit des Warnfensters in s als [UNIX-Zeit](https://de.wikipedia.org/wiki/Unixzeit). |
| 6 | Stoppzeit | 0 | Stop-Zeit des Warnfensters in s als [UNIX-Zeit](https://de.wikipedia.org/wiki/Unixzeit). |
| 7 | Text alle Warnungen | | Text, der alle aktuell gemeldeten Warnereignisse auflistet. Leer, wenn keine Warnungen vorliegen. |
| 8 | Text Wetterwarnung (Lv 1) | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis dem DWD Level 1 (=2 am Ausgang Level) entspricht. Sonst wird ein leerer Text ausgegeben. |
| 9 | Text Wetterwarnung (Lv 2) | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis dem DWD Level 2 (=3 am Ausgang Level) entspricht. Sonst wird ein leerer Text ausgegeben. |
| 10 | Text Wetterwarnung (Lv 3) | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis dem DWD Level 3 (=4 am Ausgang Level) entspricht. Sonst wird ein leerer Text ausgegeben. |
| 11 | Text Wetterwarnung (Lv 4) | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis dem DWD Level 4 (=5 am Ausgang Level) entspricht. Sonst wird ein leerer Text ausgegeben. |
| 12 | Text Vorabinformation Unwetter | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis einer Vorwarnung entspricht (=1 am Ausgang Level). Sonst wird ein leerer Text ausgegeben. |
| 13 | Text Hitzewarnung | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis einer Hitzewarnung entspricht (=10 am Ausgang Level). Sonst wird ein leerer Text ausgegeben. |
| 14 | Text UV-Warnung | | Gibt eine Liste aller Warnereignisse aus, wenn das höchste Warnereignis einer UV-Warnung entspricht (=20 am Ausgang Level). Sonst wird ein leerer Text ausgegeben. |
| 15 | Warnung aktiv (sbc) | 0 | 1 wenn die aktuelle Zeit im Warnfenster liegt, also die Warnung akut ist. |
| 16 | Error | 0 | 1 wenn ein Fehler vorliegt. Die HS-Debug-Seite (hs-ip/hslist?lst=debug)liefert in der Kategorie HSL 2.0 und der Unterkategorie hsl20_3_dwd mehr Details. |
| 17 | Json | |  |

## Beispielwerte

| Eingang | Ausgang |
| --- | --- |
| - | - |


## Other

- Neuberechnug beim Start: Nein
- Baustein ist remanent: nein
- Interne Bezeichnung: 14101
- Kategorie: Datenaustausch

### Change Log

- v1.4
    - Bug: UV und Hitze Warnungenw erden in Leveln gem. Doku unterschieden
- v1.2
    - Umstellung auf lokale Unwetterprognose (wfs Abfrage)
- v1.1
    - Hitzewarnungen werden weiter gegeben
- v1.0

### Open Issues / Know Bugs

- keine

### Support

Please use [github issue feature](https://github.com/En3rGy/14101_DWDUnwetter/issues) to report bugs or rise feature requests.
Questions can be addressed as new threads at the [knx-user-forum.de](https://knx-user-forum.de) also. There might be discussions and solutions already.


### Code

Der Code des Bausteins befindet sich in der hslz Datei oder auf [github](https://github.com/En3rGy/14101_DWDUnwetter).

### Devleopment Environment

- [Python 2.7.18](https://www.python.org/download/releases/2.7/)
    - Install python markdown module (for generating the documentation) `python -m pip install markdown`
- Python editor [PyCharm](https://www.jetbrains.com/pycharm/)
- [Gira Homeserver Interface Information](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip)


## Requirements
-

## Software Design Description


## Validation & Verification
- Unit tests are performed.

## Licence

Copyright 2021 T. Paul

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
