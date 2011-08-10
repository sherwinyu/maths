import random
import time

mathsSessionCounter = 0
mathsSessions = {}
mathsGameCounter = 0
mathsGames = {}
levelTimeLimit = (-1,15,15,20,30,30)
totalNumLevels = 5

class MathsGame:
    
    def __init__(self, gameID):
        self.id = gameID
        self.sessionIDs = []
        self.nextQuestion = ''
        self.nextAnswer = 0
        self.difficulty = 1
        self.level = 0
        self.playing = False
        self.levelStart = None
        
    def addSession(self, sessionID):
        self.sessionIDs.append(sessionID)
        
    def nextLevel(self):
        self.level+=1 
        self.levelStart = time.time()
        for i in self.sessionIDs:
            mathsSessions[i].nextLevel()
        self.computeNextQuestion()
        self.playing = True
        
    def endLevel(self): 
        self.playing = False
        self.levelStart = None
        self.nextQuestion = None
        self.nextAnswer = None
        for i in self.sessionIDs:
            mathsSessions[i].endLevel()
    
    def computeNextQuestion(self):
        self.nextQuestion, self.nextAnswer = self.createProblem(self.level, self.difficulty)

    def isNextLevelReady(self):
        if(len(self.sessionIDs)<2): 
            return False
        for id in self.sessionIDs:
            if not (mathsSessions[id].ready):
                return False
        return True

    def createProblem(self, level, difficulty):
        max = 10**(level/2+1)
        a = random.randint(1,max)
        b = random.randint(1,max)
        if level%2 == 0:
            c = a+b
            return ('%d + %d = ?' % (a,b), c)
        else:
            c = a*b
            return ('%d * %d = ?' % (a,b), c)

class MathsSession:
    def __init__(self, id, gameID):
        self.id = id
        self.gameID = gameID
        self.levelScore = 0
        self.totalScore = 0
        self.ready = False
        self.waitingForQuestion = False

    def __unicode__(self):
        return "Session id", self.id

    def nextLevel(self):
        self.levelScore = 0 
        self.waitingForQuestion = True 

    # Checks if the answer is correct.
    # If there is no question, returns no_question
    # If the timer is up, returns game_over if there are no more levels, else returns level_over
    # If the answer is not parsable into an integer, returns invalid_answer
    # If the answer is wrong, returns wrong
    # Otherwise, the answer is correct, so we return correct
    def checkAnswer(self, answer):
        game = mathsGames[self.gameID]
        if game.levelStart==None or \
            (game.levelStart + levelTimeLimit[game.level] < time.time()):
            if self.ready:
                game.endLevel()
            return "GAME_OVER" if (game.level==totalNumLevels) else "LEVEL_OVER"
        if game.nextAnswer==None:
            return "NO_QUESTION"
        if answer==None:
            return "INVALID_ANSWER"
        if answer==game.nextAnswer: # if user's answer is correct
            self.levelScore+=1 #TODO change scoring system
            return "CORRECT"
        else:
            self.levelScore-=1 #TODO same
            return "WRONG"

    def endLevel(self):
        self.totalScore+=self.levelScore
        self.ready = False
        self.waitingForQuestion = False

def startSession():
    global mathsSessionCounter
    global mathsGameCounter
    id = mathsSessionCounter
    mathsSessionCounter+=1
    gameID = id/2
    if not gameID in mathsGames:
        mathsGames[gameID] = MathsGame(gameID)
        mathsGameCounter+=1
    mathsSessions[id] = MathsSession(id, gameID)
    mathsGames[gameID].addSession(id)
    return id

def endSession(id):
    if id in mathsSessions:
        del mathsSessions[id]
