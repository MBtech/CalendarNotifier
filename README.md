# Calendar Notifier
This python application is designed to notify of newly created events as well as
events that have been deleted from a shared google Calendar

The notification application will work only on Mac OSX and Linux for now.

## Pre-requisites
    pip install python-dateutil
    pip install --upgrade google-api-python-client
#### For Mac OS
    pip install pyobjc
#### For Linux
    apt-get install python-gobject
    apt-get install libnotify-bin
    apt-get install libnotify-dev

## Setup
To get an overview of using the python Google Calendar API you can take a look at the
full [quickstart guide](https://developers.google.com/google-apps/calendar/quickstart/python) by Google.

In order to setup this application you need to have credentials to use Google Calendar API. Do the following steps to acquire credentials:

* Use this wizard to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
* On the Add credentials to your project page, click the Cancel button.
* At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
* Select the Credentials tab, click the Create credentials button and select OAuth client ID.
* Select the application type Other, enter the name "Google Calendar API Quickstart", and click the Create button.
* Click OK to dismiss the resulting dialog.
* Click the file_download (Download JSON) button to the right of the client ID.
* Move this file to your working directory and rename it client_secret.json.

## Running the program
After you are done with the setup you can run the program using:

    python main.py
To run the program as daemon in Mac, we need to use **launchctl**.

Edit the plist file to replace *repo_path* with the path to this repository.

Copy the plist file to **~/Library/LaunchAgents/**

    launchctl load ~/Library/LaunchAgents/com.learningcurve.mb.calendarnotifier.plist
## Work in progress
* Make the program work for Windows as well
* Add the instructions to run it as daemon on Linux

References:

* [Working with Python linux notification API](http://www.devdungeon.com/content/desktop-notifications-python-libnotify)
