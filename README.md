# Bursary Application collection System
I built a bursary applications collection system for the NG-CDF (Kenya).

# Project Overview
In consideration of non-developers, I wrote a more friendlier and detailed documentation on Hashnode. Check it out [here](https://brayo.hashnode.dev/a-bursary-applications-collection-system)

# - For Developers
This system is written in Django with Python.

I started by defining the model for a user, who in this case will be the system administrator.
```python
class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set', 
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)
```

I then defined a model for the applications:
```python
class Application(models.Model):
    student_name = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=20)
    year_of_study = models.CharField(max_length=50)
    constituency = models.CharField(max_length=15)
    location = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=8)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name
```

After this, followed the logic to collect the applications from our users.
I created a `forms.py` file and created a form `ApplicationForm`:
```python
from django import forms
from .models import Application


class ApplicationForm(forms.Form):
    student_name = forms.CharField(max_length=255, label="Name of Student")
    school_name = forms.CharField(max_length=255, label="Name of School")
    admission_number = forms.CharField(max_length=30, label="Admission Number")
    year_of_study = forms.CharField(max_length=50, label="Form or Year of Study")
    constituency = forms.CharField(max_length=15)
    location = forms.CharField(max_length=15)
    phone_number = forms.CharField(max_length=10)
    id_number = forms.CharField(max_length=8)

    class Meta:
        model = Application
        fields = '__all__'
```

In the `views.py` file, I began with defining the logic to collect the forms and save them in a database, before proceeding to the next steps:
```python
def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            application = Application(
                student_name=form_data['student_name'],
                school_name=form_data['school_name'],
                admission_number=form_data['admission_number'],
                year_of_study=form_data['year_of_study'],
                constituency=form_data['constituency'],
                location=form_data['location'],
                phone_number=form_data['phone_number'],
                id_number=form_data['id_number']
            )
            application.save()
```

I then defined a function to get the voter info from a database provided by the IEBC.
This info includes: The national identification number of voters, their constituencies and location.

I named the function `get_voter_info`:
```python
def get_voter_info(id_number):
    with connections['external_database'].cursor() as cursor:
        cursor.execute("SELECT constituency, location FROM voter WHERE id_number = %s", [id_number])
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None, None
```
The reference `external_database` is the name of my database. It could also have other names like "IEBC_db" to make it easy for other developers.

I then referenced the function in my view and added a logic to query the `external_database` with data in the application.
A snippet:
```python
 voter_constituency, voter_location = get_voter_info(form_data['id_number'])

            # The function below calls the "save_to_googlesheets" function below there.
            if (voter_constituency == form_data['constituency'] and
                voter_location == form_data['location']):
                # Valid voter details, save to Google Sheets
                # We won't save the phone number and ID number to the spreadsheets for security reasons
                save_to_googlesheets({
                    'student_name': form_data['student_name'],
                    'school_name': form_data['school_name'],
                    'admission_number': form_data['admission_number'],
                    'year_of_study': form_data['year_of_study'],
                    'constituency': form_data['constituency'],
                    'location': form_data['location']
                })
                return render(request, 'success.html') # This template is shown when the application has been saved to the spreadsheet(s) only!
            else:
                # Invalid voter details, send email
                send_email(form_data)
                return render(request, 'failure.html') # This template is shown when the application has been sent to the email for manual review
```

The `save_to_googlesheets` function being called in the view above saves the application data to a spreadsheet automatically. Before I share the snippet for that function, I'll explain vaguely the view above. 
In the logic for the `application_form` view, the  system checks whether the owner of the provided ID number(in the application) was last registered as a voter from the constituency they provided. If the data matches the one in the IEBC database, the function `save_to_googlesheets`. This function's code snippet is here:
```python
def save_to_googlesheets(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('#replace with the email provided in the JSON file', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('Application Sheets') # The name of the sheets right there.

    worksheet = spreadsheet.get_worksheet(0)
# The only data going into the spreadsheet(s)
    worksheet.append_row([
        data['student_name'],
        data['school_name'],
        data['admission_number'],
        data['year_of_study'],
        data['constituency'],
        data['location']
    ])
```
The view above saves specific data to the spreadsheet shared by the administrator and bears the name in the `spreadsheet = client.open('Application Sheets')`. By sharing a spreadsheet, what I mean is; the administrator will log into their Google account, create a spreadsheet online, and share it with an email address found in a file that will be downloaded from the Google Console. I'll share about this below. The name they will give to the sheet will then be added in the line I quoted above.

Back to the `application_form` view. We have another option to send the application data to an email address, if the data in the application will be found to not be matching with the related data in the IEBC database. This could be because either the voter linked to the ID number last voted from a different constituency other than the one they provided or the provided ID number was never registered as a voter in the last elections. The email account which will be used should be accessible by the bursary administrator. This will help them review the application manually, by contacting the applicant through the phone number they will have provided.

In the view, we called a function `send_email`. This function handles the application sending to the administrator's email account.
Here:
```python
def send_email(form_data):
    subject = 'New Application Review'
    message = f"Application details:\n\n" \
              f"Name: {form_data['student_name']}\n" \
              f"School: {form_data['school_name']}\n" \
              f"Admission Number: {form_data['admission_number']}\n" \
              f"Year of Study: {form_data['year_of_study']}\n" \
              f"Constituency: {form_data['constituency']}\n" \
              f"Location: {form_data['location']}\n" \
              f"Phone Number: {form_data['phone_number']}\n" \
              f"ID Number: {form_data['id_number']}\n"
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ['EMAIL_HOST_USER']
    smtp_password = os.environ['EMAIL_HOST_PASSWORD']
    recipient_email = os.environ['RECIPIENT_EMAIL']

    from_email = smtp_username
    to_email = recipient_email

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))


    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
```
The code in the view above isn't complex as much. I won't go deep into it.

Earlier, I mentioned a file that would/should be downloaded from the Google Console.
This is a JSON file containing API keys that should be generated when developing this system.
I have a step-by-step tutorial on how to go about this published on Hashnode. You can refer to it [here](https://brayo.hashnode.dev/google-spreadsheets-integration-in-python-part-one)

The rest is basic development, like running app migrations and defining url routes.

# conclusion
I hope you learnt something buddy.
Go forth and build software that'll solve problems!

# Disclaimer
This project is not an open source project, and nor is it open for recreation.
Do not clone this project to your local environment, and do not recreate it and ditribute it.
