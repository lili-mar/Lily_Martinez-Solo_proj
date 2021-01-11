from django.shortcuts import render, HttpResponse, redirect  #test HttpResponse
from .models import *               #import ALL models
from django.contrib import messages     #validation
import bcrypt
from .forms import RegForm
from .forms import LogForm
from datetime import datetime


#Login/Reg = localhost:8000/communEty
def landing(request):
    request.session.flush()
    context = {      
        'logForm': LogForm(),
    }
    return render(request, 'landing.html', context)


def login(request):
    if request.method == 'POST':
        print(request.POST) #should see QueryDict
        
        errors = User.objects.login_validator(request.POST)
        print(errors)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
                
            # context = {      
            #     'logForm': LogForm(),
            # }
            
            #return render(request, 'partialMsgs.html', context)  #AJAX!!!
                
            return redirect('/communety')    #redirect the user back to the form to fix the errors
        else:
            
            this_user = User.objects.get(email = request.POST['email'])   
            request.session['user_id'] = this_user.id
            #messages.success(request, "You have successfully logged in!")
            return redirect('/communety/today')
  
def asAnExample(request):  
    return render(request, 'Example.html')

          
        
def regPledge(request):
    request.session.flush()
    context = {
        'regForm': RegForm(),   
    }
    return render(request, 'regPledge.html', context)

def register(request):
    if request.method == 'POST':
        print(request.POST) #should see QueryDict
        
        errors = User.objects.reg_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/communety/regPledge')    #redirect the user back to the form to fix the errors
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()    
            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                street_address = request.POST['street_address'],
                city = request.POST['city'],
                state = request.POST['state'],
                zip_code= request.POST['zip_code'],
                email = request.POST['email'],
                password = hashed_pw)       
            request.session['user_id'] = new_user.id
            #messages.success(request, "You have successfully registered!")
            return redirect('/communety/today')

def guidelines(request):  
    return render(request, 'guidelines.html')


# replace with Your NEW APPLICATION    
def logout(request):
    request.session.clear()
    return redirect('/communety')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/communety')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)

def today(request):
    if 'user_id' not in request.session:
        return redirect('/communety')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'today.html', context)

#display(newGift.html via link in landing.html) and then create_gift
def newGift(request):
    if 'user_id' not in request.session:
        return redirect('/communety/today')
         
    user = User.objects.get(id=request.session['user_id'])
    my_gifts = Gift.objects.filter(creator_id = request.session['user_id']).order_by("-created_at")
    #future = Gift.objects.filter(datetime.strptime(available_date, "%d/%m/%Y"))
    #future = Gift.objects.filter(date__range=[available_date, "2040-01-31"])
    #future = Gift.objects.filter(date__range=[Gift.objects.filter(available_date), "2040-01-31"])
    #today = datetime.now()
    #greater = future.date() > today.date()
    #print (today)
    #print (future) 
    #####User.objects.all().order_by ("-first_name")
    context = {
        "categs_list": Category.objects.all(),
        "gifts_list": Gift.objects.all(),   
        "logged_user": user, 
        "my_gifts" : my_gifts, 
        #"my_gifts" : my_gifts.objects.all().order_by("-available_date"),  
        #"greater" :   greater, 
    }   
    return render(request, 'newGift.html', context) 

def create_gift(request):
    if request.method == 'POST':
        print(request.POST) #should see QueryDict
        
        errors = Gift.objects.gift_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
                print ("I am in the error section")
            return redirect('/communety/newGift')    #redirect the user back to the form to fix the errors
        else: 
            user = User.objects.get(id=request.session['user_id'])           
            myGift = Gift.objects.create(
                name = request.POST['name'],
                description = request.POST['description'],
                available_date = request.POST['available_date'],
                categoryJoin_id=request.POST['categoryJoin'],
                #categoryOneJoin_id=Category.objects.get(id=request.POST['categoryOneJoin']),
                creator = user, 
                status = False,
            )
            return redirect('/communety/newGift')
        
def showGift(request, gift_id):
    this_gift = Gift.objects.filter(id=gift_id)  #d_id comes from the urls.py parm.  FILTER is SO important here -do not use GET!       
    if len(this_gift) != 1:
        return redirect('/communety/newGift')
    context = {
        'one_gift': this_gift[0],  #need this because it is a list.  grab "value" to initially populate record for the update/view
    }
    return render(request, 'showGift.html', context) 

#display(edit.html via link in oneGift.html) and then update
def edit(request, gift_id):
    this_gift = Gift.objects.filter(id=gift_id)  #gift_id comes from the urls.py parm.  FILTER is SO important here -do not use GET!       
    if len(this_gift) != 1:
        return redirect('/communety/newGift')
    context = {
        'one_gift': this_gift[0],  #need this because it is a list.  grab "value" to initially populate record for the update/view
    }  
    return render(request, 'edit.html', context) 

def update(request, gift_id):
    if request.method == 'POST':
        this_gift = Gift.objects.filter(id=gift_id)  #gift_id comes from the urls.py parm.  FILTER is SO important here -do not use GET!            
        
        errors = Gift.objects.gift_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/communety/{gift_id}/edit')   #redirect the user back to the form to fix the errors
        else:     
            print(request.POST)      
            gift = this_gift[0]
            gift.name = request.POST['name']
            print(this_gift[0].name)
            #gift.categoryJoin=request.POST['categoryJoin']
            #gift.status = request.POST['status']
            gift.description = request.POST['description']
            gift.available_date = request.POST['available_date']
            gift.save()       #DON'T FORGET otherwise it won't update!!!
            #messages.success(request, "Gift successfully updated")
            return redirect(f'/communety/{gift_id}/show')  


def delete(request, gift_id):
    to_delete = Gift.objects.get(id=gift_id)    #This works but it is recommended to do it as POST see booksAuthors_proj
    to_delete.delete()
    #return redirect('/communety/dashboard')
    return redirect('/communety/newGift')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/communety/today')
    
    user = User.objects.get(id=request.session['user_id'])
    sortGifts = Gift.objects.all().order_by("categoryJoin")  #works also with categoryJoin_id
    context = {
        "categs_list": Category.objects.all(),
        "sortGifts" : sortGifts, 
        "logged_user": user, 
    }
    return render(request, 'dashboard.html', context)

def requestGift(request, gift_id):
    this_gift = Gift.objects.filter(id=gift_id)  #d_id comes from the urls.py parm.  FILTER is SO important here -do not use GET!       
    if len(this_gift) != 1:
        return redirect('/communety/dashboar')
    context = {
        'one_gift': this_gift[0],  #need this because it is a list.  grab "value" to initially populate record for the update/view
    }
    return render(request, 'requestGift.html', context) 

def theWall(request):
    if 'user_id' not in request.session:
        return redirect('/communety/dashboard')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'theWall.html', context)