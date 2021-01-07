from bs4 import BeautifulSoup
from selenium import webdriver

base_url = 'https://u.gg/lol/tier-list'

# invoke the webdriver
browser = webdriver.Chrome(executable_path='C:\\Users\\moooo\\Desktop\\PycharmWorkspace\\webdrivers\\chromedriver.exe')
browser.get(base_url)

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


def get_alt_img_text(item):
    img_html = item.find('img')
    img_text = img_html['alt']
    return img_text


def get_champion_name(champion):
    for champion_text in champion.find_all(name="strong"):
        return champion_text.text

# make this a function
print("Page is ready")
html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, "html.parser")
for item in soup.find_all('h1', class_='tier-list'):
    for item_text in item.find_all(name="span"):
        st += (item_text.text + "\n")   # retrieves the h1 text and current patch number
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
count = 0  # variable to keep track of which group is currently being handled
for group in stats:
    st += (group[0] + ". " + all_champions[count] + " " + all_roles[count] + " | " + group[1] + " tier | " + group[
        2] + " win rate\n")
    count += 1

print(st)
# add a search for a champion and role function. default to most common role

# close the automated browser
browser.close()
