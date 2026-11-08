from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

MAPA = Path(__file__).resolve().parent
PRAG = 20
snimke = []

# 1. ucitavanje snimki
for datoteka in sorted((MAPA / 'Podaci').glob('*.zip')):
    naziv = datoteka.stem
    if not naziv.startswith(('Pad', 'Hodanje', 'Sjedenje', 'Ustajanje', 'Odlaganje', 'Podizanje')):
        continue

    with ZipFile(datoteka) as zip_datoteka:
        podaci = pd.read_csv(BytesIO(zip_datoteka.read('Raw Data.csv')))

    a = podaci['Absolute acceleration (m/s^2)'].to_numpy(float)
    t = podaci['Time (s)'].to_numpy(float)
    if len(a) < 3:
        continue

    snimke.append({
        'snimka': naziv,
        'klasa': int(naziv.startswith('Pad')),
        'trajanje_s': float(t[-1] - t[0]),
        'broj_uzoraka': len(a),
        'maks_akceleracija': float(a.max()),
        'srednja_akceleracija': float(a.mean()),
        'std_akceleracija': float(a.std()),
        'p95_akceleracija': float(np.percentile(a, 95)),
        'raspon_akceleracije': float(a.max() - a.min()),
        'udio_iznad_20': float(np.mean(a > PRAG)),
    })

rezultati = pd.DataFrame(snimke)
if len(rezultati) != 30:
    raise ValueError(f'Ocekivano 30 snimki, pronadeno {len(rezultati)}.')

# 2. pragovni algoritam
stvarne_klase = rezultati['klasa']
pred_prag = (rezultati['maks_akceleracija'] > PRAG).astype(int)

# 3. stablo
znacajke = [
    'maks_akceleracija',
    'std_akceleracija',
    'p95_akceleracija',
    'raspon_akceleracije',
    'udio_iznad_20',
]
X = rezultati[znacajke]
model = DecisionTreeClassifier(max_depth=2, min_samples_leaf=2, random_state=42)
pred_stablo = cross_val_predict(model, X, stvarne_klase, cv=LeaveOneOut())
model.fit(X, stvarne_klase)  # Zavrsni model samo za prikaz pravila.

# 4. usporedba algoritama
def izracunaj_metrike(predvidanja):
    tn, fp, fn, tp = confusion_matrix(stvarne_klase, predvidanja, labels=[0, 1]).ravel()
    return {
        'TP': int(tp), 'FP': int(fp), 'TN': int(tn), 'FN': int(fn),
        'preciznost': precision_score(stvarne_klase, predvidanja, zero_division=0),
        'odziv': recall_score(stvarne_klase, predvidanja, zero_division=0),
        'tocnost': accuracy_score(stvarne_klase, predvidanja),
    }

usporedba = pd.DataFrame([
    {'algoritam': 'Prag 20 m/s²', **izracunaj_metrike(pred_prag)},
    {'algoritam': 'Decision Tree (LOOCV)', **izracunaj_metrike(pred_stablo)},
])
print(usporedba.to_string(index=False))
print('\nPravila stabla odlucivanja:')
print(export_text(model, feature_names=znacajke))

# 5. spremanje rezultata
rezultati['prag_20_pred'] = pred_prag
rezultati['stablo_LOOCV_pred'] = pred_stablo
rezultati.to_csv(MAPA / 'rezultati_snimki.csv', index=False, encoding='utf-8-sig')
usporedba.to_csv(MAPA / 'usporedba_algoritama.csv', index=False, encoding='utf-8-sig')

# 6. graf maksimalne akceleracije
fig, ax = plt.subplots(figsize=(9, 5))
boje = np.where(stvarne_klase == 1, 'tab:orange', 'tab:blue')
ax.scatter(range(len(rezultati)), rezultati['maks_akceleracija'], c=boje, s=48)
ax.axhline(PRAG, color='tab:red', linestyle='--', label='Prag 20 m/s²')
ax.set_xticks(range(len(rezultati)))
ax.set_xticklabels(rezultati['snimka'], rotation=75, fontsize=7)
ax.set_ylabel('Maksimalna ukupna akceleracija (m/s²)')
ax.set_title('Maksimalna akceleracija svih 30 snimki')
ax.legend()
fig.tight_layout()
fig.savefig(MAPA / 'usporedba_akceleracije.png', dpi=170)
plt.close(fig)

print('\nGotovo! Rezultati i graf spremljeni su u mapu projekta.')
