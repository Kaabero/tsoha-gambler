# Vedonlyöntisovellus jääkiekkoon

Sovelluksen avulla ylläpitäjä voi luoda vedonlyöntialustan haluamansa jääkiekon sarjan tulosvetokilpailua varten. 

Sovellus pitää kirjaa käyttäjien veikkauksista, pelien lopputuloksista sekä käyttäjien veikkauksistaan saamista pisteistä.

Sovelluksen ominaisuuksia ovat:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Ylläpitäjä voi lisätä sovellukseen veikkauskohteita.
* Käyttäjä voi nähdä tulevat pelit.
* Käyttäjä voi lisätä veikkauksen tuleville peleille.
* Ylläpitäjä voi lisätä menneille peleille oikean lopputuloksen.
* Ylläpitäjä voi lisätä käyttäjille pisteitä.
* Käyttäjät ja ylläpitäjät voivat tarkastella pistetilannetta.
* Käyttäjä voi poistaa lisäämänsä veikkauksen ennen pelin alkua. 

## Versio 4.6.2023

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Sovellukseen voi lisätä veikkauskohteita (valmiissa sovelluksessa ylläpitäjän toiminto. Tältä osin kesken).
* Käyttäjä voi nähdä tulevat pelit.
* Käyttäjä voi lisätä veikkauksen tuleville peleille.
* Menneille peleille voi lisätä lopputulokset (valmiissa sovelluksessa ylläpitäjän toiminto. Tältä osin kesken).
* Käyttäjille voi lisätä pisteitä (valmiissa sovelluksessa ylläpitäjän toiminto. Tältä osin kesken).


## Ohjeet testaamiseen

- Lataa sovellus koneellesi GitHubista

- Luo sovelluksen hakemistoon Pythonin virtuaaliympäristö komennolla: *$ python3 -m venv venv*

- Käynnistä virtuaaliympäristö suorittamalla aktivointikomento: *$ source venv/bin/activate*

- Asenna virtuaaliympäristöösi tarvittavat kirjastot komennolla: *(venv) $ pip install -r requirements.txt*

- Luo hakemistoon tiedosto .env ja lisää sinne satunnaisesti muodostettu salainen avain: *SECRET_KEY= salainen avain*

- Lisää .env tiedostoon tietokannan osoite: *DATABASE_URL=tietokannan osoite*

- Luo sovelluksen tarvitsemat taulut ohjaamalla tiedostossa schema.sql olevat komennot PostgreSQL-tulkille: *(venv) $ psql -d tietokannan nimi < schema.sql*

- Käynnistä sovellus komennolla: *(venv) $ flask run*

- Komentorivin viimeisellä rivillä näkyy osoite, jonka kautta voit käyttää sovellusta nettiselaimella. 

- Sovellus sulkeutuu painamalla Control+C komentorivillä.

- Lopeta virtuaaliympäristön käyttäminen komennolla: *(venv) $ deactivate*


