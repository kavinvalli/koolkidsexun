from django.shortcuts import render, redirect
# Importing User model
from django.contrib.auth.models import User
# Importing models from jobs
from jobs.models import Applicant
# Import login function
from django.contrib.auth import login


def register(request):
    
    if request.method == "POST":
        
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email_id = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        education= request.POST.get("education")
        age = request.POST.get("age")
        try:
            User.objects.get(username=username)
            return render(request, "register/register.html", {"message": "Username exists"})
        except:
            if "@" not in email_id:
                return render(request, "register/register.html", {"message": "Invalid Email Id"})
            else:
                if len(password) < 6:
                    return render(request, "register/register.html", {"message": "Password needs to be atleast 8 characters long"})
                else:
                    try:
                        User.objects.get(email=email_id)
                        return render(request, "register/register.html", {"message": "Email Id exists"})
                    except:
                        user = User.objects.create_user(username, email_id, password)
                        user.first_name=first_name
                        user.last_name=last_name
                        user.save()
                        login(request, user)
                        applicant = Applicant.objects.create(
                            user=user,
                            mobile=mobile,
                            gender=gender,
                            education=education,
                            age=age
                        )
                        url = 'jobs/'+str(user.id)
                        return redirect(url)
                        # I took this from one of my old works(www.kavin.me)... So the email authentication is there.
                        # I've still kept it so that it can be implemented if needed
                        # user.first_name = first_name
                        # user.is_active = False
                        # user.save()
                        # current_site = get_current_site(request)
                        # email_subject = 'Activate Your Account'
                        # message = render_to_string('activate_account.html', {
                        #     'user': user,
                        #     'domain': current_site.domain,
                        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                        #     'token': account_activation_token.make_token(user),
                        # })
                        # to_email = request.POST.get('email_id')
                        # from_email = 'EMAIL ID TO BE SENT FROM'
                        # email = EmailMessage(email_subject, message, from_email, to=[to_email])
                        # email.send()
                        # return HttpResponse('<h1>You would have recieved an email from us. Please authenticate your email id</h1>')
    return render(request, "register/register.html", {'message':None, 'heading':"Register with us today!!!"})
