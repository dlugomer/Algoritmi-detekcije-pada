Algoritmi detekcije pada: prag naspram strojnog učenja

Opis projekta

Projekt je izrađen u sklopu seminarskog rada s ciljem usporedbe dvaju pristupa detekciji pada: pragovnog algoritma i algoritma strojnog učenja (Decision Tree).

Za istraživanje su korišteni podaci akcelerometra pametnog telefona prikupljeni aplikacijom phyphox.

Prikupljanje podataka

Ukupno je prikupljeno 30 snimki:

10 simuliranih padova mobitela na madrac

4 snimke hodanja

4 snimke sjedanja

4 snimke ustajanja

4 snimke odlaganja mobitela na stol

4 snimke podizanja mobitela sa stola

Snimke su spremljene u ZIP datotekama koje sadrže izvorne CSV podatke o akceleraciji.

Korišteni algoritmi

1. Pragovni algoritam

Algoritam provjerava maksimalnu ukupnu akceleraciju tijekom snimke. Ako vrijednost prijeđe 20 m/s², snimka se klasificira kao pad.

2. Decision Tree

Algoritam strojnog učenja analizira značajke akceleracije i na temelju prethodno označenih snimki uči razlikovati padove od svakodnevnih aktivnosti.

Za testiranje je korištena metoda Leave-One-Out, pri kojoj se model trenira na 29 snimki, a testira na preostaloj.

Rezultati

Metrika

Pragovni algoritam

Decision Tree

Točnost

83,33 %

100 %

Preciznost

66,67 %

100 %

Odziv

100 %

100 %

Lažni alarmi

5

0

Rezultati se odnose na 30 kontroliranih mjerenja i ne predstavljaju potvrdu učinkovitosti sustava pri stvarnim padovima ljudi.

Pokretanje programa

Za pokretanje je potrebno instalirati Python i biblioteke:

pip install numpy pandas scikit-learn matplotlib

Nakon toga potrebno je preuzeti projekt, osigurati da su izvorne ZIP snimke dostupne programu i pokrenuti:

python analiza_padova.py

Program obrađuje podatke, uspoređuje algoritme i generira rezultate.

Sadržaj repozitorija

analiza_padova.py – programski kod za analizu podataka

Podaci/ – izvorne snimke iz aplikacije phyphox

rezultati_snimki.csv – rezultati pojedinačnih mjerenja

usporedba_algoritama.csv – usporedba algoritama

usporedba_akceleracije.png – grafički prikaz rezultata

Autor

Ime i prezime: [upiši svoje ime i prezime]

Fakultet organizacije i informatike, Varaždin

Akademska godina: 2026./2027
