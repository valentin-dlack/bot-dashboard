# Python-Lab Project : Discord Bot dashboard

## Sommaire

- [Python-Lab Project : Discord Bot dashboard](#python-lab-project--discord-bot-dashboard)
  - [Sommaire](#sommaire)
  - [Project presentation](#project-presentation)
  - [Technologies used](#technologies-used)
  - [How to use it ?](#how-to-use-it-)
    - [Prerequisites](#prerequisites)
    - [Run the applications](#run-the-applications)
  - [Credits](#credits)

## Project presentation

This project was made for my final exam in the Python Lab of [Ynov Bordeaux](https://ynov-bordeaux.com/). This project is a dashboard that allows you to control some aspects of the bot, like changing the prefix, changing the nickname, add some banned words, etc.

## Technologies used

- [Python](https://www.python.org/)
- [nextcord.py](https://docs.nextcord.dev/en/stable/)
- [Quart (async version of Flask)](https://pgjones.gitlab.io/quart/)
- Sqlite3 for demonstration purposes (use a real database)
- [TailwindCSS](https://tailwindcss.com/)

---

## How to use it ?

### Prerequisites

Python 3.6 or higher, and a Discord bot account.
For packages needed, install them with `pip install -r requirements.txt`.

Create a bot account in discord, and add the bot token and secret in a `.env` file.

*Example of `.env` file:*

```md
BOT_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXX.XXXXX.XXXXXXXXXXXX"
BOT_SECRET = "XXXXXXXXXXXXXXXXXXX"
```

### Run the applications

Open two terminals, one for the bot and one for the dashboard.
Then run the bot with `python3 bot.py` and the dashboard with `python3 dashboard.py`.

**:warning: Attention : Please start the bot BEFORE the web application :warning:**

You wait a little bit, and then you can access the dashboard with the following link: `http://localhost:5000/`

And voilà !

---

## Credits

Directors of Python Laboratory of [Ynov Bordeaux](https://ynov-bordeaux.com/) :

- [Kévin GRANGER](https://github.com/Kraizix)
- [Costa REYPE](https://github.com/TamashiYami)

Lead developer of this project (me !) :

- Valentin DAUTREMENT

---