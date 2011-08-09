import random
import time

mathsSessionCounter = 0
mathsSessions = {}
levelTimeLimit = (-1,15,5,5,10,10)
totalNumLevels = 5

class MathsGame:

    def computeNextQuestion(self):
        self.nextQuestion, self.nextAnswer = self.createProblem(self.level, self.difficulty)

    def isNextQuestionReady(self):
        return self.nextQuestionReady

    def isNextLevelReady(self):
        for s in self.sessions:
            print s.id
        print len(self.sessions)
        return len(self.sessions) % 2 == 0

    def createProblem(self, level, difficulty):
        max = 10**level
        a = random.randint(1,max)
        b = random.randint(1,max)
        c = a+b
        return ('%d + %d = ?' % (a,b), c)

    def __init__(self, game_id):
        self.id = game_id
        self.sessions = []
        self.nextAnswer  =  ''
        self.difficulty = 1
        self.level = 1
        self.computeNextQuestion()
        print "nextQuestion=", self.nextQuestion
        self.nextQuestionReady = True # by default, first question is always ready

mathsGame = MathsGame(0)

class MathsSession:
    def __init__(self, id):
        self.id = id
        self.levelScore = 0
        self.totalScore = 0
        self.levelStart = None
        self.nextAnswer = None
        self.ready = False
        self.waitingForQuestion = False

    def __unicode__(self):
        return "Session id", self.id

    def nextLevel(self):
        self.level+=1
        self.levelScore = 0
        self.levelStart = time.time()
        return self.nextQuestion()

    # Checks if the answer is correct.
    # If there is no question, returns no_question
    # If the timer is up, returns game_over if there are no more levels, else returns level_over
    # If the answer is not parsable into an integer, returns invalid_answer
    # If the answer is wrong, returns wrong
    # Otherwise, the answer is correct, so we return correct
    def answer(self, answer):
        if self.nextAnswer==None:
            return "NO_QUESTION"
        if self.levelStart + levelTimeLimit[self.level] < time.time():
            gameOver = self.endLevel()
            return "GAME_OVER" if gameOver else "LEVEL_OVER"
        if answer==None:
            return "INVALID_ANSWER"
        if answer==self.nextAnswer: # if user's answer is correct
            self.levelScore+=1 #TODO change scoring system
            return "CORRECT"
        else:
            self.levelScore-=1 #TODO same
            return "WRONG"

    def endLevel(self):
        """
        Ends current level
        Returns true if the game over, false if there are more levels
        """
        self.totalScore+=self.levelScore
        self.levelStart = None
        self.nextAnswer = None
        gameOver = False
        if(self.level==totalNumLevels):
            gameOver = True
        return gameOver

def startSession():
    global mathsSessionCounter
    id = mathsSessionCounter
    mathsSessionCounter+=1
    mathsSessions[id] = MathsSession(id)
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
