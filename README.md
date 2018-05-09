# ProiectIP

<img src="https://circleci.com/gh/ericpts/ProiectIP.svg?style=shield&circle-token=:circle-token"/>

Repository for the Software Engineering university project.

## Usage

First of all, run the init script.
```bash
./init.sh
```

### Running the server
From the colorzr folder:
```bash
python3 manage.py runserver
```
This will start a development server running on address `http://127.0.0.1:8000`.


## Project structure

The main component is the `colorzr` app.

### Sub components

#### accounts  
The accounts app handles everything related to accounts, ranging from login, logout, registration, and user profiles.

It defines views and urls for these actions and provides a reusable template for thumbnail profile picture (Facebook style): `accounts/thumbnail_profile.html`.

#### images  
The images app handles images: the news feed, users' albums,uploading images and coloring them.

Furthermore, it provides an image detail view, showing comments and ratings, which are themselves extracted from the social app component.

#### social
The social app includes comments and ratings, and an external library for friendships.

Comments and ratings are all tied to a particular image, and displayed in that image's detailed view.



## References
Login Form / Page: https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/

Register Form / Page: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

Profile: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

## Members

- Eric P. Stavarache
- Lucian Bicsi
- Andrei Baltatu
- Daniel Posdarascu

