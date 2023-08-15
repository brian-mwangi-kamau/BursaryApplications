This is a trial project for an online Bursary Application system for the NG-CDF

So, here is how it works:
It is an online system for the collection of bursary applications by the NG-CDF. I'm building it as a practice project with no intention to be used by the gov't for now.

So, we'll use one constituency, an imaginary one. The constituency, like others, has different locations.
A student will send an application with their name, name of school, adm no., gender, form, or year of study, location, ID number, and phone number (also, users won't need to register on the site).

The application will be received,  and we'll implement a logic that will compare the provided ID number and location to a database we'll assume has been provided by the IEBC, with the names,  ID numbers and locations they last voted from. For applications whose ID numbers and locations match those on the database,  they will be pushed and filled into Google spreadsheets automatically,  without the phone number and ID number (for privacy). 

Applications whose locations do not match, maybe because they voted from a location not in that constituency, or weren't registered as voters will be sent to a box, we can call "pending review" where the admin can review manually and maybe use the phone number to reach the applicant.

There are also those who will apply more than once.
Such applications will be rejected if the admission number and school are similar. I understand admission numbers could be similar across different schools,  especially secondary schools, which is why if they match, the next comparison will be the name of the school. 

That's it for now.