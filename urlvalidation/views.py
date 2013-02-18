import sys
from urlvalidation.forms import UrlForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
import urllib2
from bs4 import BeautifulSoup

def home(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UrlForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            url = request.REQUEST['url']            
            result = get_url_content(url)
            return render(request, 'home.html', {
                'imgUrl': result, 'form': form,
            }) # Redirect after POST
    else:
        form = UrlForm() # An unbound form

    return render(request, 'home.html', {
        'form': form,
    })


def get_url_content(url): # get html content for given url 
    try:
        result = urllib2.urlopen(url).read()
    except ValueError as e:
        result = ''
        return result
    html_string = result
    html_content = BeautifulSoup(html_string)
    
    max_s = 0
    max_img_src = ''
    for anchor in html_content.findAll('img'):
        try:
            w = float(anchor['width'])
        except Exception, e:
            w = 0
        
        try:
            h = float(anchor['height'])
        except Exception, e:
            h = 0
            
        s = w*h
        if max_s < s:
            max_s = s 
            max_img_src = anchor['src']
    
    return max_img_src
          
    
    