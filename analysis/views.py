from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

#bot import
from analysis.tweets_one import tweepybot
from analysis.main import sentiment_analysis
from analysis.data_retrieve import data_retrieve_caller_frontend

# from .models import Analysis
from .models import *
from .forms import CreateUserForm
from .forms import KeywordGrabForm

#import for machine learning 


# Create your views here.
k = [] #keywords available in session
i=0


def home(request):

	form = KeywordGrabForm(request.POST)
	message = ""
	
	context = {'form': form, 'message': message}
	return render(request, 'home.html',context)


def about(request):
	# keyword =  request.session['keyword'].lower()
	# data_db = data_retrieve_caller_frontend("","",keyword)
	# pos = 0
	# neg = 0
	# neu = 0
	# neglist =[]
	# for a in data_db:
	# 	if a['sentiment_data'] is None:
	# 		continue
	# 	negative = a['sentiment_data']['scores']['negative']
	# 	positive = a['sentiment_data']['scores']['positive']
	# 	neutral = a['sentiment_data']['scores']['neutral']
		
	# 	scores = [float(negative), float(neutral), float(positive)]
		
	# 	if(scores[0] > scores[1] and scores[0] > scores[2]):
	# 		neg = neg+1
	# 		neglist.append(scores[0])
	# 	elif(scores[1] > scores[0] and scores[1] > scores[2] ):
	# 		neu = neu+1
	# 	else:
	# 		pos =pos+1


	# total_graph = [pos, neu, neg]
	# context = {'data': total_graph, 'data_db': data_db, 'keyword':keyword, 'neglist':neglist, 'range':range(len(neglist))}
	
	return render(request,'about.html')
	

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def stats(request):
	keyword =  request.session['keyword'].lower()
	data_db = data_retrieve_caller_frontend("","",keyword)


	# Text processing for Word Cloud - add in views.py
	ignorelist = {'A','An','And','From','The','This','That','With','There','Http','Have','Https','Of','He','She','They','Them','Hello','Hi','Yes','No','For','','T','Co'}
	mykeyword = keyword.split()
	for i in mykeyword:
		ignorelist.add(i.title())
	s = []
	tx = ''

	for st in data_db:
		st = st['data']['text']	
		tp = ''.join(e if e.isalnum() else " " for e in st.strip())
		tp = tp.split(" ")
		tp = [i.title() for i in tp if( (i.title() not in ignorelist)  and len(i)>3 )]
		s += tp
	
	tx += ' '.join(s)


	pos = 0
	neg = 0
	neu = 0
	neglist =[]
	poslist =[]
	neulist =[]
	date_list=[]
	scores_list = [] #0-neg , 1-neu , 2-pos
	# total_stats = [] # followers_count  retweets favorites
	total_dict = {}
	most_liked = {}
	most_retweet = {}
	most_followers = {}
	for a in data_db:
		if a['sentiment_data'] is None:
			continue
		
		negative = a['sentiment_data']['scores']['negative']
		positive = a['sentiment_data']['scores']['positive']
		neutral = a['sentiment_data']['scores']['neutral']
		
		# total_stats.append([a['data']['followers_count'], a['data']['retweet_count'], a['data']['favorite_count'],a['data']['text']])
		total_dict[a['_id']] = [a['data']['text']]
		most_liked[a['_id']] = a['data']['favorite_count']
		most_retweet[a['_id']] = a['data']['retweet_count']
		most_followers[a['_id']] = a['data']['followers_count']


		scores = [float(negative), float(neutral), float(positive)]
		neglist.append(scores[0])
		neulist.append(scores[1])
		poslist.append(scores[2])
		scores_list.append(scores)
		
		if(scores[0] > scores[1] and scores[0] > scores[2]):
			neg = neg+1
			scr = 'negative'

			
		elif(scores[1] > scores[0] and scores[1] > scores[2] ):
			neu = neu+1
			scr = 'neutral'
		else:
			pos =pos+1
			scr = 'positive'
		temp = total_dict[a['_id']]
		temp.append(scr)
		total_dict[a['_id']] =temp
	scr = 'scr'
	sorted_followers = {k: v for k, v in sorted(most_followers.items(), key=lambda item: item[1], reverse = True)}
	
	for i in sorted_followers:

		max_followers = {sorted_followers[i]: total_dict[i][0], scr: total_dict[i][1]}
		break

	sumof_retweets  = sum(list(most_retweet.values()))
	sumof_favorites = sum(list(most_liked.values()))


	total = list(range(neg+pos+neu))
	total_graph = [pos, neu, neg]
	value = 0
	thavala = []

	sorted_liked = {k: v for k, v in sorted(most_liked.items(), key=lambda item: item[1], reverse = True)}

	sorted_retweeted = {k: v for k, v in sorted(most_retweet.items(), key=lambda item: item[1], reverse=True)}

	top_5_liked = {}
	top_5_retweeted = {}
	counter = 0
	for i in sorted_liked:
		top_5_liked[sorted_liked[i]] ={'tweet':total_dict[i][0], 'scr': total_dict[i][1]}
		counter += 1
		if counter == 5:
			break

	counter = 0
	for i in sorted_retweeted:
		top_5_retweeted[sorted_retweeted[i]] = {'tweet':total_dict[i][0], 'scr': total_dict[i][1]}
		counter += 1
		if counter == 5:
			break
	
	total = total[0:11]
	neulist = neulist[0:11]
	neglist = neglist[0:11]
	poslist = poslist[0:11]
	

	max_followers_number = list(max_followers.keys())[0]
	max_followers_tweet = max_followers[max_followers_number]

	favlist = []
	rtlist = []
	for likes, sentidata in top_5_liked.items():
		temp = []
		temp.append(likes)
		for key in sentidata:
			temp.append(sentidata[key])
		favlist.append(temp)

	for likes, sentidata in top_5_retweeted.items():
		temp = []
		temp.append(likes)
		for key in sentidata:
			temp.append(sentidata[key])
		rtlist.append(temp)	
	
	context = {'common':tx, 'top_tweet': thavala,'date_list': date_list,'sumof_retweets': sumof_retweets,
	 'sumof_favorites': sumof_favorites, 'max_followers': max_followers_number, 'max_tweet': max_followers_tweet,'data': total_graph, 'data_db': data_db,
	  'keyword':keyword, 'neglist': neglist,'poslist': poslist, 'neulist': neulist,'total': total,
	   'scores_list':scores_list, 'top_five_l':favlist, 'top_five_rt':rtlist}
	
	return render(request,'stats.html', context)



def test(request):
	return render(request, 'test.html')

def search(request):
	print(request.POST)
	form = KeywordGrabForm(request.POST)
	print(form.fields)
	if form.is_valid():
		message = '<div class="text-center mx-auto px-2 ml-1 p-3 mb-2 bg-success text-white"> Accepted the keyword</div>'
		keyword = form.cleaned_data['keyword']
		# start_date = form.cleaned_data['start_date']
		# end_date = form.cleaned_data['end_date']
		number_of_tweets = form.cleaned_data['number_of_tweets']
		request.session['keyword'] = keyword		
		print("Keyword : ",keyword, "No. of tweets required : ",number_of_tweets,".........\n")
		if keyword != '':
			status_flag = tweepybot(keyword.lower().strip(), int(number_of_tweets))
			#print(status_flag)
			sentiment_analysis(keyword)			
		else:
			status_flag = "@tweepybot : work avunnilla mone"
		#print(status_flag)
		return redirect('stats')
	else:
		return redirect('home')


# def result(request):
#     #load SentiModel here
#     results = Analysis.object.all()
#     return render(request,'result.html',{'results':results})