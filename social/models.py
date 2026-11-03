from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, RegexValidator
from django_fields import DefaultStaticImageField
from django.dispatch import receiver
from django.db.models.signals import post_save


class Cont(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=13)
    desc = models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    
    def __str__(self):
        return  ' Name: '+self.name +'// Email id : '+self.email+ '// MOBILE NUMBER:-'+self.phone

# Create your models here.
class MyProfile(models.Model):
    name = models.CharField(max_length = 100)
    # first_name = models.CharField(max_length=12, blank=True)
    last_name = models.CharField(max_length=12, blank=True)
    # email = models.EmailField(max_length=150)

    # unique email confirmations
    # email = models.EmailField(max_length=150,unique=True)

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18)])
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="single", choices=(("single","single"), ("married","married"), ("widow","widow"), ("seprated","seprated"), ("commited","commited")))
    gender = models.CharField(max_length=20, default="female", choices=(("male","male"), ("female","female")))
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = DefaultStaticImageField(upload_to = "Download\\",blank=True, 
        default='Download/un.jpg')

# profile signup  add 
    cr_date = models.DateTimeField(auto_now_add=True)
    signup_confirmation = models.BooleanField(default=False)

    
    def __str__(self):
        return "%s" % self.name

    

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            MyProfile.objects.create(user=instance)



@receiver(post_save,sender=User)
def save_user_profile(sender,instance,created,**kwargs):
    if instance.is_superuser:
        pass
    else:
        instance.myprofile.save()

    

class MyPost(models.Model):
    pic=models.ImageField(upload_to = "images\\", null=True ,blank=True)
    subject = models.CharField(max_length = 200)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="videofile",blank=True)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, null=True, blank=True)
    def __str__(self):
        return "%s" % self.subject


class PostComment(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    msg = models.TextField()
    commented_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length=20, null=True, blank=True, choices=(("racist","racist"), ("abbusing","abbusing")))
    def __str__(self):
        return "%s" % self.msg


# rakesh comment
class Comment(models.Model):
    post = models.ForeignKey(MyPost, related_name='comments',on_delete=models.CASCADE)
    body = models.TextField()
    commented_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)


    def __str__(self):
        return 'Comment by {}'.format(self.commented_by.name)


class PostLike(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    liked_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.liked_by


class FollowUser(models.Model):
    profile = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="profile")
    followed_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="followed_by")
    def __str__(self):
        return "%s is followed by %s" % (self.profile, self.followed_by)
