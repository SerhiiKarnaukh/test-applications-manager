from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from .forms import RegistrationForm, UserForm, UserProfileForm

from accounts.models import Account
from taberna_orders.models import Order, OrderProduct
from .models import UserProfile

from .utils import handle_cart_after_login, redirect_to_next_or_dashboard
from accounts.utils import send_activation_email


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Account.objects.get(email=email)
                if not hasattr(user, 'userprofile'):
                    # Create a user profile
                    UserProfile.objects.create(
                        user=user,
                    )
                messages.info(request, 'The user profile was created successfully. Please log in.')
                return redirect('login')
            except Account.DoesNotExist:

                user = Account.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=email,
                    username=email.split("@")[0],
                    password=form.cleaned_data['password']
                )
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
                # Create a user profile
                UserProfile.objects.create(
                    user=user,
                )
                # User registration activation
                send_activation_email(user, request)

                return redirect(
                    '/taberna-profiles/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'taberna_profiles/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # User authentication
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                handle_cart_after_login(request, user_profile)
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect_to_next_or_dashboard(request)
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
                return redirect('login')
            except Exception:
                messages.error(request, 'An error occurred during login.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'taberna_profiles/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Congratulations! Your account is activated. You can login to application!'
        )
        return redirect('activate_result')
    else:
        messages.error(request, 'Invalid activation link. Try again')
        return redirect('activate_result')


def activate_result(request):
    return render(request, 'taberna_profiles/activate.html')


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    orders = Order.objects.order_by('-created_at').filter(
        user=user.userprofile, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'taberna_profiles/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Create reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string(
                'taberna_profiles/reset_password_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request,
                'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'taberna_profiles/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'taberna_profiles/resetPassword.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'taberna_profiles/change_password.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user.userprofile,
                                  is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'taberna_profiles/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST,
                                       request.FILES,
                                       instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'taberna_profiles/edit_profile.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'taberna_profiles/order_detail.html', context)
