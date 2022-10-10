import json
import os
import re
from urllib.request import Request, urlopen

IMAGE_WIDTH = 256
SITE_URL = "https://azerusteam.com"
DISCORD_URL = "https://azerus.team/discord"
YOUTUBE_URL = "https://azerus.team/youtube"
####################################################################

AUTOMATE = r'''<p class="automate" align="center">'''

map_hyperlink = rf'''<a class="map" href=".*"><img alt=".*" width=".*px" src="{SITE_URL}/attachments/.*/.*/logo-web.png" /></a>\n'''
site_hyperlink = r'''<a class="site" href=".*" >'''
discord_hyperlink = r'<a class="discord" href=".*" >'
youtube_hyperlink = r'<a class="youtube" href=".*" >'


README_PATH = os.path.join("profile", "README.md")

UPDATING_MESSAGE = "[Updating README.md]"
SUCCESS_MESSAGE = "[README.md has been successfully updated by API]"

def get_json() -> json:
	req = Request(f'{SITE_URL}/api/maps', headers={'User-Agent': 'Mozilla/5.0'})
	return json.load(urlopen(req))

def main():
	print(UPDATING_MESSAGE)
	with open(README_PATH, "r") as f:
		README = f.read()

	# Storing json from API
	j = get_json()

	# Deleting previous map hyperlinks from readme
	README = re.sub(map_hyperlink, "", README) 
	
	# Replacing URLs to current URLs
	README = re.sub(site_hyperlink, f'<a class="site" href="{SITE_URL}" >', README)
	README = re.sub(discord_hyperlink, f'<a class="discord" href="{DISCORD_URL}" >', README)
	README = re.sub(youtube_hyperlink, f'<a class="youtube" href="{YOUTUBE_URL}" >', README)


	# Adding all maps to readme
	for i in range(len(j["maps"])-1, -1, -1):
		LAST_MAP = j["maps"][i]
		TITLE = LAST_MAP["title"]
		mapUuid = LAST_MAP["mapUuid"]
		versionUuid = LAST_MAP["versionUuid"]
		MAP_URL = f"{SITE_URL}/map/{LAST_MAP['vanity_url']}"
		new_hyperlink = f'''\n<a class="map" href="{MAP_URL}"><img alt="{TITLE}" width="{IMAGE_WIDTH}px" src="{SITE_URL}/attachments/{mapUuid}/{versionUuid}/logo-web.png" /></a>'''
		new_line = AUTOMATE + new_hyperlink
		
		README = re.sub(AUTOMATE, new_line, README)

	with open(README_PATH, "r+") as f:
		f.write(README)
		print(SUCCESS_MESSAGE)

if __name__ == "__main__":
	main()