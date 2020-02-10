I'm using python because it's the language i feel more comfortable with.

For the framework i use django. I like django because it has built in utilities for the most common back end requirements. I prefer convention over flexibility because i can understand new codebases quicker than if something was built from more basic libraries such as flask.

For unit tests i like pytest. pytest has many good features over normal unittest and django test libraries but the one i really like is that you can simply use `assert <expresion>`.

I was going to use postgresql for the database but went for sqlite to avoid setting up roles, credentials and a db in postgres. Also in django by using the orm it would be really easy to change dbs at this point.
I prefer using the orm as much as posible and only fall back to raw sql when the orm code would get too messy or would produce too many queries like in big joins.

For coding style i always like to use a formatter if one is available.
For python i use black. Luckily black uses spaces. Not so much luck for Makefiles and tabs have been used.

For the tooling since there's not much to do i only made a simple Makefile.
The Makefile avoids trying to reinstall packages when it's not needed. There are also a target for running unit tests.
As a code base grows i like to keep adding make targets as shortcuts to run scripts. Some shells can auto complete these targets by pressing tab.

## API
I went with `application/x-www-form-urlencoded` for parameters.
I like this because it's really easy to log and test from the command line. Also there are no files to upload so there's not really a need for other methods.
I wasn't sure what char limits to set so i used generous ones. In django it's easy to make a migration to update them later. No limits it's usually a bad idea since they can be a target for flooding the server.

I added a few unit tests and a command to load the data from the csv file.

The api is missing 404's

It's really easy to enable the admin in django, i did: `http://localhost:8000/admin/`
To login a django super user is required. After running `make all` just run `./manage.py createsuperuser`

## `GET /businesses`
parameters:
* name
* city
* state
* address

Extample: `http://127.0.0.1:8000/businesses?city=logan`

To search name/city/state all i did is look that the sub string is found in a case insensitive way.

For the address since there are two address fields in the db i had to look if the sub string is in any of those.


## `PUT /businesses`
Creates a new business.
Sending the exact parameters more than once will not create more than one record.
Sending a valid `id`, `uuid` or both will update a record.

## usage

### `make all`
This assumes you are already in the virtual env(or any other setup) you want to work on.
* Install python packages.
* Set up sqlite.
* Load the test data.
* Run tests.
* Run the dev server.

### `make`
This would be what a dev runs after every git pull.
* Update packages if needed.
* Run db migrations.
* Start dev server.

### `make test`
* Run all the unit tests

### `./manage.py load_data <filename>`
* Loads the data from a csv file.
