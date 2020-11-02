# libts
Modulo Python per la lettura della Carta Nazionale dei Servizi (TS-CNS)
 
##  Dipendenze

[pyscard](https://pypi.org/project/pyscard/)

## Metodi esposti

* NETLINKFormatGetName
* NETLINKFormatGetSurname
* NETLINKFormatGetDateOfBirth
* NETLINKFormatGetCf
* NETLINKFormatGetTsStartValidity
* NETLINKFormatGetTsEndValidity
* NETLINKFormatGetAddress - Indirizzo di residenza
* NETLINKFormatGetDoctor - Medico (se assegnato)
* NETLINKFormatGetPostalCode

## Utilizzo

```python
from smartcard.System import readers
from libts import TSCns

readers = readers()
reader = readers[0]
connection = reader.createConnection()
connection.connect()

tscns = TSCns(connection)	
print("indirizzo di Residenza: {}".format(tscns.NETLINKFormatGetAddress()))
...

```
