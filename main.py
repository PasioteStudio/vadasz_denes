#5 FŐ DOLOG:
#Gyöngy távolsága
#Gyöngy értéke
#Idő (+ Visszafele is betudjon zsebelni pontot)
#Gyöngyök elhelyezkedése egymástól


import math     
def tavolsag(x1, y1, z1, x2, y2, z2):
    tav = 0.0
    tav = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return tav
class Buvar():
    def __init__(self,sebesseg:float,ido:int,gyongyok:list[dict]) -> None:
        self.x=0
        self.y=0
        self.z=0
        self.sebesseg=sebesseg
        self.ido=ido
        self.gyongyok=gyongyok
        pass
    def KifuteAzIdobolHaOdamegy(self,gyongy:dict):
        ut=tavolsag(self.x,self.y,self.z,gyongy["x"],gyongy["y"],gyongy["z"]) + tavolsag(gyongy["x"],gyongy["y"],gyongy["z"],0,0,0)
        idotartam=ut/self.sebesseg
        return self.ido - idotartam >= 0
class Jatek():
    def __init__(self,ido:int,sebesseg:float,gyongyokFajlNeve:str) -> None:
        self.ido = ido
        self.sebesseg = sebesseg
        self.gyongyokFajlNeve = gyongyokFajlNeve
        self.getGyongyok()
        buvar=Buvar(sebesseg,ido,self.gyongyok)
        pass
    def getGyongyok(self) -> list[dict]:
        fajl=open(self.gyongyokFajlNeve,"r+",encoding="utf8")
        sorok=fajl.readlines()
        fajl.close()
        self.gyongyok=[]
        for sor in sorok:
            reszek=sor.strip().split(";")
            if not reszek[0].isnumeric():
                continue
            self.gyongyok.append({"x":int(reszek[0]),
                                  "y":int(reszek[1]),
                                  "z":int(reszek[2]),
                                  "e":int(reszek[3]),})
        return self.gyongyok
sebesseg=input("Sebesség (m/s): ") #Majd float kompatibilisre!
ido=input("Idő (mp): ")
gyongyFajlNeve=input("Gyöngyök fájljának neve: ")

try:
    ido=int(ido)
    sebesseg=int(sebesseg)
    ujJatek=Jatek(ido,sebesseg,gyongyFajlNeve)
except:
    pass