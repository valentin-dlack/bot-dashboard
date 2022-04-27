from dotenv import load_dotenv
import os 
import json
import sqlite3
from quart import Quart, render_template, redirect, url_for, request, make_response
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import nextcord
from nextcord.ext import ipc
load_dotenv()

app = Quart(__name__)

conn = sqlite3.connect("../database/prefix.db")
cursor = conn.cursor()

app.secret_key = b'secret'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "true"
app.config["DISCORD_CLIENT_ID"] = 940948417545375784
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get('BOT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.environ.get('BOT_TOKEN')

discord = DiscordOAuth2Session(app)
ipcClient = ipc.Client(secret_key="secret")

def insert(query, values):
    cursor.execute(query, values)
    conn.commit()

@app.route('/login')
async def login():
    return await discord.create_session()

@app.route('/callback')
async def callback():
    try:
        await discord.callback()
    except:
      return redirect(url_for('/login'))
    return redirect(url_for('dashboard'))

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/leave/<int:guild_id>")
async def leave(guild_id):
    await ipcClient.request("leave_guild", guild_id = guild_id)
    return redirect(url_for('dashboard'));

@app.route('/dashboard', methods=['GET', 'POST'])
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        user = await discord.fetch_user()
        guildCount = await ipcClient.request("get_guild_count")
        guildIds = await ipcClient.request("get_guild_ids")
        try:
            userGuilds = await discord.fetch_guilds()
        except:
            return await redirect(url_for('login'))
        guilds = []
        for guild in userGuilds:
            if guild.permissions.administrator:
                guild.class_color = "Joined" if guild.id in guildIds else "Not Joined"
                guilds.append(guild)
            
        guilds.sort(key=lambda guild: guild.class_color == "Not Joined")
    elif request.method == 'POST':
        discord.revoke()
        return redirect(url_for("index"))
    
    return await render_template("dashboard.html", user=user, gc=guildCount, guilds=guilds, gsc=len(guilds))

@app.route("/dashboard/<int:guild_id>", methods=['GET', 'POST'])
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for('login'))
    guild = await ipcClient.request("get_guild", guild_id = guild_id)
    if guild is None:
        return redirect('https://discord.com/oauth2/authorize?client_id=940948417545375784&scope=bot&permissions=27648860222')
        
    if request.method == "POST":
        newPrefix = (await request.form)["setPrefix"]
        newWelChan = (await request.form)["setWelcomeChannel"]
        newLogChan = (await request.form)["setLogsChannel"]
        newNick = (await request.form)["setNick"]
        newWarnLimit = (await request.form)["setWarnLimit"]
        newBanwords = (await request.form)["setBanwords"]
        cursor.execute(f"SELECT prefix, welcome_chan, log_chan, name, banword, warn_before_ban FROM guilds WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result:
            cursor.execute("""UPDATE guilds SET prefix = ?, welcome_chan = ?, log_chan = ?, name = ?, banword = ?, warn_before_ban = ? 
                        WHERE guild_id = ?""", (newPrefix, newWelChan, newLogChan, newNick, newBanwords, newWarnLimit, guild_id))
        else:
            cursor.execute("""INSERT INTO guilds (prefix, welcome_chan, log_chan, name, banword, warn_before_ban, guild_id) 
                        VALUES (?,?,?,?,?,?,?)""", (newPrefix, newWelChan, newLogChan, newNick, newBanwords, newWarnLimit, guild.id))
        conn.commit()
        pref = result
        await ipcClient.request("set_nickname", guild_id = guild_id, nickname = newNick)
        return redirect(url_for(f"dashboard_server", guild_id=guild_id))
    
    elif request.method == "GET":
        cursor.execute(f'SELECT prefix, welcome_chan, log_chan, name, adm_roles, banword, warn_before_ban FROM guilds WHERE guild_id = {guild_id}')
    res = cursor.fetchone()
    if res:
        pref = res
        serial_roles = json.loads(pref[4])
        getChan_1 = str(pref[1])
        getChan_2 = str(pref[2])
    else:
        try:
            cursor.execute(f"SELECT prefix FROM guilds WHERE guild_id = {guild_id}")
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", ("!", str(guild_id)))
            else:
                cursor.execute("INSERT INTO guilds (prefix, guild_id) VALUES (?,?)", ("!", str(guild_id)))
            conn.commit()
            cursor.execute(f"SELECT prefix FROM guilds WHERE guild_id = {guild_id}")
            result = cursor.fetchone()
            pref = result[0]
        except Exception:
            pref = "!"
    
    return await render_template("guild_board.html", guild=guild, pref=pref, roles=serial_roles, chan_1=getChan_1, chan_2=getChan_2)

@app.errorhandler(404)
async def page_not_found(e):
    return await render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)