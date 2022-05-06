import datetime

now = datetime.datetime.now().strftime("%H:%M:%S")

print("Current Time =", now)

date = datetime.datetime.fromtimestamp(1463288494, datetime.timezone.utc).strftime("%Y.%m.%d")

print(date)
print(type(date))