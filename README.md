This is an online Bursary Application system for the NG-CDF

**PROJECT OVERVIEW**

First, Users(who in this case are students of both unviversities and secondary schools) won't need to register for accounts to use the platform.

An applicant will fill in these details in the application form:
                  Their name,
                  The name of their school,
                  Year of study
                  Admission number
                  The constituency they call home
                  The location they live/voted from
                  Their parent/guardian's phone and national ID number

Below is a graphical template of the form:


The application will be submitted, received on the backend, and saved in a database with all the information.

The database will then be queried against another one, which I assume has been provided by the IEBC (the body responsible for elections and registration of voters in Kenya).
The 'IEBC' database contains names, ID numbers, constituencies, and locations of voters.

If the location and constituency provided in the application match with what is on the 'IEBC' database, that means that that particular form has been submitted by an applicant who last voted in that constituency for where they are applying a bursary.
For such a case, the applicant's details will be automatically filled into a Google Spreadsheet which the admin/secretary of that particular NG-CDF will have set up and can access and download.

On the contrary, applications whose details do not match those on the 'IEBC', either because they are registered as voters from other areas, or were not registered as voters in the last elections will be sent to an email address with all the details in the form. Then, the secretary, who we are calling the admin can then call the applicant using the phone number they provided and confirm that the applicant is from that particular constituency and area.


Note that if this was to be used by the NG-CDF, it would need a clone and a change of details like the constituency and locations for all the 290 constituencies in the country.

**In any case you should wish to clone this repo:**

I have made every single line of code understandable with tones of comments.

Second, here is what you need to configure in your environment:
1: I'll add the requirements.txt file later on.
2: You need to have a default database where the applications will be saved, (even before the queries are performed - this is important for future reference).
3: You'll also need an external database, already containing data "from the IEBC"
4: You'll have the external_database set up like this:
![db](https://github.com/brian-mwangi-kamau/BursaryApplications/assets/127291274/4e08333f-c47e-4a7b-9a70-b5027b655f7a)


That said, you'll also need to set up two emails, one will be the email used to send the invalid applications to the admin, whereas the second one is as you guessed. That'll be the recipient email ("admin's email"). ~ Refer to the .env file for clarity

The other step is to sign up for a Google Console account, refer to this tutorial below:
https://www.youtube.com/watch?v=aruInGd-m40

After downloading your JSON file containing the credentials, you can then refer to then configure it to the "save_to_googlespreadsheets" function.

Run the program and fix any minor errors you may experience - blame yourself for that.😎

And yes! That's all!

**Lastly**

As always, all the APIs on my Github profile are free to use by anyone, especially front-end developers.
*Do not take credits for the backend logic*
