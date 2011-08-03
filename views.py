from django.http import HttpResponse
from mathsBackend import *
from django.shortcuts import render_to_response, redirect
from forms import ContactForm

def hello_world(request): #, direction, num_hrs):
	#num_hrs = int(num_hrs)
	#if direction=="minus":
	    #num_hrs *= -1
	#dt = datetime.datetime.now() #+ datetime.timedelta(hours=num_hrs)
	#t = get_template('current_datetime.html')
	#html = t.render(Context({'time': dt}))
	ua = request.META['HTTP_USER_AGENT']
	return HttpResponse("helloworld %d\nYour browser is %s" % (test5(), ua)  )
	#return HttpResponse("hello")

def search_form(request):
	return render_to_response('search_form.html')

def ua_display_good1(request):
	pass

def search(request):
	error = False
	if 'q' in request.GET:
		if request.GET['q']:
			message = 'Youd searched for: %r' % request.GET['q']
			return HttpResponse(message)
		else: # or it's empty
			error = True
	return render_to_response('search_form.html', {'error': error})

def xhr_test(request):
	if request.is_ajax():
		message = "Hello Ajax"
	else:
		message = "Hello w/o Ajax"
	return HttpResponse(message)

def contact(request):
	if request.method == 'POST': # it's a post method // validate and display errors or thank ou
		form = ContactForm(request.POST)
		if form.is_valid():
			return HttpResponse("Thanks!")
	else:  # display the form itself
		form = ContactForm()
	return render_to_response('contact_form.html', {'form': form})

def submitAnswer(request):
	if request.is_ajax():
		return HttpResponse("It's ajax!")
	else:
		return redirect('/play')



