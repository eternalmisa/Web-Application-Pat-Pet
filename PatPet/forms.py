from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from localflavor.us.forms import USPhoneNumberField
from localflavor.us.forms import USZipCodeField
from haystack.forms import SearchForm

GENDER_CHOICE = (('male', 'Male'), ('female', 'Female'), ('other', 'Other'),)

### Person ###
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, label='Username', widget=forms.TextInput(
        attrs={'placeholder': 'Enter your username.', 'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your password.', 'class': 'form-control'}))


class SignUpForm1(forms.Form):
    username = forms.CharField(max_length=30, label='User Name',
                               widget=forms.TextInput(attrs={'placeholder': 'Username.', 'class': 'form-control'}),
                               error_messages={'required': 'Username is required.'})
    firstname = forms.CharField(max_length=30, label='First Name',
                                widget=forms.TextInput(attrs={'placeholder': 'First name.', 'class': 'form-control'}))
    lastname = forms.CharField(max_length=30, label='Last Name',
                               widget=forms.TextInput(attrs={'placeholder': 'Last name.', 'class': 'form-control'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Email address.', 'class': 'form-control'}),
                             error_messages={'required': 'Email is required.'})
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password.', 'class': 'form-control'}),
                                error_messages={'required': 'Password is required.'})
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password.', 'class': 'form-control'}),
                                error_messages={'required': 'Confirm password is required.'})
    avatar = forms.ImageField(label='avatar',
                              error_messages={'required': 'Avatar is required.', 'invalid': 'The avatar is invalid.'},
                              widget=forms.ClearableFileInput(attrs={'id': "wizard-picture"}), required=False)

    def clean(self):
        cleaned_data = super(SignUpForm1, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("The email has already been registered.")
        return email


class SignUpForm2(forms.Form):
    address = forms.CharField(max_length=50, label='Address',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'street_address'}),
                                  error_messages={'required': 'address is required.'})
    city = forms.CharField(max_length=50, label='City',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'locality'}),
                               error_messages={'required': 'city is required.'})
    state = forms.CharField(max_length=50, label='State', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'administrative_area_level_1'}),
                                error_messages={'required': 'state is required.'})
    zipcode = USZipCodeField(label='Zip Code',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'postal_code'}),
                                 error_messages={'required': 'zipcode is required.'})


class EditPersonInfoForm(forms.Form):
    avatar = forms.ImageField(label='avatar',
                              widget=forms.ClearableFileInput(attrs={'id': "wizard-picture", 'id': 'profile-picture'}),
                              required=False)
    phoneNum = USPhoneNumberField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    gender = forms.CharField(max_length=10, label='Gender',
                             widget=forms.TextInput(attrs={'label': 'Gender', 'class': 'form-control'}), required=False)
    birthday = forms.CharField(max_length=30, label='Birthday',
                               widget=forms.TextInput(attrs={'label': 'Birthday', 'class': 'form-control'}),
                               required=False)
    person_bio = forms.CharField(max_length=100, label='Bio',
                                 widget=forms.Textarea(attrs={'label': 'Biography', 'class': 'form-control'}),
                                 required=False)
    address = forms.CharField(max_length=50, label='Address',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'street_address'}),
                                  error_messages={'required': 'address is required.'})
    city = forms.CharField(max_length=50, label='City',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'locality'}),
                               error_messages={'required': 'city is required.'})
    state = forms.CharField(max_length=50, label='State', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'administrative_area_level_1'}),
                                error_messages={'required': 'state is required.'})
    zipcode = USZipCodeField(label='Zip Code',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'postal_code'}),
                                 error_messages={'required': 'zipcode is required.'})


class EditUserForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=False)
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

### Upload Multiple File ###
class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def __init__(self, *args, **kwargs):
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

### Others ###
class EnteremailForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': 'Email address.', 'pic': 'glyphicon glyphicon-envelope', 'class': 'form-control'}),
                             error_messages={'required': 'Email is required.'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email):
            raise forms.ValidationError("The email address doesn't exist")
        return email


### Search ###
class DateRangeSearchForm(SearchForm):
    q = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'tabindex': '1', 'autocomplete': 'off', 'class': 'form-control search_input_breed',
               'placeholder': "What kind of Pet do you like?"}))
    location = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'tabindex': '2', 'class': 'form-control', 'id': 'location-input', 'placeholder': 'City, State'}))

    def clean_location(self):
        location = self.cleaned_data.get('location')
        loc_split = location.split(",")
        if len(loc_split) != 3:
            raise forms.ValidationError("Wrong location format")
        else:
            return location


    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        location = self.cleaned_data['location']
        if location:
            city = location.split(',')[0].split()
            sqs = sqs.filter(pet_city=city)
        '''
        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(start_date__gte=self.cleaned_data['start_date']-datetime.timedelta(days=2),
                             start_date__lte=self.cleaned_data['start_date']+datetime.timedelta(days=2))
        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

        # Check to see if a num of days was chosen.
        if self.cleaned_data['num_of_days']:
            days = self.cleaned_data['num_of_days']
            sqs = sqs.filter(num_of_days__gte=days - days / 3, num_of_days__lte=days + days / 3)
        '''
        '''
        for sq in sqs:
            # find the owner
            sq.object.owner_image_url = "/static/PatPet/images/man.png"
            sq.object.owner_url = "hahah"
        '''
        return sqs


### Transaction ###
class ReviewForm(forms.Form):
    reviewText = forms.CharField(max_length=100, label='reviewText', widget=forms.Textarea(
        attrs={'label': 'reviewText', 'class': 'profile-input form-control'}))


class MomentPhotoForm(forms.Form):
    photos = MultiFileField()


class MomentVideoForm(forms.Form):
    videos = MultiFileField()

### Pet ###
class PetBasicForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
                           error_messages={'required': 'name is required.'})
    age = forms.IntegerField(label="Age", widget=forms.NumberInput(attrs={'placeholder': 'Age', 'class': 'form-control'}),
                             error_messages={'required': 'age is required.'})
    gender = forms.CharField(label="Gender",
                             widget=forms.TextInput(attrs={'placeholder': 'Gender', 'class': 'form-control'}),
                             error_messages={'required': 'gender is required.'})
    breed = forms.CharField(label="Breed",
                            widget=forms.TextInput(attrs={'placeholder': 'Breed', 'class': 'form-control'}),
                            error_messages={'required': 'breed is required.'})
    color = forms.CharField(label="Color",
                            widget=forms.TextInput(attrs={'placeholder': 'Color', 'class': 'form-control'}),
                            error_messages={'required': 'color is required.'})
    pet_avatar = forms.ImageField(label='Avatar', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                                  required=False)
    pet_bio = forms.CharField(max_length=100, label='Biography', widget=forms.Textarea(attrs={'class': 'form-control'}),
                              error_messages={'required': 'bio is required.'})


class PetLocationForm(forms.Form):
    pet_address = forms.CharField(max_length=50, label='Address',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'street_address'}),
                                  error_messages={'required': 'address is required.'})
    pet_city = forms.CharField(max_length=50, label='City',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'locality'}),
                               error_messages={'required': 'city is required.'})
    pet_state = forms.CharField(max_length=50, label='State', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'administrative_area_level_1'}),
                                error_messages={'required': 'state is required.'})
    pet_zipcode = USZipCodeField(label='Zip Code',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'postal_code'}),
                                 error_messages={'required': 'zipcode is required.'})


class PetMediaForm(forms.Form):
    pet_photo = MultiFileField(required=False)
    pet_video = MultiFileField(required=False)