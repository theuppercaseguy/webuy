from django.shortcuts import render,redirect
from django.db import connection
from django.contrib.auth import login, authenticate,logout 
from django.contrib import  messages 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, SignInForm
from .models import CustomUser
import pandas as pd
import os
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def home(request):

    is_verified = False  # Default value if user is not logged in or not verified
    if request.user.is_authenticated:
        is_verified = request.user.is_verified

    # excel_path = os.path.join('computer_parts','static', 'computer_parts', 'cateloge.xlsx')
    # df = pd.read_excel(excel_path)

    csv_path = os.path.join('computer_parts','static', 'computer_parts', 'cateloge.csv')
    df = pd.read_csv(csv_path)
    
    items = df.to_dict(orient='records')
    categories = set(item['Category'] for item in items)
    category_items = {category: [] for category in categories}

    for item in items:
        category_items[item['Category']].append(item)

    return render(request, "computer_parts/home.html", {
        'is_verified':is_verified,
        'items': category_items,

    })

def search_page(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        sort_by = request.POST.get('sort', 'price_low_high')
        filter_by = request.POST.get('filter', '')
        
        # excel_path = os.path.join('computer_parts', 'static', 'computer_parts', 'cateloge.xlsx')
        # df = pd.read_excel(excel_path)
        
        csv_path = os.path.join('computer_parts','static', 'computer_parts', 'cateloge.csv')
        df = pd.read_csv(csv_path)
    

        filtered_items = df[df.apply(lambda row: any(search_query.lower() in str(row[col]).lower() for col in ['Name', 'Category', 'Tags']), axis=1)]

        if filter_by:
            filtered_items = filtered_items[filtered_items['Category'] == filter_by]

         # Apply sorting
        if sort_by == 'price_low_high':
            filtered_items = filtered_items.sort_values(by='Price')
        elif sort_by == 'price_high_low':
            filtered_items = filtered_items.sort_values(by='Price', ascending=False)


        items_searched = filtered_items.to_dict(orient='records')
        return render(request, "computer_parts/search_page.html", {
            'items': items_searched, 
            'search_query': search_query,
            'request':request,
            
            })
    else:
        return render(request, "computer_parts/search_page.html", {
                        'request':request,
                    })

def signup(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        age = request.POST.get('age')
        contact_number = request.POST.get('contact_number')
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'computer_parts/signup.html', {'error': 'email is already taken'})
        else:
            otp = ''.join(random.choices('0123456789', k=6))
            send_mail(
                'Verification Code',
                f'Your OTP for signup is: {otp}',
                settings.EMAIL_HOST_USER,  # Sender's email
                [email],  # Recipient's email
                fail_silently=False,
            )
            request.session['signup_otp'] = otp
            request.session['signup_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'age': age,
                'contact_number': contact_number,
                'password':password
            }
            return redirect('/otp_verification')
            
    else:
        signup_data = request.session.get('signup_data', {})
        return render(request, 'computer_parts/signup.html', {'signup_data': signup_data})
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            print("user logged in successfully")
            return redirect('/')
        else:
            print("user login failed")
            return render(request, 'computer_parts/signin.html', {'error': 'Invalid email or password'})
    else:
        return render(request, "computer_parts/signin.html")

def otp_verification(request):
    if request.method == 'POST':
        
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('signup_otp', '')
        
        print("0")
        print(entered_otp, stored_otp)
        if entered_otp == stored_otp:
            signup_data = request.session.get('signup_data', {})
            user = CustomUser.objects.create_user(**signup_data)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('/')
        else:

            messages.error(request, 'Incorrect OTP. Please try again.')
            return redirect('/otp_verification')

    else:
        # Render OTP verification page
        return render(request, 'computer_parts/otp_verification.html')


def signout(request):
    logout(request)
    return redirect("computer_parts:home")