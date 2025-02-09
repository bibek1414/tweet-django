from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Tweet
from .forms import TweetForm
from .forms import UserRegistrationForm

# View to list all tweets
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})

# View to create a new tweet (only logged-in users can create tweets)
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # Associate the tweet with the logged-in user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweets/tweet_form.html', {'form': form})

# View to see the details of a specific tweet
def tweet_detail(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    return render(request, 'tweets/tweet_detail.html', {'tweet': tweet})

# View to edit an existing tweet (only the user who created the tweet can edit it)
@login_required
def tweet_edit(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    
    # Ensure that only the tweet's author can edit it
    if tweet.user != request.user:
        return HttpResponse("You are not authorized to edit this tweet.", status=403)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweets/tweet_form.html', {'form': form})

# View to delete a tweet (only the user who created the tweet can delete it)
@login_required
def tweet_delete(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)

    # Ensure that only the tweet's author can delete it
    if tweet.user != request.user:
        return HttpResponse("You are not authorized to delete this tweet.", status=403)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')  # Redirect after deleting the tweet
    return render(request, 'tweets/tweet_confirm_delete.html', {'tweet': tweet})

# View to register a new user
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not commit yet to set password
            user.set_password(form.cleaned_data['password1'])  # Set the password correctly
            user.save()  # Save the user object to the database

            # Log the user in immediately after registration
            login(request, user)

            return redirect('tweet_list')  # Redirect to tweet list page after successful registration
    else:
        form = UserRegistrationForm()  # Create an empty form for GET requests
    return render(request, 'registration/user_register.html', {'form': form})
