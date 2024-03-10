from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from os import makedirs
from datetime import date
from datetime import datetime
from datetime import timedelta
from calendar import month_name
from calendar import different_locale
from zoneinfo import ZoneInfo
import json

from PrayTimes.praytimes import PrayTimes

prayTimes = PrayTimes()
prayTimes.setMethod("Kemenag")

def namaBulan(index, locale = "id_ID"):
    with different_locale(locale):
        return month_name[index]

jktZone = ZoneInfo("Asia/Jakarta")
currentDate = datetime.now(jktZone).date() + timedelta(days=1)
formattedDate = f"{currentDate.day} {namaBulan(currentDate.month)} {currentDate.year}"

fileCount = 0

def getPrayTimes(coordinates: list, date: date = currentDate):
    return prayTimes.getTimes(date, tuple(coordinates), 7)

def generateImsakiyah(nama: str, koordinat: list, kota: bool = False):
    print(f"Generating Imsakiyah for: {nama}")

    # Open image file
    img = Image.open("img/awal.jpg")

    # Get image size
    width, _ = img.size

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Font
    # font = ImageFont.truetype(<font-file>, <font-size>)
    kecamatan_font = ImageFont.truetype("fonts/DMSans/DMSans-Bold.ttf", 27)
    tanggal_font = ImageFont.truetype("fonts/Monotype_Corsiva/monotype-corsiva-bold.ttf", 40)
    jadwal_font = ImageFont.truetype("fonts/Work_Sans/WorkSans-Bold.ttf", 36)

    # Draw text
    # draw.text((x, y),"Sample Text",(r,g,b))

    ## Tanggal
    tanggal_font_size = draw.textlength(formattedDate, tanggal_font)
    tanggal_size_total = (width / 2) - (tanggal_font_size / 2)
    # draw.text((tanggal_size_total, 441), formattedDate, (255,255,255), font=tanggal_font)
    # draw.text((tanggal_size_total, 310), formattedDate, (255,255,255), font=tanggal_font)
    draw.text((tanggal_size_total, 310), formattedDate, (255,255,255), font=tanggal_font)

    # draw.text((604, 297.7), kecamatan, (255,255,255), font=kecamatan_font)
    kecamatan_font_size = draw.textlength(f"{'Kota' if kota else 'Kecamatan'} {nama}", kecamatan_font)
    kecamatan_size_total = (width / 2) - (kecamatan_font_size / 2)
    # draw.text((kecamatan_size_total, 297), f"Kecamatan {kecamatan}", (255,255,255), font=kecamatan_font)
    draw.text((kecamatan_size_total, 438), f"{'Kota' if kota else 'Kecamatan'} {nama}", (255,255,255), font=kecamatan_font)

    # Get prayer times
    times = getPrayTimes(koordinat)

    ## Imsak
    draw.text((375, 498), times["imsak"], (0, 0, 0), font=jadwal_font)
    ## Shubuh
    draw.text((375, 498 + (63 * 1)), times["fajr"], (0, 0, 0), font=jadwal_font)
    ## Dhuhur
    draw.text((375, 498 + (63 * 2)), times["dhuhr"], (0, 0, 0), font=jadwal_font)
    ## Ashar
    draw.text((375 + 480, 498), times["asr"], (0, 0, 0), font=jadwal_font)
    ## Maghrib
    draw.text((375 + 480, 498 + (63 * 1)), times["maghrib"], (0, 0, 0), font=jadwal_font)
    ## Isya'
    draw.text((375 + 480, 498 + (63 * 2)), times["isha"], (0, 0, 0), font=jadwal_font)

    # Save image
    makedirs("out", exist_ok=True)
    img.save(f"out/{fileCount}. {nama}.jpg")
    img.close()

def generateTwoImsakiyah(tupleKecamatan: tuple):
    listKecamatan = [kecamatan["nama"] for kecamatan in tupleKecamatan]
    namaKecamatan = " & ".join(listKecamatan)

    print(f"Generating Imsakiyah for: {namaKecamatan}")

    # Open image file
    img = Image.open("img/awal_2.jpg")

    # Get image size
    width, _ = img.size

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Font
    # font = ImageFont.truetype(<font-file>, <font-size>)
    kecamatan_font = ImageFont.truetype("fonts/DMSans/DMSans-Bold.ttf", 27)
    tanggal_font = ImageFont.truetype("fonts/Monotype_Corsiva/monotype-corsiva-bold.ttf", 40)
    jadwal_font = ImageFont.truetype("fonts/Work_Sans/WorkSans-Bold.ttf", 36)

    ## Tanggal
    tanggal_font_size = draw.textlength(formattedDate, tanggal_font)
    tanggal_size_total = (width / 2) - (tanggal_font_size / 2)
    draw.text((tanggal_size_total, 310), formattedDate, (255,255,255), font=tanggal_font)

    for i, kecamatan in enumerate(tupleKecamatan):
        kecamatan_2_space = 303

        # Draw text
        # draw.text((x, y),"Sample Text",(r,g,b))
        # draw.text((604, 297.7), kecamatan, (255,255,255), font=kecamatan_font)
        kecamatan_font_size = draw.textlength(f"{'Kota' if kecamatan.get('kota') else 'Kecamatan'} {kecamatan['nama']}", kecamatan_font)
        kecamatan_size_total = (width / 2) - (kecamatan_font_size / 2)
        draw.text((kecamatan_size_total, 438 + (kecamatan_2_space * i)), f"{'Kota' if kecamatan.get('kota') else 'Kecamatan'} {kecamatan['nama']}", (255,255,255), font=kecamatan_font)

        # Get prayer times
        times = getPrayTimes(kecamatan["koordinat"])

        ## Imsak
        draw.text((375, 498 + (kecamatan_2_space * i)), times["imsak"], (0, 0, 0), font=jadwal_font)
        ## Shubuh
        draw.text((375, 498 + (kecamatan_2_space * i) + (63 * 1)), times["fajr"], (0, 0, 0), font=jadwal_font)
        ## Dhuhur
        draw.text((375, 498 + (kecamatan_2_space * i) + (63 * 2)), times["dhuhr"], (0, 0, 0), font=jadwal_font)
        ## Ashar
        draw.text((375 + 480, 498 + (kecamatan_2_space * i)), times["asr"], (0, 0, 0), font=jadwal_font)
        ## Maghrib
        draw.text((375 + 480, 498 + (kecamatan_2_space * i) + (63 * 1)), times["maghrib"], (0, 0, 0), font=jadwal_font)
        ## Isya'
        draw.text((375 + 480, 498 + (kecamatan_2_space * i) + (63 * 2)), times["isha"], (0, 0, 0), font=jadwal_font)

    # Save image
    makedirs("out", exist_ok=True)
    img.save(f"out/{fileCount}. {namaKecamatan}.jpg")
    img.close()

# Start generating images
with open("data/data.json", "r") as file:
    data = json.load(file)

print("Total kecamatan:", len(data))
print("")

# for kecamatan in data:
#     generateImsakiyah(**kecamatan)

def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)

for kecamatan in grouped(data, 2):
    fileCount += 1
    generateTwoImsakiyah(kecamatan)

if len(data) % 2 > 0:
    fileCount += 1
    # Elemen terakhir dari `grouped()` tidak ikut
    # Panggil `generateImsakiyah()` secara manual untuk 1 kecamatan saja
    generateImsakiyah(**data[-1])
