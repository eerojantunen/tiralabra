Ohjelman yleisrakenne:

Ohjelma koostuu tiedostoista:
board.py - Pitää sisällään lauta objektia, missä jokaisen palan sijainti tiedossa bittilautoina
moves.py - Pitää sisällään siirtojen tekemiseen tarvittavat funktiot
vision_rays.py - Pitää sisällään funktiot joilla selvitetään mitä kukin nappula näkee tyhjällä laudalla mistäkin kohdasta
vision_boards.py - Käyttää vision_rays.py funktioita ja selvittää mihin kukin nappula voi siirtyä siinä laudassa, missä pelataan
engine.py - Pitää sisällään minimax algoritmin, sitä kutsuvan algoritmin, ja siirtojen järjistämisen
evaluation.py - Pitää sisällään pelitilanteen arvioimiseen tarvittavat funktiot
annotation_data.py ja piece_data.py sisältävät tietoa pelinappuloista ja laudan sijainneista

-
Tila- ja aikavaativuudet
Minimax ilman alphabeta karsintaa olisi O(b^d) ja alphabetakarsinnan avulla se on O(b^d) ja O(√(b^d)) välillä. Tehokkuus paranee, mitä suuremmalla syvyydellä (eli suuremmalla ajalla) algoritmia suoritetaan, sillä iteratiivisen läpikäynnin ja siirtojen järjestämisen avulla, karsituiden puiden määrä kasvaa jolloin päästään lähemmäksi O(√(b^d)) missä b = laillisten siirtojen määrä kustakin tilanteesta ja d = hakusyvyys. Minimax ilman alphabeta karsintaa olisi O(b^d). Laillisten siirtojen generointi on O(n), missä n on laillisten siirotjen määrä.

-
Puutteet ja parannusehdotukset:
1. numpy.uint64 muuntaminen pythonin int tyyppiin. Tämä on mahdollista toteuttaa, ja siitä on jo "osittain" toimiva versio haarassa "intproject", mutta sen toteuttamisessa ilmeni vielä bugeja, joita en kerennyt korjata demoon mennessä, joten jatkoin uint64 käyttämistä.
2. Shakkeihin liittyvät laittomat siirrot. Tällä hetkellä moves.py funktio all_moves tuottaa laittomia siirtoja, missä kuningas jätetään shakkiin. Engine.py valitsee tämänlaisen siirron jos se näkee olevansa kuitenkin matitettu. Tämä kuitenkin tuottaa välillä huonoja siirtoja, sillä jos syvyydellä 4 ei nähdä että oma kuningas voidaan syödä syvyydellä 5, saatetaan tämä siirto tehdä, joka voi usein johtaa huonoon tilanteeseen.
3. Siirtojen generointi on hidasta. Tätä voisi tehostaa käyttämällä "magic bitboard" bittilautoja.
4. Tornituksen, en passant ja ylennyksen implementointi
5. Käyttöliittymään olisi hyvä lisätä myös undo mahdollisuus, joka löytyy jo Board luokasta. 
6. Minimaxin kuuluisi pyöriä jo silloin, kun käyttäjä miettii liikettään.
7. Avausten hakeminen tietokannasta
8. Loppupelitaulukoiden lisääminen
9. Selventää rakennetta yhdistämällä annotation_data.py ja piece_data.py
10. Pelitilanteen arviointia voi tehostaa monella tapaa. Esim kuninkaan sijaintipainojen muuttaminen riippuen palojen määrästä (loppupeli)

-
Laajojen kielimallien käyttö:
Käytin ChatGPT aivan projektin alkuvaiheessa toteutustavan ideoinnissa ja rakenteen suunnitteluun.