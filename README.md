# Things I Need To Do 

## Description
A simple ToDo List organizer and manager built with Python and Flask and deployed using Heroku.

Visit [TIN-ToDo](https://thingsineedtodo.herokuapp.com/) .

## Specifications and Requirements
* Flask==1.1.2
* Python==3.7.2
* Heroku CLI
* Please see the [requirements](requirements.txt) file for more.

## How I Deployed
To setup DB on Heroku after adding Heroku-PostgresSQL (Hobby Edition) to app, copy your `DATABASE_URL` value form setting `REVEAL CONFIG VARS` and paste into .env file after removing the deafult value.

Then run the following in your Heroku CLI :

`heroku run "python configurer.py initializeDB" --app {insert_appname}`

This will create the databases as sepcified in the [app.py](app.py) file.

Then deploy from within Heroku
