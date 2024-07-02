from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
# Characters that are not allowed in usernames
ILLEGAL_CHARS = [' ', '\\', '/', ':', ';', '*', '?',
                 '"', "'", '`', '|', '%', '/', ',']


def index(request):
    return redirect("login")

# Login the user
def login_user(request):
    if request.method == "POST":
        # Get the username & password
        username = request.POST['username']
        password = request.POST['password']

        # Check for illegal characters
        for char in ILLEGAL_CHARS:
            if char in username:
                message = f"Illegal character '{
                    char}' not allowed. Avoid these ({ILLEGAL_CHARS})"
                return render(request, "users/login.html", {"message": message})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            # Log the user
            login(request, user)
            return redirect("index")
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials, please try again!"})

    # if user logged in, don't show login page
    if request.user.is_authenticated:
        return redirect("index")

    return render(request, "users/login.html")

# Logout the user
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("index")

# Create an account for user
def signup_user(request):
    if request.method == "POST":
        # TODO create an account for user
        # Get the username, email, password and confirm password
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate the fields
        message = ""
        # Validations
        if not username:
            message = "Invalid username! try again."
        elif User.objects.filter(username=username).first():
            message = "Username already exists! try another."
        elif len(username) > 30:
            message = "Username can only contain 30 characters at most!"
        elif len(username) < 4:
            message = "Username must contain atleast 4 characters!"
        elif not email:
            message = "Invalid email! try again."
        elif User.objects.filter(email=email).first():
            message = "Email already exists! try another."
        elif password != confirm_password:
            message = "Password must be same as confirm password"
        elif len(password) < 4:
            message = "Password must have atleast 4 characters"
        elif len(password) > 30:
            message = "Password can only contain 30 characters at most!"
        else:
            # Finally check for illegal characters
            for char in ILLEGAL_CHARS:
                if char in username:
                    message = f"Illegal character '{
                        char}' not allowed. Avoid these ({ILLEGAL_CHARS})"
                    return render(request, "users/signup.html", {"message": message})

            # Everything is ok at this point, now signup
            user = User(username=username, email=email,
                        password=make_password(password))
            user.save()
            login(request, user)
            return redirect("index")

        # if anything above, goes down, this will execute...
        return render(request, "users/signup.html", {"message": message})

    # If user is already logged in, and still trying to acess this page, just redirect
    if request.user.is_authenticated:
        return redirect("index")

    # If user is not logged and not posted, render the page normally!
    return render(request, "users/signup.html")

# Change username
def change_username(request):
    # change username
    if request.method == "POST":
        username = request.POST['username']
        message = ""

        # Validate the username
        if not username:
            message = "Invalid username! try again."
        elif User.objects.filter(username=username).first():
            message = "Username already exists! try another."
        elif len(username) > 30:
            message = "Username can only contain 30 characters at most!"
        elif len(username) < 4:
            message = "Username must contain atleast 4 characters!"
        else:
            # Finally check for illegal characters
            for char in ILLEGAL_CHARS:
                if char in username:
                    message = f"Illegal character '{
                        char}' not allowed. Avoid these ({ILLEGAL_CHARS})"
                    return render(request, "notes/account.html", {"message": message})

            # Everything is ok at this point. change the username now!
            # User.objects.get(request.user)
            old_user = User.objects.get(username=request.user.username)
            old_user.username = username
            old_user.save()

            return redirect("account")

        # something went wrong! redirect to account page and pass the message
        return render(request, "notes/account.html", {"message": message})

    return redirect("account")

# Change password
def change_password(request):
    # change password
    if request.method == "POST":
        # Get the fields
        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']

        # Get the current user
        current_user = User.objects.get(username=request.user.username)

        # Validate the fields
        message = ""
        if not old_pass:
            message = "Old password field must not be empty!"
        elif not new_pass:
            message = "New password field must not be empty!"
        elif not confirm_pass:
            message = "Confirm password field must not be empty!"
        elif new_pass != confirm_pass:
            message = "New password is not the same as Confirm password!"
        elif new_pass == old_pass:
            message = "New password must not be same as Old password!"
        elif len(new_pass) > 30:
            message = "Password can only contain 30 characters at most!"
        elif len(new_pass) < 4:
            message = "Password must contain atleast 4 characters!"
        elif not check_password(old_pass, current_user.password):
            message = "Incorrect old password! try again."
        else:
            # All well, proceed
            current_user.password = make_password(new_pass)
            current_user.save()

            return redirect("account")
            # return HttpResponse(f"Password changed to {new_pass}")

        # something went wrong, re-render with error
        return render(request, "notes/account.html", {"message": message})

    return redirect("index")

# Delete account
def delete_account(request):
    # Delete the account + notes
    # POST + User must be logged in...
    if request.method == "POST" and request.user.is_authenticated:
        # Get the password
        password = request.POST['password']

        # Get user account
        user = User.objects.get(username=request.user.username)

        message = ""

        # Don't delete admin account
        if user.is_superuser:
            message = "Cannot delete admin account from here"
        elif not check_password(password, user.password):
            message = "Incorrect Password, please (don't) try again :("
        else:
            # Delete the account at this point
            user.delete()
            return redirect("index")
            # return HttpResponse("Account deleted! head to login/signup page.")

        return render(request, "notes/account.html", {
            "message": message
        })

    return redirect("index")
