#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


caracteristics = pd.read_csv('C:/Users/mnhelal/OneDrive - Université Paris 1 Panthéon-Sorbonne/Bureau/Paris/Algorithmique et Python/archive/caracteristics.csv',encoding='latin-1', sep=",")
places = pd.read_csv('C:/Users/mnhelal/OneDrive - Université Paris 1 Panthéon-Sorbonne/Bureau/Paris/Algorithmique et Python/archive/places.csv', sep=",")
users = pd.read_csv('C:/Users/mnhelal/OneDrive - Université Paris 1 Panthéon-Sorbonne/Bureau/Paris/Algorithmique et Python/archive/users.csv', sep=",")
vehicles = pd.read_csv('C:/Users/mnhelal/OneDrive - Université Paris 1 Panthéon-Sorbonne/Bureau/Paris/Algorithmique et Python/archive/vehicles.csv', sep=",")


# In[16]:



print(places.pr.isna().sum())
print(places.pr1.isna().sum())


# In[17]:



places.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=45)
#Too many missing data for V1,V2, pr and pr1
#lartpc abd larrout isn't pertinent (and i dont understand them personally)


# In[18]:




places.env1.value_counts(dropna=False)
#Beaucoup de valeurs codé 0 (des valeurs manquantes en vrai), je propose de la dropper


# In[19]:


places = places.drop(['v1', 'v2', 'pr', 'pr1', 'lartpc', 'larrout', 'voie', 'env1'], axis=1)


# In[20]:


places


# In[21]:


print(places.nbv.value_counts(dropna=False)) #nombre de voie: bizarre car il y a maximum 5 voie dane une route.. alors qu'ici
#on a des valeurs +10...


# In[22]:


#prenons que les routes avec 10 voies de circulations au maximum
places = places[places.nbv <= 10]
places


# In[23]:


#vosp	prof	plan	surf	infra	situ
#print(places.vosp.value_counts(dropna=False)) #trop de valeurs manquantes.. Presque 700000 de 0
print(places.prof.value_counts(dropna=False)) #0: 63849 et 1000 na
print(places.plan.value_counts(dropna=False)) #57847 et 1000 na
print(places.surf.value_counts(dropna=False)) #0: 26000 et 1000 na
print(places.infra.value_counts(dropna=False)) 
print(places.situ.value_counts(dropna=False)) #0 veut dire aucune situation 
print(places.circ.value_counts(dropna=False)) 
print(places.catr.value_counts(dropna=False))


    
#on devrait probablement dropper vosp et infra, et pour les autres peut être les ajoutés à la plus grande modalité


# In[24]:


#transformer les modalité de 0 en modalité avec le plus nombre d'observation
places['prof'] = places['prof'].replace(0.0, 1.0)
places['prof'] = places['prof'].fillna(1.0)

places['plan'] = places['plan'].replace(0.0, 1.0)
places['plan'] = places['plan'].fillna(1.0)

places['surf'] = places['surf'].replace(0.0, 1.0)
places['surf'] = places['surf'].fillna(1.0)

places['infra'] = places['infra'].fillna(0.0)

places['situ'] = places['situ'].fillna(1.0)

places['circ'] = places['circ'].replace(0.0, 2.0)
places['circ'] = places['circ'].fillna(2.0)

places['catr'] = places['catr'].fillna(4.0)


# In[25]:


places = places.drop(['vosp'], axis=1)


# In[26]:


places


# In[27]:


places.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=45)


# In[28]:


#BDD caracteristics
caracteristics


# In[29]:


caracteristics.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=45)


# In[30]:


caracteristics = caracteristics.drop(['adr', 'lat', 'long'], axis = 1)


# In[31]:


caracteristics.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=45)


# In[32]:


domtom = [973,974,976, 975] #But this doesn't include les Antilles (Martinique or Guadeloupe) cause they're not departements

caracteristics = caracteristics[~caracteristics.dep.isin(domtom)]
caracteristics


# In[33]:


# Dropping les Antilles so we can stay on only le Métropole
caracteristics = caracteristics[caracteristics.gps != "A"]
caracteristics


# In[34]:


#checking we're only in Métropole
caracteristics.dep.nunique()


# In[35]:


GPS = ['0', 'S', 'T', 'R', 'C', 'G', 'P']
caracteristics[caracteristics['gps'].isin(GPS)]
# I did this to check the departement number of these weird values, and they're all in Metropole


# In[36]:


print(caracteristics.lum.value_counts(dropna=False))
print(caracteristics.int.value_counts(dropna=False)) #0: 106
print(caracteristics.atm.value_counts(dropna=False)) #55 nan
print(caracteristics.col.value_counts(dropna=False)) #11 nan
print(caracteristics.com.value_counts(dropna=False))
print(caracteristics.dep.value_counts(dropna=False))


# In[37]:


caracteristics['lum'] = caracteristics['lum'].replace(0, 1)

caracteristics['int'] = caracteristics['int'].replace(0, 1)

caracteristics['atm'] = caracteristics['atm'].fillna(1.0)

caracteristics['col'] = caracteristics['col'].fillna(6.0)


# In[38]:


caracteristics.an.value_counts().plot(kind = 'bar')


# In[39]:


users


# In[40]:


users.catu.value_counts(dropna=False)


# In[41]:


users = users.drop(['place'], axis = 1)


# In[42]:


users.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=45)


# In[43]:


print(users.trajet.value_counts(dropna=False))
#trajet: 55000 0 et 369 nan
#secu: 0 càd aucun équipement a été porté et 43000 nan
#loctp, actp, etatp 1 700 000 de 0


# In[44]:


users['trajet'] = users['trajet'].replace(0, 5)
users['trajet'] = users['trajet'].fillna(5.0)

users['secu'] = users['secu'].fillna(11.0)


# In[45]:


users = users.drop(['locp', 'actp', 'etatp', 'num_veh'], axis = 1)
users


# In[46]:


vehicles


# In[49]:


vehicles.obs.value_counts(dropna=False)
#obsm (obstacle mobile heurté): 0 càd aucun 
#obs (obstacle immobile heurté, par ex un arbre): trop de 0 (1 200 000): valeur manquante
#occutc: Nombre d’occupants dans le transport en commun. 


# In[50]:


vehicles = vehicles[['Num_Acc', 'catv', 'occutc', 'choc']]
vehicles


# In[54]:


places.shape


# In[57]:


users = users.groupby(['Num_Acc'], as_index=False).max()
vehicles = vehicles.groupby(['Num_Acc'], as_index=False).max()


# In[58]:


print('places:', places.shape)
print('caracteristics:', caracteristics.shape)
print('users:', users.shape)
print('vehicles:', vehicles.shape)


# In[59]:


from functools import reduce
Merge1 = [caracteristics, places]
Merge_1 = reduce(lambda left,right: pd.merge(left,right,on=['Num_Acc'],how='left'),Merge1)


Merge2 = [Merge_1, users]
Merge_2 = reduce(lambda left,right: pd.merge(left,right,on=['Num_Acc'],how='left'),Merge2)


Merge3 = [Merge_2, vehicles]

accidents = reduce(lambda left,right: pd.merge(left,right,on=['Num_Acc'],how='left'),Merge3)
accidents

