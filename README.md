# Guya Eye - Reverse Image Search the **Kaguya-Sama: Love is War** manga

## Database setup
Connect to your postgresql instance and create a standard database using `CREATE DATABASE <dbname>`.

## Environment setup
Create a `.env` file in the root directory (where this README.md is located) with the following content:
```
DB_HOST=<dbhost>
DB_PORT=<dbport>
DB_USER=<dbuser>
DB_PASS=<dbpass>
DB_NAME=<dbname>
```
Replacing the values with the values for your database instance.

## Running the script
To create a database `python src/main.py --images <directory to the images> --threads <number of CPU threads to use>`. Please make sure there are no subfolders/subdirectories in this folder before running the script, so move all the images into the main directory to make sure it loads them into the database correctly.

To compare an image to the database `python src/main.py --compare <path to the image>`