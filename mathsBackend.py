import random
import time

mathsSessionCounter = 0
mathsSessions = {}
levelTimeLimit = (-1,5,5,5,10,10)
totalNumLevels = 5

class MathsGame:
    
    def __init__(self, gameID):
        self.id = gameID
        self.sessions = []
        self.nextQuestion = ''
        self.nextAnswer = 0
        self.difficulty = 1
        self.level = 0
        self.playing = False
        self.levelStart = None
        
    def addSession(self, sessionID):
        self.sessions.append(sessionID)
        
    def nextLevel(self):
        self.level+=1 
        self.levelStart = time.time()
        for i in self.sessions:
            mathsSessions[i].nextLevel()
        self.computeNextQuestion()
        self.playing = True
        
    def endLevel(self): 
        self.playing = False
        self.levelStart = None
        self.nextQuestion = None
        self.nextAnswer = None
        for i in self.sessions:
            mathsSessions[i].endLevel()
    
    def computeNextQuestion(self):
        self.nextQuestion, self.nextAnswer = self.createProblem(self.level, self.difficulty)

    def isNextLevelReady(self):
        if(len(self.sessions)<2): 
            return False
        for i in self.sessions:
            if not (mathsSessions[i].ready):
                return False
        return True

    def createProblem(self, level, difficulty):
        max = 10**level
        a = random.randint(1,max)
        b = random.randint(1,max)
        c = a+b
        return ('%d + %d = ?' % (a,b), c)

mathsGame = MathsGame(0)

class MathsSession:
    def __init__(self, id):
        self.id = id
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
        if mathsGame.levelStart==None or (mathsGame.levelStart + levelTimeLimit[mathsGame.level] < time.time()):
            if self.ready:
                mathsGame.endLevel()
            return "GAME_OVER" if (mathsGame.level==totalNumLevels) else "LEVEL_OVER"
        if mathsGame.nextAnswer==None:
            return "NO_QUESTION"
        if answer==None:
            return "INVALID_ANSWER"
        if answer==mathsGame.nextAnswer: # if user's answer is correct
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
    id = mathsSessionCounter
    mathsSessionCounter+=1
    mathsSessions[id] = MathsSession(id)
    mathsGame.addSession(id)
    return id

def endSession(id):
    if id in mathsSessions:
        del mathsSessions[id]



def testStack():
    id = startSession()
    sess = mathsSessions[id]
    for i in range(5):
        q = sess.nextLevel()
        while(q!="TIMEOUT"):
            if q!="WRONG":
                print q
            a = random.randint(1, 10**(i+1)*2)
            q = sess.answer(a)
        print "Your score for this level: %d" % sess.levelScore
        sess.endLevel()
    print "Your total score: %d" % sess.totalScore
    endSession(id)
