# Flask-REST
A flask based REST application <b>Recruiter data store</b> that has simple REST end-points.

* Pre-requisites:
 -> Install the required libraries mentioned in `requirements.txt`
 -> Install MongoDB >= 3.2

 -> Set up access control in MongoDB for this REST based application.

 	- Create a `<REST user>` in a separate database, name the database for e.g. `flask`
 	  > E.g. Log into the mongo shell as `<root>` user created already during the installation phase
 	  	     `<root user>` is taken to be the privileged user in the database.

 	  	$ mongo -u <root user> -p <root user password> --authenticationDatabase "admin"
 	  	> use flask
 	  	>  db.createUser({ user: "<name>",
  			pwd: "<cleartext password>",
  			customData: { <any information> },
  			roles: [
    				{ role: "readWrite", db: "flask" } | "<role>",
    				...
			  ]
			})
		> exit

 	- Create a new `collection` named `credentials` with fields: <user,password> in the database created above
 	  > You can create as many `credentials` documents in the `credentials` collection.
 	  > E.g. Log into the mongo shell with `<REST user>` and `<REST user password>`
		$ mongo -u <REST user> -p <REST user password> --authenticationDatabase "flask"
 	  	> use flask 
 	  	> db.credentials.insert({"_id":, "user":"<some username>", "password":"<some password>"})

 	  NOTE: This collection will be used for client authentication to "/auth" to receive a token and proceed with token based authentication and API invocation.

 	- Create a base64 encoding of the "username:password" while sending a POST reuest to `/auth` for authentication.
 	  > `cuRL` E.g. curl automatically encodes the username:password combination in base64
 	  	> curl -v -u '<username>:<password>' -X POST "http://<hostname>.<domain>:<port>/auth"

 	  > For other REST clients ensure to have a base64 encoding (UTF-8) of the `username:password` combination before POSTing to /auth.

 -> Edit the `dbconfig.ini` file under "db" with the required properties.
 	- `mongodb url`
 	- `db username`
 	- `db password`
 	- `db name`
 	- `credential collection`
 	- `collection name`


* Application Execution:
 -> Start the server as `python routes.py`

* List of REST end-points:
 -> To get the list of available REST end-point(s) , send a GET request to: "http://<hostname>.<domain>:<port>/list-apis"