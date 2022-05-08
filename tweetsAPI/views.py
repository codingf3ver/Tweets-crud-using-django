from re import A
from django.shortcuts import render
from tweetsAPI.models import Tweet
from tweetsAPI.models import RegisterUser
from django.contrib import messages
import logging
a_logger = logging.getLogger(__name__)
a_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s  %(name)s.%(funcName)s %(message)s')
output_file_handler = logging.FileHandler("app.log")
output_file_handler.setFormatter(formatter)
a_logger.addHandler(output_file_handler)

def home(request):
    return render(request, 'home.html')

def create_user(request,methods=['POST']):
    if request.method == 'POST':
        username = request.POST.get('username')
        if RegisterUser.objects.filter(username=username).exists():
            messages.error(request,'User already exists.')
            a_logger.info("User already exists.")
            return render(request, 'create_user.html')
    
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm_email')
        if email != confirm_email:
            messages.error(request,'Email and Confirm Email should be same.')
            return render(request, 'create_user.html')
        username = str(username)
        if len(username) <8 :
            messages.error(request,'Username should be atleast 8 characters.')
            a_logger.info("Username should be atleast 8 characters.")
            return render(request, 'create_user.html')
        if len(username) >10 :
            messages.error(request,'Username should be atmost 10 characters.')
            a_logger.info("Username should be atmost 10 characters.")
            return render(request, 'create_user.html')
        user = RegisterUser(username=username,fname=fname,lname=lname,email=email)
        user.save()
        messages.success(request,'User has created successfully.')
        a_logger.info("User has created successfully.")
    return render(request, 'create_user.html')

def create_tweet(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        tweet_text = request.POST.get('tweet_text')
        
        if len(str(tweet_text))-1 >140 :
            messages.error(request,'Tweet should be atmost 140 characters.')
            a_logger.info("Tweet should be atmost 140 characters.")
            return render(request, 'create_tweet.html')
        if len(str(tweet_text))-1 <2:
            messages.error(request,'Tweet should be atleast 2 characters.')
            a_logger.info("Tweet should be atleast 2 characters.")
            return render(request, 'create_tweet.html')
        try:
            if RegisterUser.objects.filter(username=username).exists():
                user_id = RegisterUser.objects.get(username=username)
                tweet = Tweet(user_id=user_id,tweet_text=tweet_text)
                tweet.save()
                messages.success(request,'Your tweet has been posted successfully.')
                a_logger.info("Your tweet has been posted successfully.")
                return render(request, 'create_tweet.html')
            messages.error(request,'User does not exist.')
            a_logger.info("User does not exist.")
        except Exception as e:
            a_logger.info(e)

    return render(request, 'create_tweet.html')

def read_tweet(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        date=request.POST.get('date') 
        try:
            if RegisterUser.objects.filter(username=username).exists():
                user_id = RegisterUser.objects.filter(username=username).values_list('user_id',flat=True)
                tweets = Tweet.objects.filter(user_id=user_id[0]).filter(timestamp__gte=date).values_list('tweet_text',flat=True)
                total_tweets = tweets.count()
                if total_tweets == 0:
                    messages.error(request,'No tweets found.')
                    a_logger.info("No tweets found.")
                context = {'tweets':tweets,'total_tweets':total_tweets,'username':username}
                return render(request, 'read_tweet.html',context)
            messages.error(request,'User does not exist.')
            a_logger.info("User does not exist.")
        except Exception as e:
            a_logger.info(e)
    return render(request, 'read_tweet.html')

def delete_tweet(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            if RegisterUser.objects.filter(username=username).exists():
                user = RegisterUser.objects.filter(username=username).values_list('user_id',flat=True)
                tweets = Tweet.objects.filter(user_id=user[0]).values_list('tweet_text',flat=True)
                total_tweets = tweets.count()
                tweet_id = Tweet.objects.filter(user_id=user[0]).values_list('tweet_id',flat=True)
                context = {'tweets':tweets,'total_tweets':total_tweets,'tweet_id':tweet_id}
            
                if total_tweets is None or total_tweets == 0:
                    messages.error(request,'No tweets found.')
                    a_logger.info("No tweets found.")
                    return render(request, 'delete_tweet.html')

                del_tweet =  Tweet.objects.filter(user_id=user[0])
                if del_tweet.exists():
                    messages.success(request,f'user\'s {username} tweet has been deleted successfully.')
                    a_logger.info(f"user\'s {username} tweet has been deleted successfully.")
                    del_tweet.delete()
                    return render(request, 'delete_tweet.html',context)
                print(context)
            messages.error(request,'User does not exist.')   
            a_logger.info("User does not exist.")  
        except Exception as e:
            a_logger.info(e)
           
    return render(request, 'delete_tweet.html')