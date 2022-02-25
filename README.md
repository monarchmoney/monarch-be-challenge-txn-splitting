# monarch-be-challenge-txn-splitting

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
- http://localhost:8000/api/transactions
