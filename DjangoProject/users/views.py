from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from .tokens import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.


def register(request):
    """
    User Sign-up view.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            mail_subject = 'Activate your account.'
            mail_body = render_to_string('users/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_to = [form.cleaned_data.get('email')]
            mail = EmailMessage(mail_subject, mail_body, to=mail_to)
            mail.send()

            return render(request, 'users/confirm_email.html')
    else:
        if request.user.is_anonymous:
            form = UserRegisterForm()
        else:
            messages.error(request, 'Log-out before creating a new account!')
            return redirect('blog-home')

    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


@login_required
def profile(request):
    """
    User profile page view.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': request.user
    }

    return render(request, 'users/profile.html', context)


def activate(request, uidb64, token):
    """
    User account activation process view.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'{user.username}, you have been registered')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid!')
        return render(request, 'users/confirm_email.html')


@login_required
def delete_user(request):
    """
    View for the user account deletion process.
    """
    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            request.user.delete()
            messages.success(
                request, 'Your account has been deleted successfully')
            return redirect('blog-home')

        else:
            return redirect('profile')

    else:
        return render(request, 'users/delete_user.html')
