import pandas as pd

url = r'FMScout.html'
FMScoutFile = pd.read_html(url)
FMScoutFile = FMScoutFile[0]

print(str(FMScoutFile['Name'] + str(FMScoutFile['Pac'])))