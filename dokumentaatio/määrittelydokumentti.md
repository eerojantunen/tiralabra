Opinto-ohjelma: Tietojenkäsittelytieteen kandiohjelma (TKT)

Toteutan shakki-botin, joka pyrkii löytämään optimaalisen siirron perustuen heurestiikkafunktioon ja minimax algoritmiin jota tehostettu Alpha-beta-karsinnalla. Shakki-botille syötetään jokin siirto algebraalisella notaatiolla (esim e5, Kxd2), jonka perusteella se vastaa omalla “optimaalisella” siirrollaan ja pystyy täten pelaamaan pelin alusta loppuun. Tavoiteltu aikavaativuus on O(b^d) ja O(√b) välillä.

Ydin: Lauta joka on toteutettu bitboard muodossa. Heurestiikkafunktio joka perustuu ainakin materiaaliin, aktiivisuuteen, hyökkäämisen/puolustamisen laskemiseen. Alpha-beta-karsinnalla tehostettu Minimax algoritmi joka käyttää siirtojen arvioimiseen heurestiikkafunktiota. 

Sovellus toteutetaan pythonilla. En kunnolla hallitse muita ohjelmointikieliä. 

lähteet:
https://en.wikipedia.org/wiki/Bitboard
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Alpha-beta_pruning
