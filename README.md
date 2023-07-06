# **IRAWO MEALS**
#### Video Demo:  https://youtu.be/82xGyyIVYXU
#### Description: A meal ticking web application for Irawo University Centre


## **OVERVIEW**
-------------

Irawo Meals is a web application that was built as a software solution to the
meal ticking system at Irawo University Centre.

It allows users to indicate the meals that they wish to have at the residence.
It also allows the management to view and make arrangements for the number
of people that will be around for each meal on a particular day.


## **USER CATEGORIES**
-----------------------

There are different user categories that reflect the different types of residents
at Irawo University Centre. They are:

* ### **ADMIN**

    This category of users have the ability to create new users and manage existing
    users. When the app is initialized, there is a default admin account from which
    other users can be added.

* ### **MANAGEMENT**

    This category of users have access to the meal count for each day.

* ### **PROFESSIONAL**

    This category of users has the ability to tick for packed lunch.

* ### **REGULAR**

    This category of users has the ability to tick for meals.


## **FILES**
--------------

* ### **requirements.txt**

    A list of all the requirements for the server to run the application.

* ### **LICENSE**

    Irawo Meals is under the GNU GENERAL PUBLIC LICENSE.

* ### **README.md**

    Documentation file containing all the details of the project.

* ### **run.py**

    This file starts up the Irawo Meals app in debug mode when run.

* ### **routes.py**

    Contains all the app routes for the Irawo Meals app.

* ### **createDB.txt**

    Contains all the SQLite commands to create and set up the app
    database.

* ### **helpers.py**

    Contains some helpful functions used within the webapp.

* ### **__init__.py**

    Contains the first commands that run as soon as the app is started, 
    to initialize the application.

* ### **templates**

    This is a folder containing all the templates for the webapp.

* ### **static**

    This is a folder containing all the static files for the webapp (css, 
    javascript, icons and images etc.).


## **APP ROUTES**
---------------------

* ### **login**

    Allows users to login and keeps track of their User ID and privilleges.

* ### **logout**

    Allows users to log out of the webapp, clearing the record of User ID
    and privilleges.


* ### **index**

    This route displays the meal ticking page of the app. Here, users can
    indicate the meals that they wish to have and save their choices to the
    database.

* ### **history**
    
    This route displays the meal ticking history of the logged in user between
    two dates which can be selected by the user.

* ### **account**

    This route allows the logged in user to manage his or her account. Here, the
    user can choose between two actions, either to change username or to change 
    password.

* ### **change_username**

    This route accepts a new username from the user and changes the username in
    the database. If the username is already in use, the user is prompted to pick
    another unique username.

* ### **change_password**

    This user asks user to enter the current password, a new password and a password
    confirmation. If the current password is not correct, the user is prompted to 
    enter the correct password. If the new password and the confirmation do not 
    match, the user is informed that the passwords do not match. If the current 
    password is correct and the passwords match, then the password for the user's 
    account is changed.

* ### **meal_count**

    This route gets the meal data for that day and displays it. Only users with 
    management privilleges can access this route.

* ### **general_history**

    This route allows users with management privilleges to check the meal ticking
    history of any user between two dates.

* ### **users**

    This route allows only users with admin privilleges to choose from two options, 
    either to manage users or to check user history.

* ### **manage_users**

    This route allows users with admin privilleges to manage users. Here, the admin
    user can delete any user account, reset their password or check the meal ticking
    history of the user.

* ### **user_history**

    This route can only be accessed through a POST request and carries out the action
    of displaying the meal ticking history of a particular user between two selected 
    dates.

* ### **reset_password**

    This route can only be accessed through a POST request and carries out the action
    of reseting the password of the selected user.

* ### **delete_user**

    This route can only be accessed through a POST request and carries out the action
    of deleting the account of the selected user.

* ### **add_user**

    This route allows a user with admin privilleges to add a new user. Here, the
    username and privilleges of the new user can be selected.