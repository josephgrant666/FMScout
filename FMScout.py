#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from unidecode import unidecode
from tkinter import *
import customtkinter
from PIL import Image
import webbrowser, os, sys, subprocess

# Read HTML file into Pandas DataFrame
html_file_path = r'FMScoutStats.html'
df = pd.read_html(html_file_path, header=0)[0]

# Converts foreign characters into readable text that would otherwise appear unreadable when exported from FM
def convert_accented_characters(text):
    return unidecode(text)

df['Name'] = df['Name'].apply(convert_accented_characters)

# Code to perform numeric concatenation on all columns apart from 'Name'
exclude_columns = ['Name']

# Loop through columns and convert to numeric (excluding 'Name' column)
for column in df.columns:
    if column not in exclude_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

def ScatterGraphs():
    plt.style.use('seaborn-v0_8-pastel')
    plt.scatter(df[StatsSelectionComboBox1.get()], df[StatsSelectionComboBox2.get()])
    for i, txt in enumerate(df['Name']):
        if df[StatsSelectionComboBox1.get()][i] > (max(df[StatsSelectionComboBox1.get()]) * 0.50) or df[StatsSelectionComboBox2.get()][i] > (max(df[StatsSelectionComboBox2.get()]) * 0.50):
            x_offset = 0.005
            plt.annotate(txt, (df[StatsSelectionComboBox1.get()][i] + x_offset, df[StatsSelectionComboBox2.get()][i]), rotation=10)
            plt.scatter(df[StatsSelectionComboBox1.get()][i], df[StatsSelectionComboBox2.get()][i], color='orange')
    plt.xlabel(StatsSelectionComboBox1.get())
    plt.ylabel(StatsSelectionComboBox2.get())
    plt.title(StatsSelectionComboBox1.get() + str(' Vs ') + StatsSelectionComboBox2.get())
    plt.show()

def BarGraphs():
    plt.style.use('seaborn-v0_8-pastel')
    plt.bar(df['Name'], df[StatsSelectionComboBox3.get()])
    for i, txt in enumerate(df['Name']):
        if df[StatsSelectionComboBox3.get()][i] > (max(df[StatsSelectionComboBox3.get()]) * 0.50):
            plt.bar(df['Name'][i], df[StatsSelectionComboBox3.get()][i], color='orange')
    plt.xlabel('Name')
    plt.ylabel('Av Rat')
    plt.title('Name vs Av Rating')
    plt.tick_params(axis='x', rotation=90)
    plt.show()

def AttributeRanking():
    
    global RoleInput
    RoleInput = AttributeRankingEntryBox.get()
    # Opens the exported HTML file with attributes and creates a dataframe table.
    url = r'C:\Users\User\Documents\Coding Projects\Completed Apps\FMScout\FMScout.html'
    FMScoutFile = pd.read_html(url, header=0, encoding="utf-8", keep_default_na=False)
    FMScoutFile = FMScoutFile[0]

    def generate_html(dataframe: pd.DataFrame): # Gets the table HTML from the dataframe.
        table_html = dataframe.to_html(table_id="table", index=False)
        # construct the complete HTML with jQuery Data tables.
        # You can disable paging ,enable y scrolling on lines 20 and 21 respectively.
        html = f"""
        <html>
        <header>
            <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        </header>
        <body>
        {table_html}
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready( function () {{
                $('#table').DataTable({{
                    paging: false,
                    order: [[12, 'desc']],
                    // scrollY: 400,
                }});
            }});
        </script>
        </body>
        </html>
        """
        # return the html
        return html

    Details = FMScoutFile[['Name', 'Position', 'Inf', 'Av Rat', 'Age', 'Club', 'Wage', 'Height', 'Left Foot', 'Right Foot', 'Transfer Value']]

    # Table columns for Goalkeeper roles.

    def GKfunc(): # This function as well as all other role functions add together the required attributes for this role, reduces the influence of preferred attributes by 40% and then produces an average score.
        FMScoutFile['GK'] = ((FMScoutFile['1v1'] * 0.6) + 
                            (FMScoutFile['Aer']) + 
                            (FMScoutFile['Agi']) + 
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmd']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Com']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Han']) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Ref']) +
                            (FMScoutFile['Thr'] * 0.6)
                            )/12
        FMScoutFile.GK = FMScoutFile.GK.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.GK], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='GK', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser. 

    def SKdefunc(): 
        FMScoutFile['SKde'] = ((FMScoutFile['1v1'] * 0.6) + 
                            (FMScoutFile['Aer']) + 
                            (FMScoutFile['Acc']) + 
                            (FMScoutFile['Agi'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmd'] * 0.6) +
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Com']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Fir']) + 
                            (FMScoutFile['Han']) +
                            (FMScoutFile['Kic'] * 0.6) + 
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Ref'] * 0.6) +
                            (FMScoutFile['Thr']) +
                            (FMScoutFile['Vis']) 
                            )/17
        FMScoutFile.SKde = FMScoutFile.SKde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.SKde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='SKde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser. 

    def SKsufunc(): 
        FMScoutFile['SKsu'] = ((FMScoutFile['1v1'] * 0.6) + 
                            (FMScoutFile['Aer']) + 
                            (FMScoutFile['Acc']) + 
                            (FMScoutFile['Agi'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmd'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) + 
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Com']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Fir']) + 
                            (FMScoutFile['Han']) +
                            (FMScoutFile['Kic'] * 0.6) + 
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Ref'] * 0.6) +
                            (FMScoutFile['Thr']) +
                            (FMScoutFile['TRO'] * 0.6) +
                            (FMScoutFile['Vis']) 
                            )/18
        FMScoutFile.SKsu = FMScoutFile.SKsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.SKsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='SKsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser. 

    def SKatfunc(): 
        FMScoutFile['SKat'] = ((FMScoutFile['1v1'] * 0.6) + 
                            (FMScoutFile['Aer']) + 
                            (FMScoutFile['Acc']) + 
                            (FMScoutFile['Agi'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmd'] * 0.6) +
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Com']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Ecc']) +
                            (FMScoutFile['Fir']) + 
                            (FMScoutFile['Han']) +
                            (FMScoutFile['Kic'] * 0.6) + 
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Ref'] * 0.6) +
                            (FMScoutFile['Thr']) +
                            (FMScoutFile['Vis']) 
                            )/18
        FMScoutFile.SKat = FMScoutFile.SKat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.SKat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='SKat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser. 

    # Table columns for Fullback roles 

    def FBdefunc():
        FMScoutFile['FBde'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'])
                            )/12

        FMScoutFile.FBde = FMScoutFile.FBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.FBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='FBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def FBsufunc():
        FMScoutFile['FBsu'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Dri']) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'])
                            )/14
        FMScoutFile.FBsu = FMScoutFile.FBsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.FBsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='FBsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def FBatfunc():
        FMScoutFile['FBat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'])
                            )/17
        FMScoutFile.FBat = FMScoutFile.FBat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.FBat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='FBat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.    

    def WBdefunc():
        FMScoutFile['WBde'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6)
                            )/19
        FMScoutFile.WBde = FMScoutFile.WBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WBsufunc():
        FMScoutFile['WBsu'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6)
                            )/19
        FMScoutFile.WBsu = FMScoutFile.WBsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WBsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WBsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WBatfunc():
        FMScoutFile['WBat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6)
                            )/19
        FMScoutFile.WBat = FMScoutFile.WBat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WBat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WBat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CWBsufunc():
        FMScoutFile['CWBsu'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6)
                            )/19
        FMScoutFile.GK = FMScoutFile.GK.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.GK], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CWBsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CWBatfunc():
        FMScoutFile['CWBat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Fla'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6)
                            )/19
        FMScoutFile.CWBat = FMScoutFile.CWBat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CWBat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CWBat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IWBdefunc():
        FMScoutFile['IWBde'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Sta'])
                            )/16
        FMScoutFile.IWBde = FMScoutFile.IWBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IWBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IWBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IWBsufunc():
        FMScoutFile['IWBsu'] = ((FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Sta'])
                            )/17
        FMScoutFile.IWBsu = FMScoutFile.IWBsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IWBsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IWBsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IWBatfunc():
        FMScoutFile['IWBat'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'])
                            )/22
        FMScoutFile.IWBat = FMScoutFile.IWBat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IWBat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IWBat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IFBdefunc(): 
        FMScoutFile['IFBde'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Jum']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6)
                            )/19
        FMScoutFile.IFBde = FMScoutFile.IFBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IFBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IFBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def NNFBdefunc(): 
        FMScoutFile['NNFBde'] = ((FMScoutFile['Hea']) +
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Str'])
                            )/9
        FMScoutFile.NNFBde = FMScoutFile.NNFBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.NNFBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='NNFBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Centre-back roles

    def WCBdefunc(): 
        FMScoutFile['WCBde'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) + 
                            (FMScoutFile['Agg']) + 
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Str'] *0.6)
                            )/19
        FMScoutFile.WCBde = FMScoutFile.WCBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WCBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WCBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WCBsufunc(): 
        FMScoutFile['WCBsu'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) + 
                            (FMScoutFile['Agg']) + 
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str'] * 0.6)
                            )/22
        FMScoutFile.WCBsu = FMScoutFile.WCBsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WCBsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WCBsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WCBatfunc(): 
        FMScoutFile['WCBat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) + 
                            (FMScoutFile['Agg']) + 
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) +
                            (FMScoutFile['Str'] * 0.6)
                            )/22
        FMScoutFile.WCBat = FMScoutFile.WCBat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WCBat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WCBat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def LIBdefunc(): 
        FMScoutFile['LIBde'] = ((FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp'] * 0.6) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str'] * 0.6)
                            )/17
        FMScoutFile.LIBde = FMScoutFile.LIBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.LIBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='LIBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def LIBsufunc(): 
        FMScoutFile['LIBsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp'] * 0.6) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str'] * 0.6)
                            )/19
        FMScoutFile.LIBsu = FMScoutFile.LIBsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.LIBsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='LIBsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def BPDdefunc(): 
        FMScoutFile['BPDde'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp'] * 0.6) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Str'] * 0.6)
                            )/17
        FMScoutFile.BPDde = FMScoutFile.BPDde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.BPDde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='BPDde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def BPDstfunc(): 
        FMScoutFile['BPDst'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Agg'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) + 
                            (FMScoutFile['Cmp'] * 0.6) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Str'] * 0.6)
                            )/16
        FMScoutFile.BPDst = FMScoutFile.BPDst.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.BPDst], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='BPDst', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def BPDcofunc(): 
        FMScoutFile['BPDco'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Hea']) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) + 
                            (FMScoutFile['Cmp'] * 0.6) + 
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Jum']) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Str'] * 0.6)
                            )/16
        FMScoutFile.BPDco = FMScoutFile.BPDco.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.BPDco], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='BPDco', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def NNCBdefunc(): 
        FMScoutFile['NNCBde'] = ((FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Str'] * 0.6)
                            )/11
        FMScoutFile.NNCBde = FMScoutFile.NNCBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.NNCBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='NNCBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def NNCBstfunc(): 
        FMScoutFile['NNCBst'] = ((FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Agg'] * 0.6) +
                            (FMScoutFile['Bra'] * 0.6) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Str'] * 0.6)
                            )/10
        FMScoutFile.NNCBst = FMScoutFile.NNCBst.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.NNCBst], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='NNCBst', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def NNCBcofunc(): 
        FMScoutFile['NNCBco'] = ((FMScoutFile['Hea']) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Jum']) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Str'])
                            )/10
        FMScoutFile.NNCBco = FMScoutFile.NNCBco.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.NNCBco], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='NNCBco', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CBdefunc(): 
        FMScoutFile['CBde'] = ((FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Agg']) + 
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) + 
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Str'] * 0.6)
                            )/13
        FMScoutFile.CBde = FMScoutFile.CBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CBstfunc(): 
        FMScoutFile['CBst'] = ((FMScoutFile['Hea'] * 0.6) + 
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Agg'] * 0.6) + 
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) + 
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) + 
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Str'] * 0.6)
                            )/1
        FMScoutFile.CBst = FMScoutFile.CBst.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CBst], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CBst', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CBcofunc(): 
        FMScoutFile['CBco'] = ((FMScoutFile['Hea']) + 
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp']) + 
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) + 
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Jum']) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Str'])
                            )/12
        FMScoutFile.CBco = FMScoutFile.CBco.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CBco], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CBco', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Defensive midfield roles

    def BWMdefunc():
        FMScoutFile['BWMde'] = ((FMScoutFile['Mar']) +
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Agg'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Pos']) + 
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) + 
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6) + 
                            (FMScoutFile['Str'])
                            )/13
        FMScoutFile.BWMde = FMScoutFile.BWMde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.BWMde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='BWMde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def BWMsufunc():
        FMScoutFile['BWMsu'] = ((FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Agg'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) + 
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6) + 
                            (FMScoutFile['Str'])
                            )/13
        FMScoutFile.BWMsu = FMScoutFile.BWMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.BWMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='BWMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def SVsufunc():
        FMScoutFile['SVsu'] = ((FMScoutFile['Fin']) + 
                            (FMScoutFile['Fir']) + 
                            (FMScoutFile['Lon']) +   
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) + 
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) + 
                            (FMScoutFile['Str'])
                            )/18
        FMScoutFile.SVsu = FMScoutFile.SVsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.SVsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='SVsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def SVatfunc():
        FMScoutFile['SVat'] = ((FMScoutFile['Fin'] * 0.6) + 
                            (FMScoutFile['Fir']) + 
                            (FMScoutFile['Lon'] * 0.6) +   
                            (FMScoutFile['Mar']) + 
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) + 
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) + 
                            (FMScoutFile['Str'])
                            )/18
        FMScoutFile.SVat = FMScoutFile.SVat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.SVat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='SVat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def HBdefunc():
        FMScoutFile['HBde'] = ((FMScoutFile['Fir']) +   
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck'] * 0.6) +   
                            (FMScoutFile['Agg']) + 
                            (FMScoutFile['Ant'] * 0.6) +  
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +  
                            (FMScoutFile['Tea'] * 0.6) + 
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Jum']) +
                            (FMScoutFile['Sta']) + 
                            (FMScoutFile['Str'])
                            )/16
        FMScoutFile.HBde = FMScoutFile.HBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.HBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='HBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def HBdefunc():
        FMScoutFile['HBde'] = ((FMScoutFile['Fir']) +   
                            (FMScoutFile['Mar'] * 0.6) + 
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck'] * 0.6) +   
                            (FMScoutFile['Agg']) + 
                            (FMScoutFile['Ant'] * 0.6) +  
                            (FMScoutFile['Bra']) + 
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +  
                            (FMScoutFile['Tea'] * 0.6) + 
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Jum']) +
                            (FMScoutFile['Sta']) + 
                            (FMScoutFile['Str'])
                            )/16
        FMScoutFile.HBde = FMScoutFile.HBde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.HBde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='HBde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def ANCdefunc():
        FMScoutFile['ANCde'] = ((FMScoutFile['Mar'] * 0.6) +  
                            (FMScoutFile['Tck'] * 0.6) +  
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +  
                            (FMScoutFile['Tea']) +
                            (FMScoutFile['Str'])
                            )/9
        FMScoutFile.ANCde = FMScoutFile.ANCde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.ANCde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='ANCde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DMdefunc():
        FMScoutFile['DMde'] = ((FMScoutFile['Mar']) +
                            (FMScoutFile['Pas']) +    
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Agg']) +   
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +  
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Sta']) + 
                            (FMScoutFile['Str'])
                            )/13
        FMScoutFile.DMde = FMScoutFile.DMde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DMde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DMde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DMsufunc():
        FMScoutFile['DMsu'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) +
                            (FMScoutFile['Pas']) +    
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Agg']) +   
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Pos'] * 0.6) +  
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Sta']) + 
                            (FMScoutFile['Str'])
                            )/14
        FMScoutFile.DMsu = FMScoutFile.DMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def RPMsufunc():
        FMScoutFile['RPMsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) +    
                            (FMScoutFile['Tec'] * 0.6) +  
                            (FMScoutFile['Ant'] * 0.6) + 
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos']) +  
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor']) + 
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6) 
                            )/19
        FMScoutFile.RPMsu = FMScoutFile.RPMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.RPMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='RPMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def REGsufunc():
        FMScoutFile['REGsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) +    
                            (FMScoutFile['Tec'] * 0.6) +  
                            (FMScoutFile['Ant']) + 
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Bal'])  
                            )/13
        FMScoutFile.REGsu = FMScoutFile.REGsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.REGsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='REGsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DLPMdefunc():
        FMScoutFile['DLPde'] = ((FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck']) +   
                            (FMScoutFile['Tec'] * 0.6) +  
                            (FMScoutFile['Ant']) + 
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Bal'])  
                            )/13
        FMScoutFile.DLPde = FMScoutFile.DLPde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DLPde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DLPde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DLPMsufunc():
        FMScoutFile['DLPsu'] = ((FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['OtB']) +   
                            (FMScoutFile['Tec'] * 0.6) +  
                            (FMScoutFile['Ant']) + 
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Bal'])  
                            )/13
        FMScoutFile.DLPsu = FMScoutFile.DLPsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DLPsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DLPsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Central midfield roles 

    def CMdefunc():
        FMScoutFile['CMde'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Sta'])  
                            )/14
        FMScoutFile.CMde = FMScoutFile.CMde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CMde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CMde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CMsufunc():
        FMScoutFile['CMsu'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Sta'])  
                            )/13
        FMScoutFile.CMsu = FMScoutFile.CMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CMatfunc():
        FMScoutFile['CMat'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Sta'])  
                            )/14
        FMScoutFile.CMat = FMScoutFile.CMat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CMat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CMat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CARsufunc():
        FMScoutFile['CARsu'] = ((FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Tea']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Sta'])  
                            )/14
        FMScoutFile.CARsu = FMScoutFile.CARsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CARsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CARsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def MEZsufunc():
        FMScoutFile['MEZsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Bal'])  +
                            (FMScoutFile['Sta'])  
                            )/15
        FMScoutFile.MEZsu = FMScoutFile.MEZsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.MEZsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='MEZsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def MEZatfunc():
        FMScoutFile['MEZat'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Bal'])  +
                            (FMScoutFile['Sta'])  
                            )/17
        FMScoutFile.MEZat = FMScoutFile.MEZat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.MEZat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='MEZat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def B2Bsufunc():
        FMScoutFile['B2Bsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta'] * 0.6) +
                            (FMScoutFile['Str'])  
                            )/20
        FMScoutFile.B2Bsu = FMScoutFile.B2Bsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.B2Bsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='B2Bsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Wide midfield roles 

    def WPMsufunc():
        FMScoutFile['WPMsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Agi']) 
                            )/10
        FMScoutFile.WPMsu = FMScoutFile.WPMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WPMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WPMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WPMatfunc():
        FMScoutFile['WPMat'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Agi']) 
                            )/13
        FMScoutFile.WPMat = FMScoutFile.WPMat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WPMat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WPMat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DWdefunc():
        FMScoutFile['DWde'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) +
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Sta'] * 0.6) 
                            )/18
        FMScoutFile.DWde = FMScoutFile.DWde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DWde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DWde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DWsufunc():
        FMScoutFile['DWsu'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tck']) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Sta'] * 0.6) 
                            )/18
        FMScoutFile.DWsu = FMScoutFile.DWsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DWsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DWsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WMdefunc():
        FMScoutFile['WMde'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Mar']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Pos'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Sta']) 
                            )/14
        FMScoutFile.WMde = FMScoutFile.WMde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WMde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WMde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WMsufunc():
        FMScoutFile['WMsu'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck'] * 0.6) + 
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Pos']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) 
                            )/15
        FMScoutFile.WMsu = FMScoutFile.WMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WMatfunc():
        FMScoutFile['WMat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tck']) + 
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) 
                            )/15
        FMScoutFile.WMat = FMScoutFile.WMat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WMat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WMat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Central attacking midfield roles

    def APMsufunc():
        FMScoutFile['APMsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Agi'])  
                            )/12
        FMScoutFile.APMsu = FMScoutFile.APMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.APMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='APMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def APMatfunc():
        FMScoutFile['APMat'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Acc']) +
                            (FMScoutFile['Agi'])  
                            )/12
        FMScoutFile.APMat = FMScoutFile.APMat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.APMat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='APMat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def AMsufunc():
        FMScoutFile['AMsu'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Lon'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Agi'])  
                            )/12
        FMScoutFile.AMsu = FMScoutFile.AMsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.AMsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='AMsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def AMatfunc():
        FMScoutFile['AMat'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Lon'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Agi'])  
                            )/13
        FMScoutFile.AMat = FMScoutFile.AMat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.AMat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='AMat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def SSatfunc():
        FMScoutFile['SSat'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) + 
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pace']) + 
                            (FMScoutFile['Sta'])  
                            )/16
        FMScoutFile.SSat = FMScoutFile.SSat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.SSat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='SSat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def TREatfunc():
        FMScoutFile['TREat'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) + 
                            (FMScoutFile['Bal']) 
                            )/14
        FMScoutFile.TREat = FMScoutFile.TREat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.TREat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='TREat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def ENGsufunc():
        FMScoutFile['ENGsu'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) + 
                            (FMScoutFile['Bal']) 
                            )/14
        FMScoutFile.ENGsu = FMScoutFile.ENGsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.ENGsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='ENGsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Wide attacking midfield roles 

    def IWsufunc():
        FMScoutFile['IWsu'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/16
        FMScoutFile.IWsu = FMScoutFile.IWsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IWsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IWsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IWatfunc():
        FMScoutFile['IWat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'] * 0.6) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/18
        FMScoutFile.IWat = FMScoutFile.IWat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IWat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IWat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IFsufunc():
        FMScoutFile['IFsu'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/17
        FMScoutFile.IFsu = FMScoutFile.IFsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IFsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IFsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def IFatfunc():
        FMScoutFile['IFat'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/16
        FMScoutFile.IFat = FMScoutFile.IFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.IFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='IFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WINsufunc():
        FMScoutFile['WINsu'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/12
        FMScoutFile.WINsu = FMScoutFile.WINsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WINsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WINsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WINatfunc():
        FMScoutFile['WINat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/14
        FMScoutFile.WINat = FMScoutFile.WINat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WINat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WINat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def RMDatfunc():
        FMScoutFile['RMDat'] = ((FMScoutFile['Cro'] * 0.6) +
                            (FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) + 
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Pac']) +
                            (FMScoutFile['Sta']) 
                            )/15
        FMScoutFile.RMDat = FMScoutFile.RMDat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.RMDat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='RMDat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WTFsufunc():
        FMScoutFile['WTFsu'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str']) 
                            )/12
        FMScoutFile.WTFsu = FMScoutFile.WTFsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WTFsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WTFsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def WTFatfunc():
        FMScoutFile['WTFat'] = ((FMScoutFile['Cro']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Bal']) +
                            (FMScoutFile['Jum'] * 0.6) +
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str']) 
                            )/12
        FMScoutFile.WTFat = FMScoutFile.WTFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.WTFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='WTFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    # Table columns for Striker roles 

    def AFatfunc():
        FMScoutFile['AFat'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Pas']) + 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) 
                            )/15
        FMScoutFile.AFat = FMScoutFile.AFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.AFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='AFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CFsufunc():
        FMScoutFile['CFsu'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Lon'] * 0.6) +
                            (FMScoutFile['Pas'] * 0.6)+ 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea']) +
                            (FMScoutFile['Vis'] * 0.6) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Jum']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str'] * 0.6) 
                            )/21
        FMScoutFile.CFsu = FMScoutFile.CFsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CFsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CFsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def CFatfunc():
        FMScoutFile['CFat'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Lon']) +
                            (FMScoutFile['Pas'])+ 
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea']) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Wor']) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'] * 0.6) +
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Jum']) + 
                            (FMScoutFile['Pac']) + 
                            (FMScoutFile['Sta']) +
                            (FMScoutFile['Str'] * 0.6) 
                            )/21
        FMScoutFile.CFat = FMScoutFile.CFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.CFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='CFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def POAatfunc():
        FMScoutFile['POAat'] = ((FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea']) +
                            (FMScoutFile['Tec']) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi'])  
                            )/10
        FMScoutFile.POAat = FMScoutFile.POAat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.POAat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='POAat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def PFdefunc():
        FMScoutFile['PFde'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Agg'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +  
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) +
                            (FMScoutFile['Str']) 
                            )/14
        FMScoutFile.PFde = FMScoutFile.PFde.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.PFde], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='PFde', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def PFsufunc():
        FMScoutFile['PFsu'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Pas']) +
                            (FMScoutFile['Agg'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +  
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) +
                            (FMScoutFile['Str']) 
                            )/16
        FMScoutFile.PFsu = FMScoutFile.PFsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.PFsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='PFsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def PFatfunc():
        FMScoutFile['PFat'] = ((FMScoutFile['Fir']) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Agg'] * 0.6) +
                            (FMScoutFile['Ant'] * 0.6) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Cnt']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Wor'] * 0.6) +
                            (FMScoutFile['Acc'] * 0.6) +
                            (FMScoutFile['Agi']) +  
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Pac'] * 0.6) +
                            (FMScoutFile['Sta'] * 0.6) +
                            (FMScoutFile['Str']) 
                            )/16
        FMScoutFile.PFat = FMScoutFile.PFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.PFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='PFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DLFsufunc():
        FMScoutFile['DLFsu'] = ((FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Agi']) +  
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Str']) 
                            )/14
        FMScoutFile.DLFsu = FMScoutFile.DLFsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DLFsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DLFsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def DLFatfunc():
        FMScoutFile['DLFat'] = ((FMScoutFile['Dri']) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Vis']) +
                            (FMScoutFile['Agi']) +  
                            (FMScoutFile['Bal']) + 
                            (FMScoutFile['Str']) 
                            )/15
        FMScoutFile.DLFat = FMScoutFile.DLFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.DLFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='DLFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def TFsufunc():
        FMScoutFile['TFsu'] = ((FMScoutFile['Fin']) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['Cmp']) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB']) +
                            (FMScoutFile['Tea'] * 0.6) +
                            (FMScoutFile['Bal'] * 0.6) + 
                            (FMScoutFile['Jum'] * 0.6) + 
                            (FMScoutFile['Str'] * 0.6) 
                            )/13
        FMScoutFile.TFsu = FMScoutFile.TFsu.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.TFsu], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='TFsu', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def TFatfunc():
        FMScoutFile['TFat'] = ((FMScoutFile['Fin'] * 0.6) +
                            (FMScoutFile['Fir']) +
                            (FMScoutFile['Hea'] * 0.6) +
                            (FMScoutFile['Agg']) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Bra'] * 0.6) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea']) +
                            (FMScoutFile['Bal'] * 0.6) + 
                            (FMScoutFile['Jum'] * 0.6) + 
                            (FMScoutFile['Str'] * 0.6) 
                            )/13
        FMScoutFile.TFat = FMScoutFile.TFat.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.TFat], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='TFat', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.

    def F9sufunc():
        FMScoutFile['F9su'] = ((FMScoutFile['Dri'] * 0.6) +
                            (FMScoutFile['Fir'] * 0.6) +
                            (FMScoutFile['Fin']) +
                            (FMScoutFile['Pas'] * 0.6) +
                            (FMScoutFile['Tec'] * 0.6) +
                            (FMScoutFile['Ant']) +
                            (FMScoutFile['Cmp'] * 0.6) +
                            (FMScoutFile['Dec'] * 0.6) +
                            (FMScoutFile['Fla']) +
                            (FMScoutFile['OtB'] * 0.6) +
                            (FMScoutFile['Tea']) 
                            (FMScoutFile['Vis'] * 0.6) + 
                            (FMScoutFile['Acc'] * 0.6) + 
                            (FMScoutFile['Agi'] * 0.6) + 
                            (FMScoutFile['Bal']) 
                            )/15
        FMScoutFile.F9su = FMScoutFile.F9su.round(1) # Rounds the result to the nearest tenth
        Output = pd.concat([Details, FMScoutFile.F9su], axis=1, join='inner') # Adds the column to the table with the columns with player details in it and creates one table.
        html = generate_html(Output.sort_values(by='F9su', ascending=False)) # Generates an html file containing the new dataframe and sorts in in descending order by the role that is being analysed.
        filename = str('FMScoutOutput' + ".html") # Creates a file and gives it the name of 'FMScoutOutput'.
        open(filename, "w", encoding="utf-8").write(html) # Opens the file on the system and adds the data to it.
        webbrowser.open(os.path.realpath(filename)) # Opens the newly created file in the browser.


    # Intro and asks which role is being analysed.
    # Then based upon the input of the user or RoleInput == passes the custom function of the role that the input text matches to.
    # The input text is matched to one of many possible inputs that has been used to describe the role that the user wants to analyse.
    # The input text is caseor RoleInput == space and dash insensitive for user experience.
    def RoleQs(): # Asks user which role they would like analysed.

            # Goal-keeper roles

            if RoleInput == 'gk'  or RoleInput ==  'gkdefend'  or RoleInput ==  'gk(defend)'  or RoleInput ==  'gk(de)'  or RoleInput ==  'goalkeeper'  or RoleInput ==  'goal-keeper'   or RoleInput ==  'goalkeeper(de)'   or RoleInput ==  'goal-keeper(de)'   or RoleInput ==  'goalkeeperde'  or RoleInput ==  'goal-keeperde'   or RoleInput ==  'goalkeeperdefend'  or RoleInput ==  'goal-keeperdefend':
                GKfunc()
                 
            elif RoleInput == 'sk'  or RoleInput ==  'sk(defend)'  or RoleInput ==  'skdefend'  or RoleInput ==  'sk(de)'  or RoleInput ==  'skde'  or RoleInput ==  'sweeperkeeper'  or RoleInput ==  'sweeper-keeper'  or RoleInput ==  'sweeperkeeper(de)'  or RoleInput ==  'sweeper-keeper(de)'  or RoleInput ==  'sweeperkeeperde'  or RoleInput ==  'sweeper-keeperde'  or RoleInput ==  'sweeper-keeperdefend'  or RoleInput ==  'sweeperkeeperdefend' :
                SKdefunc()
                 
            elif RoleInput == 'sksu'  or RoleInput ==  'sksupport' or RoleInput ==  'sk(support)' or RoleInput ==  'sk(su)' or RoleInput ==  'sweeperkeeper(su)'  or RoleInput ==  'sweeper-keeper(su)'  or RoleInput ==  'sweeperkeepersu'  or RoleInput ==  'sweeper-keepersu' or RoleInput ==  'sweeper-keepersupport' or RoleInput ==  'sweeperkeepersupport' :
                SKsufunc()
                 
            elif RoleInput == 'skat'  or RoleInput ==  'skattack' or RoleInput ==  'sk(attack)' or RoleInput ==  'sk(at)' or RoleInput ==  'sweeperkeeper(at)'  or RoleInput ==  'sweeper-keeper(at)'  or RoleInput ==  'sweeperkeeperat'  or RoleInput ==  'sweeper-keeperat' or RoleInput ==  'sweeperkeeperattack' or RoleInput ==  'sweeper-keeperattack' :
                SKatfunc()
                 

            # Full-back roles 

            elif RoleInput == 'fb'  or RoleInput ==  'fbdefend' or RoleInput ==  'fb(defend)' or RoleInput ==  'fb(de)' or RoleInput ==  'fbde'  or RoleInput ==  'fullback'  or RoleInput ==  'full-back'  or RoleInput ==  'fullback(de)'  or RoleInput ==  'full-back(de)'  or RoleInput ==  'fullbackde'  or RoleInput ==  'full-backde'  or RoleInput ==  'fullbackdefend'  or RoleInput ==  'full-backdefend':
                FBdefunc()
                 
            elif RoleInput == 'fbsu' or RoleInput ==  'fbsupport' or RoleInput ==  'fb(support)' or RoleInput ==  'fb(su)'  or RoleInput ==  'fullback(su)'  or RoleInput ==  'full-back(su)'  or RoleInput ==  'fullbacksu'  or RoleInput ==  'full-backsu'  or RoleInput ==  'fullbacksupport'  or RoleInput ==  'full-backsupport'  or RoleInput ==  'fullback(support)'  or RoleInput ==  'full-back(support)' :
                FBsufunc()
                 
            elif RoleInput == 'fbat' or RoleInput ==  'fbattack' or RoleInput ==  'fb(attack)'  or RoleInput ==  'fb(at)' or RoleInput ==  'fullback(at)'  or RoleInput ==  'full-back(at)'  or RoleInput ==  'fullbackat'  or RoleInput ==  'full-backat'  or RoleInput ==  'fullbackattack'  or RoleInput ==  'full-backattack'  or RoleInput ==  'fullback(attack)'  or RoleInput ==  'full-back(attack)' :
                FBatfunc()
                 
            elif RoleInput == 'wbde' or RoleInput ==  'wbdefend' or RoleInput ==  'wb(defend)' or RoleInput ==  'wb(de)'  or RoleInput ==  'wingback(de)'  or RoleInput ==  'wing-back(de)'  or RoleInput ==  'wingbackde'  or RoleInput ==  'wing-backde'  or RoleInput ==  'wingbackdefend'  or RoleInput ==  'wing-backdefend'  or RoleInput ==  'wingback(defend)'  or RoleInput ==  'wing-back(defend)' :
                WBdefunc()
                 
            elif RoleInput == 'wbsu'  or RoleInput == 'wb' or RoleInput == 'wingback' or RoleInput == 'wing-back' or RoleInput ==  'wbsupport' or RoleInput ==  'wb(support)' or RoleInput ==  'wb(su)' or RoleInput ==  'wingback(su)'  or RoleInput ==  'wing-back(su)'  or RoleInput ==  'wingbacksu'  or RoleInput ==  'wing-backsu'  or RoleInput ==  'wingbacksupport'  or RoleInput ==  'wing-backsupport'  or RoleInput ==  'wingback(support)'  or RoleInput ==  'wing-back(support)' :
                WBsufunc()
                 
            elif RoleInput == 'wbat'   or RoleInput ==  'wb(at)'   or RoleInput ==  'wbattack'   or RoleInput ==  'wb(attack)'   or RoleInput ==  'wingback(at)'    or RoleInput ==  'wing-back(at)'    or RoleInput ==  'wingbackat'    or RoleInput ==  'wing-backat'    or RoleInput ==  'wingbackattack'    or RoleInput ==  'wing-backattack'    or RoleInput ==  'wingback(attack)'    or RoleInput ==  'wing-back(attack)':
                WBatfunc()
                 
            elif RoleInput == 'cwbsu'  or RoleInput ==  'cwb(su)' or RoleInput ==  'cwbsupport' or RoleInput ==  'cwb(support)' or RoleInput ==  'completewingback(su)'  or RoleInput ==  'completewing-back(su)'  or RoleInput ==  'completewingbacksu'  or RoleInput ==  'completewing-backsu'  or RoleInput ==  'completewingbacksupport'  or RoleInput ==  'completewing-backsupport'  or RoleInput ==  'completewingback(support)'  or RoleInput ==  'completewing-back(support)' or RoleInput ==  'complete-wingback(su)'  or RoleInput ==  'complete-wingbacksu'  or RoleInput ==  'complete-wing-backsu'  or RoleInput ==  'complete-wingbacksupport'  or RoleInput ==  'complete-wing-backsupport'  or RoleInput ==  'complete-wingback(support)'  or RoleInput ==  'complete-wing-back(support)' :
                CWBsufunc()
                 
            elif RoleInput == 'cwbat'  or RoleInput ==  'cwb(at)' or RoleInput ==  'cwbattack' or RoleInput ==  'cwb(attack)' or RoleInput ==  'completewingback(at)'  or RoleInput ==  'completewing-back(at)'  or RoleInput ==  'completewingbackat'  or RoleInput ==  'completewing-backat'  or RoleInput ==  'completewingbackattack'  or RoleInput ==  'completewing-backattack'  or RoleInput ==  'completewingback(attack)'  or RoleInput ==  'completewing-back(attack)' or RoleInput ==  'complete-wingback(at)'  or RoleInput ==  'complete-wingbackat'  or RoleInput ==  'complete-wing-backat'  or RoleInput ==  'complete-wingbackattack'  or RoleInput ==  'complete-wing-backattack'  or RoleInput ==  'complete-wingback(attack)'  or RoleInput ==  'complete-wing-back(attack)' :
                CWBatfunc()
                 
            elif RoleInput == 'iwb'  or RoleInput == 'iwbde'  or RoleInput ==  'iwb(de)' or RoleInput ==  'iwbdefend' or RoleInput ==  'iwb(defend)' or RoleInput == 'invertedwingback' or RoleInput == 'invertedwing-back' or RoleInput == 'inverted-wing-back' or RoleInput == 'inverted-wingback' or RoleInput ==  'invertedwingback(de)'  or RoleInput ==  'invertedwing-back(de)'  or RoleInput ==  'invertedwingbackde'  or RoleInput ==  'invertedwing-backde'  or RoleInput ==  'invertedwingbackdefend'  or RoleInput ==  'invertedwing-backdefend'  or RoleInput ==  'invertedwingback(defend)'  or RoleInput ==  'invertedwing-back(defend)' or RoleInput ==  'inverted-wingback(de)'  or RoleInput ==  'inverted-wingbackde'  or RoleInput ==  'inverted-wing-backde'  or RoleInput ==  'inverted-wingbackdefend'  or RoleInput ==  'inverted-wing-backdefend'  or RoleInput ==  'inverted-wingback(defend)'  or RoleInput ==  'inverted-wing-back(defend)' :
                IWBdefunc()
                 
            elif RoleInput == 'iwbsu'  or RoleInput ==  'iwb(su)' or RoleInput ==  'iwbsupport' or RoleInput ==  'iwb(support)' or RoleInput ==  'invertedwingback(su)'  or RoleInput ==  'invertedwing-back(su)'  or RoleInput ==  'invertedwingbacksu'  or RoleInput ==  'invertedwing-backsu'  or RoleInput ==  'invertedwingbacksupport'  or RoleInput ==  'invertedwing-backsupport'  or RoleInput ==  'invertedwingback(support)'  or RoleInput ==  'invertedwing-back(support)' or RoleInput ==  'inverted-wingback(su)'  or RoleInput ==  'inverted-wingbacksu'  or RoleInput ==  'inverted-wing-backsu'  or RoleInput ==  'inverted-wingbacksupport'  or RoleInput ==  'inverted-wing-backsupport'  or RoleInput ==  'inverted-wingback(support)'  or RoleInput ==  'inverted-wing-back(support)' :
                IWBsufunc()
                 
            elif RoleInput == 'iwbat'  or RoleInput ==  'iwb(at)' or RoleInput ==  'iwbattack' or RoleInput ==  'iwb(attack)' or RoleInput ==  'invertedwingback(at)'  or RoleInput ==  'invertedwing-back(at)'  or RoleInput ==  'invertedwingbackat'  or RoleInput ==  'invertedwing-backat'  or RoleInput ==  'invertedwingbackattack'  or RoleInput ==  'invertedwing-backattack'  or RoleInput ==  'invertedwingback(attack)'  or RoleInput ==  'invertedwing-back(attack)' or RoleInput ==  'inverted-wingback(at)'  or RoleInput ==  'inverted-wingbackat'  or RoleInput ==  'inverted-wing-backat'  or RoleInput ==  'inverted-wingbackattack'  or RoleInput ==  'inverted-wing-backattack'  or RoleInput ==  'inverted-wingback(attack)'  or RoleInput ==  'inverted-wing-back(attack)' :
                IWBatfunc()
                 
            elif RoleInput == 'ifbde'  or RoleInput ==  'ifb(de)' or RoleInput ==  'ifbdefend' or RoleInput ==  'ifb(defend)' or RoleInput ==  'ifb' or RoleInput ==  'invertedfullback' or RoleInput ==  'invertedfull-back'  or RoleInput ==  'inverted-fullback' or RoleInput ==  'invertedfullback(de)'  or RoleInput ==  'invertedfull-back(de)'  or RoleInput ==  'invertedfullbackde'  or RoleInput ==  'invertedfull-backde'  or RoleInput ==  'invertedfullbackdefend'  or RoleInput ==  'invertedfull-backdefend'  or RoleInput ==  'invertedfullback(defend)'  or RoleInput ==  'invertedfull-back(defend)' or RoleInput ==  'inverted-fullback(de)'  or RoleInput ==  'inverted-fullbackde'  or RoleInput ==  'inverted-full-backde'  or RoleInput ==  'inverted-fullbackdefend'  or RoleInput ==  'inverted-full-backdefend'  or RoleInput ==  'inverted-fullback(defend)'  or RoleInput ==  'inverted-full-back(defend)' :
                IFBdefunc()
                 
            elif RoleInput == 'nnfbde' or RoleInput == 'nnfb(de)' or RoleInput == 'nnfbdefend' or RoleInput == 'nnfb(defend)' or RoleInput == 'nnfb' or RoleInput ==  'nononsensefullback' or RoleInput ==  'nononsensefull-back'  or RoleInput ==  'nononsense-fullback' or RoleInput ==  'no-nonsensefullback' or RoleInput ==  'no-nonsense-fullback' or RoleInput ==  'no-nonsense-full-back' or RoleInput ==  'nononsense-full-back' or RoleInput ==  'no-nonsensefull-back' or RoleInput ==  'nononsensefullback(de)' or RoleInput ==  'nononsensefull-back(de)'  or RoleInput ==  'nononsense-fullback(de)' or RoleInput ==  'no-nonsensefullback(de)' or RoleInput ==  'no-nonsense-fullback(de)' or RoleInput ==  'no-nonsense-full-back(de)' or RoleInput ==  'nononsense-full-back(de)' or RoleInput ==  'no-nonsensefull-back(de)' or RoleInput ==  'nononsensefullback(defend)' or RoleInput ==  'nononsensefull-back(defend)'  or RoleInput ==  'nononsense-fullback(defend)' or RoleInput ==  'no-nonsensefullback(defend)' or RoleInput ==  'no-nonsense-fullback(defend)' or RoleInput ==  'no-nonsense-full-back(defend)' or RoleInput ==  'nononsense-full-back(defend)' or RoleInput ==  'no-nonsensefull-back(defend)' or RoleInput ==  'nononsensefullbackdefend' or RoleInput ==  'nononsensefull-backdefend'  or RoleInput ==  'nononsense-fullbackdefend' or RoleInput ==  'no-nonsensefullbackdefend' or RoleInput ==  'no-nonsense-fullbackdefend' or RoleInput ==  'no-nonsense-full-backdefend' or RoleInput ==  'nononsense-full-backdefend' or RoleInput ==  'no-nonsensefull-backdefend':
                NNFBdefunc()
                 

            # Centre-back roles 

            elif RoleInput == 'wcbde'  or RoleInput ==  'wcbdefend' or RoleInput ==  'wcb(defend)' or RoleInput ==  'wcb(de)' or RoleInput ==  'wcb' or RoleInput ==  'widecentreback' or RoleInput ==  'widecentre-back'  or RoleInput ==  'wide-centreback' or RoleInput ==  'widecentreback(de)'  or RoleInput ==  'widecentre-back(de)'  or RoleInput ==  'widecentrebackde'  or RoleInput ==  'widecentre-backde'  or RoleInput ==  'widecentrebackdefend'  or RoleInput ==  'widecentre-backdefend'  or RoleInput ==  'widecentreback(defend)'  or RoleInput ==  'widecentre-back(defend)' or RoleInput ==  'wide-centreback(de)'  or RoleInput ==  'wide-centrebackde'  or RoleInput ==  'wide-centre-backde'  or RoleInput ==  'wide-centrebackdefend'  or RoleInput ==  'wide-centre-backdefend'  or RoleInput ==  'wide-centreback(defend)'  or RoleInput ==  'wide-centre-back(defend)' :
                WCBdefunc()
                 
            elif RoleInput == 'wcbsu'  or RoleInput ==  'wcbsupport' or RoleInput ==  'wcb(support)' or RoleInput ==  'wcb(su)' or RoleInput ==  'widecentreback(su)'  or RoleInput ==  'widecentre-back(su)'  or RoleInput ==  'widecentrebacksu'  or RoleInput ==  'widecentre-backsu'  or RoleInput ==  'widecentrebacksupport'  or RoleInput ==  'widecentre-backsupport'  or RoleInput ==  'widecentreback(support)'  or RoleInput ==  'widecentre-back(support)' or RoleInput ==  'wide-centreback(su)'  or RoleInput ==  'wide-centrebacksu'  or RoleInput ==  'wide-centre-backsu'  or RoleInput ==  'wide-centrebacksupport'  or RoleInput ==  'wide-centre-backsupport'  or RoleInput ==  'wide-centreback(support)'  or RoleInput ==  'wide-centre-back(support)' :
                WCBsufunc()
                 
            elif RoleInput == 'wcbat'  or RoleInput ==  'wcbattack' or RoleInput ==  'wcb(attack)' or RoleInput ==  'wcb(at)' or RoleInput ==  'widecentreback(at)'  or RoleInput ==  'widecentre-back(at)'  or RoleInput ==  'widecentrebackat'  or RoleInput ==  'widecentre-backat'  or RoleInput ==  'widecentrebackattack'  or RoleInput ==  'widecentre-backattack'  or RoleInput ==  'widecentreback(attack)'  or RoleInput ==  'widecentre-back(attack)' or RoleInput ==  'wide-centreback(at)'  or RoleInput ==  'wide-centrebackat'  or RoleInput ==  'wide-centre-backat'  or RoleInput ==  'wide-centrebackattack'  or RoleInput ==  'wide-centre-backattack'  or RoleInput ==  'wide-centreback(attack)'  or RoleInput ==  'wide-centre-back(attack)' :
                WCBatfunc()
                 
            elif RoleInput == 'cbde' or RoleInput ==  'cbdefend' or RoleInput ==  'cb(defend)' or RoleInput ==  'cb' or RoleInput ==  'centreback' or RoleInput ==  'centre-back' or RoleInput ==  'cb(de)'  or RoleInput ==  'centreback(de)'  or RoleInput ==  'centre-back(de)'  or RoleInput ==  'centrebackde'  or RoleInput ==  'centre-backde'  or RoleInput ==  'centrebackdefend'  or RoleInput ==  'centre-backdefend'  or RoleInput ==  'centreback(defend)'  or RoleInput ==  'centre-back(defend)' :
                CBdefunc()
                 
            elif RoleInput == 'cbst' or RoleInput ==  'cbstopper' or RoleInput ==  'cb(stopper)' or RoleInput ==  'cb(st)'  or RoleInput ==  'centreback(st)'  or RoleInput ==  'centre-back(st)'  or RoleInput ==  'centrebackst'  or RoleInput ==  'centre-backst'  or RoleInput ==  'centrebackstopper'  or RoleInput ==  'centre-backstopper'  or RoleInput ==  'centreback(stopper)'  or RoleInput ==  'centre-back(stopper)' :
                CBstfunc()
                 
            elif RoleInput == 'cbco' or RoleInput ==  'cbcover' or RoleInput ==  'cb(cover)' or RoleInput ==  'cb(co)'  or RoleInput ==  'centreback(co)'  or RoleInput ==  'centre-back(co)'  or RoleInput ==  'centrebackco'  or RoleInput ==  'centre-backco'  or RoleInput ==  'centrebackcover'  or RoleInput ==  'centre-backcover'  or RoleInput ==  'centreback(cover)'  or RoleInput ==  'centre-back(cover)' :
                CBcofunc()
                 
            elif RoleInput == 'nncbde'  or RoleInput ==  'nncb(de)' or RoleInput ==  'nncbdefend' or RoleInput ==  'nncb(defend)' or RoleInput ==  'nncb' or RoleInput ==  'nononsensecentreback' or RoleInput ==  'nononsensecentre-back'  or RoleInput ==  'nononsense-centreback' or RoleInput ==  'no-nonsensecentreback' or RoleInput ==  'no-nonsense-centreback' or RoleInput ==  'no-nonsense-centre-back' or RoleInput ==  'nononsense-centre-back' or RoleInput ==  'no-nonsensecentre-back' or RoleInput ==  'nononsensecentreback(de)' or RoleInput ==  'nononsensecentre-back(de)'  or RoleInput ==  'nononsense-centreback(de)' or RoleInput ==  'no-nonsensecentreback(de)' or RoleInput ==  'no-nonsense-centreback(de)' or RoleInput ==  'no-nonsense-centre-back(de)' or RoleInput ==  'nononsense-centre-back(de)' or RoleInput ==  'no-nonsensecentre-back(de)' or RoleInput ==  'nononsensecentreback(defend)' or RoleInput ==  'nononsensecentre-back(defend)'  or RoleInput ==  'nononsense-centreback(defend)' or RoleInput ==  'no-nonsensecentreback(defend)' or RoleInput ==  'no-nonsense-centreback(defend)' or RoleInput ==  'no-nonsense-centre-back(defend)' or RoleInput ==  'nononsense-centre-back(defend)' or RoleInput ==  'no-nonsensecentre-back(defend)' or RoleInput ==  'nononsensecentrebackdefend' or RoleInput ==  'nononsensecentre-backdefend'  or RoleInput ==  'nononsense-centrebackdefend' or RoleInput ==  'no-nonsensecentrebackdefend' or RoleInput ==  'no-nonsense-centrebackdefend' or RoleInput ==  'no-nonsense-centre-backdefend' or RoleInput ==  'nononsense-centre-backdefend' or RoleInput ==  'no-nonsensecentre-backdefend' :
                NNCBdefunc()
                 
            elif RoleInput == 'bpdde'  or RoleInput ==  'bpddefend' or RoleInput ==  'bpd(defend)' or RoleInput ==  'bpd(de)' or RoleInput ==  'bpd' or RoleInput ==  'ballplayingdefender' or RoleInput ==  'ballplaying-defender'  or RoleInput ==  'ball-playingdefender' or RoleInput ==  'ballplayingdefender(de)'  or RoleInput ==  'ballplaying-defender(de)'  or RoleInput ==  'ballplayingdefenderde'  or RoleInput ==  'ballplaying-defenderde'  or RoleInput ==  'ballplayingdefenderdefend'  or RoleInput ==  'ballplaying-defenderdefend'  or RoleInput ==  'ballplayingdefender(defend)'  or RoleInput ==  'ballplaying-defender(defend)' or RoleInput ==  'ball-playingdefender(de)'  or RoleInput ==  'ball-playingdefenderde'  or RoleInput ==  'ball-playing-defenderde'  or RoleInput ==  'ball-playingdefenderdefend'  or RoleInput ==  'ball-playing-defenderdefend'  or RoleInput ==  'ball-playingdefender(defend)'  or RoleInput ==  'ball-playing-defender(defend)' :
                BPDdefunc()
                 
            elif RoleInput == 'bpdst'  or RoleInput ==  'bpdstopper' or RoleInput ==  'bpd(stopper)' or RoleInput ==  'bpd(st)' or RoleInput ==  'ballplayingdefender(st)'  or RoleInput ==  'ballplaying-defender(st)'  or RoleInput ==  'ballplayingdefenderst'  or RoleInput ==  'ballplaying-defenderst'  or RoleInput ==  'ballplayingdefenderstopper'  or RoleInput ==  'ballplaying-defenderstopper'  or RoleInput ==  'ballplayingdefender(stopper)'  or RoleInput ==  'ballplaying-defender(stopper)' or RoleInput ==  'ball-playingdefender(st)'  or RoleInput ==  'ball-playingdefenderst'  or RoleInput ==  'ball-playing-defenderst'  or RoleInput ==  'ball-playingdefenderstopper'  or RoleInput ==  'ball-playing-defenderstopper'  or RoleInput ==  'ball-playingdefender(stopper)'  or RoleInput ==  'ball-playing-defender(stopper)' :
                BPDstfunc()
                 
            elif RoleInput == 'bpdco'  or RoleInput ==  'bpdcover' or RoleInput ==  'bpd(cover)' or RoleInput ==  'bpd(co)' or RoleInput ==  'ballplayingdefender(co)'  or RoleInput ==  'ballplaying-defender(co)'  or RoleInput ==  'ballplayingdefenderco'  or RoleInput ==  'ballplaying-defenderco'  or RoleInput ==  'ballplayingdefendercover'  or RoleInput ==  'ballplaying-defendercover'  or RoleInput ==  'ballplayingdefender(cover)'  or RoleInput ==  'ballplaying-defender(cover)' or RoleInput ==  'ball-playingdefender(co)'  or RoleInput ==  'ball-playingdefenderco'  or RoleInput ==  'ball-playing-defenderco'  or RoleInput ==  'ball-playingdefendercover'  or RoleInput ==  'ball-playing-defendercover'  or RoleInput ==  'ball-playingdefender(cover)'  or RoleInput ==  'ball-playing-defender(cover)' :
                BPDcofunc()
                 
            elif RoleInput == 'libde'   or RoleInput ==  'lib'   or RoleInput ==  'libero'   or RoleInput ==  'lib(de)'   or RoleInput ==  'libdefend'   or RoleInput ==  'lib(defend)'   or RoleInput ==  'libero(de)'   or RoleInput ==  'liberodefend'   or RoleInput ==  'libero(defend)':
                LIBdefunc()
                 
            elif RoleInput == 'libsu'   or RoleInput ==  'lib(su)'   or RoleInput ==  'libsupport'   or RoleInput ==  'lib(support)'   or RoleInput ==  'libero(su)'   or RoleInput ==  'liberosupport'   or RoleInput ==  'libero(support)':
                LIBsufunc()
                 
            
            # Defensive midfield roles 

            elif RoleInput == 'dlpmde'  or RoleInput == 'dlpde' or RoleInput == 'dlp(de)' or RoleInput ==  'dlpm(de)' or RoleInput ==  'dlpmdefend' or RoleInput ==  'dlpm(defend)' or RoleInput ==  'dlpm' or RoleInput ==  'deeplyingplaymaker' or RoleInput ==  'deeplyingplay-maker'  or RoleInput ==  'deeplying-playmaker' or RoleInput ==  'deep-lyingplaymaker' or RoleInput ==  'deep-lying-playmaker' or RoleInput ==  'deep-lying-play-maker' or RoleInput ==  'deeplying-play-maker' or RoleInput ==  'deep-lyingplay-maker' or RoleInput ==  'deeplyingplaymaker(de)' or RoleInput ==  'deeplyingplay-maker(de)'  or RoleInput ==  'deeplying-playmaker(de)' or RoleInput ==  'deep-lyingplaymaker(de)' or RoleInput ==  'deep-lying-playmaker(de)' or RoleInput ==  'deep-lying-play-maker(de)' or RoleInput ==  'deeplying-play-maker(de)' or RoleInput ==  'deep-lyingplay-maker(de)' or RoleInput ==  'deeplyingplaymaker(defend)' or RoleInput ==  'deeplyingplay-maker(defend)'  or RoleInput ==  'deeplying-playmaker(defend)' or RoleInput ==  'deep-lyingplaymaker(defend)' or RoleInput ==  'deep-lying-playmaker(defend)' or RoleInput ==  'deep-lying-play-maker(defend)' or RoleInput ==  'deeplying-play-maker(defend)' or RoleInput ==  'deep-lyingplay-maker(defend)' or RoleInput ==  'deeplyingplaymakerdefend' or RoleInput ==  'deeplyingplay-makerdefend'  or RoleInput ==  'deeplying-playmakerdefend' or RoleInput ==  'deep-lyingplaymakerdefend' or RoleInput ==  'deep-lying-playmakerdefend' or RoleInput ==  'deep-lying-play-makerdefend' or RoleInput ==  'deeplying-play-makerdefend' or RoleInput ==  'deep-lyingplay-makerdefend' :
                DLPMdefunc()
                  
            elif RoleInput == 'dlp' or RoleInput == 'dlpsu' or RoleInput == 'dlp(su)' or RoleInput == 'dlpmsu'  or RoleInput ==  'dlpm(su)' or RoleInput ==  'dlpmsupport' or RoleInput ==  'dlpm(support)' or RoleInput ==  'deeplyingplaymaker(su)' or RoleInput ==  'deeplyingplay-maker(su)'  or RoleInput ==  'deeplying-playmaker(su)' or RoleInput ==  'deep-lyingplaymaker(su)' or RoleInput ==  'deep-lying-playmaker(su)' or RoleInput ==  'deep-lying-play-maker(su)' or RoleInput ==  'deeplying-play-maker(su)' or RoleInput ==  'deep-lyingplay-maker(su)' or RoleInput ==  'deeplyingplaymaker(support)' or RoleInput ==  'deeplyingplay-maker(support)'  or RoleInput ==  'deeplying-playmaker(support)' or RoleInput ==  'deep-lyingplaymaker(support)' or RoleInput ==  'deep-lying-playmaker(support)' or RoleInput ==  'deep-lying-play-maker(support)' or RoleInput ==  'deeplying-play-maker(support)' or RoleInput ==  'deep-lyingplay-maker(support)' or RoleInput ==  'deeplyingplaymakersupport' or RoleInput ==  'deeplyingplay-makersupport'  or RoleInput ==  'deeplying-playmakersupport' or RoleInput ==  'deep-lyingplaymakersupport' or RoleInput ==  'deep-lying-playmakersupport' or RoleInput ==  'deep-lying-play-makersupport' or RoleInput ==  'deeplying-play-makersupport' or RoleInput ==  'deep-lyingplay-makersupport' :
                DLPMsufunc()
                 
            elif RoleInput == 'dmde' or RoleInput ==  'dmdefend' or RoleInput ==  'dm(defend)' or RoleInput ==  'dm' or RoleInput ==  'defensivemid' or RoleInput ==  'defensive-mid' or RoleInput ==  'defensivemidfielder' or RoleInput ==  'defensive-midfielder' or RoleInput ==  'dm(de)'  or RoleInput ==  'defensivemid(de)'  or RoleInput ==  'defensivemidfielder(de)'  or RoleInput ==  'defensive-mid(de)'  or RoleInput ==  'defensive-midfielder(de)'  or RoleInput ==  'defensivemid(defend)'  or RoleInput ==  'defensivemidfielder(defend)'  or RoleInput ==  'defensive-mid(defend)'  or RoleInput ==  'defensive-midfielder(defend)'  or RoleInput ==  'defensivemidde'  or RoleInput ==  'defensivemidfielderde'  or RoleInput ==  'defensive-midde'  or RoleInput ==  'defensive-midfielderde'  or RoleInput ==  'defensivemiddefend'  or RoleInput ==  'defensivemidfielderdefend'  or RoleInput ==  'defensive-middefend'  or RoleInput ==  'defensive-midfielderdefend'  :
                DMdefunc()
                 
            elif RoleInput == 'dmsu' or RoleInput ==  'dmsupport' or RoleInput ==  'dm(support)' or RoleInput ==  'dm' or RoleInput ==  'defensivemid' or RoleInput ==  'defensive-mid' or RoleInput ==  'defensivemidfielder' or RoleInput ==  'defensive-midfielder' or RoleInput ==  'dm(su)'  or RoleInput ==  'defensivemid(su)'  or RoleInput ==  'defensivemidfielder(su)'  or RoleInput ==  'defensive-mid(su)'  or RoleInput ==  'defensive-midfielder(su)'  or RoleInput ==  'defensivemid(support)'  or RoleInput ==  'defensivemidfielder(support)'  or RoleInput ==  'defensive-mid(support)'  or RoleInput ==  'defensive-midfielder(support)'  or RoleInput ==  'defensivemidsu'  or RoleInput ==  'defensivemidfieldersu'  or RoleInput ==  'defensive-midsu'  or RoleInput ==  'defensive-midfieldersu'  or RoleInput ==  'defensivemidsupport'  or RoleInput ==  'defensivemidfieldersupport'  or RoleInput ==  'defensive-midsupport'  or RoleInput ==  'defensive-midfieldersupport'  :
                DMsufunc()
                 
            elif RoleInput == 'regsu'   or RoleInput ==  'reg'   or RoleInput ==  'regista'   or RoleInput ==  'reg(su)'   or RoleInput ==  'regsupport'   or RoleInput ==  'reg(support)'   or RoleInput ==  'regista(su)'   or RoleInput ==  'registasupport'   or RoleInput ==  'regista(support)':
                REGsufunc()
                 
            elif RoleInput == 'hb'  or RoleInput ==  'hbdefend' or RoleInput ==  'hb(defend)' or RoleInput ==  'hb(de)' or RoleInput ==  'hbde'  or RoleInput ==  'halfback'  or RoleInput ==  'half-back'  or RoleInput ==  'halfback(de)'  or RoleInput ==  'half-back(de)'  or RoleInput ==  'halfbackde'  or RoleInput ==  'half-backde'  or RoleInput ==  'halfbackdefend'  or RoleInput ==  'half-backdefend':
                HBdefunc()
                 
            elif RoleInput == 'rpmsu' or RoleInput ==  'rpm'  or RoleInput ==  'rpm(su)' or RoleInput ==  'rpmsupport' or RoleInput ==  'rpm(support)' or RoleInput ==  'roamingplaymaker' or RoleInput ==  'roaming-playmaker' or RoleInput ==  'roaming-play-maker' or RoleInput ==  'roamingplay-maker' or RoleInput ==  'roamingplaymaker(su)' or RoleInput ==  'roamingplay-maker(su)'  or RoleInput ==  'roaming-playmaker(su)' or RoleInput ==  'roaming-play-maker(su)' or RoleInput ==  'roamingplaymaker(support)' or RoleInput ==  'roamingplay-maker(support)'  or RoleInput ==  'roaming-playmaker(support)' or RoleInput ==  'roaming-play-maker(support)' or RoleInput ==  'roamingplaymakersupport' or RoleInput ==  'roamingplay-makersupport'  or RoleInput ==  'roaming-playmakersupport' or RoleInput ==  'roaming-play-makersupport' :
                RPMsufunc()
                 
            elif RoleInput == 'ancde'   or RoleInput ==  'anc'   or RoleInput ==  'anchor'   or RoleInput ==  'anc(de)'   or RoleInput ==  'ancdefend'   or RoleInput ==  'anc(defend)'   or RoleInput ==  'anchor(de)'   or RoleInput ==  'anchordefend'   or RoleInput ==  'anchor(defend)':
                ANCdefunc()
                 
            elif RoleInput == 'svsu' or RoleInput ==  'svsupport' or RoleInput ==  'sv(support)' or RoleInput ==  'sv' or RoleInput ==  'segundovolante' or RoleInput ==  'segundo-volante' or RoleInput ==  'sv(su)'  or RoleInput ==  'segundovolante(su)'  or RoleInput ==  'segundo-volante(su)'  or RoleInput ==  'segundovolantesu'  or RoleInput ==  'segundo-volantesu'  or RoleInput ==  'segundovolantesupport'  or RoleInput ==  'segundo-volantesupport'  or RoleInput ==  'segundovolante(support)'  or RoleInput ==  'segundo-volante(support)' :
                SVsufunc()
                 
            elif RoleInput == 'svat' or RoleInput ==  'svattack' or RoleInput ==  'sv(attack)' or RoleInput ==  'sv(at)'  or RoleInput ==  'segundovolante(at)'  or RoleInput ==  'segundo-volante(at)'  or RoleInput ==  'segundovolanteat'  or RoleInput ==  'segundo-volanteat'  or RoleInput ==  'segundovolanteattack'  or RoleInput ==  'segundo-volanteattack'  or RoleInput ==  'segundovolante(attack)'  or RoleInput ==  'segundo-volante(attack)' :
                SVatfunc()
                 
            elif RoleInput == 'bwmde'  or RoleInput ==  'bwm(de)' or RoleInput ==  'bwmdefend' or RoleInput ==  'bwm(defend)' or RoleInput ==  'bwm' or RoleInput ==  'ballwinningmidfielder' or RoleInput ==  'ballwinningmid-fielder'  or RoleInput ==  'ballwinning-midfielder' or RoleInput ==  'ball-winningmidfielder' or RoleInput ==  'ball-winning-midfielder' or RoleInput ==  'ball-winning-mid-fielder' or RoleInput ==  'ballwinning-mid-fielder' or RoleInput ==  'ball-winningmid-fielder' or RoleInput ==  'ballwinningmidfielder(de)' or RoleInput ==  'ballwinningmid-fielder(de)'  or RoleInput ==  'ballwinning-midfielder(de)' or RoleInput ==  'ball-winningmidfielder(de)' or RoleInput ==  'ball-winning-midfielder(de)' or RoleInput ==  'ball-winning-mid-fielder(de)' or RoleInput ==  'ballwinning-mid-fielder(de)' or RoleInput ==  'ball-winningmid-fielder(de)' or RoleInput ==  'ballwinningmidfielder(defend)' or RoleInput ==  'ballwinningmid-fielder(defend)'  or RoleInput ==  'ballwinning-midfielder(defend)' or RoleInput ==  'ball-winningmidfielder(defend)' or RoleInput ==  'ball-winning-midfielder(defend)' or RoleInput ==  'ball-winning-mid-fielder(defend)' or RoleInput ==  'ballwinning-mid-fielder(defend)' or RoleInput ==  'ball-winningmid-fielder(defend)' or RoleInput ==  'ballwinningmidfielderdefend' or RoleInput ==  'ballwinningmid-fielderdefend'  or RoleInput ==  'ballwinning-midfielderdefend' or RoleInput ==  'ball-winningmidfielderdefend' or RoleInput ==  'ball-winning-midfielderdefend' or RoleInput ==  'ball-winning-mid-fielderdefend' or RoleInput ==  'ballwinning-mid-fielderdefend' or RoleInput ==  'ball-winningmid-fielderdefend' :
                BWMdefunc()
                 
            elif RoleInput == 'bwmsu'  or RoleInput ==  'bwm(su)' or RoleInput ==  'bwmsupport' or RoleInput ==  'bwm(support)' or RoleInput ==  'ballwinningmidfielder(su)' or RoleInput ==  'ballwinningmid-fielder(su)'  or RoleInput ==  'ballwinning-midfielder(su)' or RoleInput ==  'ball-winningmidfielder(su)' or RoleInput ==  'ball-winning-midfielder(su)' or RoleInput ==  'ball-winning-mid-fielder(su)' or RoleInput ==  'ballwinning-mid-fielder(su)' or RoleInput ==  'ball-winningmid-fielder(su)' or RoleInput ==  'ballwinningmidfielder(support)' or RoleInput ==  'ballwinningmid-fielder(support)'  or RoleInput ==  'ballwinning-midfielder(support)' or RoleInput ==  'ball-winningmidfielder(support)' or RoleInput ==  'ball-winning-midfielder(support)' or RoleInput ==  'ball-winning-mid-fielder(support)' or RoleInput ==  'ballwinning-mid-fielder(support)' or RoleInput ==  'ball-winningmid-fielder(support)' or RoleInput ==  'ballwinningmidfieldersupport' or RoleInput ==  'ballwinningmid-fieldersupport'  or RoleInput ==  'ballwinning-midfieldersupport' or RoleInput ==  'ball-winningmidfieldersupport' or RoleInput ==  'ball-winning-midfieldersupport' or RoleInput ==  'ball-winning-mid-fieldersupport' or RoleInput ==  'ballwinning-mid-fieldersupport' or RoleInput ==  'ball-winningmid-fieldersupport' :
                BWMsufunc()
                 
            
            # Central midfield roles 

            elif RoleInput == 'cmde' or RoleInput ==  'cmdefend' or RoleInput ==  'cm(defend)' or RoleInput ==  'cm(de)'  or RoleInput ==  'centralmid(de)'  or RoleInput ==  'centralmidfielder(de)'  or RoleInput ==  'central-mid(de)'  or RoleInput ==  'central-midfielder(de)'  or RoleInput ==  'centralmid(defend)'  or RoleInput ==  'centralmidfielder(defend)'  or RoleInput ==  'central-mid(defend)'  or RoleInput ==  'central-midfielder(defend)'  or RoleInput ==  'centralmidde'  or RoleInput ==  'centralmidfielderde'  or RoleInput ==  'central-midde'  or RoleInput ==  'central-midfielderde'  or RoleInput ==  'centralmiddefend'  or RoleInput ==  'centralmidfielderdefend'  or RoleInput ==  'central-middefend'  or RoleInput ==  'central-midfielderdefend'  :
                CMdefunc()
                 
            elif RoleInput == 'cmsu' or RoleInput ==  'cm' or RoleInput ==  'centralmid' or RoleInput ==  'centralmidfielder' or RoleInput ==  'centremid' or RoleInput ==  'centermid' or RoleInput ==  'centermidfielder' or RoleInput ==  'cmsupport' or RoleInput ==  'cm(support)' or RoleInput ==  'cm(su)'  or RoleInput ==  'centralmid(su)'  or RoleInput ==  'centralmidfielder(su)'  or RoleInput ==  'central-mid(su)'  or RoleInput ==  'central-midfielder(su)'  or RoleInput ==  'centralmid(support)'  or RoleInput ==  'centralmidfielder(support)'  or RoleInput ==  'central-mid(support)'  or RoleInput ==  'central-midfielder(support)'  or RoleInput ==  'centralmidsu'  or RoleInput ==  'centralmidfieldersu'  or RoleInput ==  'central-midsu'  or RoleInput ==  'central-midfieldersu'  or RoleInput ==  'centralmidsupport'  or RoleInput ==  'centralmidfieldersupport'  or RoleInput ==  'central-midsupport'  or RoleInput ==  'central-midfieldersupport'  :
                CMsufunc()
                 
            elif RoleInput == 'cmat' or RoleInput ==  'cmdattack' or RoleInput ==  'cm(attack)' or RoleInput ==  'cm(at)'  or RoleInput ==  'centralmid(at)'  or RoleInput ==  'centralmidfielder(at)'  or RoleInput ==  'central-mid(at)'  or RoleInput ==  'central-midfielder(at)'  or RoleInput ==  'centralmid(attack)'  or RoleInput ==  'centralmidfielder(attack)'  or RoleInput ==  'central-mid(attack)'  or RoleInput ==  'central-midfielder(attack)'  or RoleInput ==  'centralmidat'  or RoleInput ==  'centralmidfielderat'  or RoleInput ==  'central-midat'  or RoleInput ==  'central-midfielderat'  or RoleInput ==  'centralmidattack'  or RoleInput ==  'centralmidfielderattack'  or RoleInput ==  'central-midattack'  or RoleInput ==  'central-midfielderattack'  :
                CMatfunc()
                 
            elif RoleInput == 'carsu'   or RoleInput ==  'car'   or RoleInput ==  'carrilero'   or RoleInput ==  'car(su)'   or RoleInput ==  'carsupport'   or RoleInput ==  'car(support)'   or RoleInput ==  'carrilero(su)'   or RoleInput ==  'carrilerosupport'   or RoleInput ==  'carrilero(support)':
                CARsufunc()
                 
            elif RoleInput == 'mezsu'   or RoleInput ==  'mez'   or RoleInput ==  'mezzala'   or RoleInput ==  'mez(su)'   or RoleInput ==  'mezsupport'   or RoleInput ==  'mez(support)'   or RoleInput ==  'mezzala(su)'   or RoleInput ==  'mezzalasupport'   or RoleInput ==  'mezzala(support)':
                MEZsufunc()
                 
            elif RoleInput == 'mezat'   or RoleInput ==  'mez(at)'   or RoleInput ==  'mezattack'   or RoleInput ==  'mez(attack)'   or RoleInput ==  'mezzala(at)'   or RoleInput ==  'mezzalaattack'   or RoleInput ==  'mezzala(attack)':
                MEZatfunc()
                 
            elif RoleInput == 'B2Bsu'   or RoleInput ==  'b2b'   or RoleInput ==  'b2bm'   or RoleInput ==  'b2bmsu'   or RoleInput ==  'b2bm(su)'   or RoleInput ==  'btb'   or RoleInput ==  'btbm'   or RoleInput ==  'btbmsu'   or RoleInput ==  'btbm(su)'   or RoleInput ==  'boxtoboxmidfielder'   or RoleInput ==  'box-toboxmidfielder'   or RoleInput ==  'box-to-boxmidfielder'   or RoleInput ==  'box-to-box-midfielder'   or RoleInput ==  'box-to-box-mid-fielder'   or RoleInput ==  'boxto-box-mid-fielder'   or RoleInput ==  'boxtobox-mid-fielder'   or RoleInput ==  'boxtoboxmid-fielder'   or RoleInput ==  'boxtoboxmid-fielder'   or RoleInput ==  'box-tobox-mid-fielder'   or RoleInput ==  'box-to-boxmid-fielder'   or RoleInput ==  'boxtoboxmidfieldersu'   or RoleInput ==  'box-toboxmidfieldersu'   or RoleInput ==  'box-to-boxmidfieldersu'   or RoleInput ==  'box-to-box-midfieldersu'   or RoleInput ==  'box-to-box-mid-fieldersu'   or RoleInput ==  'boxto-box-mid-fieldersu'   or RoleInput ==  'boxtobox-mid-fieldersu'   or RoleInput ==  'boxtoboxmid-fieldersu'   or RoleInput ==  'boxtoboxmid-fieldersu'   or RoleInput ==  'box-tobox-mid-fieldersu'   or RoleInput ==  'box-to-boxmid-fieldersu'   or RoleInput ==  'boxtoboxmidfielder(su)'   or RoleInput ==  'box-toboxmidfielder(su)'   or RoleInput ==  'box-to-boxmidfielder(su)'   or RoleInput ==  'box-to-box-midfielder(su)'   or RoleInput ==  'box-to-box-mid-fielder(su)'   or RoleInput ==  'boxto-box-mid-fielder(su)'   or RoleInput ==  'boxtobox-mid-fielder(su)'   or RoleInput ==  'boxtoboxmid-fielder(su)'   or RoleInput ==  'boxtoboxmid-fielder(su)'   or RoleInput ==  'box-tobox-mid-fielder(su)'   or RoleInput ==  'box-to-boxmid-fielder(su)'   or RoleInput ==  'boxtoboxmidfieldersupport'   or RoleInput ==  'box-toboxmidfieldersupport'   or RoleInput ==  'box-to-boxmidfieldersupport'   or RoleInput ==  'box-to-box-midfieldersupport'   or RoleInput ==  'box-to-box-mid-fieldersupport'   or RoleInput ==  'boxto-box-mid-fieldersupport'   or RoleInput ==  'boxtobox-mid-fieldersupport'   or RoleInput ==  'boxtoboxmid-fieldersupport'   or RoleInput ==  'boxtoboxmid-fieldersupport'   or RoleInput ==  'box-tobox-mid-fieldersupport'   or RoleInput ==  'box-to-boxmid-fieldersupport'   or RoleInput ==  'boxtoboxmidfielder(support)'   or RoleInput ==  'box-toboxmidfielder(support)'   or RoleInput ==  'box-to-boxmidfielder(support)'   or RoleInput ==  'box-to-box-midfielder(support)'   or RoleInput ==  'box-to-box-mid-fielder(support)'   or RoleInput ==  'boxto-box-mid-fielder(support)'   or RoleInput ==  'boxtobox-mid-fielder(support)'   or RoleInput ==  'boxtoboxmid-fielder(support)'   or RoleInput ==  'boxtoboxmid-fielder(support)'   or RoleInput ==  'box-tobox-mid-fielder(support)'   or RoleInput ==  'box-to-boxmid-fielder(support)':
                B2Bsufunc()
                 
            
            # Wide midfield roles 

            elif RoleInput == 'wpmsu'   or RoleInput ==  'wpm'    or RoleInput ==  'wpm(su)'   or RoleInput ==  'wpmsupport'   or RoleInput ==  'wpm(support)'   or RoleInput ==  'wideplaymaker'   or RoleInput ==  'wide-playmaker'   or RoleInput ==  'wideplay-maker'   or RoleInput ==  'wide-play-maker'   or RoleInput ==  'wideplaymaker(su)'   or RoleInput ==  'wideplay-maker(su)'    or RoleInput ==  'wide-playmaker(su)'   or RoleInput ==  'wide-play-maker(su)'   or RoleInput ==  'wideplaymaker(support)'   or RoleInput ==  'wideplay-maker(support)'    or RoleInput ==  'wide-playmaker(support)'   or RoleInput ==  'wide-play-maker(support)'   or RoleInput ==  'wideplaymakersupport'   or RoleInput ==  'wideplay-makersupport'    or RoleInput ==  'wide-playmakersupport'   or RoleInput ==  'wide-play-makersupport' :
                WPMsufunc()
                 
            elif RoleInput == 'wpmat'   or RoleInput ==  'wpm'    or RoleInput ==  'wpm(at)'   or RoleInput ==  'wpmattack'   or RoleInput ==  'wpm(attack)'   or RoleInput ==  'wideplaymaker(at)'   or RoleInput ==  'wideplay-maker(at)'    or RoleInput ==  'wide-playmaker(at)'   or RoleInput ==  'wide-play-maker(at)'   or RoleInput ==  'wideplaymaker(attack)'   or RoleInput ==  'wideplay-maker(attack)'    or RoleInput ==  'wide-playmaker(attack)'   or RoleInput ==  'wide-play-maker(attack)'   or RoleInput ==  'wideplaymakerattack'   or RoleInput ==  'wideplay-makerattack'    or RoleInput ==  'wide-playmakerattack'   or RoleInput ==  'wide-play-makerattack' :
                WPMatfunc()
                 
            elif RoleInput == 'dwde'  or RoleInput ==  'dw(de)' or RoleInput ==  'dw' or RoleInput ==  'dwdefend' or RoleInput ==  'dw(defend)' or RoleInput ==  'defensivewinger'  or RoleInput ==  'defensive-winger'  or RoleInput ==  'defensivewinger(de)'  or RoleInput ==  'defensive-winger(de)'  or RoleInput ==  'defensivewingerde'  or RoleInput ==  'defensive-wingerde'  or RoleInput ==  'defensivewingerdefend'  or RoleInput ==  'defensive-wingerdefend' or RoleInput ==  'defensivewinger(defend)'  or RoleInput ==  'defensive-winger(defend)' :
                DWdefunc()
                 
            elif RoleInput == 'dwsu'  or RoleInput ==  'dw(su)' or RoleInput ==  'dwsupport' or RoleInput ==  'dw(support)' or RoleInput ==  'defensivewinger(su)'  or RoleInput ==  'defensive-winger(su)'  or RoleInput ==  'defensivewingersu'  or RoleInput ==  'defensive-wingersu'  or RoleInput ==  'defensivewingersupport'  or RoleInput ==  'defensive-wingersupport' or RoleInput ==  'defensivewinger(support)'  or RoleInput ==  'defensive-winger(support)' :
                DWsufunc()
                 
            elif RoleInput == 'wmde' or RoleInput ==  'wmdefend' or RoleInput ==  'wm(defend)' or RoleInput ==  'wm(de)'  or RoleInput ==  'widemid(de)'  or RoleInput ==  'widemidfielder(de)'  or RoleInput ==  'wide-mid(de)'  or RoleInput ==  'wide-midfielder(de)'  or RoleInput ==  'widemid(defend)'  or RoleInput ==  'widemidfielder(defend)'  or RoleInput ==  'wide-mid(defend)'  or RoleInput ==  'wide-midfielder(defend)'  or RoleInput ==  'widemidde'  or RoleInput ==  'widemidfielderde'  or RoleInput ==  'wide-midde'  or RoleInput ==  'wide-midfielderde'  or RoleInput ==  'widemiddefend'  or RoleInput ==  'widemidfielderdefend'  or RoleInput ==  'wide-middefend'  or RoleInput ==  'wide-midfielderdefend'  or RoleInput ==  'widemid-fielder(de)'  or RoleInput ==  'wide-mid(de)'  or RoleInput ==  'wide-mid-fielder(de)'  or RoleInput ==  'widemid(defend)'  or RoleInput ==  'widemid-fielder(defend)'  or RoleInput ==  'wide-mid(defend)'  or RoleInput ==  'wide-mid-fielder(defend)'  or RoleInput ==  'widemidde'  or RoleInput ==  'widemid-fielderde'  or RoleInput ==  'wide-midde'  or RoleInput ==  'wide-mid-fielderde'  or RoleInput ==  'widemiddefend'  or RoleInput ==  'widemid-fielderdefend'  or RoleInput ==  'wide-middefend'  or RoleInput ==  'wide-mid-fielderdefend'  :
                WMdefunc()
                 
            elif RoleInput == 'wmsu' or RoleInput ==  'wm' or RoleInput ==  'widemid' or RoleInput ==  'widemidfielder' or RoleInput ==  'wmsupport' or RoleInput ==  'wm(support)' or RoleInput ==  'wm(su)'  or RoleInput ==  'widemid(su)'  or RoleInput ==  'widemidfielder(su)'  or RoleInput ==  'wide-mid(su)'  or RoleInput ==  'wide-midfielder(su)'  or RoleInput ==  'widemid(support)'  or RoleInput ==  'widemidfielder(support)'  or RoleInput ==  'wide-mid(support)'  or RoleInput ==  'wide-midfielder(support)'  or RoleInput ==  'widemidsu'  or RoleInput ==  'widemidfieldersu'  or RoleInput ==  'wide-midsu'  or RoleInput ==  'wide-midfieldersu'  or RoleInput ==  'widemidsupport'  or RoleInput ==  'widemidfieldersupport'  or RoleInput ==  'wide-midsupport'  or RoleInput ==  'wide-midfieldersupport'  or RoleInput ==  'widemid-fielder(su)'  or RoleInput ==  'wide-mid(su)'  or RoleInput ==  'wide-mid-fielder(su)'  or RoleInput ==  'widemid(support)'  or RoleInput ==  'widemid-fielder(support)'  or RoleInput ==  'wide-mid(support)'  or RoleInput ==  'wide-mid-fielder(support)'  or RoleInput ==  'widemidsu'  or RoleInput ==  'widemid-fieldersu'  or RoleInput ==  'wide-midsu'  or RoleInput ==  'wide-mid-fieldersu'  or RoleInput ==  'widemidsupport'  or RoleInput ==  'widemid-fieldersupport'  or RoleInput ==  'wide-midsupport'  or RoleInput ==  'wide-mid-fieldersupport'  :
                WMsufunc()
                 
            elif RoleInput == 'wmat' or RoleInput ==  'wmattack' or RoleInput ==  'wm(attack)' or RoleInput ==  'wm(at)'  or RoleInput ==  'widemid(at)'  or RoleInput ==  'widemidfielder(at)'  or RoleInput ==  'wide-mid(at)'  or RoleInput ==  'wide-midfielder(at)'  or RoleInput ==  'widemid(attack)'  or RoleInput ==  'widemidfielder(attack)'  or RoleInput ==  'wide-mid(attack)'  or RoleInput ==  'wide-midfielder(attack)'  or RoleInput ==  'widemidat'  or RoleInput ==  'widemidfielderat'  or RoleInput ==  'wide-midat'  or RoleInput ==  'wide-midfielderat'  or RoleInput ==  'widemidattack'  or RoleInput ==  'widemidfielderattack'  or RoleInput ==  'wide-midattack'  or RoleInput ==  'wide-midfielderattack'  or RoleInput ==  'widemid-fielder(at)'  or RoleInput ==  'wide-mid(at)'  or RoleInput ==  'wide-mid-fielder(at)'  or RoleInput ==  'widemid(attack)'  or RoleInput ==  'widemid-fielder(attack)'  or RoleInput ==  'wide-mid(attack)'  or RoleInput ==  'wide-mid-fielder(attack)'  or RoleInput ==  'widemidat'  or RoleInput ==  'widemid-fielderat'  or RoleInput ==  'wide-midat'  or RoleInput ==  'wide-mid-fielderat'  or RoleInput ==  'widemiddefend'  or RoleInput ==  'widemid-fielderattack'  or RoleInput ==  'wide-midattack'  or RoleInput ==  'wide-mid-fielderattack'  :
                WMatfunc()
                 

            # Central attacking midfield roles

            elif RoleInput == 'apmsu' or RoleInput == 'apsu' or RoleInput ==  'apm'  or RoleInput ==  'apm(su)' or RoleInput ==  'apmsupport' or RoleInput ==  'apm(support)' or RoleInput ==  'advancedplaymaker' or RoleInput ==  'advanced-playmaker' or RoleInput ==  'advanced-play-maker' or RoleInput ==  'advancedplay-maker' or RoleInput ==  'advancedplaymaker(su)' or RoleInput ==  'advancedplay-maker(su)'  or RoleInput ==  'advanced-playmaker(su)' or RoleInput ==  'advanced-play-maker(su)' or RoleInput ==  'advancedplaymaker(support)' or RoleInput ==  'advancedplay-maker(support)'  or RoleInput ==  'advanced-playmaker(support)' or RoleInput ==  'advanced-play-maker(support)' or RoleInput ==  'advancedplaymakersupport' or RoleInput ==  'advancedplay-makersupport'  or RoleInput ==  'advanced-playmakersupport' or RoleInput ==  'advanced-play-makersupport' :
                APMsufunc()
                 
            elif RoleInput == 'ap' or RoleInput == 'apat' or RoleInput == 'apmat' or RoleInput ==  'apm(at)' or RoleInput ==  'apmattack' or RoleInput == 'apm(attack)' or RoleInput == 'advancedplaymaker' or RoleInput == 'advancedplay-maker' or RoleInput == 'advanced-play-maker' or RoleInput == 'advanced-playmaker' or RoleInput ==  'advancedplaymaker(at)' or RoleInput ==  'advancedplay-maker(at)'  or RoleInput ==  'advanced-playmaker(at)' or RoleInput ==  'advanced-play-maker(at)' or RoleInput ==  'advancedplaymaker(attack)' or RoleInput ==  'advancedplay-maker(attack)'  or RoleInput ==  'advanced-playmaker(attack)' or RoleInput ==  'advanced-play-maker(attack)' or RoleInput ==  'advancedplaymakerattack' or RoleInput ==  'advancedplay-makerattack'  or RoleInput ==  'advanced-playmakerattack' or RoleInput ==  'advanced-play-makerattack' :
                APMatfunc()
                 
            elif RoleInput == 'amsu' or RoleInput ==  'amsupport' or RoleInput ==  'am(support)' or RoleInput ==  'am' or RoleInput ==  'attackingmid' or RoleInput ==  'attacking-mid' or RoleInput ==  'attackingmidfielder' or RoleInput ==  'attacking-midfielder' or RoleInput ==  'am(su)'  or RoleInput ==  'attackingmid(su)'  or RoleInput ==  'attackingmidfielder(su)'  or RoleInput ==  'attacking-mid(su)'  or RoleInput ==  'attacking-midfielder(su)'  or RoleInput ==  'attackingmid(support)'  or RoleInput ==  'attackingmidfielder(support)'  or RoleInput ==  'attacking-mid(support)'  or RoleInput ==  'attacking-midfielder(support)'  or RoleInput ==  'attackingmidsu'  or RoleInput ==  'attackingmidfieldersu'  or RoleInput ==  'attacking-midsu'  or RoleInput ==  'attacking-midfieldersu'  or RoleInput ==  'attackingmidsupport'  or RoleInput ==  'attackingmidfieldersupport'  or RoleInput ==  'attacking-midsupport'  or RoleInput ==  'attacking-midfieldersupport'  :
                AMsufunc()
                 
            elif RoleInput == 'amat' or RoleInput ==  'amattack' or RoleInput ==  'am(attack)' or RoleInput ==  'am(at)'  or RoleInput ==  'attackingmid(at)'  or RoleInput ==  'attackingmidfielder(at)'  or RoleInput ==  'attacking-mid(at)'  or RoleInput ==  'attacking-midfielder(at)'  or RoleInput ==  'attackingmid(attack)'  or RoleInput ==  'attackingmidfielder(attack)'  or RoleInput ==  'attacking-mid(attack)'  or RoleInput ==  'attacking-midfielder(attack)'  or RoleInput ==  'attackingmidat'  or RoleInput ==  'attackingmidfielderat'  or RoleInput ==  'attacking-midat'  or RoleInput ==  'attacking-midfielderat'  or RoleInput ==  'attackingmidattack'  or RoleInput ==  'attackingmidfielderattack'  or RoleInput ==  'attacking-midattack'  or RoleInput ==  'attacking-midfielderattack'  :
                AMatfunc()
                 
            elif RoleInput == 'ssat'  or RoleInput ==  'ss' or RoleInput ==  'ss(at)' or RoleInput ==  'ssattack' or RoleInput ==  'ss(attack)' or RoleInput ==  'shadowstriker' or RoleInput ==  'shadowstriker(at)'  or RoleInput ==  'shadow-striker(at)'  or RoleInput ==  'shadowstrikerat'  or RoleInput ==  'shadow-striker'  or RoleInput ==  'shadowstrikerattack'  or RoleInput ==  'shadow-strikerattack' or RoleInput ==  'shadowstriker(attack)'  or RoleInput ==  'shadow-striker(attack)' :
                SSatfunc()
                 
            elif RoleInput == 'treat'   or RoleInput ==  'tre'   or RoleInput ==  'tre(at)'   or RoleInput ==  'treattack'   or RoleInput ==  'tre(attack)'   or RoleInput ==  'trequartista'   or RoleInput ==  'trequartista(at)'   or RoleInput ==  'trequartistaattack'   or RoleInput ==  'trequartista(attack)' :
                TREatfunc()
                 
            elif RoleInput == 'engsu'   or RoleInput ==  'eng'   or RoleInput ==  'enganche'   or RoleInput ==  'eng(su)'   or RoleInput ==  'engsupport'   or RoleInput ==  'eng(support)'   or RoleInput ==  'enganche(su)'   or RoleInput ==  'enganchesupport'   or RoleInput ==  'enganche(support)' :
                ENGsufunc()
                 
            
            # Wide attacking midfield roles 

            elif RoleInput == 'iwsu'  or RoleInput ==  'iw' or RoleInput ==  'iw(su)' or RoleInput ==  'iwsupport' or RoleInput ==  'iw(support)' or RoleInput ==  'invertedwinger' or RoleInput ==  'inverted-winger' or RoleInput ==  'invertedwinger(su)'  or RoleInput ==  'inverted-winger(su)'  or RoleInput ==  'invertedwingersu'  or RoleInput ==  'inverted-wingersu'  or RoleInput ==  'invertedwingersupport'  or RoleInput ==  'inverted-wingersupport' or RoleInput ==  'invertedwinger(support)'  or RoleInput ==  'inverted-winger(support)' :
                IWsufunc()
                 
            elif RoleInput == 'iwat'  or RoleInput ==  'iw(at)' or RoleInput ==  'iwattack' or RoleInput ==  'iw(attack)' or RoleInput ==  'invertedwinger(at)'  or RoleInput ==  'inverted-winger(at)'  or RoleInput ==  'invertedwingerat'  or RoleInput ==  'inverted-wingerat'  or RoleInput ==  'invertedwingerattack'  or RoleInput ==  'inverted-wingerattack' or RoleInput ==  'invertedwinger(attack)'  or RoleInput ==  'inverted-winger(attack)' :
                IWatfunc()
                 
            elif RoleInput == 'ifsu'  or RoleInput ==  'if' or RoleInput ==  'if(su)' or RoleInput ==  'ifsupport' or RoleInput ==  'if(support)' or RoleInput ==  'insidewinger' or RoleInput ==  'inside-forward' or RoleInput ==  'insideforward(su)'  or RoleInput ==  'inside-forward(su)'  or RoleInput ==  'insideforwardsu'  or RoleInput ==  'inside-forwardsu'  or RoleInput ==  'insideforwardsupport'  or RoleInput ==  'inside-forwardsupport' or RoleInput ==  'insideforward(support)'  or RoleInput ==  'inside-forward(support)' :
                IFsufunc()
                 
            elif RoleInput == 'ifat'  or RoleInput ==  'if(at)' or RoleInput ==  'ifattack' or RoleInput ==  'if(attack)' or RoleInput ==  'insideforward(at)'  or RoleInput ==  'inside-forward(at)'  or RoleInput ==  'insideforwardat'  or RoleInput ==  'inside-forwardat'  or RoleInput ==  'insideforwardattack'  or RoleInput ==  'inside-forwardattack' or RoleInput ==  'insideforward(attack)'  or RoleInput ==  'inside-forward(attack)' :
                IFatfunc()
                 
            elif RoleInput == 'winsu'   or RoleInput ==  'w'   or RoleInput ==  'wsu'   or RoleInput ==  'w(su)'   or RoleInput ==  'win'   or RoleInput ==  'winger' or RoleInput ==  'wingersu'  or RoleInput ==  'win(su)'   or RoleInput ==  'winsupport'   or RoleInput ==  'win(support)'   or RoleInput ==  'winger(su)'   or RoleInput ==  'wingersupport'   or RoleInput ==  'winger(support)' :
                WINsufunc()
                 
            elif RoleInput == 'winat'   or RoleInput ==  'wat'   or RoleInput ==  'w(at)'   or RoleInput ==  'win(at)'   or RoleInput ==  'winattack' or RoleInput ==  'wingerat'   or RoleInput ==  'win(attack)'   or RoleInput ==  'winger(at)'   or RoleInput ==  'wingerattack'   or RoleInput ==  'winger(attack)' :
                WINatfunc()
                 
            elif RoleInput == 'rmdat'   or RoleInput ==  'rmd'   or RoleInput ==  'rmd(at)'   or RoleInput ==  'rmdattack'   or RoleInput ==  'rmd(attack)'   or RoleInput ==  'raumdeuter'   or RoleInput ==  'raumdeuter(at)'   or RoleInput ==  'raumdeuterattack'   or RoleInput ==  'raumdeuter(attack)' :
                RMDatfunc()
                 
            elif RoleInput == 'wtmsu'   or RoleInput ==  'wtm'    or RoleInput ==  'wtm(su)'   or RoleInput ==  'wtmsupport'   or RoleInput ==  'wtm(support)'   or RoleInput ==  'widetargetman'   or RoleInput ==  'wide-targetman'   or RoleInput ==  'widetarget-man'   or RoleInput ==  'wide-target-man'   or RoleInput ==  'widetargetman(su)'   or RoleInput ==  'widetarget-man(su)'    or RoleInput ==  'wide-targetman(su)'   or RoleInput ==  'wide-target-man(su)'   or RoleInput ==  'widetargetman(support)'   or RoleInput ==  'widetarget-man(support)'    or RoleInput ==  'wide-targetman(support)'   or RoleInput ==  'wide-target-man(support)'   or RoleInput ==  'widetargetmansupport'   or RoleInput ==  'widetarget-mansupport'    or RoleInput ==  'wide-targetmansupport'   or RoleInput ==  'wide-target-mansupport' or RoleInput == 'wtfsu'   or RoleInput ==  'wtf'    or RoleInput ==  'wtf(su)'   or RoleInput ==  'wtfsupport'   or RoleInput ==  'wtf(support)'   or RoleInput ==  'widetargetforward'   or RoleInput ==  'wide-targetforward'   or RoleInput ==  'widetarget-forward'   or RoleInput ==  'wide-target-forward'   or RoleInput ==  'widetargetforward(su)'   or RoleInput ==  'widetarget-forward(su)'    or RoleInput ==  'wide-targetforward(su)'   or RoleInput ==  'wide-target-forward(su)'   or RoleInput ==  'widetargetforward(support)'   or RoleInput ==  'widetarget-forward(support)'    or RoleInput ==  'wide-targetforward(support)'   or RoleInput ==  'wide-target-forward(support)'   or RoleInput ==  'widetargetforwardsupport'   or RoleInput ==  'widetarget-forwardsupport'    or RoleInput ==  'wide-targetforwardsupport'   or RoleInput ==  'wide-target-forwardsupport' :
                WTFsufunc()
                 
            elif RoleInput == 'wtmat'   or RoleInput ==  'wtm(at)'   or RoleInput ==  'wtmattack'   or RoleInput ==  'wtm(attack)'   or RoleInput ==  'widetargetman(at)'   or RoleInput ==  'widetarget-man(at)'    or RoleInput ==  'wide-targetman(at)'   or RoleInput ==  'wide-target-man(at)'   or RoleInput ==  'widetargetman(attack)'   or RoleInput ==  'widetarget-man(attack)'    or RoleInput ==  'wide-targetman(attack)'   or RoleInput ==  'wide-target-man(attack)'   or RoleInput ==  'widetargetmanattack'   or RoleInput ==  'widetarget-manattack'    or RoleInput ==  'wide-targetmanattack'   or RoleInput ==  'wide-target-manattack' or RoleInput == 'wtfat'  or RoleInput ==  'wtf(at)'   or RoleInput ==  'wtfattack'   or RoleInput ==  'wtf(attack)' or RoleInput ==  'widetargetforward(at)'   or RoleInput ==  'widetarget-forward(at)'    or RoleInput ==  'wide-targetforward(at)'   or RoleInput ==  'wide-target-forward(at)'   or RoleInput ==  'widetargetforward(attack)'   or RoleInput ==  'widetarget-forward(attack)'    or RoleInput ==  'wide-targetforward(attack)'   or RoleInput ==  'wide-target-forward(attack)'   or RoleInput ==  'widetargetforwardattack'   or RoleInput ==  'widetarget-forwardattack'    or RoleInput ==  'wide-targetforwardattack'   or RoleInput ==  'wide-target-forwardattack' :
                WTFatfunc()
                 
            
            # Striker roles 

            elif RoleInput == 'afat'  or RoleInput ==  'af' or RoleInput ==  'af(at)' or RoleInput ==  'afattack' or RoleInput ==  'af(attack)' or RoleInput ==  'attackingforward'  or RoleInput ==  'attacking-forward' or RoleInput ==  'attackingforward(at)'  or RoleInput ==  'attacking-forward(at)'  or RoleInput ==  'attackingforwardat'  or RoleInput ==  'attacking-forwardat'  or RoleInput ==  'attackingforwardattack'  or RoleInput ==  'attacking-forwardattack' or RoleInput ==  'attackingforward(attack)'  or RoleInput ==  'attacking-forward(attack)' :
                AFatfunc()
                 
            elif RoleInput == 'cfat'  or RoleInput ==  'cf' or RoleInput ==  'cf(at)' or RoleInput ==  'cfattack' or RoleInput ==  'cf(attack)' or RoleInput ==  'completeforward'  or RoleInput ==  'complete-forward' or RoleInput ==  'completeforward(at)'  or RoleInput ==  'complete-forward(at)'  or RoleInput ==  'completeforwardat'  or RoleInput ==  'complete-forwardat'  or RoleInput ==  'completeforwardattack'  or RoleInput ==  'complete-forwardattack' or RoleInput ==  'completeforward(attack)'  or RoleInput ==  'complete-forward(attack)' :
                CFatfunc()
                 
            elif RoleInput == 'poaat'   or RoleInput ==  'poa'   or RoleInput ==  'poa(at)'   or RoleInput ==  'poaattack'   or RoleInput ==  'poa(attack)'   or RoleInput ==  'poacher'   or RoleInput ==  'poacher(at)'   or RoleInput ==  'poacherattack'   or RoleInput ==  'poacher(attack)' :
                POAatfunc()
                 
            elif RoleInput == 'pfde'  or RoleInput ==  'pf(de)' or RoleInput ==  'pfdefend' or RoleInput ==  'pf(defend)' or RoleInput ==  'pressingforward(de)'  or RoleInput ==  'pressing-forward(de)'  or RoleInput ==  'pressingforwardde'  or RoleInput ==  'pressing-forwardde'  or RoleInput ==  'pressingforwarddefend'  or RoleInput ==  'pressing-forwarddefend' or RoleInput ==  'pressingforward(defend)'  or RoleInput ==  'pressing-forward(defend)' :
                PFdefunc()
                             
            elif RoleInput == 'pfsu'  or RoleInput ==  'pf' or RoleInput ==  'pf(su)' or RoleInput ==  'pfsupport' or RoleInput ==  'pf(support)' or RoleInput ==  'pressingforward'  or RoleInput ==  'pressing-forward' or RoleInput ==  'pressingforward(su)'  or RoleInput ==  'pressing-forward(su)'  or RoleInput ==  'pressingforwardsu'  or RoleInput ==  'pressing-forwardsu'  or RoleInput ==  'pressingforwardsupport'  or RoleInput ==  'pressing-forwardsupport' or RoleInput ==  'pressingforward(support)'  or RoleInput ==  'pressing-forward(support)' :
                PFsufunc()
                 
            elif RoleInput == 'pfat'  or RoleInput ==  'pf(at)' or RoleInput ==  'pfattack' or RoleInput ==  'pf(attack)' or RoleInput ==  'pressingforward(at)'  or RoleInput ==  'pressing-forward(at)'  or RoleInput ==  'pressingforwardat'  or RoleInput ==  'pressing-forwardat'  or RoleInput ==  'pressingforwardattack'  or RoleInput ==  'pressing-forwardattack' or RoleInput ==  'pressingforward(attack)'  or RoleInput ==  'pressing-forward(attack)' :
                PFatfunc()
                 
            elif RoleInput == 'dlfsu'   or RoleInput ==  'dlf'    or RoleInput ==  'dlf(su)'   or RoleInput ==  'dlfsupport'   or RoleInput ==  'dlf(support)'   or RoleInput ==  'deeplyingforward'   or RoleInput ==  'deep-lyingforward'   or RoleInput ==  'deeplying-forward'   or RoleInput ==  'deep-lying-forward'   or RoleInput ==  'deeplyingforward(su)'   or RoleInput ==  'deeplying-forward(su)'    or RoleInput ==  'deep-lyingforward(su)'   or RoleInput ==  'deep-lying-forward(su)'   or RoleInput ==  'deeplyingforward(support)'   or RoleInput ==  'deeplying-forward(support)'    or RoleInput ==  'deep-lyingforward(support)'   or RoleInput ==  'deep-lying-forward(support)'   or RoleInput ==  'deeplyingforwardsupport'   or RoleInput ==  'deeplying-forwardsupport'    or RoleInput ==  'deep-lyingforwardsupport'   or RoleInput ==  'deep-lying-forwardsupport' :
                DLFsufunc()
                 
            elif RoleInput == 'dlfat'   or RoleInput ==  'dlf(at)'   or RoleInput ==  'dlfattack'   or RoleInput ==  'dlf(attack)'   or RoleInput ==  'deeplyingforward(at)'   or RoleInput ==  'deeplying-forward(at)'    or RoleInput ==  'deep-lyingforward(at)'   or RoleInput ==  'deep-lying-forward(at)'   or RoleInput ==  'deeplyingforward(attack)'   or RoleInput ==  'deeplying-forward(attack)'    or RoleInput ==  'deep-lyingforward(attack)'   or RoleInput ==  'deep-lying-forward(attack)'   or RoleInput ==  'deeplyingforwardattack'   or RoleInput ==  'deeplying-forwardattack'    or RoleInput ==  'deep-lyingforwardattack'   or RoleInput ==  'deep-lying-forwardattack' :
                DLFatfunc()
                 
            elif RoleInput == 'tmsu'  or RoleInput ==  'tm' or RoleInput ==  'tm(su)' or RoleInput ==  'tmsupport' or RoleInput ==  'tm(support)' or RoleInput ==  'targetman'  or RoleInput ==  'target-man' or RoleInput ==  'targetman(su)'  or RoleInput ==  'target-man(su)'  or RoleInput ==  'targetmansu'  or RoleInput ==  'target-mansu'  or RoleInput ==  'targetmansupport'  or RoleInput ==  'target-mansupport' or RoleInput ==  'targetman(support)'  or RoleInput ==  'target-man(support)' or RoleInput == 'tmsu'  or RoleInput ==  'tm' or RoleInput ==  'tm(su)' or RoleInput ==  'tmsupport' or RoleInput ==  'tm(support)' or RoleInput ==  'targetforward'  or RoleInput ==  'target-forward' or RoleInput ==  'targetforward(su)'  or RoleInput ==  'target-forward(su)'  or RoleInput ==  'targetforwardsu'  or RoleInput ==  'target-forwardsu'  or RoleInput ==  'targetforwardsupport'  or RoleInput ==  'target-forwardsupport' or RoleInput ==  'targetforward(support)'  or RoleInput ==  'target-forward(support)' :
                TFsufunc()
                 
            elif RoleInput == 'tmat'  or RoleInput ==  'tm(at)' or RoleInput ==  'tmattack' or RoleInput ==  'tm(attack)' or RoleInput ==  'targetman(at)'  or RoleInput ==  'target-man(at)'  or RoleInput ==  'targetmanat'  or RoleInput ==  'target-manat'  or RoleInput ==  'targetmanattack'  or RoleInput ==  'target-manattack' or RoleInput ==  'targetman(attack)'  or RoleInput ==  'target-forward(attack)' or RoleInput == 'tmat'  or RoleInput ==  'tm(at)' or RoleInput ==  'tmattack' or RoleInput ==  'tm(attack)' or RoleInput ==  'targetforward(at)'  or RoleInput ==  'target-forward(at)'  or RoleInput ==  'targetforwardat'  or RoleInput ==  'target-forwardat'  or RoleInput ==  'targetforwardattack'  or RoleInput ==  'target-forwardattack' or RoleInput ==  'targetforward(attack)'  or RoleInput ==  'target-forward(attack)' :
                TFatfunc()
                 
            elif RoleInput == 'f9su'  or RoleInput ==  'f9' or RoleInput ==  'f9(su)' or RoleInput ==  'f9support' or RoleInput ==  'f9(support)' or RoleInput ==  'falsenine'  or RoleInput ==  'false-nine' or RoleInput ==  'falsenine(su)'  or RoleInput ==  'false-nine(su)'  or RoleInput ==  'falseninesu'  or RoleInput ==  'false-ninesu'  or RoleInput ==  'falseninesupport'  or RoleInput ==  'false-ninesupport' or RoleInput ==  'falsenine(support)'  or RoleInput ==  'false-nine(support)' or RoleInput ==  'false9'  or RoleInput ==  'false-9' or RoleInput ==  'false9(su)'  or RoleInput ==  'false-9(su)'  or RoleInput ==  'false9su'  or RoleInput ==  'false-9su'  or RoleInput ==  'false9support'  or RoleInput ==  'false-9support' or RoleInput ==  'false9(support)'  or RoleInput ==  'false-9(support)' :
                F9sufunc()
                 

            else: 
                print(r'''I'm sorry, that role isn't recognised by this program. Try again.''')
            pass
        
    RoleQs()

def GUI():
    app = customtkinter.CTk() 
    app.title("FMScout")
    app.geometry("750x500")
    customtkinter.set_appearance_mode("Dark")  
    customtkinter.set_default_color_theme("blue")
    customtkinter.deactivate_automatic_dpi_awareness()
    # customtkinter.set_window_scaling()
    # customtkinter.set_widget_scaling()
    w, h = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry("%dx%d+0+0" % (w, h))

    app.grid_rowconfigure(7, weight=1)
    app.grid_columnconfigure(4, weight=1)

    def restart_program():
        python = sys.executable
        subprocess.Popen([python] + sys.argv)
        sys.exit()

    def Clear():
        AttributeRankingEntryBox.delete(0,END)

    LeftSpacer = customtkinter.CTkLabel(app, text=" ", font=("Trebuchet MS", 24))
    LeftSpacer.grid(row=2, column=0, padx=100, pady=20, sticky="ew")

    RightSpacer = customtkinter.CTkLabel(app, text=" ", font=("Trebuchet MS", 24))
    RightSpacer.grid(row=2, column=4, padx=100, pady=20, sticky="ew")

    AppTitle = customtkinter.CTkLabel(app, text="FMScout", font=("Trebuchet MS Bold", 30)) 
    AppTitle.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
    app.iconbitmap(r'C:\Users\User\Pictures\Icons\favicon.ico')

    LogoImg = customtkinter.CTkImage(light_image=Image.open('Dark Logo.png'),
                                     dark_image=Image.open('Light Logo.png'),
                                     size=(50,50))
    
    LogoLabel = customtkinter.CTkLabel(app, text="", image=LogoImg)
    LogoLabel.grid(row=1,column=3,padx=20, pady=20, sticky="ew")

    ScatterTitle = customtkinter.CTkLabel(app, text="Scatter Graph", font=("Trebuchet MS", 20)) 
    ScatterTitle.grid(row=2,column=1,padx=20, pady=20, sticky="ew")

    global StatsSelectionComboBox1
    StatsSelectionComboBox1 = customtkinter.CTkComboBox(app,
                                                    values= df.keys(),
                                                    height=50,
                                                    width=200,
                                                    corner_radius=5,
                                                    border_width=2,
                                                    border_color="#181b35",
                                                    button_color="#928393",
                                                    button_hover_color="#928393",
                                                    dropdown_hover_color="#cfe6cb",
                                                    dropdown_fg_color="#928393",
                                                    dropdown_text_color="#d9d4da",
                                                    text_color="#d9d4da",
                                                    state=NORMAL
                                                    )
    StatsSelectionComboBox1.grid(row=3,column=1,padx=20, pady=20, sticky="ew")

    global StatsSelectionComboBox2
    StatsSelectionComboBox2 = customtkinter.CTkComboBox(app,
                                                    values= df.keys(),
                                                    height=50,
                                                    width=200,
                                                    corner_radius=5,
                                                    border_width=2,
                                                    border_color="#181b35",
                                                    button_color="#928393",
                                                    button_hover_color="#928393",
                                                    dropdown_hover_color="#cfe6cb",
                                                    dropdown_fg_color="#928393",
                                                    dropdown_text_color="#d9d4da",
                                                    text_color="#d9d4da",
                                                    state=NORMAL)
    StatsSelectionComboBox2.grid(row=4,column=1,padx=20, pady=20, sticky="ew")

    ScatterGraphSelectionButton = customtkinter.CTkButton(app, 
                                                        text="Submit", 
                                                        command=lambda: [ScatterGraphs()],
                                                        fg_color="#928393")
    ScatterGraphSelectionButton.grid(row=5,column=1,padx=20, pady=20, sticky="nsew")

    BarTitle = customtkinter.CTkLabel(app, text="Bar Graph", font=("Trebuchet MS", 20)) 
    BarTitle.grid(row=2,column=2,padx=20, pady=20, sticky="ew")
    
    global StatsSelectionComboBox3
    StatsSelectionComboBox3 = customtkinter.CTkComboBox(app,
                                                    values= df.keys(),
                                                    height=50,
                                                    width=200,
                                                    corner_radius=5,
                                                    border_width=2,
                                                    border_color="#181b35",
                                                    button_color="#928393",
                                                    button_hover_color="#928393",
                                                    dropdown_hover_color="#cfe6cb",
                                                    dropdown_fg_color="#928393",
                                                    dropdown_text_color="#d9d4da",
                                                    text_color="#d9d4da",
                                                    state=NORMAL)
    StatsSelectionComboBox3.grid(row=3,column=2,padx=20, pady=20, sticky="ew")

    BarGraphSelectionButton = customtkinter.CTkButton(app, 
                                                        text="Submit", 
                                                        command=lambda: [BarGraphs()],
                                                        fg_color="#928393")
    BarGraphSelectionButton.grid(row=5,column=2,padx=20, pady=20, sticky="ew")
    
    ScoutTitle = customtkinter.CTkLabel(app, text="Attribute Ranking", font=("Trebuchet MS", 20)) 
    ScoutTitle.grid(row=2,column=3,padx=20, pady=20, sticky="ew")

    global AttributeRankingEntryBox
    AttributeRankingEntryBox = customtkinter.CTkEntry(app,
                                                    height=50,
                                                    width=200,
                                                    corner_radius=5,
                                                    fg_color='#928393',
                                                    border_width=2,
                                                    border_color="#181b35",
                                                    text_color="#d9d4da",
                                                    state=NORMAL)
    AttributeRankingEntryBox.grid(row=3,column=3,padx=20, pady=20, sticky="ew")

    AttributeRankingSelectionButton = customtkinter.CTkButton(app, 
                                                        text="Submit", 
                                                        command=AttributeRanking,
                                                        fg_color="#928393")
    AttributeRankingSelectionButton.grid(row=5,column=3,padx=20, pady=20, sticky="nsew")

    FMScoutInstructions = customtkinter.CTkLabel(app, 
                                                text=r'''
FMScout Instructions: 
1) Make sure you export both files correctly. Use the correct view to organise the data correctly within the game. Export the statistics as 'FMScoutStats' and the Player Attributes as 'FMScout'. 
2) Scatter Graph: The top selection box chooses the variable on the x-axis, and the second box chooses the variable on the y-axis. When 'Submit' is then pressed, a graph is produced that highlights players who are in the top 50% for either variable.
3) Bar Graph: The top selection box chooses the variable on the x-axis. When 'Submit' is then pressed, a graph is produced that highlights players who are in the top 50% for the chosen variable. 
4) Attribute Ranking. Type the name of a player role in the entry box, and then pressed 'Submit' to get a generated table of player rankings for that attribute.''', 
                                                font=("Trebuchet MS", 12),
                                                justify="left") 
    FMScoutInstructions.grid(row=7,column=1,columnspan=3,rowspan=2,padx=20, pady=20, sticky="nw")

    AttributeRankingSelectionClearButton = customtkinter.CTkButton(app,
                                                                   text="Clear",
                                                                   command=Clear,
                                                                   fg_color="#928393")
    AttributeRankingSelectionClearButton.grid(row=4,column=3,padx=20, pady=20, sticky="ew")

    ReloadButton = customtkinter.CTkButton(app,
                                        text="Reload",
                                        command=restart_program)
    ReloadButton.grid(row=6, column=2, pady=20, sticky="ew")

    
    app.mainloop()

GUI()
