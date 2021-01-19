from django.urls import path
from . import views


urlpatterns = [
  
    #localhost:8000/COMMUNETY  
    path('', views.landing),  #GET route renders landing.html.  Login/Reg = localhost:8000
    path('login', views.login),     
    path('Example', views.asAnExample),
     
    path('regPledge', views.regPledge),
    path('register', views.register), 
    path('guidelines', views.guidelines),
    path('logout', views.logout),
    
    path('today', views.today),  
    path('newGift', views.newGift),  #displays gift form
    path('create', views.create_gift), #validate new gift form and create gift
    path('<int:gift_id>/show', views.showGift),  #localhost:8000/communety/<gift_id/show>
    path('<int:gift_id>/edit', views.edit),   #display EDIT gift form
    path('<int:gift_id>/update', views.update),
    path('<int:gift_id>/delete', views.delete),
    
    path('dashboard', views.dashboard), 
    path('<int:gift_id>/request', views.requestGift),  #localhost:8000/communety/<gift_id/request>
    path('theWall', views.theWall),   
    
]