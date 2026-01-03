from django import forms
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth import login, get_user_model
User = get_user_model()




class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )

    password = forms.CharField(
        required=True,
        min_length=6,  # ✅ minimum length
        widget=forms.PasswordInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        }),
        error_messages={
            "min_length": "Password must be at least 6 characters long."
        }
    )

    confirmation_password = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )

    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )


    middle_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded",
            "rows": 2,  # <-- sets the height to roughly 2 lines
            "resize": "vertical"  # optional: allow only vertical resize
        })
    )

    occupation = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "border border-gray-200 px-2 py-2 w-full rounded"
        })
    )


    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",   # shows a date picker in modern browsers
                "class": "border rounded px-2 py-2 ",  # optional Tailwind/Bootstrap styling
            }
        )
    )



    # clean_<attribute>() methods for custom validation of specific fields
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation = cleaned_data.get("confirmation_password")

        if password and confirmation and password != confirmation:
            raise forms.ValidationError("Passwords do not match")



class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "",
            "class": "border border-gray-200 px-4 py-2 w-full rounded"
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "",
            "class": "border border-gray-200 px-4 py-2 w-full rounded"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError("Invalid username or password")

            # Store the authenticated user for the view
            self.user = user

        return cleaned_data
    


class FoodForm(forms.Form):
    description = forms.CharField(
        max_length=200, 
        required=True,
        widget=forms.TextInput(
            attrs={
            "placeholder": "",
            "class": "border border-gray-200 px-2 py-1 w-full"
            }
        )
    )

    serving_size = forms.CharField(
        max_length=200, 
        required=True,
        widget=forms.TextInput(
            attrs={
            "placeholder": "",
            "class": "border border-gray-200  px-2 py-1 w-full"
            }
        )
    )
    
    calories = forms.IntegerField(
        required=True,
        widget=forms.NumberInput    (
            attrs={
            "placeholder": "",
            "class": "border border-gray-200  px-2 py-1 w-full"
            }
        )
    )

    details = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
            "placeholder": "",
            "class": "border border-gray-200  px-2 py-1 w-full"
            }
        )
    )

    def clean_calories(self):
        calories = self.cleaned_data["calories"]
        if calories < 1:
            raise forms.ValidationError("Calories must be a positive number.")
        return calories