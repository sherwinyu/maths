from django.http import HttpResponse
from mathsBackend import *

def hello_world(request): #, direction, num_hrs):
	#num_hrs = int(num_hrs)
	#if direction=="minus":
	    #num_hrs *= -1
	#dt = datetime.datetime.now() #+ datetime.timedelta(hours=num_hrs)
	#t = get_template('current_datetime.html')
	#html = t.render(Context({'time': dt}))
	return HttpResponse("helloworld %d" % test5() )
