# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 08:19:20 2022

@author: rgouaud, elabastie, eetcheverry
"""


#Importation de fonction mathématique permettant de calculer des distances à partir de coordonnées GPS
from math import sin, cos, acos, pi
#Importation de pandas pour exploiter des CSV ou des Json via des DataFrames
import pandas as pd


#ouverture du csv
donnees = pd.read_table('C:\\Temp\\donneesbus.csv',sep=";", encoding = "ANSI", index_col=0, decimal=",")
#Conversion du DataFrame en dictionnaire
donneesbus=donnees.to_dict('index')


#création d'une liste contenant tout les noms d'arrets
nom_arrets=[]
for i in donneesbus: 
    nom_arrets.append(i)
       

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
    chaine = donneesbus[nom_som]['listesucc']
    retour=eval(chaine)
    return retour


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


#génère la matrice pondérée du réseau de bus
def poids_bus(): 
    M=[]
    for i in donneesbus:
       M.append([]) 
       for j in donneesbus:
           M[indice_som(i)].append(distarc(i,j))#utilisation de indice_som pour récupérer l'indice du sommet courant
    return M  


def Bellman(arret_dep, arret_arriv):
    mat = poids_bus() #graphe pondéré du réseau de bus
    n = len(mat) #taille du graphe
    dist = [float('inf')]*n #liste des distances des sommets
    pred = [None]*n #liste des prédécesseurs des sommets
    dist[indice_som(arret_dep)] = 0 #le premier sommet à comme distance 0
    compteur = 0 #compteur pour sortir de la boucle si le relachement de tous les arcs ne montre aucun changement
    
    #relachements
    for k in range(n-1): #parcours de tous les arcs
        compteur += 1 #incrémenter le compteur
        for i in range(n):
            for j in range(n):
                if dist[i] + mat[i][j] < dist[j]: #effectuer des changements si la nouvelle distance de l'arc est plus petite que la distance actuelle
                    pred[j] = nom(i)
                    dist[j] = dist[i] + mat[i][j] #mise à jour du predecesseur et de la distance minimum de l'arc
                    compteur = 0 #si un changement a lieu, réinitialiser le compteur
        if compteur == n:
            break 
        
    chemin = [] #liste du chemin le plus court
    distList = [] #liste des distances minimum de chaque sommet du plus court chemin
    while arret_arriv != None: #parcours en profondeur pour mettre le chemin et les distances dans des listes à retourner
        distList.insert(0, round(dist[indice_som(arret_arriv)])) #insérer la distance minimale du sommet en début de liste
        chemin.insert(0, arret_arriv)
        arret_arriv = pred[indice_som(arret_arriv)] #insérer le nom du sommet en début de liste

        
    return chemin, distList

print(Bellman('ACAC', '7PUI'))