# What's the word?

What's the word? is a web application that can extract information from a WhatsApp chat:
http://fergabi17-whats-the-word.herokuapp.com/

From a text file containing a WhatsApp history, this app can extract:
- How many messages were sent
- The participants of the chat
- The number of messages each participant sent
- The length of time in months
- The most common words
- The longest word
- An analysis counting the number of characters per message to test Benford's law

This data is presented to the user in one single page in a story format.

The web app also includes a how to use page to show how to export a WhatsApp history in a text format.
With all the data collected, a page called global words is created: this page shows how many messages were checked by the app so far, the most common words of all users and also the average result for all Benford's law graphics from all users' inputs.
 
## UX

![1](resources/UX/responsive.png)


### PROJECT IDEA: WhatsApp words checker
The users of this app are WhatsApp users that also enjoy checking their personal data along balance along time. It's being common now that apps present to the users a balance of their behavior in the past week, month or even year. Music, photos, social media and even banks are presenting an analysis of the user's data in their apps. From this, the idea of creating a tool that could extract information of a personal chat was born.

### STRATEGY PLANE

Basic website objectives:
- Gather data about common words in a WhatsApp chat
- Verify Benford's law observation with a large amount of data
- Gather data about ignored words from users

User needs:
- WhatsApp users that would like to have a personal analysis of their chat
- Mathematic enthusiasts that would like to check the data collected to validate Benford's law
- WhatsApp users that would like to share an analysis of their chat

### SCOPE PLANE

Functions:
- Upload a text file from WhatsApp and get a result
- Exclude data about your chat from the results and database
- Delete completely the data from your chat
- Consult the results with a session id
- Consult the global results

Features:
- Exclude words from your result
- Edit chat participants names
- Share results

Future implementation
- Separate inputs according to language
- Add most common user's ignored words to the main functionality

### STRUCTURE PLANE

Find Here the wire frames for the information architecture:

[Wireframes](https://fergabi17.github.io/whats-the-word/resources/wireframes/wireframes.html)

### SKELETON PLANE

Website main colors:

![Colors](resources/UX/colours.png)

Website fonts:
![Do Hyeon](resources/UX/font-doHyeon.png)
![Nanum Gothic](resources/UX/font-NanumGothic.png)



### SURFACE

Find the project live on http://fergabi17-whats-the-word.herokuapp.com/

User Stories:
- A user wants to find out the most common word in a WhatsApp chat: on the main page, the user loads a text file with the WhatsApp history clicking on the "chose file" button. Next, they click on "Check this chat". This button will bring the results page for that specific chat.

- A user wants to exclude specific words from their result: on the main page, the user adds those words in the text box bellow the "chose file". Then, they can load their text file and check the results excluding the selected words.

- A user needs to consult a previous session result: from the main page, they click on "You can consult data from a previous session with your session id here". They enter the session's id and they click consult. The results will be presented if the session id was found.

- A user wants to edit chat's participants names: From the results page or from the edit results page, they click on "Update Names". A new area will be revealed, with all names in a text input format. They can edit the inputs and click on "change".

- A user wants to see the data stored from their session: at the bottom of the results page, they can click on "Restrict the use of this data"

- A user wants to exclude some data from their session: at the bottom of the results page, they can click on "Restrict the use of this data". From there, above the information they would like to exclude, they click on "remove".

- A user wants to delete their full session's data: at the bottom of the results page, they can click on "Restrict the use of this data". From there, they go to the bottom of the page and click on "Delete all my results"

- A user wants to check the global results: they can click on "global words" from any page at the navigation bar

- A user doesn't know how to extract a WhatsApp chat: they can consult the "how to use" from any page at the navigation bar


## Technologies Used

- [Html](https://html.com)
    - The project uses HTML5, standard markup language for creating Web pages.

- [CSS](https://www.css3.info)
    - The project uses CSS to style the website.

- [Javascript](https://www.javascript.com/)
    - The project uses javascript for the website functionalities

- [Charts JS](https://www.chartjs.org/)
    - Charts JS was used to present user's data and global website data

- [Python](https://www.python.org/)
    - The project uses python to process data

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    - The project uses flask for routing

- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
    - Jinja templates to render html from python

- [MongoDB](https://account.mongodb.com/)
    - Used to store the website's database

- [BOOTSTRAP](https://getbootstrap.com)
    - The project uses the grid system from BOOTSTRAP to get the website responsive.

- [Regex Tester](https://regex101.com/)
    - Consulted to test and validate regex used

- [Google fonts](https://fonts.google.com/)
    - Used as a source for all fonts
    
- [Google Chrome](https://www.schemecolor.com/)
    - To generate the green colour scheme 

- [Google Chrome](https://www.google.com/chrome/)
    - This project used google CHROME browser and its developer tools.

- [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new)
    - This project used MOZILLA FIREFOX browser.

- [Safari](https://www.apple.com/safari/)
    - This project used SAFARI browser.

- [Visual Studio Code](https://code.visualstudio.com/)
    - This project was built using Visual Studio Code IDE.

- [Git](https://git-scm.com/)
    - The project used GIT for Version Control.

- [GitHub](https://github.com/)
    - This project used GITHUB for files repository.

- [Am I Responsive](http://ami.responsivedesign.is)
    - This tool was used for testing the responsiveness of the website.

- [Html validator](https://validator.w3.org/nu/#textarea)
    - This tool was used to valide the website's HTML code.

- [Css validator](https://jigsaw.w3.org/css-validator/validator)
    - This tool was used to valide the website's CSS code.
    

## Testing

For manual tests, the following browsers were used:
- Google chrome (desktop and mobile)
- Safari (desktop and mobile)
- Mozilla Firefox

Manual tests included: 
- Functional links
- Links to other websites open on a new tab
- Editing names will edit them in all results that include names
- The total number of appearances of a word matches its frequency on the chart
- Navigating back and forth doesn't break paths
- Information easily found
- Readability

The CSS and the HTML codes were validated on jigsaw.w3.org and validator.w3.org.

## Deployment

This project is hosted on [GitHub](https://github.com/fergabi17/whats_the_word) and on [Heroku](http://fergabi17-whats-the-word.herokuapp.com/)

The git repository contains:
 - README file
 - app.py: runs the app 
 - libs.py: library to process text from WhatsApp
 - benford.py: library to process data according to Benford's law
 - Procfile and requirements.txt to deployment
 - static folder contains:
    - css: to style the website
    - js: website functionality and charts.js tool
    - images: website images
 - templates folder contains:
    - base.html: a base for all pages using jinja templates
    - all html pages, using jinja templates
 - resources folder contains:
    - UX: website's visual identity elements
    - wireframes: website's wireframes created during the structure plan
 
To deploy your own version of the web app:
- Have git installed
- Visit the [repository]([GitHub](https://github.com/fergabi17/whats_the_word))
- Open your chosen IDE (Cloud9, VS Code, etc.)
- Open a terminal in your root directory
- Type 'git clone ' followed by the code taken from github repository
    - ```git clone https://github.com/fergabi17/whats_the_word/```
- Install python requirements: pip3 install -r requirements. txt
- Create a env.py file to store variables related to the database you'll use:
"SECRET_KEY", "MONGO_DBNAME", "MONGO_URI"
- Set your flask env as development on the terminal: export FLASK_ENV=development
- Enter: python3 -m flask run
- When this completes you have your own version of the website

This website was developed in Visual Studio Code.

## Credits

### Acknowledgements

Websites consulted during the project developement. Those websites were used for reseach in the slot machine subject and functionality, as well as for coding references:
- [CSS-tricks](https://css-tricks.com/)
- [W3schools](https://www.w3schools.com/)
- [StackOverflow](https://stackoverflow.com/)
- [Oireachtas-ifd-project](https://github.com/Pattern-Projects/oireachtas-ifd-project/)
- [Regex Tester](https://regex101.com/)
- [WhatsApp](https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/?lang=en)


Thank you for mentoring and suport:
 - The Code institute
 - Antonija Simic and Dick Vlaanderen for our mentoring sections
 - Guilherme Vieira for all the patience in testing