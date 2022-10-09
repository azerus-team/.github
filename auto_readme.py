import json
import os
import re
from urllib.request import Request, urlopen

README_PATH = os.path.join("profile", "README.md")
with open(README_PATH, "r") as f:
	README = f.read()

# Storing json from API
req = Request('https://azerusteam.com/api/maps', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
j = json.load(webpage)


if len(j["maps"]) == len(re.findall('class=\"map\"', README)):
	print("Up to date.")
else:
	AUTOMATE = r'''<p class="automate" align="center">'''
	map = r'''<a class="map" href=".*"><img alt=".*" width="256px" src="https://azerusteam.com/attachments/.*/.*/logo-web.png" /></a>\n'''
	FIXED_README = README
	FIXED_README = re.sub(map, "", FIXED_README) # Deleting previous maps from readme
	
	# Adding all maps to readme
	for i in range(len(j["maps"])-1, -1, -1):
		LAST_MAP = j["maps"][i]
		TITLE = LAST_MAP["title"]
		mapUuid = LAST_MAP["mapUuid"]
		versionUuid = LAST_MAP["versionUuid"]
		MAP_URL = "https://azerusteam.com/map/" + LAST_MAP["vanity_url"]

		new_line = AUTOMATE + f'''\n<a class="map" href="{MAP_URL}"><img alt="{TITLE}" width="256px" src="https://azerusteam.com/attachments/{mapUuid}/{versionUuid}/logo-web.png" /></a>'''
		FIXED_README = re.sub(AUTOMATE, new_line, FIXED_README)

	with open(README_PATH, "r+") as f:
		f.write(FIXED_README)