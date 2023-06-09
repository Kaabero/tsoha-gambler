# Vedonlyöntisovellus jääkiekkoon

Sovelluksen avulla ylläpitäjä voi luoda vedonlyöntialustan haluamansa jääkiekon sarjan tulosvetokilpailua varten. 

Sovellus pitää kirjaa käyttäjien veikkauksista, pelien lopputuloksista sekä käyttäjien veikkauksistaan saamista pisteistä.

Sovellus ei ole testattavissa Fly.iossa. Ohjeet sovelluksen käynnistämiseen paikallisesti alempana.

Sovelluksen ominaisuuksia ovat:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Ylläpitäjä voi lisätä sovellukseen veikkauskohteita tulevaisuuteen.
* Käyttäjä voi nähdä tulevat pelit.
* Käyttäjä voi lisätä veikkauksen tuleville peleille.
* Ylläpitäjä voi lisätä menneille peleille lopputulokset ja pisteyttää pelit.
* Käyttäjä voi tarkastella annettuja veikkauksia.
* Käyttäjä voi tarkastella pelien lopputuloksia. 
* Käyttäjä voi tarkastella pisteytystä.
* Käyttäjä voi katsoa kokonaispistetilanteen. 
* Käyttäjä voi poistaa oman veikkauksensa tuleville peleille.
* Ylläpitäjä voi aloittaa uuden kisan.


## Ohjeet sovelluksen käynnistämiseen paikallisesti:

- Lataa sovellus koneellesi GitHubista ja siirry sen juurihakemistoon.

- Luo hakemistoon tiedosto .env ja lisää sinne satunnaisesti muodostettu salainen avain: *SECRET_KEY= salainen avain*

- Lisää .env tiedostoon tietokannan osoite: *DATABASE_URL=tietokannan osoite*

- Luo sovelluksen hakemistoon Pythonin virtuaaliympäristö komennolla: *$ python3 -m venv venv*

- Käynnistä virtuaaliympäristö suorittamalla aktivointikomento: *$ source venv/bin/activate*

- Asenna virtuaaliympäristöösi tarvittavat kirjastot komennolla: *(venv) $ pip install -r requirements.txt*

- Luo sovelluksen tarvitsemat taulut ohjaamalla tiedostossa schema.sql olevat komennot PostgreSQL-tulkille: *(venv) $ psql -d tietokannan nimi < schema.sql*

- Käynnistä sovellus komennolla: *(venv) $ flask run*

- Komentorivin viimeisellä rivillä näkyy osoite, jonka kautta voit käyttää sovellusta nettiselaimella.

- Sovellus sulkeutuu painamalla Control+C komentorivillä.

- Lopeta virtuaaliympäristön käyttäminen komennolla: *(venv) $ deactivate*

## Ohjeet ylläpitäjän toimintojen testaamiseksi:  

- Voit testata ylläpitäjän toiminnallisuuksia luomalla ensin käyttäjätunnuksen ja sitten päivittämällä tietokantaan käyttäjän ylläpitäjäksi komentorivillä:

  - *(venv) $ psql*

  - *# UPDATE users SET admin=1 WHERE username='käyttäjätunnus';*




