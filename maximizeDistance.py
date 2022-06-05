import numpy
import random
import uuid
import copy
import json

class Wrestler():
    def __init__(self,age,weight,skill):
        self.uuid=str(uuid.uuid4())
        self.age=age
        self.weight=weight
        self.skill=skill
        self.numMatches=0
    def __eq__(self,other):
        return self.age == other.age and self.weight == other.weight and self.skill == other.skill
    def __hash__(self):
        return self.uuid.__hash__()

class Match():
    def __init__(self,mat,guy1,guy2):
        self.mat=mat
        self.wrestlers=[guy1,guy2]
    def totalCompositeScore(self):
        return sum([x.age + x.weight + x.skill for x in self.wrestlers])
    def setGroup(self,group):
        self.group=group
    def setIndex(self,index):
        self.index=index
def conflict(match,otherMatch):
    return match.wrestlers[0] in otherMatch.wrestlers or match.wrestlers[1] in otherMatch.wrestlers

def getRandomWrestler():
    # random age (avg 11), random weight(avg 80 lbs), random composite score(avg 3.5)
    ret=list(numpy.random.normal([11,80,3.5],[1,10,1]))
    return Wrestler(ret[0],ret[1],ret[2])
def closeEnough(guy1,guy2):
    return abs(guy1.age - guy2.age) < 1.5 and abs(guy1.weight - guy2.weight) < .1*min(guy1.weight,guy2.weight) and abs(guy1.skill-guy2.skill) < 1.5


def createAndPlaceMatches(mats,team1,team2):
    for guy1 in teams[i]:
        for guy2 in teams[j]:
            if closeEnough(guy1,guy2) and guy1.numMatches < 4 and guy2.numMatches < 4:
               createAndPlaceMatch(mats,guy1,guy2)
def createAndPlaceMatch(mats,guy1,guy2):
    matNumber=random.randint(0,len(mats)-1)
    guy1.numMatches +=1
    guy2.numMatches +=1
    mats[matNumber].append(Match(matNumber,guy1,guy2))
    mats[matNumber][-1].setIndex(len(mats[matNumber])-1)
def match(teams):
    mats=[[] for i in range(4)]
    for i in range(len(teams)):
        for j in range(i,len(teams)):
            createAndPlaceMatches(mats,teams[i],teams[j])
    return mats
def makeTeams():
    team1,team2,team3=[],[],[]
    for i in range(20):
        team1.append(getRandomWrestler())
        team2.append(getRandomWrestler())
        team3.append(getRandomWrestler())
    return team1,team2,team3

def parseWrestler(wrestlerJson):
	return Wrestler(wrestlerJson['age'],wrestlerJson['weight'],wrestlerJson['skill'])
def makeRealTeams():
	teamWrestlerDicts=json.loads(open("../exampleTournament.json","r").read())
	teams=[]
	for team in teamWrestlerDicts.values():
		wrestlers=[parseWrestler(wrestler) for wrestler in team.values()]
		teams.append(wrestlers)
	return teams

def minDistance(mats):
    mn=420
    for  i in range(len(mats)):
        for j in range(len(mats[i])):
            for k in range(j+1,len(mats[i])):
                if k-j < mn and conflict(mats[i][k],mats[i][j]):
                    mn=k-j
                    break
            for k in range(i+1,len(mats)):
                for l in range(len(mats[k])):
                    if abs(l-j) < mn and conflict(mats[k][l],mats[i][j]):
                        mn=abs(l-j)
    return mn

def getWrestlerMatches(mats):
    wrestlerMatches={}
    for mat in mats:
        for match in mat:
            for wrestler in match.wrestlers:
                if wrestler not in wrestlerMatches:
                    wrestlerMatches[wrestler]=[]
                wrestlerMatches.append(match.index)
    return wrestlerMatches
def _fastestMinDistance(wrestlerMatches):
    mn=123456789
    for wrestlerMatchList in wrestlerMatches.values():
        for i in range(len(wrestlerMatchList)):
            for j in range(i,len(wrestlerMatchList)):
                mn=min(mn,abs(wrestlerMatchList[i] - wrestlerMatchList[j]))
    return mn

def fastestMinDistance(mats):
    wrestlerMatches=getWrestlerMatches(mats)
    return _fastestMinDistance(wrestlerMatches)
    
def makeSwap(mats,i,j,k,l):
    tmp=mats[i][j]
    mats[i][j]=mats[k][l]
    mats[k][l]=tmp
    mats[i][j].setIndex(j)
    mats[k][l].setIndex(l)

def fastestHillClimb(mats):
    currentScore,mins=score(mats)
    nextMins=None
    while True:
        startingScore=currentScore
        for min in mins:
            mind=min.index
            mat=min.mat
            mxSwap,mxScore=None,-3
            for i in range(len(mats[mat])):
                makeSwap(mats,mat,mind,mat,i)
                tmpScore,tmpMins=score(mats)
                if tmpScore > mxScore:
                    mxScore=tmpScore
                    mxSwap=[mind,i]
                    mxMins=tmpMins
                makeSwap(mats,mat,mind,mat,i)
            if mxScore > currentScore:
                start_ind,end_ind=mxSwap
                makeSwap(mats,mat,start_ind,mat,end_ind)
                currentScore=mxScore
                nextMins=mxMins
        if startingScore == currentScore:
            break
        mins=nextMins
def score(mats):
    mn = fastestMinDistance(mats)
    numMins = 0
    mins=[]
    for i in range(len(mats)):
        for j in range(len(mats[i])):
            for k in range(i,len(mats)):
                for l in range(j+1 if k == i else 0,len(mats[k])):
                    if abs(j-l) == mn and conflict(mats[i][j],mats[k][l]):
                        numMins+=1
                        mins.append(mats[i][j])
                        mins.append(mats[k][l])
    return mn - numMins/100,mins
def main():
    team1,team2,team3=makeTeams()
    mats=match([team1,team2,team3])
    fastestHillClimb(mats)
    return score(mats)[0]
def runWithRealData():
    team1,team2,team3=makeRealTeams()
    mats=match([team1,team2,team3])
    print("number of matches: by mat")
    print([len(mat) for mat in mats])
    fastestHillClimb(mats)
    return score(mats)[0]
if __name__ == "__main__":
    for i in range(100):
        scr=runWithRealData()
        if scr <= 3:
            print("FAILED THIS ONE",scr)
            exit()
        print("PASS",scr)