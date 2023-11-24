Setting Up Gmail API in Python:

Before fetching Gmail emails, follow the steps outlined in the official Google Developers page for setting up the Gmail API in Python. Detailed instructions can be found in the Quickstart guide at the following URL: https://developers.google.com/gmail/api/quickstart/python.

Install Python:

Ensure you have Python version 3.5 or above installed. If not, download it from the official Python website: https://www.python.org/downloads/.

Install Required Packages:

Open a terminal or command prompt and navigate to the project directory.

Run the following command to download all the required packages for the project:

python -m pip install -r requirements.txt
Install PostgreSQL and Create a Database:

Install PostgreSQL by following the instructions on the official PostgreSQL download page: https://www.postgresql.org/download/.
Once installed, create a new database using the tutorial at: https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e.

Update Database Configuration:

Navigate to the app/settings.py file in your project.
Replace the database name and password with the ones you created in the PostgreSQL setup.
Migrate the Database:

In the terminal or command prompt, run the following command to apply the database migrations:
python manage.py migrate

Run Standalone Script:

  Execute the standalone script fetch_emails.py, which is used for dumping email data into the PostgreSQL database.

Start the Server:

Launch the server by running the following command:

python manage.py runserver

Run Unit Test Cases:

To run all unit test cases written in the YAML file, execute the following command:

pytest --execute-all=true

Postman API Collection:

For a sample request collection, use the following Postman collection link: https://api.postman.com/collections/12573617-c4daa010-1c87-4630-b4b7-4e0502e74e7b?access_key=PMAT-01HG09HHM3FDSCEJFVJ1Y9A6YN.

Now, your Django Rest Framework server is up and running, ready to handle your requests!
