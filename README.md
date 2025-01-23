# Bestille oversettelse av bøker 

## Introduksjon til appen
Dette prosjektet er en webapplikasjon laget med Flask (Python) og MariaDB som database. Appen lar brukere registrere seg med navn, e-post og passord. Den sjekker at informasjonen er gyldig før den lagrer den i databasen. Flask fungerer som serveren som kobler sammen nettsiden og databasen. Applikasjonen har som mål at kunden skal kunne bestille oversettning av bøker og at dette skal lagre i en database.

## Hva du trenger 📁

Før du begynner, må du ha følgende installert på datamaskinen din:

- **Git**: For å klone prosjektet fra GitHub.

- **Python**: For å kunne kjøre Flask og andre Python-biblioteker.

- **MariaDB**: For å kunne lagre brukerdata.

Hvis du er usikker på hvordan dette gjøres, kan du følge disse veiledningene for å sette opp MariaDB på Ubuntu 20.04 eller 22.04.
  
📍  [How To Install MariaDB on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04)
📍 [How To Install MariaDB on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-22-04)

--- 
Følg trinnene nedenfor for å sette opp appen på din 
maskin.

## Sette opp prosjektet ⌨️
1. Klon prosjektet: Først, åpne terminalen (eller kommandolinjen) på datamaskinen din og klon prosjektet ved å bruke 

````bash
git clone https://github.com/lauryteey/order_books.git
````
Dette laster ned hele prosjektet til din maskin.

Men du kan også last ned ZIP-filen og pakk den ut.

2. Installer nødvendige biblioteker: Gå til prosjektmappen som du nettopp klonet

````bash
cd <prosjekt-mappen>
````

Opprett et virtuelt miljø for å holde alle bibliotekene bare for de prosjektet.

`````bash
python3 -m venv myenv
````````
Deretter aktiver den virtuelle miljøet.

`````bash
myenv\Scripts\activate
``````
---
Når du har aktivert det virtuelle miljøet, kan du installere alle nødvendige biblioteker fra ````requirements.txt````

````bash
pip install -r requirements.txt
````
Hvis filen requirements.txt mangler, kan du installere de viktigste manuelt:

````bash
pip install flask mysql-connector
pip install Flask
````
Deretter i terminalen gå til mappen der filene ligger og start applikasjonen:
`````bash
python app.py
```````

Åpne nettleseren og gå til ip adressen du får fra flask med ````CTRL + click````
