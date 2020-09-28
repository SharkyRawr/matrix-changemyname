[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W52AOXC)

# Matrix ChangeMyName

![Screenshot-20200929001406-859x600](https://user-images.githubusercontent.com/246984/94491566-c4291800-01e8-11eb-85d5-c5a4fb983e2a.png)


A tool to quickly change your display-name and avatar for any sub-selection of rooms.

## Requirements

- PyQt5
- requests

To create distribution builds you also need `PyInstaller`.

## Running

Basically just create a virtualenv (or not, I too like to live dangerously) and install the requirements with pip:

```
pip install -r requirements.txt
```

If everything is successful, start the tool with:

```
python pymain.py
```

You should see a not-so-pretty (be gentle) but functional UI.

## How to use

First of, click the login button in the upper left. Enter your homeserver, user-id and accesstoken.  
You can find your access token in Element by going into settings, "*Help & About*", scroll down, click "*click here to reveal*". KEEP IT SAFE.  
This tool offers to save the details as a convenience in plain text. There is no encryption involved. I might work on that some day but not today.

# Keep your settings.json and access token safe! Never share them with anyone!

Next, on the right side, select the rooms you wish to set the new display-name and/or avatar on.

Beneat that are the fields for you to type stuff into. You know.. with a a keyboard.. or whatever you use. Have fun.

You can also upload an avatar and the mxc url will automatically be replaced.

Beneath all that are options to "*Load*" or "*Save*" those two fields. Convenience!

Finally click the apply button to apply the changes. Magic!

---------------------------------------

Software is provided as-is, I don't take responsibility if your server blows up, tokens get stolen or whatever. It's open source software, do with it what you will (but stay within the terms of the LICENSE). :)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W52AOXC)
