# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 08:19:20 2022

@author: rgouaud, elabastie, eetcheverry
"""


#Importation de fonction mathématique permettant de calculer des distances à partir de coordonnées GPS
from math import sin, cos, acos, pi
#Importation de pandas pour exploiter des CSV ou des Json via des DataFrames
import pandas as pd


"""A"""
#ouverture du csv
donnees = pd.read_table('C:/Users/estel/Desktop/S2.02/donneesbus.csv',sep=";", encoding = "ANSI", index_col=0, decimal=",")
#Conversion du DataFrame en dictionnaire
donneesbus=donnees.to_dict('index')

json=pd.read_json('C:/Users/estel/Desktop/S2.02/donneesbus.json')


"""B"""
#création d'une liste contenant tout les noms d'arrets
nom_arrets=[]
for i in donneesbus: 
    nom_arrets.append(i)
       
    
"""C"""

#retourne le nom de l'arret d'indice ind
def nom(ind): 
    return nom_arrets[ind]


#retourne l'indice de l'arret de nom nom_som
def indice_som(nom_som): 
    for i in range(len(nom_arrets)):
        if nom_som == nom_arrets[i]:
            return i


#retourne la latitude de l'arret de nom nom_som
def latitude(nom_som): 
    return donneesbus[nom_som]['lattitude'] 


#retourne la longitude de l'arret de nom nom_som
def longitude(nom_som): 
    return donneesbus[nom_som]['longitude']


#retourne la liste de voisin de l'arret de nom nom_som
def voisin(nom_som): 
    return json[nom_som][2]

#Appel des fonctions
print(voisin('NOVE')[1])


"""D"""

#retourne la liste d'adjascence des arrets(en fonction de leur indice)
def dic_bus(): 
    D={}
    for i in donneesbus:
        D[i]=donneesbus[i]['listesucc']
    return D

#retourne la matrice d'adjascence des arrets(en fonction de leur indice)
def mat_bus():
    M=[]
    for i in donneesbus:
        M.append([])
        for j in donneesbus:
            if i in voisin(j):
                M[indice_som(i)].append(1)
            else:
                M[indice_som(i)].append(0)	
    return M



"""E"""

#########################################################
# calcul de la distance entre deux points A et B dont #
# on connait la lattitude et la longitude #
#########################################################
def distanceGPS(latA,latB,longA,longB):
 # Conversions des latitudes en radians
 ltA=latA/180*pi
 ltB=latB/180*pi
 loA=longA/180*pi
 loB=longB/180*pi
 # Rayon de la terre en mètres (sphère IAG-GRS80)
 RT = 6378137
 # angle en radians entre les 2 points
 S = acos(round(sin(ltA)*sin(ltB) + cos(ltA)*cos(ltB)*cos(abs(loB-loA)),14))
 # distance entre les 2 points, comptée sur un arc de grand cercle
 return S*RT

#renvoie la distance a vol d'oiseau entre arret1 et arret2
def distarrets(arret1,arret2): 
    latA =donneesbus[arret1]['lattitude']    
    latB =donneesbus[arret2]['lattitude']    
    longA=donneesbus[arret1]['longitude']
    longB=donneesbus[arret2]['longitude']                 
    return (distanceGPS(latA,latB,longA,longB))

#renvoie la distance à vol d'oiseau entre arret1 et arret2 quand l'arc 1/2 existe
#si arc 1/2 existe pas, renvoie l'infini 
def distarc(arret1,arret2): 
    if arret2 in voisin(arret1):
        return distarrets(arret1, arret2)
    else:
        return float('inf')

#Appel des fonctions
#Appel des fonctions
print(distarc('VECL', 'VBOU'))
print(distarrets('VECL', 'VBOU'))

"""F"""

#génère la matrice pondérée du réseau de bus
def poids_bus(): 
    M=[]
    for i in donneesbus:
       M.append([]) 
       for j in donneesbus:
           M[indice_som(i)].append(distarc(i,j))#utilisation de indice_som pour récupérer l'indice du sommet courant
    return M

#Appel de la fonction


def dijkstra(arret_dep,arret_fin):
    
    #Initialisation
    poids=0
    pred=[]
    dist=[]
   
    s=0
    minimum=0
    arret_traites=[]
    pred.append("")
    dist.append(0)
    arret_atraiter=[]
    
    for i in nom_arrets:
         arret_atraiter.append(i)
    print(arret_atraiter)
    

        
    

    extract()
print(dijkstra('maboule','arret_fin'))

    
"""    
    arret_traites.append(arret_dep)
    #mimimum dans voisin(arret_dep)
    poids=poids+distarc(s,minimum)
    dist.append(poids)
    pred.append(s)
    arret_traites.append(s)
     
    s=minimum
    #mimimum dans voisin(arret_dep)
    
       
     
    
   
print( dijkstra('MUSE','MM'))
    
 """

def extract(dist,nom, aTraiter):
    mini = float('inf')
    for i in range(len(dist)): 
        if dist[i] < mini:
            if nom[i] in aTraiter:
                mini = dist[i]
                arret_succ=nom[i]
    return arret_succ , mini 
    


arret_atraiter=[]
distsucc=[]
nomsucc=[]
arret_dep='AVRI'
arret_fin='MUSE'
pred=[]
poids=0
poidst=0
dist=[]

for i in nom_arrets:
    arret_atraiter.append(i)

while(arret_dep != arret_fin):
    
    for i in voisin(arret_dep):
        distsucc.append(distarrets(arret_dep, i))
        nomsucc.append(i)
    
    arret_atraiter.remove(arret_dep)
    arret_dep=extract(distsucc, nomsucc, arret_atraiter)[0]
    poids=extract(distsucc, nomsucc, arret_atraiter)[1]
    poidst= poidst + poids
    dist.append(poidst)
    pred.append(arret_dep)
    
    
print(pred)
print(dist)         



