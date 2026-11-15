# Videokirjasto
Tietokannat ja web-ohjelmointi -opintojaksolla itsenäisesti toteutettu 
tietokantaa käyttävä web-sovellus.

# Ohjeet 2. välipalautusta varten:

Sovelluksen käyttönotto:
1. Kloonaa repo
2. Suorita:
cd Videokirjasto
python3 -m venv venv
source venv/bin/activate
pip install flask
sqlite3 database.db < schema.sql
flask run
3. Mene "Running on" -sivustolle.

Sovelluksen käyttö ja testaus:
- Etusivulta pääsee rekisteröitymään tai kirjautumaan sisään (samoin ylänavigoinnista)
- Kun tunnus ja salasana on luotu, pitää vielä kirjautua sisään.
- Seuraavat sivustot vaativat sisäänkirjautumista:
    - "Lisää videolinkki"-sivusto: 
        - Lisätään tietokantaan YouTube-linkki (URL), videon nimi ja halutessaan luokka, joka kuvaa videota (esim. musiikki, jazz jne.). Luokkaa ei ole pakko lisätä, mutta nimi ja linkki on.
    - "Kaikki videolinkit"-sivusto:
        - Haku, joka hakee hakusanaa linkkien nimistä, URL-osoitteista ja linkeille lisätyistä luokista.
        - Pystyy tarkastelemaan omia ja muiden lisäämiä YouTube-linkkejä: videon nimi, videolinkki, kuka käyttäjä lisännyt ja muokkaa-painike
            - Muokkaa-painike avaa sivuston, jossa voi muokata kaikkia aiemmin lisättyjä tietoja ja tallentaa muutokset (vain linkin lisännyt käyttäjä voi näin tehdä, toisten linkkejä ei voi muokata).
        - Listasta videon nimeä painamalla pääsee videosivulle:
            - löytyy samat tiedot kuin "Kaikki videolinkit"-sivustolta (myös muokkaus-painike). 
            - "Poista"-nappulasta voi poistaa koko linkin (vain linkin lisännyt käyttäjä voi näin tehdä, toisten linkkejä ei voi poistaa)
            - Videolinkkiin liittyen voi lisätä kommentin ("Lähetä kommentti"-nappulasta), vaikkapa videon sisältöön liittyen. Kommentteja voi jättää omiin sekä muiden videoihin. Omia kommentteja voi poistaa kommentin alapuolella olevasta "poista kommentti"-napista. Muiden kommentteja ei voi poistaa.
    - Ylänavigoinnista pääsee kirjautumaan ulos painamalla "kirjaudu ulos"-nappia, jonka jälkeen etusivu näkymä avautuu.

# Kuvaus 1. välipalautusta varten:

Videokirjastosovellukseen pystyy lisäämään YouTube-videon linkin (pääasiallinen 
tietokohde) ja haluamansa nimen videolinkille. Käyttäjät voivat lisätä kommentin 
(toissijainen tietokohde) muiden käyttäjien lisäämiin videolinkkeihin. 
Sovelluksessa on seuraavat toiminnot:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lisäämiään 
videolinkkien tietoja.
- Käyttäjä voi lisätä kommentin myös muiden lisäämiin videolinkkeihin, 
mutta ei voi poistaa muiden lisäämiä pääasiallisia tai toissijaisia tietokohteita.
- Käyttäjä näkee omien videolinkkiensä ja lisäämiensä kommenttien lisäksi muiden 
lisäämät videolinkit ja kommentit.
- Videolinkki voi kuulua yhteen tai useampaan luonnehdintaluokkaan, joka kuvaa 
videon sisältöä esim. lapsille sopivat, musiikki, kiipeily. Käyttäjä valitsee
itse luokat videolinkille.
- Käyttäjä pystyy hakemaan videolinkkejä hakusanalla tai suodattamaan niitä 
luonnehdintaluokkien mukaan.
- Sovelluksessa on sivusto, jossa näkyy käyttäjien lisäämät videolinkit 
ja tilastoa mm. lisättyjen linkkien määrästä ja prosentuaalinen kuvaus siitä, 
kuinka paljon mitäkin luonnehdintaluokkaa käyttäjän lisäämät linkit ovat 
edustaneet.

© 2026 Tiina Saari. Kaikki oikeudet pidätetään. Koodi on julkaistu ainoastaan
tarkastelua varten.