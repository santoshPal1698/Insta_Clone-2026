from django.shortcuts import render,HttpResponse  ,redirect ,get_object_or_404
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from social.models import FollowUser, MyPost, MyProfile, PostComment, PostLike
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from social.models import Contact, Comment
from django.http import HttpResponse, HttpResponseRedirect ,JsonResponse
from social.forms import PostCommentForm, CommentForm 
from social.forms import UserLogin ,SignUpForm ,updateform
from social.decorater import unauthenticated_user

# Create your views here.

# login logout account sectionn

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from social.token_generator import account_activation_token
# email confirmations

# default signup
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# Create your views here.
# default signup

def confirm(request):
    return render(request, 'social/confirm.html')    


@unauthenticated_user
def register(request):
    form = SignUpForm()
    if  request.method =='POST':
        form = SignUpForm(request.POST,request.FILES)
        username = None
        try:
            username = User.objects.get(username = request.POST.get('username'))
            if username:
                messages.success(request, 'username is already exsist..')       
                return redirect('register')
        except:
            print('username',request.POST['username'])
            if form.is_valid():
                username  = request.POST.get('username')
                user = User.objects.create_user(username=username.lower(), password=request.POST['password'],email=request.POST['username'])
                user.myprofile.name = request.POST.get('name')
                print('name',request.POST['name'])
                user.myprofile.last_name = request.POST.get('last_name')
                print('last name',request.POST.get('last_name'))
                # user.myprofile.email = request.POST.get('email')
                user.myprofile.gender = request.POST.get('gender')
                user.myprofile.phone_no = request.POST.get('phone_no')
                user.myprofile.pic = request.FILES.get('pic')
                user.save()
                
                # mail confirmations
                current_site = get_current_site(request)
                print('current_site#######################',current_site,user)
                subject = 'Please Activate Your Account'
                # load a template like get_template() 
                # and calls its render() method immediately.
                message = render_to_string('social/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('username')
                email = EmailMessage(subject, message, to=[to_email])
                email.send()
                return render(request, 'social/confirm.html')    
                # return HttpResponse('email is sent !!')
                # print(user)
    return render(request, 'social/register.html', {'form': form})



def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def userprofile(request):
    user = request.user.myprofile 
    print('user',user)
    form  = SignUpForm(instance=user)
    if request.method=='POST':
        form = SignUpForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            print('form is valid')
            form.save()
    context={'form':form}
    return render(request,'social/userprofile.html',context)



def updateprofile(request):
    profile = request.user.myprofile
    if request.method == 'POST':
        form = updateform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    else:
        form = updateform(instance=profile)
    return render(request, 'social/updateprofile.html', {'form': form})


@unauthenticated_user
def user_login(req):
    form = UserLogin()
    if req.method == 'POST':
        print(req.POST)
        form = UserLogin(req.POST)
        if form.is_valid():
            # Here we check user is available in the database or not if available then is authenticate the user
            # But not set in session so because of this we can't get the info of authenticate user
            user=authenticate(username = req.POST.get('username'),password=req.POST.get('password'))
            if user is not None:
                # Here login is set the user in session. Now we get whole info of user
                login(req,user)
                return redirect('home')
            else:
                return HttpResponse('You are not authenticated')
    return render(req,'social/login.html',{'form':form})



def user_logout(req):
    if req.user.is_authenticated:
        logout(req)
        return redirect('login')

# login loout account sectionn


@method_decorator(login_required, name="dispatch")  
class HomeView(TemplateView):
    template_name = "social/home.html"

    def get_context_data(self,**kwargs):
        context = TemplateView.get_context_data(self,**kwargs)
        followedList = FollowUser.objects.filter(followed_by = self.request.user.myprofile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        postList = MyPost.objects.filter(uploaded_by__in = followedList2).order_by("-id")     
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post = p1,liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True        
            obList = PostLike.objects.filter(post = p1)
            p1.likedno = obList.count()

        context["mypost_list"] = postList
        print('mypost_list all data',postList)
        return context;

def comment(req,pk):
    post = MyPost.objects.get(pk=pk)
    comments = post.comments.filter(active=True, parent__isnull=True)
    context = {'comment':comments}
    return render(req,'social/home.html',context)


@method_decorator(login_required, name="dispatch")    
class AboutView(TemplateView):
    template_name = "social/about.html"


def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")


def like(req, pk):
    print('i am in like',pk)
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = req.user.myprofile)
    # Ajaximplemention for calling base.html
    data = {'success':'success'}
    return JsonResponse(data,safe=False)


def unlike(req, pk):
    print('i am in unlike',pk)
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = req.user.myprofile).delete()
    # Ajaximplemention for calling base.html
    data = {'success':'success'}
    return JsonResponse(data,safe=False)


def comment(req,pk):
    form = PostCommentForm(instance=request.user.myprofile)
    if request.method=='POST':
        form = PostCommentForm(request.POST,request.FILES,instance=request.user.myprofile)
        if form.is_valid:
            print('form is valid')
            form.save()
    return render(request, 'social/home.html',{'form':form})    



@method_decorator(login_required, name="dispatch")    
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "description", "pic"]


@method_decorator(login_required, name="dispatch")    
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject", "videofile" ,"msg", "pic"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class MyPostUpdateView(UpdateView):
    model = MyPost
    fields = ["subject", "videofile", "msg", "pic"]
    template_name = "social/mypost_form.html"

    def get_queryset(self):
        if not hasattr(self.request.user, "myprofile"):
            return MyPost.objects.none()
        return MyPost.objects.filter(uploaded_by=self.request.user.myprofile)


@method_decorator(login_required, name="dispatch")    
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by = self.request.user.myprofile)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id");
 

def myPostDetail(req,pk):
    post = MyPost.objects.get(pk=pk)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if req.method=='POST':
        comment_form = CommentForm(data=req.POST)
        print('come in side of comment form',comment_form)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(req.POST.get('parent_id'))
            except:
                parent_id=None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            print('user===================',req.user.myprofile)
            new_comment.commented_by = req.user.myprofile
            new_comment.save()
            messages.success(req, ' your Data has Been Successfully Send ??')       
            url = '/social/mypost/'+str(pk)
            return redirect(url)
            print('save is complite')
        else:
            print('error',comment_form.errors)
    else:
        comment_form = CommentForm()

    post_likes = PostLike.objects.filter(post=post)
    liked = False
    if req.user.is_authenticated and hasattr(req.user, "myprofile"):
        liked = post_likes.filter(liked_by=req.user.myprofile).exists()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
        'like_count': post_likes.count(),
    }
    return render(req,'social/mypost_detail.html',context)



@method_decorator(login_required, name="dispatch")    
class MyPostDeleteView(DeleteView):
    model = MyPost

@method_decorator(login_required, name="dispatch")    
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profList = MyProfile.objects.filter(Q(name__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id");
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1,followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return profList

@method_decorator(login_required, name="dispatch")    
class MyProfileDetailView(DetailView):
    model = MyProfile


@login_required() 
def contact(request):
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone)
        if len(name)<2 or len(email)<4 or len(phone)<10 or len(content)<5:
            messages.error(request, 'Sorry ,please fill the form in a right manner')
        else:
            contact=Cont(name=name,email=email,phone=phone,desc=content)
            contact.save()
            messages.success(request, ' your Data submitted successfully')       
    return render(request,'social/contact.html')

 
