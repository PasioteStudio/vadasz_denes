import math     
def tavolsag(x1, y1, z1, x2, y2, z2):
    tav = 0.0
    tav = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return tav
class Buvar():
    def __init__(self,SEBESSEG:float,IDO:int,GYONGYOK:list[dict]) -> None:
        self.x=0
        self.y=0
        self.z=0
        self.SEBESSEG=SEBESSEG
        self.ido=IDO
        self.GYONGYOK=GYONGYOK
        pass
    def KifuteAzIdobolHaOdamegy(self,GYONGY:dict):
        ut=tavolsag(self.x,self.y,self.z,GYONGY["x"],GYONGY["y"],GYONGY["z"]) + tavolsag(GYONGY["x"],GYONGY["y"],GYONGY["z"],0,0,0)
        idotartam=ut/self.SEBESSEG
        return self.ido - idotartam >= 0
class Jatek():
    def __init__(self,IDO:int,SEBESSEG:float,gyongyokFajlNeve:str) -> None:
        self.ido = IDO
        self.SEBESSEG = SEBESSEG
        self.gyongyokFajlNeve = gyongyokFajlNeve
        self.getGyongyok()
        buvar=Buvar(SEBESSEG,IDO,self.GYONGYOK)
        pass
    def getGyongyok(self) -> list[dict]:
        fajl=open(self.gyongyokFajlNeve,"r+",encoding="utf8")
        sorok=fajl.readlines()
        fajl.close()
        self.GYONGYOK=[]
        for sor in sorok:
            reszek=sor.strip().split(";")
            if not reszek[0].isnumeric():
                continue
            self.GYONGYOK.append({"x":int(reszek[0]),
                                  "y":int(reszek[1]),
                                  "z":int(reszek[2]),
                                  "e":int(reszek[3]),})
        return self.GYONGYOK
SEBESSEG=input("Sebesség (m/s): ") #Majd float kompatibilisre!
IDO=input("Idő (mp): ")
gyongyFajlNeve=input("Gyöngyök fájljának neve: ")

try:
    IDO=int(IDO)
    SEBESSEG=int(SEBESSEG)
    ujJatek=Jatek(IDO,SEBESSEG,gyongyFajlNeve)
except:
    pass