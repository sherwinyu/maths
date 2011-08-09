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
    resp = sess.answer(ans)
    if(resp=="WRONG"):
        resp+=","+str(ans)
    elif(resp=="LEVEL_OVER"):
        resp+=","+str(sess.levelScore)
    elif resp=="GAME_OVER":
        resp+=","+str(sess.levelScore)+","+str(sess.totalScore)
    elif resp=="CORRECT":
        mathsGame.computeNextQuestion()
        for session in mathsGame.sessions:
            session.waitingForQuestion = True
    return HttpResponse(resp)

def newSession(request):
    sessionID = startSession()
    print "sessionID", sessionID
    return render_to_response('play.html', {'form': AnswerForm, 'sessionID': sessionID} )

def newLevel(request):
    if not request.is_ajax() or request.method != 'POST':
        return redirect('/play')
    try: id = int(request.POST.get('sessionID', -1))
    except: id = -1
    if id == -1:
        return redirect('/play')
    sess = mathsSessions[id]
    q = sess.nextLevel()
    time = levelTimeLimit[sess.level]
    return HttpResponse(",".join(map(str,(sess.level,time,q))))

def playerReady(request):
    """
    called when user clicks next level
    sets sess.ready to true for the session of the current id
    binds session to game
    """
    print "in Player Ready"
    # if not request.is_ajax() or request.method != 'POST':
        # return redirect('/play')
    try:
        id = int(request.POST.get('sessionID', -1))
        print id
    except:
        id = -1
    if id == -1:
        return redirect('/play')
    sess = mathsSessions[id]
    sess.ready = True
    print "sess=", sess
    print "mG.s=", mathsGame.sessions
    mathsGame.sessions.append(sess)
    print "sess=", sess
    print "mG.s=", mathsGame.sessions
    return HttpResponse('success!thisisnnotparsed')

def pollNextLevel(request):
    print "pollNextlevel"
    if not request.is_ajax() or request.method != 'GET':
        return redirect('/play')
    try: id = int(request.GET.get('sessionID', -1))
    except: id = -1
    if id == -1:
        return redirect('/play')
    if not mathsGame.isNextLevelReady():
        return HttpResponse('FAIL') # TODO json this shit
    mathsGame.sessions[id].waitingForQuestion = True
    html = "SUCCESS,%d,%d" % (mathsGame.level, levelTimeLimit[mathsGame.level] )
    return HttpResponse(html)

def pollNextQuestion(request):
    try:
        if not request.is_ajax() or request.method != 'GET':
            return redirect('/play')
        try: id = int(request.GET.get('sessionID', -1))
        except: id = -1
        if id == -1:
            return redirect('/play')
        if not mathsGame.sessions[id].waitingForQuestion:
            return HttpResponse('FAIL')
        mathsGame.sessions[id].waitingForQuestion = False
        html = 'SUCCESS,%s' % mathsGame.nextQuestion
        return HttpResponse(html)
    except Exception as error:
        print error
        return HttpResponse(error)

def test(request):
    try:
        asdf
    except Exception as e:
        print e
        return HttpResponse(e)
    print "else"



