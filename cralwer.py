import urllib.request

year = 2012
month = 6
day = 1
hour = 0
minute = "00"

for month in range(6,13):
    for day in range(1,29):
        for hour in range(0,24,6):
            form = str(year) + str(month).zfill(2) + str(day).zfill(2) + str(hour).zfill(2) + minute
            url = "https://images.lightningmaps.org/blitzortung/america/index.php?map=usa_big&date=" + form + "-360"
            print(url)
            name = form + ".png"
            mem = urllib.request.urlopen(url).read()

            with open(name,mode="wb") as f:
                f.write(mem)

