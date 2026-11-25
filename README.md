# Videokirjasto
Videokirjastosovellukseen pystyy lisäämään YouTube-videon linkin ja sille haluamansa nimen. Käyttäjät voivat lisätä kommentteja muiden käyttäjien lisäämiin videolinkkeihin.
(Sovellus on toteutettu "Tietokannat ja web-ohjelmointi" -opintojaksolla itsenäisenä kurssityönä.)

# Ohjeet käyttöönottoon:
1. Kloonaa repo
2. Suorita:
cd Videokirjasto,
python3 -m venv venv,
source venv/bin/activate,
pip install flask,
sqlite3 database.db < schema.sql,
flask run
3. Siirry "Running on" -sivustolle.

© 2026 Tiina Saari. Kaikki oikeudet pidätetään. Koodi on julkaistu ainoastaan tarkastelua varten.