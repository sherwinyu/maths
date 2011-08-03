from django.http import HttpResponse
from mathsBackend import *
from django.shortcuts import render_to_response, redirect
from forms import AnswerForm

def submitAnswer(request):
	if not request.is_ajax() or request.method != 'POST':
		return redirect('/play')
	try: ans = int(request.POST.get('answer', None))
	except: ans = None
	try: id = int(request.POST.get('sessID', -1))
	except: id = -1
	if(id==-1):
		return redirect('/play')
	sess = mathsSessions[id]
	resp = sess.answer(ans)
	if(resp=="WRONG"):
		resp+=","+str(ans)
	elif(resp=="LEVEL_OVER"):
		resp+=","+str(sess.levelScore)
	elif(resp=="GAME_OVER"):
		resp+=","+str(sess.levelScore)+","+str(sess.totalScore)
	return HttpResponse(resp)

def newSession(request):
	sessID = startSession()
	sess = mathsSessions[sessID]
	return render_to_response('play.html', {'form': AnswerForm, 'sessID': sessID} )

def newLevel(request):
	if not request.is_ajax() or request.method != 'POST':
		return redirect('/play')
	try: id = int(request.POST.get('sessID', -1))
	except: id = -1
	if(id==-1):
		return redirect('/play')
	sess = mathsSessions[id]
	q = sess.nextLevel()
	time = levelTimeLimit[sess.level]
	return HttpResponse(",".join(map(str,(sess.level,time,q))))
