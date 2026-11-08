import os,glob,zipfile,io
import numpy as np,pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut,cross_val_predict
from sklearn.metrics import confusion_matrix,precision_score,recall_score,accuracy_score
import matplotlib.pyplot as plt
from pathlib import Path
out = str(Path(__file__).resolve().parent)
rows=[]
for p in sorted(glob.glob(str(Path(out) / 'Podaci' / '*.zip'))):
 name=os.path.basename(p).removesuffix('.zip')
 if not name.startswith(('Pad','Hodanje','Sjedenje','Ustajanje','Odlaganje','Podizanje')):continue
 with zipfile.ZipFile(p) as z:
  df=pd.read_csv(io.BytesIO(z.read('Raw Data.csv')))
 a=df['Absolute acceleration (m/s^2)'].to_numpy(float)
 t=df['Time (s)'].to_numpy(float)
 if len(a)<3:continue
 rows.append({'snimka':name,'klasa':int(name.startswith('Pad')),'trajanje_s':float(t[-1]-t[0]),'broj_uzoraka':len(a),'maks_akceleracija':float(a.max()),'srednja_akceleracija':float(a.mean()),'std_akceleracija':float(a.std()),'p95_akceleracija':float(np.percentile(a,95)),'raspon_akceleracije':float(a.max()-a.min()),'udio_iznad_20':float(np.mean(a>20))})
data=pd.DataFrame(rows)
assert len(data)==30, f'Ocekivano 30 snimki, pronadeno {len(data)}. Provjeri mapu Podaci.'
features=['maks_akceleracija','std_akceleracija','p95_akceleracija','raspon_akceleracije','udio_iznad_20']
X=data[features];y=data.klasa
threshold=(data.maks_akceleracija>20).astype(int)
model=DecisionTreeClassifier(max_depth=2,min_samples_leaf=2,random_state=42)
pred=cross_val_predict(model,X,y,cv=LeaveOneOut())
model.fit(X,y)
data['prag_20_pred']=threshold;data['stablo_LOOCV_pred']=pred
def report(pred):
 tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
 return {'TP':int(tp),'FP':int(fp),'TN':int(tn),'FN':int(fn),'preciznost':precision_score(y,pred,zero_division=0),'odziv':recall_score(y,pred,zero_division=0),'tocnost':accuracy_score(y,pred)}
print('THRESHOLD',report(threshold));print('TREE LOOCV',report(pred));print('FEATURES',features)
print('RULES');from sklearn.tree import export_text;print(export_text(model,feature_names=features))
print(data[['snimka','maks_akceleracija','prag_20_pred','stablo_LOOCV_pred']].to_string(index=False))
data.to_csv(out+'/rezultati_snimki.csv',index=False,encoding='utf-8-sig')
results=pd.DataFrame([{'algoritam':'Prag 20 m/s²',**report(threshold)},{'algoritam':'Decision Tree (LOOCV)',**report(pred)}])
results.to_csv(out+'/usporedba_algoritama.csv',index=False,encoding='utf-8-sig')
fig,ax=plt.subplots(figsize=(9,5));col=np.where(y==1,'tab:orange','tab:blue');ax.scatter(range(len(data)),data.maks_akceleracija,c=col,s=48);ax.axhline(20,linestyle='--',color='tab:red',label='Prag 20 m/s²');ax.set_xticks(range(len(data)));ax.set_xticklabels(data.snimka,rotation=75,fontsize=7);ax.set_ylabel('Maksimalna ukupna akceleracija (m/s²)');ax.set_title('Maksimalna akceleracija svih 30 snimki');ax.legend();fig.tight_layout();fig.savefig(out+'/usporedba_akceleracije.png',dpi=170);plt.close(fig)
