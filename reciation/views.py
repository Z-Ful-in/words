from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ShowWordForm
from . import models
import datetime
import random
from utils import getForm
# from Spire.doc import *
# from Spire.doc.common import *
# Create your views here.


TodayWordIndex = 0

def addwords(request):
    if request.method == 'GET':
        return render(request,'addwords.html')
    if request.method == 'POST':
        form = ShowWordForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            word_error = form.errors.get('word')
            return render(request,'addwords.html',{'word_error':word_error})
    return render(request,'addwords.html')


def home(request):
    """This function returns the home page of the recitation app.
    We want to show user the list of words and their meanings.
    And you can directly add words from here.
    """
    if request.method == 'GET':
        # "Randomly"(by correct) display 5 words from the database
        form = getForm.getForm(10,'memory_strength','last_correct')
        return render(request, 'home.html', {'form': form})
    # if request.method == 'POST':
    #     form = ShowWordForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponse('Word added successfully')
    return render(request, 'home.html')

def display(request):
    """This function returns the list of words and their meanings."""
    if request.method == 'GET':
        form = models.Word.objects.all().order_by('-create_time')
        paginator = Paginator(form, 8)
        page = request.GET.get('page')
        try:
            form = paginator.page(page)
        except PageNotAnInteger:
            form = paginator.page(1)
        except EmptyPage:
            form = paginator.page(paginator.num_pages)
        return render(request, 'display.html', {'form': form})
    return render(request, 'display.html')


def delete(request):
    if request.method=="POST":
        word=request.POST.get('word')
        models.Word.objects.filter(word=word)[0].delete()
        return JsonResponse({'status':'success'})
    
def ediWords(request):
    if request.method == 'POST':
        word= request.POST.get('word')
        meaning = request.POST.get('meaning')
        obj=models.Word.objects.filter(word=word).first()
        if obj:
            obj.meaning=meaning
            obj.save()
            return JsonResponse({'status':'success'})
        return JsonResponse({'status':'fail'})
    
def spell(request):
    if request.method == 'GET':
        # "Randomly" display 10 words from the database
        form = getForm.getForm(10,'memory_strength','last_correct')
        return render(request, 'spell.html', {'form': form})
    return render(request,'spell.html')

def check(request):
    """ receive the ajax request"""
    if request.method == 'POST':
        word = request.POST.get('word')
        meaning = request.POST.get('meaning')
        obj = models.Word.objects.filter(meaning=meaning).first()
        obj.submission += 1
        obj.save()
        if str(word) == str(obj.word):
            obj.correct += 1
            obj.correct_rate = obj.correct / obj.submission
            obj.memory_strength += 0.5
            obj.save()
            return JsonResponse({'status':'success','correct_rate':obj.correct_rate})
        else:
            obj.correct_rate = obj.correct / obj.submission
            if obj.memory_strength <= 6:
                obj.memory_strength -= 1
            else:
                obj.memory_strength = 6
            obj.save()
        return JsonResponse({'status':'error','word':obj.word})

def recite(request):
    """process the ajax request and modify the database."""
    if request.method == 'POST':
        word = request.POST.get('word')
        status = request.POST.get('status')
        obj = models.Word.objects.filter(word=word).first()
        obj.submission += 1
        if status == 'rem':
            obj.correct += 1
            obj.memory_strength +=0.5
            obj.correct_rate = obj.correct / obj.submission
            obj.save()
            return JsonResponse({'status':'success','rate':obj.correct_rate,'meaning':obj.meaning})
        elif status == 'blur':
            if obj.memory_strength <= 6:
                obj.memory_strength -= 0.5
            else:
                obj.memory_strength = 6
            obj.correct_rate = obj.correct / obj.submission
            obj.save()
            return JsonResponse({'status':'success','meaning':obj.meaning,'word':obj.word})
        elif status == 'for':
            if obj.memory_strength <= 6:
                obj.memory_strength -= 1
            else:
                obj.memory_strength = 6
            obj.correct_rate = obj.correct / obj.submission
            obj.save()
            return JsonResponse({'status':'success','meaning':obj.meaning,'word':obj.word})
        elif status == 'fam':
            obj.correct += 1
            obj.memory_strength +=5
            obj.correct_rate = obj.correct / obj.submission
            obj.save()
            return JsonResponse({'status':'success','meaning':obj.meaning,'word':obj.word})
        return JsonResponse({'status':'success'})
    
def one_day_words_recite(request):
    """recite the words that have been added, and 
        create date is less than one day from today"""
    if request.method == 'GET':
        global TodayWordIndex
        total_form = models.Word.objects.filter(create_time__date__gt=datetime.date.today()\
                                                -datetime.timedelta(days=2))
        if TodayWordIndex >= len(total_form):
            TodayWordIndex = 0
        form = total_form.order_by('-create_time')[TodayWordIndex:TodayWordIndex+10]
        # disrupt the order of the form randomly
        form = sorted(form,key=lambda x:random.random())
        TodayWordIndex += 10
        return render(request, 'home.html', {'form': form})
    return render(request, 'home.html')

def one_day_words_spell(request):
    """spell the words that have been added today"""
    if request.method == 'GET':
        global TodayWordIndex
        total_form = models.Word.objects.filter(create_time__date__gt=datetime.date.today()\
                                                -datetime.timedelta(days=2))     
        if TodayWordIndex >= len(total_form):
            TodayWordIndex = 0
        form= total_form.order_by('-create_time')[TodayWordIndex:TodayWordIndex+10] 
        # disrupt the order of the form randomly
        form = sorted(form,key=lambda x:random.random())
        TodayWordIndex += 10
        return render(request, 'spell.html', {'form': form})
    return render(request, 'spell.html')

# def printList(request):
#     """print the list of words and their meanings"""
#     with open('wordList.txt','w', encoding='utf-8') as f:
#         for word in models.Word.objects.all():
#             f.write(word.word+'\t'+word.meaning+'\n')
#     return redirect('display')

def search(request):
    """search the words and their meanings"""
    if request.method == 'GET':
        return render(request,'search.html')
    if request.method == 'POST':
        seaData = request.POST.get('seaData')
        # Jugde whether the data string is word(engString) or meaning(cheseString)
        if seaData.encode('UTF-8').isalpha():
            form = models.Word.objects.filter(word__icontains=seaData)
        else:
            # For the Chinese string, we need to use the icontains 
            form = models.Word.objects.filter(meaning__icontains=seaData)
        data={'words':[],'meanings':[],'examples':[]}
        for i in form:
            data['words'].append(i.word)
            data['meanings'].append(i.meaning)
            data['examples'].append(i.example)
        return JsonResponse(data)

def page_not_found(request,exception):
    return render(request,'404.html')

def page_error(request):
    return render(request,'500.html')