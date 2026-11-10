
# Algoritmi detekcije pada: prag naspram strojnog učenja

##  Opis projekta

Projekt je izrađen u sklopu seminarskog rada s ciljem usporedbe dvaju pristupa detekciji pada: **pragovnog algoritma** i algoritma strojnog učenja **Decision Tree**.

Za istraživanje su korišteni podaci akcelerometra pametnog telefona prikupljeni pomoću aplikacije **phyphox**

##  Prikupljanje podataka

Ukupno je prikupljeno **30 snimki**:

- 10 simuliranih padova mobitela na madrac
- 4 snimke hodanja
- 4 snimke sjedanja
- 4 snimke ustajanja
- 4 snimke odlaganja mobitela na stol
- 4 snimke podizanja mobitela sa stola

Snimke su spremljene u ZIP datotekama koje sadrže izvorne CSV podatke o akceleraciji.

##  Korišteni algoritmi

### 1. Pragovni algoritam

Algoritam provjerava maksimalnu ukupnu akceleraciju tijekom snimke.

Ako akceleracija prijeđe **20 m/s²**, snimka se klasificira kao pad.

### 2. Decision Tree

Algoritam strojnog učenja analizira različite značajke akceleracije i na temelju prethodno označenih snimki uči razlikovati padove od svakodnevnih aktivnosti.

Za testiranje je korištena metoda **Leave-One-Out**, pri kojoj se model trenira na 29 snimki, a testira na preostaloj.

##  Rezultati

| Metrika | Pragovni algoritam | Decision Tree |
|---|---:|---:|
| Točnost | 83,33 % | 100 % |
| Preciznost | 66,67 % | 100 % |
| Odziv | 100 % | 100 % |
| Lažni alarmi | 5 | 0 |

Rezultati se odnose na 30 kontroliranih mjerenja i ne predstavljaju potvrdu učinkovitosti sustava pri stvarnim padovima ljudi.

##  Pokretanje programa

Za pokretanje programa potrebno je instalirati Python i potrebne biblioteke.

**1. Instalacija biblioteka**

```bash
pip install numpy pandas scikit-learn matplotlib
```

**2. Pokretanje programa**

Preuzeti projekt i osigurati da su izvorne ZIP snimke dostupne programu.

```bash
python analiza_padova.py
```

Program obrađuje podatke, uspoređuje algoritme i generira rezultate.

##  Struktura projekta

```text
detekcija-pada/
│
├── analiza_padova.py
├── README.md
├── rezultati_snimki.csv
├── usporedba_algoritama.csv
├── usporedba_akceleracije.png
│
└── Podaci/
    ├── Pad1.zip ... Pad10.zip
    ├── Hodanje1.zip ... Hodanje4.zip
    ├── Sjedenje1.zip ... Sjedenje4.zip
    ├── Ustajanje1.zip ... Ustajanje4.zip
    ├── Odlaganje1.zip ... Odlaganje4.zip
    └── Podizanje1.zip ... Podizanje4.zip
```

##  Autor

**Ime i prezime:** Dino Lugomer <br>
**Fakultet:** Fakultet organizacije i informatike, Varaždin  <br>
**Akademska godina:** 2026./2027.
