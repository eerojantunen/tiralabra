Käyttöohjeet:

Projektin kloonauksen jälkeen suorita:
Asenna riippuvuuden
```bash
poetry install
```
Aktivoi virtuaaliympäristö
```bash
poetry shell
```
Suorita ohjelma
```bash
python3 src/game.py
```
Tämän jälkeen ohjelma antaa lisää käyttöohjeita

Testien suorittaminen:

Aktivoi virtuaaliympäristö
```bash
poetry shell
```
Suorita testit
```bash
poetry run pytest
```
coverage:
```bash
poetry run coverage html
```