
from django import forms
from social.models import PostComment ,Comment


from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from social.models import MyProfile
# from social.forms import ModelForm



class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your Email','class':'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'input100'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter confirm password','class':'input100'}))
    # confirm_Email = forms.EmailField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your valid email ','class':'input100'}))

    class Meta:
        model = MyProfile
        fields = ['username','name','last_name','password','confirm_password', 'phone_no','gender','pic']

        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Enter name','class':'input100'}),
            'last_name': forms.TextInput(attrs={'placeholder':'Enter Last name','class':'input100'}),
            # 'email': forms.TextInput(attrs={'placeholder':'Enter your Email','class':'input100'}),
            'gender': forms.Select(attrs={'id':'gender','class':'form-control custom-selec selcls input100'}),
            'birth_date' : forms.TextInput(attrs={'placeholder':' format 2000-04-16','class':'input100'}),
            'phone_no' : forms.TextInput(attrs={'placeholder':'Enter Phone','class':'input100'}),


        }



class updateform(forms.ModelForm):
	class Meta:
		model = MyProfile
		fields = ['name' ,'last_name','pic']



class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter  unique username','class':'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'input100'}))



class PostCommentForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['msg' ,'commented_by', 'post' ,'commented_by',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']