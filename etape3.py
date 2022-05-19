# -*- coding: utf-8 -*-
"""
Created on Wed May 18 08:33:26 2022

@author: rgouaud
"""

#importation des algos de lecture, des algos de parcours, et de la classe graphique
#import etape1 as e1
#import etape2 as e2
from etape1 import donneesbus
import graphics as gr



long=[]
lat=[]
#récupération de toutes les longitudes / lattitudes du csv, pour pouvoir par la suite sélectionner
#faire une mise a l'échelle dynamique (en cas de mise a jours du csv)
for i in donneesbus :
    lat.append(donneesbus[i]['lattitude'])
    long.append(donneesbus[i]['longitude'])


def arrets():
    win = gr.GraphWin("test", 900, 900)    
   
    for i in donneesbus :
        
        #Mise à l'échelle sur une valeur de 880px, pour ne pas etre collé sur les bords
        #formule : (d-c/b-a)*(x-a)+c
        #effectué dynamiquement avec les valeurs minimales et maximales du CSV
        lattx = (880/(max(lat)-min(lat)))*(donneesbus[i]['lattitude']-min(lat))+10
        longy = (880/(max(long)-min(long)))*(donneesbus[i]['longitude']-min(long))+10
               
        #Dessin du point
        p= gr.Point(lattx, longy)
        p.draw(win)
        
        #Dessin du cercle
        c = gr.Circle(gr.Point(lattx, longy), 4)
        c.draw(win)
     
    win.getMouse() # pause for click in window
    win.close()


arrets()


