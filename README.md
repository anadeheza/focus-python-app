# Focus App
This is just a simple web app that helps users focus on their studies/work with the pomodoro method, with a cozy pixelated style.

First, you'll see a start screen where you can press Enter or just click on the screen to get to the main page

In the main page, at the center, there is a fully rounded timer, on the right top corner, the time and weather info according to your PC's location, and at the bottom corners the "Dashboard" and "Study Buddy" buttons.

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

>The assistant may take some time to answer since it is linked to a local ollama API


## Why this?
I made this principally to get t know how to make customizable backgrounds and sound effects.

Besides, this project has also helped me learn how to integrate a simple AI chatbot using python, and a basic to-do list in javascript.

## How to use?

The use is really simple. To start the timer and pause it you have the buttons below. To chat with the AI you have to press the "Study Buddy" button, type wathever you wanna ask and click send or press enter. 

Every other feautre lays behind the "Dashboard" button, just type your tasks and add them with enter, click on the "Select Theme" input box to change the background and change the ambient mixer to your liking.

## How did I make it?

I made the structure with HTML, the styling with CSS and the script with JavaScript inside the script tag in the HTML file.
<br>
I also used python for the chatbot.