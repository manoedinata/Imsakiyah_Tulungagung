from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.types import Media

import logging
import os

USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")

cl = Client()

print("Logging in...")
cl.login(USERNAME, PASSWORD)
cl.get_timeline_feed()

files = [os.path.join("out", fn) for fn in next(os.walk("./out"))[2]]
files.sort(key=lambda fname: int(fname.split('.')[0].split("/")[1]))

print("Uploading...")
upload: Media = cl.album_upload(files, "Tes boloo")
print(upload.code)

cl.logout()
