<p align="center"><a href="http://127.0.0.1:5000/" target="_blank" rel="noreferrer noopener"><img alt="Logo" src="https://media.discordapp.net/attachments/590667063165583409/1134371140228354128/pdcmlogoclear.png"></a></p>
<h1 align="center">PDCM Music Player/Database
<br><br></h1>


## Description

A web application written in Flask, Jinja, HTML/CSS, and JavaScript. This webapp displays hundreds of songs stored in local CSV files, allowing you to sort and search through them by Genre, Artist, Album, Title, and Duration. You can listen to each song by navigating to its page and clicking on the play button next to the title.
<br><br>
You can review songs by logging in or registering ("Login" on the top navbar), going to a particular track, and clicking "Leave a Review". Your review will then show up on the said track's page.
<br><br>
You can get song recommendations:

-   by browsing to a song you enjoy and checking out the "If you like \_\_\_, check out:" section on each track's page. These recommendations will be based on the song in question.

-   by logging in, reviewing at least one track at ≥ 3/6 stars, and navigating to "Discover" in the navbar. These recommendations will be based on the ratings you give songs.

<br>
You can sort songs on the homepage by clicking on the column titles ("Title", "Artist", "Album", "Duration). Clicking on said title a second time will reverse the sort. Click on a specific song's artist or album to see all songs in said artist/album. You can also sort through genres in the "Genres" tab - you can click on the genre title to see all songs in said genre.
<br><br>

You can search for songs by:

-   Typing what you think the song's title is in the searchbar up the top right of the navbar. This is a fuzzy search which uses Levenshtein distance.

-   Clicking on "Advanced Search" in the top right, and filling in each field of the advanced search form before clicking "Search". The "Fuzzy Search" toggle only applies to title. All other search options must be exact.
    <br><br>

## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment.

## Execution

**Running the application**

From the project directory, and within the activated virtual environment (see _venv\Scripts\activate_ above):

```shell
$ flask run
```

Then, go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or your localhost page to view.

## Configuration

The _PDCM/.env_ file contains variable settings. They are set with appropriate values.

-   `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
-   `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
-   `SECRET_KEY`: Secret key used to encrypt session data.
-   `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
-   `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

These settings are for the database version of the code:

-   `SQLALCHEMY_DATABASE_URI`: The URI of the SQlite database, by default it will be created in the root directory of the project.
-   `SQLALCHEMY_ECHO`: If this flag is set to True, SQLAlchemy will print the SQL statements it uses internally to interact with the tables.
-   `REPOSITORY`: This flag allows us to easily switch between using the Memory repository or the SQLAlchemyDatabase repository.

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment.

To run the tests for the database components, these are in the folder 'tests_db', so you can call 'python -m pytest tests_db' to run them from the command line.


## Collaboration

Made in collaboration with [NachoToast](https://github.com/NachoToast/) in a locked repository. Permission was granted to have this repository public.


## Images

<a href="https://media.discordapp.net/attachments/590667063165583409/1134375680080097400/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134375680080097400/image.png"></a>
<a href="https://media.discordapp.net/attachments/590667063165583409/1134375888092405880/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134375888092405880/image.png"></a>
<a href="https://media.discordapp.net/attachments/590667063165583409/1134375941930504363/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134375941930504363/image.png"></a>
<a href="https://media.discordapp.net/attachments/590667063165583409/1134376204959502336/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134376204959502336/image.png"></a>
<a href="https://media.discordapp.net/attachments/590667063165583409/1134376633806098472/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134376633806098472/image.png"></a>
<a href="https://media.discordapp.net/attachments/590667063165583409/1134376167219154944/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134376167219154944/image.png"></a>
<a href="https://media.discordapp.net/attachments/590667063165583409/1134376429728047155/image.png" target="_blank" rel="noreferrer noopener"><img width="400" src="https://media.discordapp.net/attachments/590667063165583409/1134376429728047155/image.png"></a>




## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052 or
https://github.com/mdeff/fma

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections:

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.


