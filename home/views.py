from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.contrib.sites.shortcuts import get_current_site
from iGo import env
from django.views import View
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from .models import VerificationToken, Profile, Education, Feeds, Like, Comment
import hashlib, datetime
from .feed_control import upload_feed


@login_required
def index(request):
    content = {}
    content['server'] = env.content
    return render(request, 'home/index.html', content)


class Register(View):
    def get(self, request):
        content = {}
        content['server'] = env.content
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        return render(request, 'registration/register.html', content)

    def post(self, request):
        content = {}
        content['server'] = env.content
        has_error = False
        username = 
        request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(username) < 5:
            content['form_error'] = 'Username is not valid'
            has_error = True
        elif len(password) < 8:
            content['form_error'] = 'Password is not valid'
            has_error = True
        elif len(email) < 8:
            content['form_error'] = 'Email is not valid'
            has_error = True
        if User.objects.filter(username=username).exists():
            content['form_error'] = 'Username already exists'
            has_error = True
        elif User.objects.filter(email=email).exists():
            content['form_error'] = 'Email Address already exists'
            has_error = True
        if has_error:
            return render(request, 'registration/register.html', content)
        else:
            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.is_active = False
            new_user.save()
            if User.objects.filter(username=username, email=email).exists():
                token = generate_verification_token(username)
                tok = VerificationToken(user=new_user, token=token)
                tok.save()
                content['form_success'] = 'Registration successful<br>Check your email for verification token'
                template = get_template('mail/mail.html')
                subject = "iGo - Registration Successful"
                to = [email]
                from_email = 'licoltd36@gmail.com'
                url = 'http://' + get_current_site(request).domain
                right = url+'/account/activate?token='+token+'&username='+username+'&link='+str(tok.pk)+'&verify=true'
                wrong = url+'/account/activate?token='+token+'&username='+username+'&link='+str(tok.pk)+'&verify=false'
                msg = "Your registration with iGo is successful. You need to verify your account to login to the server" \
                      ", This process is to prevent fake registrations on the server. Kindly verify your account."
                context = {'msg': msg, 'usr': username, 'right': right, 'wrong': wrong}
                message = template.render(context)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()
                return render(request, 'registration/register.html', content)
            else:
                content['form_error'] = 'Registration failed'
                return render(request, 'registration/register.html', content)


# generation verification token
def generate_verification_token(username):
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


# activating user account
def activate_account(request):
    content = {}
    content['server'] = env.content
    token = request.GET['token']
    user = request.GET['username']
    id = int(request.GET['link'])
    verify = request.GET['verify']
    try:
        req = User.objects.get(username=user)
        check = VerificationToken.objects.get(token=token, pk=id, expired=False)
    except VerificationToken.DoesNotExist:
        raise Http404
    except User.DoesNotExist:
        raise Http404
    else:
        if verify == "true":
            req.is_active = True
            check.expired = True
            req.save()
            check.save()
            return render(request, 'registration/activation.html', content)
        else:
            req.delete()
            return render(request, 'registration/notice.html', content)


# Initial profile Update Views
class StepOne(View):  # Step ->1
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        content = {}
        content['server'] = env.content
        user = User.objects.get(username=request.user.username)
        if user.profile_set.exists():
            return HttpResponseRedirect(reverse('home:update_2'))
        else:
            return render(request, 'registration/step1.html', content)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        user = User.objects.get(username=request.user.username)
        if user.profile_set.exists():
            return HttpResponseRedirect(reverse('home:update_2'))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = datetime.datetime.strptime(request.POST.get('dob'), '%m/%d/%Y').strftime('%Y-%m-%d')
        status = request.POST.get('status')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        website = request.POST.get('website')
        dp = request.POST.get('dp')
        user.first_name = first_name
        user.last_name = last_name
        profile = Profile(user=user, dob=dob, status=status, gender=gender, current_location=location, website=website, dp=dp)
        user.save()
        profile.save()
        return HttpResponseRedirect(reverse('home:update_2'))


class StepTwo(View):  # Step ->2
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        user = User.objects.get(username=request.user.username)
        if not user.profile_set.exists():
            return HttpResponseRedirect(reverse('home:update_1'))
        elif user.education_set.exists():
            return HttpResponseRedirect(reverse('home:index'))
        else:
            content = {}
            content['server'] = env.content
            return render(request, 'registration/step2.html', content)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        user = User.objects.get(username=request.user.username)
        if not user.profile_set.exists():
            return HttpResponseRedirect(reverse('home:update_1'))
        ins_1 = request.POST.get('institution_1')
        grade_1 = request.POST.get('grade_1')
        content = {}
        content['server'] = env.content
        if ins_1 == "" or grade_1 == "":
            content['errors'] = "Institution is empty."
            return render(request, 'registration/step2.html', content)
        is_studying_1 = request.POST.get('is_studying_1')
        ins_2 = request.POST.get('institution_2')
        grade_2 = request.POST.get('grade_2')
        is_studying_2 = request.POST.get('is_studying_2')
        intro = request.POST.get('intro')
        if ins_1 != "" and grade_1 != "":
            one = Education()
            one.user = user
            one.institution = ins_1
            one.grade = grade_1
            if is_studying_1 == "True":
                one.is_studying = True
            one.save()
        if ins_2 != "" and grade_2 != "":
            two = Education()
            two.user = user
            two.institution = ins_2
            two.grade = grade_2
            if is_studying_2 == "True":
                two.is_studying = True
            two.save()
        if intro:
            int_1 = Profile.objects.get(user=user)
            int_1.intro = intro
            int_1.save()
        return HttpResponseRedirect(reverse('home:index'))


@login_required
def post_feed(request):
        if request.method == "POST":
            content_feed = request.POST.get('upload_feed')
            upload_image = request.POST.get('upload_pic')
            upload_video = request.POST.get('upload_video')
            upload_location = request.POST.get('upload_location')
            content = {}
            content['server'] = env.content
            if not upload_feed(request.user, content_feed, upload_image, upload_video, upload_location):
                content['form_error'] = "Failed to feed"
                return render(request, 'home/index.html', content)
            else:
                return HttpResponseRedirect(reverse('home:index'))


@login_required
def show_feeds(request):
        feeds = Feeds.objects.all().order_by('-created_at')
        for feed in feeds:
            for likes in feed.like_set.all():
                if likes.user.username == request.user.username:
                    feed.liked = True
        env.content['feeds'] = feeds
        return render(request, 'home/feeds.html', env.content)


@login_required
def like_feed(request, feed_to_like):
        try:
            feed = Feeds.objects.get(pk=feed_to_like)
        except Feeds.DoesNotExist:
            return HttpResponseRedirect(reverse('home:index'))
        else:
            try:
                likes = Like.objects.get(feed=feed, user=request.user)
            except Like.DoesNotExist:
                new_like = Like(feed=feed, user=request.user)
                new_like.save()
                return HttpResponse('liked')
            else:
                likes.delete()
                return HttpResponse('unliked')

@login_required
def comment_feed(request):
    if request.method == 'POST':
        comment = Comment()
        if request.POST.get('ping') != "":
                comment.comment = request.POST.get('ping')
                comment.feed = Feeds.objects.get(pk=request.POST.get('feed_id'))
                comment.user = request.user
                comment.save()
                return HttpResponse('success')
        else:
            return HttpResponse('failure')
    if request.method == 'GET':
        comments = {}
        comments['comments'] = Comment.objects.filter(feed=Feeds.objects.get(pk=request.GET['feed_id'])).order_by('-time')
        return render(request,'home/comment.html', comments)
