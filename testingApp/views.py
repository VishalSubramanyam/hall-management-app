from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect


# Create your views here.
def handle_complaint_page(request):
    if "successful" in request.GET:
        if request.GET['successful'] == 'true':
            return render(request, 'complaint.html', {"success": "1"})
        else:
            return render(request, 'complaint.html', {"success": "0"})
    return render(request, "complaint.html", {"success": "-1"})


def handle_comp_submission(request):
    if 'comp-type' not in request.POST or 'description' not in request.POST:
        return HttpResponseBadRequest("Form data missing")

    comp_type = request.POST['comp-type']
    descr = request.POST['description']
    # Add database code
    return HttpResponseRedirect("complaint?successful=true")
