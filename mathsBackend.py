import random
import time

mathsSessionCounter = 0
mathsSessions = {}
levelTimeLimit = (-1,5,5,5,5,5)

class MathsSession:
    def __init__(self, id):
        self.id = id
        self.difficulty = 1
        self.level = 0
        self.levelScore = 0
        self.totalScore = 0
        self.levelStart = None
        self.nextAnswer = None
        
    def nextLevel(self):
        self.level+=1
        self.levelScore = 0
        self.levelStart = time.time()
        return self.nextQuestion()
        
    def nextQuestion(self):
        question,answer = createProblem(self.level, self.difficulty)
        self.nextAnswer = answer
        return question
    
    def answer(self, answer):
        if self.levelStart+levelTimeLimit[self.level]<time.time():
            return "TIMEOUT"
        if self.nextAnswer==None:
            return "NO_QUESTION"
        if answer==self.nextAnswer:
            self.levelScore+=1
            return self.nextQuestion()
        else:
            self.levelScore-=1
            return "WRONG"
    
    def endLevel(self):
        self.totalScore+=self.levelScore
        self.levelStart = None
        self.nextAnswer = None

def startSession():
    global mathsSessionCounter
    id = mathsSessionCounter
    mathsSessionCounter+=1
    mathsSessions[id] = MathsSession(id)
    return id

def endSession(id):
    if id in mathsSessions:
        del mathsSessions[id]

def createProblem(level, difficulty):
    max = 10**level
    a = random.randint(1,max)
    b = random.randint(1,max)
    c = a+b
    return ('%d + %d = ?' % (a,b), c)


def testStack():
    id = startSession()
    sess = mathsSessions[id]
    for i in range(5):
        q = sess.nextLevel()
        while(q!="TIMEOUT"):
            if q!="WRONG":
                print q
            a = int(raw_input())
            q = sess.answer(a)
        print "Your score for this level: %d" % sess.levelScore
        sess.endLevel()
    print "Your total score: %d" % sess.totalScore
    endSession(id)
    
testStack()
    
    
    
    
    
    