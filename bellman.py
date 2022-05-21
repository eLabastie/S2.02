# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:33:24 2022

@author: eetchever004
"""

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