# Flask-REST
A flask based REST application <b>Recruiter data store</b> that has simple REST end-points exposed.

* Pre-requisites:
 -> Install the required libraries mentioned in `requirements.txt`
 -> Install MongoDB >= 3.2
 -> Set up access control in MongoDB.
 	- Create a `root` account in `admin` database
 	- Create a `<REST user>` in a separate database, name the database for e.g. `flask`
 -> Edit the `dbconfig.ini` file under "db" with the required properties.
 	- `mongodb url`
 	- `db username`
 	- `db password`
 	- `dbname`
 	- `collection name`


* Application Execution:
 -> Run the application as `python routes.py`

* List of REST end-points:
 -> To get the list of available REST end-point(s) , send a GET request : "/list-apis"