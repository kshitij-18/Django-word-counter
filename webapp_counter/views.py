from django.shortcuts import render, redirect
from .forms import URLForm
from .models import URLModel, WordModel
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from collections import Counter
# Create your views here.

blacklist = ['a', 'the', 'it', 'they', 'are', 'in', 'of', 'to', 'on', 'and']


def homepage(request):
    return render(request, 'webapp_counter/landing.html')


def frequency(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = request.POST.get('url')
            if URLModel.objects.filter(url=url):
                # Here the url is already in the database
                url_obj = URLModel.objects.filter(url=url).first()
                messages.info(request, "Data was already in the database")
                return redirect('result', url_id=url_obj.id)
                print("I am already in the databse")
            else:
                url_obj = form.save()
                print(url_obj)
                url_scrap = url
                source = requests.get(url_scrap).text

                soup = BeautifulSoup(source, 'lxml')
                soup2 = [x.extract()
                         for x in soup.findAll(['script', 'style'])]
                sorted(soup.text.split(),
                       key=soup.text.split().count, reverse=True)
                url_assign = URLModel.objects.filter(
                    url=url).first()  # getting the url which was saved
                count = 0
                for word in soup.text.split():
                    if count == 10:
                        break
                    if WordModel.objects.filter(word=word, url=url_obj.id) or word.lower() in blacklist:
                        continue
                    else:
                        url_obj.words.create(
                            word=word, count=soup.text.split().count(word))
                        count += 1
                messages.success(request, "This data is served fresh")
                return redirect('result', url_id=url_obj.id)

            print(url)

            return redirect('frequency-form')
        else:
            return redirect('frequency-form')
    else:
        form = URLForm()
    front = {
        'form': form
    }
    return render(request, 'webapp_counter/frequency.html', front)


def result(request, url_id):
    url_obj = URLModel.objects.filter(pk=url_id).first()
    words = url_obj.words.order_by("-count")
    frontend = {
        'words': words
    }
    return render(request, 'webapp_counter/result.html', frontend)
