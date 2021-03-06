# monarch-be-challenge-txn-splitting
This is a Django based backend takehome challenge.

## Prerequisites
- A machine with Docker desktop / runtime set up. See https://www.docker.com/products/docker-desktop to install
- Python runtime
- Code editor of your choice (we recommend VSCode if you don't have a 

## Getting Started
Clone this repo

Build the Docker images
```
docker-compose build
```

Start running Docker containers
```
docker-compose up -d
```

Enter the web docker container. You will need to use this to run commands and the interactive shell.
```
docker-compose exec web bash
```

Create a superuser (we can use this as both the admin user and your main test user). Choose any email and password from the prompt.
```
./manage.py createsuperuser
```

Seed initial test data (Accounts, Categories, Transactions) for that user
```
./manage.py seed_user_data <EMAIL>
```

Check that the local webserver is running, you should see a Django 404 page.
- http://localhost:8000/

Log in to the admin (this is the easiest way to log in as your user)
- https://localhost:8000/admin

Poke around the REST API 
- http://localhost:8000/api/users/me
- http://localhost:8000/api/accounts
- http://localhost:8000/api/categories
- http://localhost:8000/api/transactions


## Useful Dev Commands
Interactive Django shell
```
./manage.py shell
```

See logs from Docker
```
docker-compose logs -f     # logs from all containers
docker-compose logs -f web    # logs from only web container
```

## Database Migrations
1. Make a change to a model
2. Run `./manage.py makemigrations monarch` to generate a migration file
3. Apply migration with `./manage.py migrate`

## Unit Tests
We use pytest for unit tests. If you'd like to write unit tests, or it is helpful with your development, feel free to write some tests. You can put them in `monarch/tests` or wherever you like.

Run tests by doing
```
runtests
```

Or do
```
pytest
```
