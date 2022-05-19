# -*- coding: utf-8 -*-
"""
Created on Thu May 19 18:33:13 2022

@author: eetchever004
"""

def voisin(nom_som): 
    chaine = donneesbus[nom_som]['listesucc']
    retour=eval(chaine)
    return retour

dist = [8,9,5,3,7,2]
aTraiter = [1,3,12]
def extract(dist, aTraiter):
    mini = float('inf') #Le minimum est initialisé à l'infini pour que n'importe quelle valeur puisse le remplacer
    for i in range(len(dist)):
        if dist[i] < mini and dist[i] in aTraiter:
            mini = dist[i]
    return mini
print(extract(dist, aTraiter))



def Dijkstra(arret_dep, arret_arriv):
    chemin = [None]*len(poids_bus())              #Chemin le plus court
    aVisiter=[i for i in range(len(poids_bus()))] #Liste des sommets à visiter
    distAct = 0                                   #Distance actuelle
    distList = [float('inf')]*len(poids_bus())    #Liste des distances
    arretAct = indice_som(arret_dep)              #Au début, l'arrêt actuel est le sommet de départ
    mat = poids_bus()                             #Importation du graphe pondéré du réseau de bus
    
    while aVisiter != []: #Boucler tant qu'il reste des sommets à visiter
        voisinList = voisin(nom(arretAct)) #Liste des sommets voisins au sommet actuel
        for arretVoisin in voisinList: 
            indVoisin = indice_som(arretVoisin) #Indice de l'arrêt voisin
            if (distarrets(nom(arretAct), arretVoisin)+distAct) < distList[indVoisin]:
                distAct += distarrets(nom(arretAct), arretVoisin) #Adition de la distance actuelle
                distList[indVoisin] = distarrets(nom(arretAct), arretVoisin)+distAct #Ajouter la distance dans le tableau
                chemin[indVoisin] = aVisiter[arretAct]
        aVisiter.pop(arretAct)
        arretAct = indice_som(extract(distList, aVisiter))

    
Dijkstra('MUSE','CITA')