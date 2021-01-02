import discord
from discord.ext import commands
from selenium import webdriver
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="l!")
bot.remove_command('help')


def get_alt_img_text(item):
    img_html = item.find('img')
    img_text = img_html['alt']
    return img_text


def get_champion_name(champion):
    for champion_text in champion.find_all(name="strong"):
        return champion_text.text


def build_url(champion, role):
    if role == "not specified":
        return 'https://u.gg/lol/champions/' + champion + '/build'
    return 'https://u.gg/lol/champions/' + champion + '/build?role=' + role


@bot.event
async def on_ready():
    print("League Bot is ready to be used!")


@bot.command(aliases=['tl', 'TL'])
async def tierlist(message, num=10, role="all"):
    # initialize the arrays and other variables that will be used
    stats = []
    odd_roles = []
    even_roles = []
    all_roles = []
    odd_champions = []
    even_champions = []
    all_champions = []
    i = 0
    st = ""

    role = role.lower()
    if role in 'all, a':
        base_url = 'https://u.gg/lol/tier-list'
    elif role in 'top lane, top, tl, t':
        base_url = 'https://u.gg/lol/top-lane-tier-list'
    elif role in 'jungle, jg, j':
        base_url = 'https://u.gg/lol/jungle-tier-list'
    elif role in 'middle lane, mid lane, middle, mid, ml, m':
        base_url = 'https://u.gg/lol/mid-lane-tier-list'
    elif role in 'bot lane, bot, adc, apc, b':
        base_url = 'https://u.gg/lol/adc-tier-list'
    elif role in 'support, supp, sup, s':
        base_url = 'https://u.gg/lol/support-tier-list'
    else:
        st += "Role could not be found! Using general tier list with all roles.\n"
        base_url = 'https://u.gg/lol/tier-list'

    # invoke the webdriver
    browser = webdriver.Chrome(
        executable_path=r'C:\Users\moooo\Desktop\PycharmWorkspace\webdrivers\chromedriver.exe')
    browser.get(base_url)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('h1', class_='tier-list'):
        for item_text in item.find_all(name="span"):
            st += (item_text.text + "\n")  # retrieves the h1 text and current patch number
            break
    for item in soup.find_all('div', class_='rt-tbody'):
        group = []  # group array variable to keep track of the stat texts that aren't associated with an image
        for item_text in item.find_all(name="span"):
            group.append(item_text.text)
            i += 1
            if i == 6:
                i = 0
                stats.append(group)
                group = []  # resets the group array variable for the next group
        for odd_role in soup.find_all('div', class_='rt-td role is-in-odd-row'):
            odd_roles.append(get_alt_img_text(odd_role))
        for even_role in soup.find_all('div', class_='rt-td role'):
            even_roles.append(get_alt_img_text(even_role))
        for odd_champion in soup.find_all('div', class_='rt-td champion is-in-odd-row'):
            odd_champions.append(get_champion_name(odd_champion))
        for even_champion in soup.find_all('div', class_='rt-td champion'):
            even_champions.append(get_champion_name(even_champion))
    while True:
        try:  # merge roles and champions into the same respective array
            all_roles.append(odd_roles.pop(0))
            all_roles.append(even_roles.pop(0))
            all_champions.append(odd_champions.pop(0))
            all_champions.append(even_champions.pop(0))
        except IndexError:  # catch the exception when there are no remaining values in the individual arrays
            break  # exit the while loop

    if num > 30:
        st += "Sorry! The League bot can only get the top 30 ranked champions at the moment. Here are the top 30 " \
              "champions.\n "

    count = 0  # variable to keep track of which group is currently being handled
    for group in stats:
        st += (group[0] + ". " + all_champions[count] + " " + all_roles[count] + " | " + group[1] + " tier | " + group[
            2] + " win rate\n")
        count += 1
        if count == num:
            break

    await message.send(st)

    # close the automated browser
    browser.close()


@bot.command(aliases=['s', 'S'])
async def search(message, champion, role="not specified"):
    st = ""
    base_url = build_url(champion, role)

    # invoke the webdriver
    browser = webdriver.Chrome(
        executable_path=r'C:\Users\moooo\Desktop\PycharmWorkspace\webdrivers\chromedriver.exe')
    browser.get(base_url)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('div', class_='champion-label'):
        for item_text in item.find_all(name="span"):
            st += (item_text.text + "\n")  # retrieves the h1 text and current patch number

    await message.send(st)


@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color=discord.Color.blue()
    )
    embed.add_field(name='l!tierlist <Number> <Role>', value='Returns the first 30 ranked champions for all roles from '
                                                             'u.gg unless specified otherwise.The number and role type '
                                                             'is not necessary. If you want a role, then you must '
                                                             'specify a number. The maximum number of statistics this '
                                                             'bot can provide is 30.\n'
                                                             '**Choose from the following roles (case insensitive):**\n'
                                                             '**[all, a]**, **[top lane, top, tl, t]**, '
                                                             '**[jungle, jg, j]**, '
                                                             '**[middle lane, mid lane, middle, mid, ml, m]**,'
                                                             '**[bot lane, bot, adc, apc, b]**, '
                                                             '**[support, supp, sup, s]**\n'
                                                             'Equivalent commands usable: tl, TL', inline=False)

    await author.send(embed=embed)
    embed.set_author(name='Help')


bot.run("INSERT TOKEN HERE")  # my token is substituted out
