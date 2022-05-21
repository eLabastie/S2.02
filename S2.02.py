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
       
    


#retourne la liste de voisin de l'arret de nom nom_som
def voisin(nom_som): 
    return json[nom_som][2]



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




    

""" ////// ETAPE 2 : DIJKSTRA ////// """

def extract(poids, aTraiter):
    mini = float('inf')              
    global arret_succ
    for i in poids : 
        if poids[i][0] < mini:          # Pour chaque successeurs i on définit lequel a le poids le plus petit
            if i in aTraiter :          # Si ce poids concerne un successeur qui n'a pas été traité 
                mini = poids[i][0]       # le minimum prends la valeur du poids du successeur 
                arret_succ = i           # prend le nom du successeur avec le poids le plus petit
    return arret_succ , mini           

def dijkstra ( arret_dep , arret_fin):

#Initialisation
#Creation d'une liste contenant le nom de tout les arrets du réseau
#Des que l'on aura fini de traiter tout les successeurs d'un arret on le retirera de la liste

    arret_atraiter=[]
    for i in nom_arrets:
        arret_atraiter.append(i)

#Creation d'un dicitonnaire qui contiendra le poids minimum pour acceder à un sommet donné
# et en deuxième paramètre son chemin pour y acceder
    info_sommet={}
    for i in nom_arrets:
            info_sommet[i]=[]
            info_sommet[i].append(float('inf'))  # chemin non défini
            info_sommet[i].append(str(None))     #predecesseur non défini


#Initialisation du sommet de départ qui ne possède pas de poids et pas de predecesseur
    info_sommet[arret_dep][0]= 0
    info_sommet[arret_dep][1]='' 


    while ( arret_atraiter ):           # Tant qu'il reste des sommets a traiter
    
        for i in voisin(arret_dep):            #pour i successeur de l'arret actuel
            if (distarrets(arret_dep, i) +info_sommet[arret_dep][0]  < info_sommet[i][0] ):    #si poids du chemin actuel est meilleur que celui deja établi sur le successeur visé
                info_sommet[i][0]= (distarrets(arret_dep, i)) + info_sommet[arret_dep][0]   # alors le poids du succeseur visé est réajusté dans le dictionnaire
                
                info_sommet[i][1]=(str(info_sommet[arret_dep][1] + "[" + str(i) + "]"))              # Initialisation dans le dictionnaire du chemin complet menant au successeur
         
             
        arret_atraiter.remove(arret_dep)                           # Si tous les successeurs visités --> Sommet traité donc on le retire de la liste des sommets non traités
        arret_dep= extract( info_sommet , arret_atraiter)[0]       # On se déplace vers le successeur qui semble le meilleur ( avec le poids le plus faible) 
    


    print(" Chemin  :" ,info_sommet[arret_fin][1])            #Affichage du chemin de l'arret final ,enregistré dans le dictionnaire
    print("Distance minimum :" , info_sommet[arret_fin][0])  # Affichage du poids total de l'arret final , ,enregistré dans le dictionnaire



dijkstra('7PUI','ACAC')




