from django.http import HttpResponse
from mathsBackend import *
from django.shortcuts import render_to_response, redirect
from forms import AnswerForm

def submitAnswer(request):
	if not request.is_ajax() or request.method != 'POST':
		return redirect('/play')
	id = int(request.POST.get('sessID', -1))
	ans = int(request.POST.get('answer', 0))
	print id, ans
	if(id==-1):
		return redirect('/play')
	sess = mathsSessions[id]
	resp = sess.answer(ans)
	if(resp=="TIMEOUT "):
		sess.endLevel()
		resp+=sess.levelscore
	return HttpResponse(resp)

def newSession(request):
	sessID = startSession()
	sess = mathsSessions[sessID]
	q = sess.nextLevel()
	return render_to_response('play.html', {'form': AnswerForm, 'sessID': sessID, 'question': q} )


