from django.db import models
from datetime import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        
        if len(postData['street_address']) < 8:
            errors['street_address'] = 'Street Address must be at least 8 characters'   
         
        if len(postData['city']) < 2:
            errors['city'] = 'City must be at least 2 characters'
            
        if len(postData['state']) < 2:
            errors['state'] = 'State must be at least 2 characters'
        
        if len(postData['zip_code']) < 5:
            errors['zip_code'] = 'Zip Code must be at least 5 digits'
        
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):    #check format of email
            errors['email'] = 'Invalid Email Address'
        
        existing_user = User.objects.filter(email=postData['email'])
                # email_check = self.filter(email=postData['email'])
                # if email_check:
                #     errors['email'] = "Email already in use"
        if len(existing_user) !=0:
            errors['user'] = "Email already in use"
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'        
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = 'Password and Confirm Password must match'  #don't tell them which one is wrong!
        
        return errors
      
    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(postData['email']):    #check format of email
            errors['email'] = 'Invalid Email Address'
    
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) !=1:      #now checking that at least one is found
            errors['email'] = "User not found"
        else:
            if len(postData['password']) < 8:
                errors['password'] = 'Password must be at least 8 characters' 
                
            else :    
                if bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:  #authenticate
                    errors['email'] = 'Email and Password do not match'  #don't tell them which one is wrong!
            
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zip_code= models.CharField(max_length=5)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = UserManager()
    
#-------------------end of USER ---------------------------------------------------------
class Category(models.Model):    #join as OneToOne with Gift (rather than being part/column in Gift table)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
  
class GiftManager(models.Manager):
    def gift_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "Name cannot be blank."

        print('whatever word here' + postData['description'])         
        if len(postData['description']) != 0:  #not required but if something then not less than 10chars
            if len(postData['description']) < 10:
                errors["description"] = "Gift description should be at least 10 characters"

        if datetime.strptime(postData['available_date'], '%Y-%m-%d') < datetime.now():
            errors['available_date'] = 'Avilable Date should be in the future' 

        return errors

class Gift(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    status = models.BooleanField()
    available_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoryJoin = models.ForeignKey(Category, related_name="gift_Join",null=True,on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="has_created_gifts", on_delete=models.CASCADE) #OneUser can upload/create ManyGifts
    favorited_by = models.ManyToManyField(User, related_name="favorited_gifts")     #liker and liked
    
    objects = GiftManager()
    
