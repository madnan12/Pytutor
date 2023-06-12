from django.shortcuts import render
from django.views.generic import View

class HomePageView(View):
	template_name = 'homepage.html'

	def get(self, request):
		context = {
			'title'		: 'PyTutor-OM - Home'
		}
		return render(request, self.template_name, context)


# Error Views
def error_404(request, exception):
	return render(request, 'error_templates/error404.html')

def error_500(request, *args, **argv):
	return render(request, 'error_templates/error500.html', status=500)

def error_403(request, exception):

	return render(request,'error_templates/error403.html')

def error_400(request,  exception):
	return render(request,'error_templates/error400.html')  