"""Buqeia variants of the walking-route test. Run after dem.py; uses route.py in the same folder."""
import os
RP=os.path.join(os.path.dirname(os.path.abspath(__file__)),'route.py')
src=open(RP,encoding='utf-8').read()
head=src.split("res_all={}")[0]
g={'__file__':RP}; exec(head.replace("('nuweimeh','1,17')","('buqeia','1,17')"),g)
g['test'](list(range(7)),g['T'],'Jericho block, Achor = Buqeia, walking hours')
g={'__file__':RP}; exec(head.replace("('nuweimeh','1,17'),('wadi_qumran','20')","('buqeia','1,17'),('buqeia','20')"),g)
g['test']([0,2,3,4,5,6],g['T'],'Jericho block, Achor & Secacah valley = Buqeia, walking hours')
