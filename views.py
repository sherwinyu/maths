from django.http import HttpResponse
from mathsBackend import *
from django.shortcuts import render_to_response, redirect
from forms import AnswerForm

def submitAnswer(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try: ans = int(request.POST.get('answer', None))
    except: ans = None
    try: id = int(request.POST.get('sessionID', -1))
    except: id = -1
    if(id==-1):
        return redirect('/play')
    
    session = mathsSessions[id]
    game = mathsGames[session.gameID]
    resp = session.checkAnswer(ans)
    if(resp=="WRONG"):
        resp+=","+str(ans)
    elif(resp=="LEVEL_OVER"): 
        resp+=","+str(session.levelScore)
    elif resp=="GAME_OVER":
        resp+=","+str(session.levelScore)+","+str(session.totalScore)
    elif resp=="CORRECT":
        game.computeNextQuestion()
        for sessionID in game.sessions:
            mathsSessions[sessionID].waitingForQuestion = True
    return HttpResponse(resp)

def newSession(request):
    sessionID = startSession()
    return render_to_response('play.html', {'form': AnswerForm, 'sessionID': sessionID} )

def playerReady(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try:
        id = int(request.POST.get('sessionID', -1))
    except:
        id = -1
    if id == -1:
        return redirect('/play')
    
    session = mathsSessions[id]
    game = mathsGames[session.gameID]
    session.ready = True
    if game.isNextLevelReady():
        game.nextLevel()
    return HttpResponse('Success')

def pollNextLevel(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try: id = int(request.POST.get('sessionID', -1))
    except: id = -1
    if id == -1:
        return redirect('/play')
   
    session = mathsSessions[id]
    game = mathsGames[session.gameID]
    if not game.playing:
        return HttpResponse('FAIL')
    
    html = "SUCCESS,%d,%d" % (game.level, levelTimeLimit[game.level] )
    return HttpResponse(html) 

def pollNextQuestion(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try: id = int(request.POST.get('sessionID', -1))
    except: id = -1
    if id == -1:
        return redirect('/play')
    
    session = mathsSessions[id]
    game = mathsGames[session.gameID]
    if not session.waitingForQuestion:
        return HttpResponse('FAIL')
    
    session.waitingForQuestion = False
    html = 'SUCCESS,'+game.nextQuestion
    return HttpResponse(html)

