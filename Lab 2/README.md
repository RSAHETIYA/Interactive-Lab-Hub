# Interactive Prototyping: The Clock of Pi
**NAMES OF COLLABORATORS HERE**

Does it feel like time is moving strangely during this semester?

For our first Pi project, we will pay homage to the [timekeeping devices of old](https://en.wikipedia.org/wiki/History_of_timekeeping_devices) by making simple clocks.

It is worth spending a little time thinking about how you mark time, and what would be useful in a clock of your own design.

**Please indicate anyone you collaborated with on this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Prep

Lab Prep is extra long this week. Make sure to start this early for lab on Thursday.

1. ### Set up your Lab 2 Github

Before the start of lab Thursday, [pull changes from the Interactive Lab Hub](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md#to-pull-lab-updates) so that you have your own copy of Lab 2 on your own lab hub.


  If you are organizing your Lab Hub through folder in local machine, go to terminal, cd into your Interactive-Lab-Hub folder and run:

  ```
  Interactive-Lab-Hub $ git remote add upstream https://github.com/FAR-Lab/Interactive-Lab-Hub.git
  Interactive-Lab-Hub $ git pull upstream Fall2022
  ```
  
  The reason why we are adding a upstream with **course lab-hub** instead of yours is because the local Interactive-Lab-Hub folder is linked with your own git repo already. Try typing ``git remote -v`` and you should see there is the origin branch with your own git repo. We here add the upstream to get latest updates from the teaching team by pulling the **course lab-hub** to your local machine. After your local folder got the latest updates, push them to your remote git repo by running:
  
  ```
  Interactive-Lab-Hub $ git add .
  Interactive-Lab-Hub $ git commit -m "message"
  Interactive-Lab-Hub $ git push
  ```
  Your local and remote should now be up to date with the most recent files.


2. ### Get Kit and Inventory Parts
Prior to the lab session on Thursday, taken inventory of the kit parts that you have, and note anything that is missing:

***Update your [parts list inventory](partslist.md)***

3. ### Prepare your Pi for lab this week
[Follow these instructions](prep.md) to download and burn the image for your Raspberry Pi before lab Thursday.




## Overview
For this assignment, you are going to 

A) [Connect to your Pi](#part-a)  

B) [Try out cli_clock.py](#part-b) 

C) [Set up your RGB display](#part-c)

D) [Try out clock_display_demo](#part-d) 

E) [Modify the code to make the display your own](#part-e)

F) [Make a short video of your modified barebones PiClock](#part-f)

G) [Sketch and brainstorm further interactions and features you would like for your clock for Part 2.](#part-g)

## The Report
This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

Labs are due on Mondays. Make sure this page is linked to on your main class hub page.

## Part A. 
### Connect to your Pi
Just like you did in the lab prep, ssh on to your pi. Once you get there, create a Python environment by typing the following commands.

```
ssh pi@<your Pi's IP address>
...
pi@ixe00:~ $ virtualenv circuitpython
pi@ixe00:~ $ source circuitpython/bin/activate
(circuitpython) pi@ixe00:~ $ 

```
### Setup Personal Access Tokens on GitHub
The support for password authentication of GitHub was removed on August 13, 2021. That is, in order to link and sync your own lab-hub repo with your Pi, you will have to set up a "Personal Access Tokens" to act as the password for your GitHub account on your Pi when using git command, such as `git clone` and `git push`.

Following the steps listed [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) from GitHub to set up a token. Depends on your preference, you can set up and select the scopes, or permissions, you would like to grant the token. This token will act as your GitHub password later when you use the terminal on your Pi to sync files with your lab-hub repo.


## Part B. 
### Try out the Command Line Clock
Clone your own lab-hub repo for this assignment to your Pi and change the directory to Lab 2 folder (remember to replace the following command line with your own GitHub ID):

```
(circuitpython) pi@ixe00:~$ git clone https://github.com/<YOURGITID>/Interactive-Lab-Hub.git
(circuitpython) pi@ixe00:~$ cd Interactive-Lab-Hub/Lab\ 2/
```
Depends on the setting, you might be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you just set up as the password instead of your account one!


Install the packages from the requirements.txt and run the example script `cli_clock.py`:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ pip install -r requirements.txt
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ python cli_clock.py 
02/24/2021 11:20:49
```

The terminal should show the time, you can press `ctrl-c` to exit the script.
If you are unfamiliar with the Python code in `cli_clock.py`, have a look at [this Python refresher](https://hackernoon.com/intermediate-python-refresher-tutorial-project-ideas-and-tips-i28s320p). If you are still concerned, please reach out to the teaching staff!


## Part C. 
### Set up your RGB Display
We have asked you to equip the [Adafruit MiniPiTFT](https://www.adafruit.com/product/4393) on your Pi in the Lab 2 prep already. Here, we will introduce you to the MiniPiTFT and Python scripts on the Pi with more details.

<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="200" />

The Raspberry Pi 3 has a variety of interfacing options. When you plug the pi in the red power LED turns on. Any time the SD card is accessed the green LED flashes. It has standard USB ports and HDMI ports. Less familiar it has a set of 20x2 pin headers that allow you to connect a various peripherals.

<img src="https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png" height="400" />

To learn more about any individual pin and what it is for go to [pinout.xyz](https://pinout.xyz/pinout/3v3_power) and click on the pin. Some terms may be unfamiliar but we will go over the relevant ones as they come up.

### Hardware (you have done this in the prep)

From your kit take out the display and the [Raspberry Pi 3](https://cdn-shop.adafruit.com/970x728/3775-07.jpg)

Line up the screen and press it on the headers. The hole in the screen should match up with the hole on the raspberry pi.

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/087/539/medium640/adafruit_products_4393_quarter_ORIG_2019_10.jpg?1579991932" height="200" />
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/861/original/adafruit_products_image.png" height="200">
</p>

### Testing your Screen

The display uses a communication protocol called [SPI](https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/) to speak with the raspberry pi. We won't go in depth in this course over how SPI works. The port on the bottom of the display connects to the SDA and SCL pins used for the I2C communication protocol which we will cover later. GPIO (General Purpose Input/Output) pins 23 and 24 are connected to the two buttons on the left. GPIO 22 controls the display backlight.

We can test it by typing 
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ python screen_test.py
```

You can type the name of a color then press either of the buttons on the MiniPiTFT to see what happens on the display! You can press `ctrl-c` to exit the script. Take a look at the code with
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ cat screen_test.py
```

#### Displaying Info with Texts
You can look in `stats.py` for how to display text on the screen!

#### Displaying an image

You can look in `image.py` for an example of how to display an image on the screen. Can you make it switch to another image when you push one of the buttons?



## Part D. 
### Set up the Display Clock Demo
Work on `screen_clock.py`, try to show the time by filling in the while loop (at the bottom of the script where we noted "TODO" for you). You can use the code in `cli_clock.py` and `stats.py` to figure this out.

### How to Edit Scripts on Pi
Option 1. One of the ways for you to edit scripts on Pi through terminal is using [`nano`](https://linuxize.com/post/how-to-use-nano-text-editor/) command. You can go into the `screen_clock.py` by typing the follow command line:
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ nano screen_clock.py
```
You can make changes to the script this way, remember to save the changes by pressing `ctrl-o` and press enter again. You can press `ctrl-x` to exit the nano mode. There are more options listed down in the terminal you can use in nano.

Option 2. Another way for you to edit scripts is to use VNC on your laptop to remotely connect your Pi. Try to open the files directly like what you will do with your laptop and edit them. Since the default OS we have for you does not come up a python programmer, you will have to install one yourself otherwise you will have to edit the codes with text editor. [Thonny IDE](https://thonny.org/) is a good option for you to install, try run the following command lines in your Pi's ternimal:

  ```
  pi@ixe00:~ $ sudo apt install thonny
  pi@ixe00:~ $ sudo apt update && sudo apt upgrade -y
  ```

Now you should be able to edit python scripts with Thonny on your Pi.



## Part E.
### Modify the barebones clock to make it your own

Does time have to be linear?  How do you measure a year? [In daylights? In midnights? In cups of coffee?](https://www.youtube.com/watch?v=wsj15wPpjLY)

Can you make time interactive? You can look in `screen_test.py` for examples for how to use the buttons.

```
Three different "water" pots that fill up based on time. There will be a corresponding one for hours, min, and sec. There will also be a binary subsection of the display for fast and precise telling of time if needed. The binary will only be used to represent hours. 
```

Please sketch/diagram your clock idea. (Try using a [Verplank digram](http://www.billverplank.com/IxDSketchBook.pdf)!

![Sketch](sketch.jpeg)

**We strongly discourage and will reject the results of literal digital or analog clock display.**


\*\*\***A copy of your code should be in your Lab 2 Github repo.**\*\*\*

Entire code integration is located within screen_clock.py 
```
draw.line([(210, height-11), (230, height-11)], fill=(255, 0, 0))
draw.line([(210, height-11), (210, height-70)], fill=(255, 0, 0))
draw.line([(230, height-11), (230, height-70)], fill=(255, 0, 0))

draw.line([(130, height-11), (170, height-11)], fill=(255, 255, 0))
draw.line([(130, height-11), (130, height-80)], fill=(255, 255, 0))
draw.line([(170, height-11), (170, height-80)], fill=(255, 255, 0))

draw.line([(10, height-11), (100, height-11)], fill=(0, 255, 0))
draw.line([(10, height-11), (10, height-90)], fill=(0, 255, 0))
draw.line([(100, height-11), (100, height-90)], fill=(0, 255, 0))

now = datetime.datetime.now().time()
hour = now.hour + 10
binaryhour = bin(hour).replace("0b", "").zfill(5)

if binaryhour[4] == "1":
    draw.line([(230, 10), (225, 10)], fill=(0, 0, 255)) 
else:
    draw.line([(230, 10), (225, 10)], fill=(255, 0, 0)) 
if binaryhour[3] == "1":
    draw.line([(215, 10), (210, 10)], fill=(0, 0, 255)) 
else:
    draw.line([(215, 10), (210, 10)], fill=(255, 0, 0))
if binaryhour[2] == "1":
    draw.line([(200, 10), (195, 10)], fill=(0, 0, 255))
else:
      draw.line([(200, 10), (195, 10)], fill=(255, 0, 0))
if binaryhour[1] == "1":
    draw.line([(185, 10), (180, 10)], fill=(0, 0, 255)) 
else:
    draw.line([(185, 10), (180, 10)], fill=(255, 0, 0)) 
if binaryhour[0] == "1":
    draw.line([(170, 10), (165, 10)], fill=(0, 0, 255)) 
else:
    draw.line([(170, 10), (165, 10)], fill=(255, 0, 0)) 

for i in range(hour * 3):
    draw.line([(11, height-12-i), (99, height-12-i)], fill=(0, 0, 255))

for i in range(now.minute):
    draw.line([(131, height-12-i), (169, height-12-i)], fill=(0, 0, 255))

for i in range(now.second):
    draw.line([(211, height-12-i), (229, height-12-i)], fill=(0, 0, 255))
```

After you edit and work on the scripts for Lab 2, the files should be upload back to your own GitHub repo! You can push to your personal github repo by adding the files here, commiting and pushing.

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git add .
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git commit -m 'your commit message here'
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git push
```

After that, Git will ask you to login to your GitHub account to push the updates online, you will be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you set up in Part A as the password instead of your account one! Go on your GitHub repo with your laptop, you should be able to see the updated files from your Pi!


## Part F. 
## Make a short video of your modified barebones PiClock

\*\*\***Take a video of your PiClock.**\*\*\*

[Link to Video](https://youtube.com/shorts/5KK4k9H3ito?feature=share)

## Part G. 
## Sketch and brainstorm further interactions and features you would like for your clock for Part 2.

```
- Add an animation for water overflow to go to next larger pot.
- Create interactive portions of the clock with the buttons and have button press trigger pouring of small pot into larger pot.
- Use binary representations of minutes and second as well ... although would be very close to a normal clock at that point.
- Add in aesthetics: maybe a plant grows throughout the day as water is added.
```

![Sketch](sketchG.jpeg)

# Prep for Part 2

1. Pick up remaining parts for kit on Thursday lab class. Check the updated [parts list inventory](partslist.md) and let the TA know if there is any part missing.
  

2. Look at and give feedback on the Part G. for at least 2 other people in the class (and get 2 people to comment on your Part G!)

# Lab 2 Part 2

## Idea

The main goal for this part will be to make the clock more interactive with the user. This will be accomplished with a visual timer that provides helpful cues to the user based on what they want to accomplish. 
Parts used in this lab were
- Raspberry Pi
- Mini PiTFT Display
- Green Button LED
- Rotary Encoder
- Electrocapacitive Touch Sensor
- Very cool and technologically advanced sound making plushie dinosaur 

## Sketches/Storyboards

### Sketches

![Sketch](Part2Sketch1.jpeg)
![Sketch](Part2Sketch2.jpeg)

1) General display view of timer/clock

2) Turn of rotary encoder to increase visual when setting timer

3) Rotary encoder button press sequence when in timer mode

4) Turn off alarm through electrocapacitive sensor

5) General device sketch of entire system put together

### Storyboard

![Sketch](Part2Storyboard.jpeg)

1) Viewing the time when passing by through water bucket visualizations

2) Using the clock device as a helpful, non-instrusive aid when studying

3) Interacting with timer set buttons/encoders to create a timer

4) Using the device as an alarm on the bedside table after setting timer

5) Turning off alarm (after waking up from 4 hours of sleep lol) through electrocapacitive touch "button"

## Code

**Entire code integration is located within screen_clock.py*

Draws the empty bins/buckets
```
def draw_bins():
    draw.line([(210, height-11), (230, height-11)], fill=(255, 0, 0))
    draw.line([(210, height-11), (210, height-70)], fill=(255, 0, 0))
    draw.line([(230, height-11), (230, height-70)], fill=(255, 0, 0))

    draw.line([(130, height-11), (170, height-11)], fill=(255, 255, 0))
    draw.line([(130, height-11), (130, height-80)], fill=(255, 255, 0))
    draw.line([(170, height-11), (170, height-80)], fill=(255, 255, 0))

    draw.line([(10, height-11), (100, height-11)], fill=(0, 255, 0))
    draw.line([(10, height-11), (10, height-90)], fill=(0, 255, 0))
    draw.line([(100, height-11), (100, height-90)], fill=(0, 255, 0))
```

Controls display when clock mode is "on"
```
def clock_display():

    draw_bins()

    draw.text((5, 5), "Clock :D", font=font, fill=(255, 255, 255))

    now = datetime.datetime.now().time()
    hour = now.hour
    binaryhour = bin(hour).replace("0b", "").zfill(5)

    if binaryhour[4] == "1":
        draw.line([(230, 10), (225, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(230, 10), (225, 10)], fill=(255, 0, 0)) 
    if binaryhour[3] == "1":
        draw.line([(215, 10), (210, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(215, 10), (210, 10)], fill=(255, 0, 0))
    if binaryhour[2] == "1":
        draw.line([(200, 10), (195, 10)], fill=(0, 0, 255))
    else:
         draw.line([(200, 10), (195, 10)], fill=(255, 0, 0))
    if binaryhour[1] == "1":
        draw.line([(185, 10), (180, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(185, 10), (180, 10)], fill=(255, 0, 0)) 
    if binaryhour[0] == "1":
        draw.line([(170, 10), (165, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(170, 10), (165, 10)], fill=(255, 0, 0)) 

    for i in range(hour * 3):
        draw.line([(11, height-12-i), (99, height-12-i)], fill=(0, 0, 255))

    for i in range(now.minute):
        draw.line([(131, height-12-i), (169, height-12-i)], fill=(0, 0, 255))
    
    for i in range(now.second):
        draw.line([(211, height-12-i), (229, height-12-i)], fill=(0, 0, 255))
```

Manages different states within the timer mode
```
def timer_display():
    draw_bins()

    #draw.text((5, 5), "Timer :D", font=font, fill=(255, 255, 255))
    global timer_set
    global current_timer_denom
    global current_timer
    global button_held
    global hour_timer
    global minute_timer
    global second_timer
    global start_time
    global primary_mode

    if not rotary_button.value and not button_held:
        button_held = True

    draw_timer()

    if (timer_set):
        draw.text((5, 5), "Timer Started :D", font=font, fill=(255, 255, 255))
        if calculate_time_left().days < 0:
            primary_mode = 2
        
    else:
        draw.text((5, 5), "Timer :D", font=font, fill=(255, 255, 255))
        if (current_timer_denom == "hours"):
            hour_timer = abs(-encoder.position) % 24
            if rotary_button.value and button_held:
                button_held = False
                current_timer_denom = "minutes"
        elif (current_timer_denom == "minutes"):
            minute_timer = abs(-encoder.position) % 60
            if rotary_button.value and button_held:
                button_held = False
                current_timer_denom = "seconds"
        else:
            second_timer = abs(-encoder.position) % 60
            green_button.LED_on(100)
            if rotary_button.value and button_held:
                button_held = False
                current_timer_denom = "hours"
                green_button.LED_off()
            if (green_button.is_button_pressed()):
                current_timer = 3600 * hour_timer + 60 * minute_timer + second_timer
                green_button.LED_off()
                current_timer_denom = "hours"
                timer_set = True
                start_time = datetime.datetime.now()
```

Calculates time left for timer
```
def calculate_time_left():
    global start_time
    global hour_timer
    global minute_timer
    global second_timer

    now = datetime.datetime.now()
    time_elapsed = now - start_time
    time_elapsed = datetime.timedelta(seconds=current_timer) - time_elapsed
    seconds = time_elapsed.total_seconds()
    hour_timer_div = divmod(seconds, 3600)     
    hour_timer = int(hour_timer_div[0])   
    minute_timer_div = divmod(hour_timer_div[1], 60)  
    minute_timer = int(minute_timer_div[0])          
    second_timer_div = divmod(minute_timer_div[1], 1) 
    second_timer = int(second_timer_div[0])
    
    return time_elapsed
```

Draws timer buckets in accordance to time left
```
def draw_timer():

    global hour_timer
    global minute_timer
    global second_timer

    for i in range(hour_timer * 3):
                draw.line([(11, height-12-i), (99, height-12-i)], fill=(0, 0, 255))
    for i in range(minute_timer):
        draw.line([(131, height-12-i), (169, height-12-i)], fill=(0, 0, 255))
    
    for i in range(second_timer):
        draw.line([(211, height-12-i), (229, height-12-i)], fill=(0, 0, 255))
```

Tracks end of timer state and "listens" for touch input before resetting

```
if (primary_mode == 2):
        draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
        draw.text((120, 65), "BEEP!!!", font=font, fill=(255, 255, 255))
        if (mpr121[0].value):
            current_timer = 0
            timer_set = False
            current_timer_denom = "hours"
            primary_mode = 0
```


## Video

SOUND WARNING when you see the dinosaur!!! 

[Link to Video](https://youtu.be/aQ3BOyx5Lls)


