import numpy as np
class pair:
    def __init__(self, pairID, num1,num2):
        self.pairID = pairID
        self.num1 = num1
        self.num2 = num2

class pair2:
    def __init__(self, num1,num2):
        self.num1 = num1
        self.num2 = num2
def identify(listIDs):
    #listIDs=np.array(listIDs)
    listproducts = [10, 20, 25, 30]
    listpairs =[]
    for i in listproducts:
        identical=np.where(listIDs == i)
        #print(identical[0])
        if len(identical[0])==2:
            p1=pair(i,identical[0][0],identical[0][1])
            listpairs+=[p1]

    return listpairs

# seconde tentative gestion plusieurs QR codes
# argument en + : la bonne paire
# si il y a présence de cette paire -> le dire, pas de tableau variable pour éviter les erreurs
def identify2(listIDs,numGoodPair):
    listIDs=np.array(listIDs)
    #goodPairDetected = False
    listproducts = [10, 20, 25, 30]

    # on détecte si on trouve la bonne ID dans les QR codes détectés
    identical=np.where(listIDs == numGoodPair)
    # s'il est trouvé deux fois, il y a une gate détectée
    if len(identical[0])==2:
        #goodPairDetected=True
        goodPair=pair2(identical[0][0],identical[0][1])
    else:
        goodPair = pair2(99,99)

    return goodPair

if __name__=="__main__":
    bidule=[10,20,30,30,20,10]
    #result=identify(bidule)
    #print((result[0]).pairID)
    #print((result[0]).num1)
    #print((result[0]).num2)
    result2=identify2(bidule,30)
    print(result2.num1)
    print(result2.num2)
