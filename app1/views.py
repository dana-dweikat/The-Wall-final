from django.shortcuts import render,redirect
from .models import Users ,Comments,Messages 
from django.contrib import messages
import bcrypt

def registration(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        return redirect('app1:wall')
    
    return render(request, "registration.html") 


def register(request):
    if request.method == "POST":
        
        errors = Users.objects.validate(request.POST)
        
        # There is some errors
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect('app1:index')
        
        first_name_form = request.POST['first_name']
        last_name_form = request.POST['last_name']
        email_form = request.POST['email']
        password_form = request.POST['password1']
        confirm_password_form = request.POST['password2']
        
        if password_form == confirm_password_form:
            hash_password = bcrypt.hashpw(password_form.encode(), bcrypt.gensalt()).decode()
            
            new_user =Users.objects.create(
                first_name=first_name_form,
                last_name = last_name_form,
                email=email_form,
                password=hash_password)
            
            
            request.session['user_id'] = new_user.id
            return redirect('app1:wall')

        # if password didn't match
        else:
            messages.error(request, 'Password not match.')
            return redirect('app1:index')



def login(request):
    if request.method == "POST":
        email_form = request.POST['email']
        password_form = request.POST['password1']
        
        users = Users.objects.filter(email=email_form)
        
        if len(users) == 0:
            messages.error(request, "Email doesn't exist.")
            return redirect('app1:registration')
        
        if bcrypt.checkpw(password_form.encode(), users.first().password.encode()):
            request.session['user_id'] = users.first().id
            return redirect('app1:wall')
        # if password is wrong
        else:
            messages.error(request, 'Password not correct.')
            return redirect('app1:registration')



def logout(request):
    request.session.flush()
    return redirect('app1:registration')


def wall(request):
    user_id = request.session.get('user_id')
    # if user not logged in
    if not user_id:
        return redirect('app1:registration')
    
    user = Users.objects.get(id=user_id)
    # To order by the most recent message
    messages = Messages.objects.all().order_by('-created_at')
    
    context = {
        'user': user,
        'messages': messages
    }
    return render(request, 'wall.html', context)



# POST message
def message(request):
    text = request.POST['text']
    user_id = request.session.get('user_id')
    current_user = Users.objects.get(id=user_id)
    
    Messages.objects.create(user_id=current_user, message=text)
    return redirect('app1:wall')


# POST comment
def comment(request):
    comment = request.POST['comment']
    
    message_id = request.POST['message_id']
    current_message = Messages.objects.get(id=message_id)
    
    user_id = request.session.get('user_id')
    current_user = Users.objects.get(id=user_id)
    
    Comments.objects.create(user_id=current_user, message_id=current_message, comment=comment)
    
    return redirect('app1:wall')







