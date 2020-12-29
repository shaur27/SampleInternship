from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
#from .forms import CustomerForm
from .forms import CreateUserForm
from django.views import View
from django.contrib.auth.decorators import login_required
#from .forms import CustomerUploadForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegForm, CreateUserForm
#from .forms import RegFileForm
from .models import Customer, CustomerReg
import schedule
import time
from background_task.models import Task
#from .models import multi_fileupload
#from django.contrib.auth.forms import UserChangeForm
# Create your views here.
"""
def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        phone= self.cleaned_data["phone"].split()
        user.phone = phone
        if commit:
            user.save()
        return user
"""
# View to register page
def registerPage(request):
    #if the customer is logged in, redirected to form page
    if request.user.is_authenticated:
        return redirect('form')
    #else the user registers via a form
    else:
        form=CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if(form.is_valid()):
                form.save()

                user=form.cleaned_data['username']
                #user_profile=User.objects.get(username=user)
                #phone=form.cleaned_data['phone']
                #user_profile.phone_number=phone
                #user_profile.save()
                messages.success(request, 'Account created for '+ user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'customer/register.html', context)
"""
def get_initial_data(request):
        form=RegForm(initial={
        'first_name':request.session.get('first_name',''),
        'last_name':request.session.get('last_name',''),
        'personal_email':request.session.get('personal_email',''),
        'official_email':request.session.get('official_email',''),
        'permanent_address':request.session.get('current_address',''),
        'current_address':request.session.get('permanent_address',''),
        'pan_card_number':request.session.get('pan_card_number',''),
        'aadhar_card_number':request.session.get('aadhar_card_number',''),
        'loan_amount':request.session.get('loan_amount','')})
        return form
"""
"""
def get(request):
        if request.session.has_key('pan_card_number'):
            form=RegForm(get_initial_data(request))
        context = {'form': form}
        return render(request, 'customer/index.html', context)
"""
@login_required(login_url='login') # only logged in users can access form page
def multi_form(request): #view for multi-form page
        form=RegForm()
        if request.method=='POST':
            form=RegForm(request.POST, request.FILES)
            if form.is_valid():
                
                #request.session['first_name']=form.cleaned_data['first_name']
                #request.session['last_name']=form.cleaned_data['last_name']
                #request.session['personal_email']=form.cleaned_data['personal_email']
                #request.session['official_email']=form.cleaned_data['official_email']
                #request.session['current_address']=form.cleaned_data['current_address']
                #request.session['permanent_address']=form.cleaned_data['permanent_address']
                #request.session['pan_card_number']=form.cleaned_data['pan_card_number']
                #request.session['aadhar_card_number']=form.cleaned_data['aadhar_card_number']
                #request.session['loan_amount']=form.cleaned_data['loan_amount']
                reg=form.save(commit=False)
                reg.customerReg=request.user
                if (not (reg.personal_photo or reg.bank_statement_1 or reg.bank_statement_2 or reg.bank_statement_3 or reg.pan_card or reg.salary_slip_1 or reg.salary_slip_2 or reg.salary_slip_3 or reg.aadhar_card_front or reg.aadhar_card_back)):
                #if (not (reg.personal_photo or reg.bank_statement or reg.pan_card or reg.salary_slip or reg.aadhar_card)):
                    reg.status='Incomplete' #status incomplete if a user has not uploaded the docs
                else:
                    reg.status='Pending' #status pending if a user has uploaded the docs and filled all the fields
                reg.save()
                print(request.user.id)
                #customer_obj = Customer.objects.get(id=request.user.id) # fetch new object from db
                #form.instance.customerReg = customer_obj
                print(request.user.id)
                messages.success(request, "Your Response has been recorded")
                context={'form':form}
                return render(request, 'customer/success.html', context)
            else :
                return render(request, 'customer/index.html', {'form': form})

        else: #a get request for multi-form page
            """
            customer=Customer.objects.get(request.id)
            data = {'first_name' : customer.first_name}
            form = RegForm(initial=data)
            """
            #if user logged in earlier and already submitted a form 
            if (request.user.is_authenticated):
                try:
                    customer=request.user.customer_set.last() #shows status of latest form submission of the logged in user 
                    print(customer)
                    #the fields stored in last form submission are retrieved from database
                    form = RegForm(initial={
                        'status':customer.status,
                        'first_name':customer.first_name,
                        'last_name':customer.last_name,
                        'personal_email':customer.personal_email,
                        'official_email':customer.official_email,
                        'permanent_address':customer.permanent_address,
                        'current_address':customer.current_address,
                        'pan_card_number':customer.pan_card_number,
                        'aadhar_card_number':customer.aadhar_card_number,
                        'loan_amount':customer.loan_amount})
                    #customer=Customer.objects.get(id=request.user.id)
                    #if(customer.first_name.)
                    #print(customer)
                    #print(request.user.id)
                    #print(request.user.username)
                    #customer=Customer.objects.filter(id=request.user.id).latest('first_name', 'last_name', 'personal_email', 'official_email', 'permanent_address', 'current_address', 'pan_card_number', 'loan_amount')
                    #customer= Customer.objects.get(first_name=customer.first_name)
                    #obj = Customer.objects.filter(first_name=customer.first_name)
                    #print(request.user.username)
                    #print(obj)
                    
                        #'first_name':customer[len(customer)-1].first_name,
                        #'last_name':customer[len(customer)-1].last_name,
                        #'personal_email':customer[len(customer)-1].personal_email,
                        #'official_email':customer[len(customer)-1].official_email,
                        #'permanent_address':customer[len(customer)-1].permanent_address,
                        #'current_address':customer[len(customer)-1].current_address,
                        #'pan_card_number':customer[len(customer)-1].pan_card_number,
                        #'aadhar_card_number':customer[len(customer)-1].aadhar_card_number,
                        #'loan_amount':customer[len(customer)-1].loan_amount})
                
                except: # if new user --> sees a blank form on get request of form page
                    customer=None
                    print(customer)
                    form=RegForm()
            """
            cur_customer = Customer.objects.get(id=request.user.id)
            form=RegForm(initial={
                    'first_name':cur_customer.get('first_name',''),
                    'last_name':cur_customer.get('last_name',''),
                    'personal_email':cur_customer.get('personal_email',''),
                    'official_email':cur_customer.get('official_email',''),
                    'permanent_address':cur_customer.get('current_address',''),
                    'current_address':cur_customer.get('permanent_address',''),
                    'pan_card_number':cur_customer.get('pan_card_number',''),
                    'aadhar_card_number':cur_customer.get('aadhar_card_number',''),
                    'loan_amount':cur_customer.get('loan_amount','')})
            """
            #if request.session.has_key('pan_card_number'):
                #form=RegForm(initial={
                    #'first_name':request.session.get('first_name',''),
                    #'last_name':request.session.get('last_name',''),
                    #'personal_email':request.session.get('personal_email',''),
                    #'official_email':request.session.get('official_email',''),
                    #'permanent_address':request.session.get('current_address',''),
                    #'current_address':request.session.get('permanent_address',''),
                    #'pan_card_number':request.session.get('pan_card_number',''),
                    #'aadhar_card_number':request.session.get('aadhar_card_number',''),
                    #'loan_amount':request.session.get('loan_amount','')})

            context = {'form': form}
            return render(request, 'customer/index.html', context)


# Python3 code to remove whitespace 
def removeSpace(string): 
    return string.replace(" ", "") 

from background_task import background
from django.contrib.auth.models import User

@background(schedule=10)
def validation():
    import requests
    import json
    from django.core import serializers
    #from StringIO import StringIO
    #buffer = StringIO()
    my_list=[]
    customer_object=Customer.objects.all()
    
    print(customer_object)
    for cus in (customer_object):
        flagP=0
        textP='No'
        flagA=0
        textA='No'
        #listboolA=[]
        #listboolP=[]
        if(cus.customer_valid==None):
            if (cus.first_name and cus.pan_card and (cus.aadhar_card_front or cus.aadhar_card_back)):
                #cus=customer_object
                print(cus.customer_valid)
                my_list.append(cus)
            
                #pan validation
                API_ENDPOINT = 'https://vsrnxr5yo0.execute-api.us-east-1.amazonaws.com/default'
                dataP = cus.pan_card
                headersP = {
                    "Content-Type":"application/binary",
                }
                reqP = requests.post(API_ENDPOINT, data=dataP, headers = headersP)
                #print(req.text)
            
                apiP=json.loads(reqP.content)
                print(apiP)
                #api_listP.append(apiP)
                #for keyP,valueP in apiP.items():
                #    tempP=[valueP]
                #    listboolP.append(tempP)
                #print(listbool[2])
                #key,val=api.items()[3]
                #myJsonA=json.dumps(api)
                #print(str(val))
                #str2=""
                #for eleP in listboolP[2]:
                #    str2 += eleP
            
                #print(str2)
                if(apiP['PAN Number']==None):
                    textP='Not Readable'
                    print("Pan not readable")
                    pass
                else:
                    if(removeSpace(apiP['PAN Number'])==cus.pan_card_number):
                        flagP=1
                        textP='Yes'
                        Customer.objects.filter(pk=cus.id).update(customer_valid="Yes")
                        print("Pan macthing")
                    else:
                        print("Pan not macthing")
                        Customer.objects.filter(pk=cus.id).update(customer_valid="No")
                        pass
                print("Pan validation request success")
            

                #aadhar validation
                API_ENDPOINT = 'https://7pogz8lql3.execute-api.us-east-1.amazonaws.com/default'
                data = cus.aadhar_card_front
                headers = {
                    "Content-Type":"application/binary",
                }
                req = requests.post(API_ENDPOINT, data=data, headers = headers)
                #print(req.text)
            
                api=json.loads(req.content)
                print(api)
                print(removeSpace(api['Aadhaar Number']))
                #api_list.append(api)
                #for key,value in api.items():
                #    temp=[value]
                #    listboolA.append(temp)
                #print(listbool[2])
                #key,val=api.items()[3]
                #myJsonA=json.dumps(api)
                #print(str(val))
                #str1=""
                #for ele in listboolA[2]:
                #    str1 += ele
                if(api['Aadhaar Number']==None):
                    textA='Not Readable'
                    print("Aadhaar not readable")
                    pass
                else:
                    if(removeSpace(api['Aadhaar Number'])==cus.aadhar_card_number):
                        flagA=1
                        textA='Yes'
                        Customer.objects.filter(pk=cus.id).update(customer_valid="Yes")
                        print("Aadhaar matching")
                    else:
                        Customer.objects.filter(pk=cus.id).update(customer_valid="No")
                        print("Aadhaar not matching")
                        pass
                print("Aadhar validation request success")
                #api_request_pan = requests.get("https://vsrnxr5yo0.execute-api.us-east-1.amazonaws.com/default")
                context={'my_list': my_list, 'cus':cus, 'textA':textA, 'textP':textP}
            else:
                print("Customer not provided aadhar or pan")
                pass
        else:
            print("Customer already validated")
            pass
"""
def multi_upload(request, *args, **kwargs):
    #file_form=RegFileForm
    if request.method == "POST":
        file_form=RegFileForm(request.POST, request.FILES)
        files=request.FILES.getlist('bank_statement')
        if file_form.is_valid():
            for f in files:
                file_instance=Customer(bank_statement=f)
                file_instance.save()
    else:
        file_form=RegFileForm()
        context = {'file_form': file_form}
        return render(request, 'customer/index.html', context)
"""
"""
def edit_form(request):
    if request.method=='POST':
        form=edit_regform(request.POST, instance=request.user)

        if(form.is_valid):
            form.save()
        return redirect('edit')

    else:
        form=edit_regform(instance=request.pan_card_number)
        context={'form': form}
        return render (request, 'customer/form/edit_form.html', context)
"""
"""
class multi_form(View):
    model=Customer
    template_name='login.html'

    def loginPage(self, request):
        if request.user.is_authenticated:
            return redirect('customer')
        else:
            if(request.method == 'POST'):
                username = request.POST.get('username')
                password = request.POST.get('password')
                user=authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, 'Username or Password is incorrect.')

            context={}
            return render(request, 'customer/login.html', context)

    def get_initial_data(self, request):
        form=RegForm(initial={
        'first_name':request.session.get('first_name',''),
        'last_name':request.session.get('last_name',''),
        'personal_email':request.session.get('personal_email',''),
        'official_email':request.session.get('official_email',''),
        'permanent_address':request.session.get('current_address',''),
        'current_address':request.session.get('permanent_address',''),
        'pan_card_number':request.session.get('pan_card_number',''),
        'aadhar_card_number':request.session.get('aadhar_card_number',''),
        'loan_amount':request.session.get('loan_amount','')})
        return form

    def get(self, request):
        if request.session.has_key('pan_card_number'):
            form=self.get_initial_data(request)
        context = {'form': form}
        return render(request, 'customer/index.html', context)
    
    
    def post(self, request):
        form=RegForm()
        if request.method=='POST':
            form=RegForm(request.POST, request.FILES)
            if form.is_valid():
                request.session['first_name']=form.cleaned_data['first_name']
                request.session['last_name']=form.cleaned_data['last_name']
                request.session['personal_email']=form.cleaned_data['personal_email']
                request.session['official_email']=form.cleaned_data['official_email']
                request.session['current_address']=form.cleaned_data['current_address']
                request.session['permanent_address']=form.cleaned_data['permanent_address']
                request.session['pan_card_number']=form.cleaned_data['pan_card_number']
                request.session['aadhar_card_number']=form.cleaned_data['aadhar_card_number']
                request.session['loan_amount']=form.cleaned_data['loan_amount']
                form.save()
                messages.success(request, "Your Response has been recorded")
                return render(request, 'customer/index.html')

            
        context = {'form': form}
        return render(request, 'customer/index.html', context)
"""
flag_background_task=0
#customer log in view
def loginPage(request):
    if request.user.is_authenticated:
        global flag_background_task
        flag_background_task=flag_background_task+1
        if flag_background_task<2:
            validation(repeat=600, repeat_until=None)
        else:
            pass
        #validation(repeat=600, repeat_until=None)
        #Task.objects.all().delete()
        return redirect('form')
    else:
        if(request.method == 'POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request, username=username, password=password)

            if user is not None: #if user instance has been created
                login(request, user)
                return redirect('/')
            else: # else the fields contain incorrect credentials
                messages.info(request, 'Username or Password is incorrect.')
        context={}
        return render(request, 'customer/login.html', context)

def logoutUser(request): #redirects to login page
    logout(request)
    return redirect('login')

"""
class multi_form(View):
    #form_class=RegForm, UploadForm
    model=Customer
    template_name='index.html'
    fname='new user'
    def get(self, request):
        
        if(request.session.has_key('fname')):
            fname=request.session['fname']
            lname=request.session['lname']
            pmail=request.session['Pid']
            omail=request.session['Oid']
            cadd=request.session['Cadd']
            padd=request.session['Padd']
            pan=request.session['Pan']
            aadhar=request.session['Aadhar']
            loan=request.session['Lamount']
            try:
                CustomerInfoForm=CustomerInfo(fname=fname,lname=lname,pmail=pmail,omail=omail,cadd=cadd,padd=padd,pan=pan,aadhar=aadhar,loan=loan)
                CustomerInfoForm.save()
                return render(request, 'customer/index.html')
            #except:
        return render(request, 'customer/index.html')

    def post(self,request):
        if(request.method=="POST"):
            first_name=request.POST.get("fname")
            #fname=first_name

            last_name=request.POST.get("lname")
            #lname=last_name

            personal_email=request.POST.get("Pid")
            #pmail=personal_email

            official_email=request.POST.get("Oid")
            #omail=official_email

            current_address=request.POST.get("Cadd")
            #cadd=current_address

            permanent_address=request.POST.get("Padd")
            #padd=permanent_address

            pan_card_number=request.POST.get("Pan")
            #pan=pan_card_number

            aadhar_card_number=request.POST.get("Aadhar")
            #aadhar=aadhar_card_number

            loan_amount=request.POST.get("LAmount")
            #loan=loan_amount

            request.session['fname']=first_name
            request.session['lname']=last_name
            request.session['Pid']=personal_email
            request.session['Oid']=official_email
            request.session['Cadd']=current_address
            request.session['Padd']=permanent_address
            request.session['Pan']=pan_card_number
            request.session['Aadhar']=aadhar_card_number
            request.session['Lamount']=loan_amount

            personal_photo=request.FILES['PhotoAttachment']
            bank_statement=request.FILES['BankAttachment']
            salary_slip=request.FILES['SalaryAttachment']
            pan_card=request.FILES['PanAttachment']
            aadhar_card=request.FILES['AadharAttachment']
            try:
                #CustomerInfoForm=CustomerInfo(fname=fname,lname=lname,pmail=pmail,omail=omail,cadd=cadd,padd=padd,pan=pan,aadhar=aadhar,loan=loan)
                #CustomerForm1=CustomerInfo(first_name=first_name, last_name=last_name, personal_email= personal_email, official_email=official_email, current_address=current_address, permanent_address=permanent_address, pan_card_number=pan_card_number, aadhar_card_number=aadhar_card_number, loan_amount=loan_amount)
                CustomerForm=Customer(first_name=first_name, last_name=last_name, personal_email= personal_email, official_email=official_email, current_address=current_address, permanent_address=permanent_address, pan_card_number=pan_card_number, aadhar_card_number=aadhar_card_number, loan_amount=loan_amount, personal_photo=personal_photo, bank_statement=bank_statement, salary_slip=salary_slip, pan_card=pan_card, aadhar_card=aadhar_card)
                #CustomerInfoForm.save()
                CustomerForm.save()
                #CustomerForm2.save()
                messages.success(request, "Your Response has been recorded")
                return render(request, 'customer/index.html')
            except:
                return render(request, 'customer/index.html')

    def multiform_submit(self, request):
        return render(request, 'customer/index.html')
"""
        



"""
def form_submit(request):
    form=CustomerForm()

    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Form Submitted, Continue to upload documents')
            form=CustomerForm()
        #else:
        #    messages.success(request, 'Please fill the from again')
        #    form=CustomerForm()
    context={'form':form}
    return render(request, 'customer/index.html', context)

def content_file_name(instance, filename):
    return '/'.join(['content', instance.first_name, filename])

"""

"""
def form_submit_upload(request):
    formUp=CustomerUploadForm()
    
    if request.method=='POST':
        formUp=CustomerUploadForm(request.POST, request.FILES)
        if formUp.is_valid():
            formUp.save()
            messages.success(request, 'Registeration Successful')
            formUp=CustomerUploadForm

    context={'formUp':formUp}
    return render(request, 'customer/upload.html', context)
"""

"""import requests, gspread
from oauth2client.client import SignedJwtAssertionCredentials

def authenticate_google_docs():
    f = file(os.path.join('l2gproject1-2b1d19335733.p12'), 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    credentials = SignedJwtAssertionCredentials('shauryashekhar1947@gmail.com', SIGNED_KEY, scope)

    data = {
        'refresh_token' : '1//0gdGvqcOT3-i5CgYIARAAGBASNwF-L9IrlUMPImaQH5hehrXEsKQCgFce-nkWG7C07RISy41_StEbTwU_QbD0Bdmz1qFoTiiJiFc',
        'client_id' : '632610458429-u09vk9t5u0ekga09s5c897il8btthtj0.apps.googleusercontent.com',
        'client_secret' : 'A1PcZoG2UhnPcokR1eGaSi76',
        'grant_type' : 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['ya29.a0AfH6SMDJWj735URE5CTx6VA9jyUDvix38uVz4nIoUg8zmfyoGbDILjd2ok7jBGqqXBtNxQx_BjoqrVuqYX3uTLQrP_79-wuXKf8P4MpromYgTLW5yBF0gkbfRs8_GwtrW3o_mlwoUrS7SGyh0D5mD4kucrvGkWk8Uac']

    gc = gspread.authorize(credentials)
    sh = gc.open("sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/18COXF7tx_E21L1nMu1ZV2Kj17rX2kuk4SQlpslOTk58/edit#gid=0')")
    
    return gc"""