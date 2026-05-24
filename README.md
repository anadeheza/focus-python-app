# Focus App
This is just a simple web app that helps users focus on their studies/work with the pomodoro method, with a cozy pixelated style.

You'll get asked to make an account, it is just for keeping the data (tasks, environment preferences) accurate for your next session.

After creating an account, you'll see a start screen where you can press Enter or just click on it to get to the main page

In the main page, at the center, there is a fully rounded timer, on the right top corner, the time and weather info according to your PC's location, on the lef top corner you'll see your profile picture (if you touch it you can see your settings and log out if you want), and at the bottom corners the "Dashboard" and "Study Buddy" buttons.

## Features

### Timer 
A 25-minute timer with it's respective Start/Stop and Reset buttons.

When pressing start, the timer will, well... start, and, if you chose some background music or sound, it'll start playing along with the timer.

When a session finishes, you'll get a "Time's up!" pop up msg along with a bell sound and an encouraging message from the Study Buddy.

### "Dashboard"
In the Dashboard you'll find: 

A simple To-Do list under the "Tasks" header

Background image and music configuration:
<br>
With 3 different background options, a sounds mixer, with adjustable volume for rain and coffee shop sounds and a Lo-fi music checkbox. You can fully customize this, having louder or quieter sounds, with or without background music.


### "Study Buddy "
Study Buddy is an AI Assistant that will help you with any doubt you may have and encourage you to keep your focus after a session.

## Why this?
I made this principally to get to know how to make customizable backgrounds and sound effects, then, it kind of escalated a bit and i took it as an oportunity to get familiarized with clerk (for user management), postgres (SQL database), AI integration and making a simple but functional to-do list.

## How to use?
The use is really simple. To start, pause and reset the timer, you have the buttons at the bottom of it. To chat with the AI you have to press the "Study Buddy" button, type wathever you wanna ask and click send or press enter. 

Every other feautre lays behind the "Dashboard" button, just type in your tasks and add them with enter
<br>
Click on the "Select Theme" input box to change the background video and use the ambient mixer to modify sound effects and music to your liking.

## How did I make it?
I made the structure with HTML, the styling with CSS and the scripting with JavaScript (inside the script tag in the HTML file).
<br>
I also used python for the backend (mainly APIs: AI chatbot, database, auth).

### AI Use 
I used the Gemini API for the AI chatbot "Studdy Buddy" 

I also got some help from claude for the connections of the keys from external websites, such as clerk, google (for gemini) and render, since some mixed typos and terms of use were giving me a bit of trouble (like using the right gemini version or getting clerk to work correctly for my website)