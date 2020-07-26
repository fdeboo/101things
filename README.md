 <div align="center">

<img src="wireframes/mockup.png" alt="Mockup on all Devices"/>
 
 </div>

# Table of contents
1. [Introduction](#introduction)
    * [Objective](#objective)
    * [User stories](#users)
    * [Wireframes](#wireframes)
    * [Design Notes](#design)
2. [UX](#design)
3. [Features](#features)
    * [Existing Features](#existing_feat)
    * [Features left to implment](#future_feat)
4. [Technologies Used](#technologies)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Credits](#credits)
    * [Content](#content)
    * [Media](#media)
    * [Acknowledgements](#acknowledgements)

## Introduction <a name="introduction"></a>

#### Objective <a name="strategy"></a>
+ The focus of this project is to create a platform for adventurers to share their good experiences of their local area with other travellers in the community who would benefit from the local knowledge and advice. 
+ The app is designed for people who love to travel and explore. The colour themes will be inspired by the earth/globe.

Visit 101 Things [here](https://cityexplorer-ms.herokuapp.com/) 


#### User Stories <a name="users"></a>
"As a user, I would like to ___________"
+ Add my location to the app
+ Add suggestions to the list
+ Search for a city in the app
+ Browse suggestions by all users for a location
+ Find all free things to do in a city
+ View all my own suggestions
+ Edit my suggestion
+ Find all suggestions that are Museums


#### Wireframes <a name="wireframes"></a>
+ The header contains a hero image background and the navigation bar has a transparent background so that the header image is visible beneath.
+ The header will contain the search bar so it accessible on whichever page the user has navigated to
+ The content section is where the page templates are displayed. All templates will have a top margin of 50px to space it from the header.
+ The locations added to the database appear as cards on the home page and will also contain image backgrounds to add colour to the page
+ A reel of suggestions and the username of the author is displayed on the home screen to give the user an idea of the kind of suggestions


<div align="center">

Display on large screens: <br /><br />
  <img src="wireframes/lg_screen_ui.png">

</div>


<div align="center">
Display on mobile devices: <br /><br />
  <img src="wireframes/mobile_ui.png">

</div>

+ The footer has a 'sticky' position so that even if the content does not fill the viewport height, the footer will remain anchored at the bottom of the screen.

<div align="center">

Content in the central circle is limited to the most important information: <br /><br />
  <img src="wireframes/centercircle.png">

</div>

+ Modals are used for the
+ Each modal should follow the same layout for consistency.




#### Design <a name="design"></a>
+ The design is intended to feel modern but warm and traditional. It uses earth tones. 
+ The colour pallette used in the app in  fill the UI so that it feels vibrant and positive.
+ The game takes precedence over everything else. The navigation bar providing any extra links will be tucked away off screen and toggled down from the top using a imple burger icon.
+ Font Awesome icons are employed as visual cues to help make the UI as intuitive as possible. It is important that these are used in moderation so that they do not become distracting. 

##### Typography
+ The fonts chosen for this project are <b>"Patua One,"</b> <b>"Lato"</b> and <b>"EB Garamond."</b> from google fonts
+ Patua One is used for the logo and top level headings and for the location card. It's serifs are traditional
+ Any quoted data such as the searched input or suggestions , but using a lighter weight for better legibility.
+ All headings and titles are written in lowercase to compliment the informality of the site.
+ Montserrat was chosen for all paragraph text and navigational links where legibility was most important. The font pairs well with Londrina Solid because it is neutral, has a clean rounded form and is light in weight.


## Features <a name="features"></a>
#### Existing Features <a name="existing_feat"></a>
+ User Login
    + Every time the user repeats back the complete sequence correctly, 5 points is added to their running score. The points total is updated on the UI so that the user is aware of their progress.
+ Accout Page and Update Details
    + The modal is accessed via a link, which is primely positioned just beneath the play button for visibility. It provides 2-step instructions for any users who are new to the game.  
+ Add Location 
    + This modal allows the user to choose alternative game sounds from a drop down menu. 
    + The settings are implemented straight away after clicking 'OK' 
    + The user may also choose the starting level for the game from this panel.
+ Add a Suggestion
    + Presents...
+ Edit Suggestion
    + An option...
+ Search for a location
    + Enables...
+ Filter List items
    + Launched...
+ Level up
    + The duration of each colour flash is decreassed once the user reaches a target score. This triggers an animation on screen that lets the user that they have reached a new level. As a result, the speed of the game increases which makes the game more challenging.

#### Features Left to Implement <a name="future_feat"></a>
+ The opportunity for a user to create a username against which their highscores can be saved
+ High scores are available for all global users of the game, making the game more competitive

## Technologies Used <a name="technologies"></a>
#### Frontend:
+ HTML, CSS, Javascript
    + Frontend programming languages
+ [JQuery](https://jquery.com/)
    + Simplifies access and manipluation of the DOM
+ [Bootstrap](https://getbootstrap.com/)
    + Provides the visual formatting of the website and it's responsiveness accross all devices
+ [Cloudinary](https://cloudinary.com/)
    + Manages and delivers the images, optimized for every device and channel.
+ [Google Fonts](https://fonts.google.com/)
    + Provides access to the web fonts used in this project
+ [Font Awesome](https://fontawesome.com/)
    + Provides the icons used in this project to guide the users' navigation.

#### Backend:
+ [MongoDB](https://www.mongodb.com/)
    + Provides the NoSQL database

#### Other:
+ [Visual Studio Code](https://code.visualstudio.com/)
    + The IDE that facilitated the devlopment of this project.
+ [GitHub](https://github.com/)
    + The platform where the project code is stored remotely
+ [Heroku](https://heroku.com/)
    + For deployment of the app
+ Adobe Illustrator
    + Facilitated the creation of images used in this project 


## Testing <a name="testing"></a>
#### Validators

The following services were used to check the web code:

+ HTML
    + [W3C Markup Validation](https://validator.w3.org/)
+ CSS
    + [CSS Lint](http://csslint.net/)
+ Javascript
    + [Javascript Lint](https://jshint.com/)
+ Python
    + [Pylint]()  
    In the \_\_init__.py file,  the following line of code is placed at the bottom of the file and therefore flags as an error:  <pre><code>from cityexplorer import routes</code></pre>
    This deliberate action was taken because the line is not necessary to the views in \_\_init__.py and is just to ensure that module is imported. The routes.py file depends on \_\_init__.py and so it is a circular import.


#### Manual
These were the manual tests performed and passed:



#### Known bugs


## Deployment <a name="deployment"></a>
#### Remote
The following steps were taken to deploy the project to Heroku where <b>101 things</b> is hosted:

1. From within Github, navigate to fdeboo/simon
2. Select the Settings tab from the menu, found beneath the repository name 
3. Scroll down to the GitHib Pages section.
4. Under 'Source', choose 'Master Branch' from the dropdown menu
5. The page will automatically refresh and the site is deployed
6. A link to the live site is provided


#### Local
1. To run this project locally, navigate to the repository on github [here](https://github.com/fdeboo/101things)
2. Click on the green "Clone or Download" button
3. Copy the URL from the dropdown
4. In your local IDE, open the terminal ensure the current working directory is set to where you want the clone to be created
5. Type <code>git clone</code> and then paste the copied link: <pre><code>git clone https://github.com/fdeboo/101things</code></pre>
6. Press enter. This completes the deployment.


## Credits <a name="credits"></a>

#### Content <a name="content"></a>
All paragraph text and content was written by me.

#### Media <a name="media"></a> 
##### Images
+ The...


#### Code <a name="code"></a> 
+ My understanding of... [Pretty Printed ]() 
+ My understanding of... was explained to me at []() 
+ The code used to... was sourced from this... [Stack Overflow]() post.
+ The code...
+ [W3Schools](w3schools.com) was 

#### Acknowledgements <a name="acknowledgements"></a>
Special thanks to, 
+ Mentor Aaron Sinott, for the sessions that ran into overtime 
+ [GBrachetta](https://github.com/GBrachetta) 