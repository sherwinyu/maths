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
    sess = mathsSessions[id]
    resp = sess.checkAnswer(ans)
    if(resp=="WRONG"):
        resp+=","+str(ans)
    elif(resp=="LEVEL_OVER"):
        resp+=","+str(sess.levelScore)
    elif resp=="GAME_OVER":
        resp+=","+str(sess.levelScore)+","+str(sess.totalScore)
    elif resp=="CORRECT":
        mathsGame.computeNextQuestion()
        for sessionID in mathsGame.sessions:
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
    sess = mathsSessions[id]
    sess.ready = True
    if mathsGame.isNextLevelReady():
        mathsGame.nextLevel()
    return HttpResponse('success!thisisnnotparsed')

def pollNextLevel(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try: id = int(request.POST.get('sessionID', -1))
    except: id = -1
    if id == -1:
        return redirect('/play')
    if not mathsGame.playing:
        return HttpResponse('FAIL') # TODO json this shit
    html = "SUCCESS,%d,%d" % (mathsGame.level, levelTimeLimit[mathsGame.level] )
    return HttpResponse(html) 

def pollNextQuestion(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try: id = int(request.POST.get('sessionID', -1))
    except: id = -1
    if id == -1:
        return redirect('/play')
    if not mathsSessions[id].waitingForQuestion:
        return HttpResponse('FAIL')
    
    mathsSessions[id].waitingForQuestion = False
    html = 'SUCCESS,'+mathsGame.nextQuestion
    return HttpResponse(html)


