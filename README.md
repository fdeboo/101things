 <div align="center">

<img src="assets/images/simon_logo.png" alt="101 things Logo"/>
 
 </div>
<br />
<div>

An app that encourages city-based adventurers around the world to share ideas on what to do in their local city. The lists of '101' things, in turn provide a rich resource for anyone less familiar with the location, to feel assured that they are not missing out on anything. View the 101 things app [here](https://github.com/fdeboo/101things)

</div>

# Table of contents
1. [UX](#introduction)
    * [Objective](#objective)
    * [User stories](#users)
    * [Wireframes](#wireframes)
    * [Design Notes](#design)
2. [Features](#features)
    * [Existing Features](#existing_feat)
    * [Features left to implment](#future_feat)
3. [Technologies Used](#technologies)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Credits](#credits)
    * [Content](#content)
    * [Media](#media)
    * [Acknowledgements](#acknowledgements)

## UX <a name="introduction"></a>

#### Objective <a name="strategy"></a>
+ The focus of this project is for users to offer suggestions that will be read by other users.
+ The app is designed for people who love to travel and explore. The colour themes will be inspired by the earth/globe.


#### User Stories <a name="users"></a>
"As a user, I would like to ___________"
+ Add my city to the app
+ Add an idea to the list
+ Search for a city in the app
+ Find all free things to do in a city
+ View all my own suggestions
+ Edit my suggestion




#### Wireframes <a name="wireframes"></a>
+ The game interface will be relative to the size of the view port. This means that whatever device the game is played on, there should be no overflowing content requiring the user to scroll. 

+ The game interface will be divided into the 4 game colours, each 50% of the viewport's width and height. 

<div align="center">

Display on large screens: <br /><br />
  <img src="wireframes/lg_screen_ui.png">

</div>


<div align="center">
Display on mobile devices: <br /><br />
  <img src="wireframes/mobile_ui.png">

</div>

+ The central circle is the focal point of the UI and will contain the game logo and the features that are vital to the game; the play button and a link to the instructions. Any other features will be accessible via a toggled navigation bar, keeping the UI minimal and uncluttered. 

<div align="center">

Content in the central circle is limited to the most important information: <br /><br />
  <img src="wireframes/centercircle.png">

</div>

+ Modals are used to display any further content and features, overlaying the game interface but crucially not navigating away from it.
+ Each modal should follow the same layout for consistency.

<div align="center">

 Illustrations that support the text are displayed on larger screens but are removed on smaller devices<br /><br />
  <img src="wireframes/modal_lg_ui.png">      <img src="wireframes/modal_sm_ui.png">

</div>


#### Design <a name="design"></a>
+ The design is intended to be minimalistic but should provide enough information to be intuitive. 
+ The colours of Simon game fill the UI so that it feels vibrant and positive.
+ The game takes precedence over everything else. The navigation bar providing any extra links will be tucked away off screen and toggled down from the top using a imple burger icon.
+ Font Awesome icons are employed as visual cues to help make the UI as intuitive as possible. It is important that these are used in moderation so that they do not become distracting. 

##### Typography
+ The fonts chosen for this project are <b>"Londrina Solid"</b> and <b>"Montserrat."</b> from google fonts
+ Londrina Solid is used for the Game Title and headings. It exudes friendly character and stability due to a combination of it's rounded corners and solid weight.
+ The Modal headings also use Londrina Solid, but using a lighter weight for better legibility.
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
    The init.py file 


#### Manual
    These were the manual tests performed and passed:



#### Known bugs


## Deployment <a name="deployment"></a>
#### Remote
The following steps were taken to deploy the project to GitHub Pages where the Simon Game is hosted:

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