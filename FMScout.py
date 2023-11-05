import pandas as pd
import webbrowser, os, time, sys

# Opens the exported HTML file with attributes and creates a dataframe table.
url = r'FMScout.html'
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

def AnotherRoleQ(): # Asks the user if they would like to analyse another role in FM. This block of code has to come before the Into Q in order for AnotherRoleQ to be recognised as a function.
    print('The attribute role ranking should now be open in your browser')
    print('Would you like to analyse any other roles?')
    AnotherRoleAns = input()
    if AnotherRoleAns == str.lower('Yes'):
        RoleQs()
    else:
        print('Thank you for using FMScout')
        time.sleep(2)
        sys.exit()

# Table columns for Goalkeeper roles.

def GKfunc(): # This block of code adds together the rquired attributes for this role, reduces the influence of preferred attributes by 40% and then produces an average score.
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

def SKdefunc(): # This block of code adds together the rquired attributes for this role, reduces the influence of preferred attributes by 40% and then produces an average score.
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

def SKsufunc(): # This block of code adds together the rquired attributes for this role, reduces the influence of preferred attributes by 40% and then produces an average score.
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

def SKatfunc(): # This block of code adds together the rquired attributes for this role, reduces the influence of preferred attributes by 40% and then produces an average score.
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

# Intro and asks which role is being analysed.
# Then based upon the input of the useror RoleInput == passes the custom function of the role that the input text matches to.
# The input text is matched to one of many possible inputs that has been used to describe the role that the user wants to analyse.
# The input text is caseor RoleInput == space and dash insensitive for user experience.
def RoleQs(): # Asks user which role they would like analysed.
    while True:
        print('Hello, welcome to FMScout by Joe Grant. Which role would you like analysed? Type the full name of the role, its short-hand name on FM.')
        RoleInput = input()
        RoleInput = ''.join(RoleInput.split()).lower()

        # Goal-keeper roles

        if RoleInput == 'gk'  or RoleInput ==  'gkdefend'  or RoleInput ==  'gk(defend)'  or RoleInput ==  'gk(de)'  or RoleInput ==  'goalkeeper'  or RoleInput ==  'goal-keeper'   or RoleInput ==  'goalkeeper(de)'   or RoleInput ==  'goal-keeper(de)'   or RoleInput ==  'goalkeeperde'  or RoleInput ==  'goal-keeperde'   or RoleInput ==  'goalkeeperdefend'  or RoleInput ==  'goal-keeperdefend':
            GKfunc()
            AnotherRoleQ()
        elif RoleInput == 'sk'  or RoleInput ==  'sk(defend)'  or RoleInput ==  'skdefend'  or RoleInput ==  'sk(de)'  or RoleInput ==  'skde'  or RoleInput ==  'sweeperkeeper'  or RoleInput ==  'sweeper-keeper'  or RoleInput ==  'sweeperkeeper(de)'  or RoleInput ==  'sweeper-keeper(de)'  or RoleInput ==  'sweeperkeeperde'  or RoleInput ==  'sweeper-keeperde'  or RoleInput ==  'sweeper-keeperdefend'  or RoleInput ==  'sweeperkeeperdefend' :
            SKdefunc()
            AnotherRoleQ()
        elif RoleInput == 'sksu'  or RoleInput ==  'sksupport' or RoleInput ==  'sk(support)' or RoleInput ==  'sk(su)' or RoleInput ==  'sweeperkeeper(su)'  or RoleInput ==  'sweeper-keeper(su)'  or RoleInput ==  'sweeperkeepersu'  or RoleInput ==  'sweeper-keepersu' or RoleInput ==  'sweeper-keepersupport' or RoleInput ==  'sweeperkeepersupport' :
            SKsufunc()
            AnotherRoleQ()
        elif RoleInput == 'skat'  or RoleInput ==  'skattack' or RoleInput ==  'sk(attack)' or RoleInput ==  'sk(at)' or RoleInput ==  'sweeperkeeper(at)'  or RoleInput ==  'sweeper-keeper(at)'  or RoleInput ==  'sweeperkeeperat'  or RoleInput ==  'sweeper-keeperat' or RoleInput ==  'sweeperkeeperattack' or RoleInput ==  'sweeper-keeperattack' :
            SKatfunc()
            AnotherRoleQ()

        # Full-back roles 

        elif RoleInput == 'fb'  or RoleInput ==  'fbdefend' or RoleInput ==  'fb(defend)' or RoleInput ==  'fb(de)' or RoleInput ==  'fbde'  or RoleInput ==  'fullback'  or RoleInput ==  'full-back'  or RoleInput ==  'fullback(de)'  or RoleInput ==  'full-back(de)'  or RoleInput ==  'fullbackde'  or RoleInput ==  'full-backde'  or RoleInput ==  'fullbackdefend'  or RoleInput ==  'full-backdefend':
            FBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'fbsu' or RoleInput ==  'fbsupport' or RoleInput ==  'fb(support)' or RoleInput ==  'fb(su)'  or RoleInput ==  'fullback(su)'  or RoleInput ==  'full-back(su)'  or RoleInput ==  'fullbacksu'  or RoleInput ==  'full-backsu'  or RoleInput ==  'fullbacksupport'  or RoleInput ==  'full-backsupport'  or RoleInput ==  'fullback(support)'  or RoleInput ==  'full-back(support)' :
            FBsufunc()
            AnotherRoleQ()
        elif RoleInput == 'fbat' or RoleInput ==  'fbattack' or RoleInput ==  'fb(attack)'  or RoleInput ==  'fb(at)' or RoleInput ==  'fullback(at)'  or RoleInput ==  'full-back(at)'  or RoleInput ==  'fullbackat'  or RoleInput ==  'full-backat'  or RoleInput ==  'fullbackattack'  or RoleInput ==  'full-backattack'  or RoleInput ==  'fullback(attack)'  or RoleInput ==  'full-back(attack)' :
            FBatfunc()
            AnotherRoleQ()
        elif RoleInput == 'wbde' or RoleInput ==  'wbdefend' or RoleInput ==  'wb(defend)' or RoleInput ==  'wb(de)'  or RoleInput ==  'wingback(de)'  or RoleInput ==  'wing-back(de)'  or RoleInput ==  'wingbackde'  or RoleInput ==  'wing-backde'  or RoleInput ==  'wingbackdefend'  or RoleInput ==  'wing-backdefend'  or RoleInput ==  'wingback(defend)'  or RoleInput ==  'wing-back(defend)' :
            WBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'wbsu'  or RoleInput ==  'wbsupport' or RoleInput ==  'wb(support)' or RoleInput ==  'wb(su)' or RoleInput ==  'wingback(su)'  or RoleInput ==  'wing-back(su)'  or RoleInput ==  'wingbacksu'  or RoleInput ==  'wing-backsu'  or RoleInput ==  'wingbacksupport'  or RoleInput ==  'wing-backsupport'  or RoleInput ==  'wingback(support)'  or RoleInput ==  'wing-back(support)' :
            WBsufunc()
            AnotherRoleQ()
        elif RoleInput == 'wbat'   or RoleInput ==  'wb(at)'   or RoleInput ==  'wbattack'   or RoleInput ==  'wb(attack)'   or RoleInput ==  'wingback(at)'    or RoleInput ==  'wing-back(at)'    or RoleInput ==  'wingbackat'    or RoleInput ==  'wing-backat'    or RoleInput ==  'wingbackattack'    or RoleInput ==  'wing-backattack'    or RoleInput ==  'wingback(attack)'    or RoleInput ==  'wing-back(attack)':
            WBatfunc()
            AnotherRoleQ()
        elif RoleInput == 'cwbsu'  or RoleInput ==  'cwb(su)' or RoleInput ==  'cwbsupport' or RoleInput ==  'cwb(support)' or RoleInput ==  'completewingback(su)'  or RoleInput ==  'completewing-back(su)'  or RoleInput ==  'completewingbacksu'  or RoleInput ==  'completewing-backsu'  or RoleInput ==  'completewingbacksupport'  or RoleInput ==  'completewing-backsupport'  or RoleInput ==  'completewingback(support)'  or RoleInput ==  'completewing-back(support)' or RoleInput ==  'complete-wingback(su)'  or RoleInput ==  'complete-wingbacksu'  or RoleInput ==  'complete-wing-backsu'  or RoleInput ==  'complete-wingbacksupport'  or RoleInput ==  'complete-wing-backsupport'  or RoleInput ==  'complete-wingback(support)'  or RoleInput ==  'complete-wing-back(support)' :
            CWBsufunc()
            AnotherRoleQ()
        elif RoleInput == 'cwbat'  or RoleInput ==  'cwb(at)' or RoleInput ==  'cwbattack' or RoleInput ==  'cwb(attack)' or RoleInput ==  'completewingback(at)'  or RoleInput ==  'completewing-back(at)'  or RoleInput ==  'completewingbackat'  or RoleInput ==  'completewing-backat'  or RoleInput ==  'completewingbackattack'  or RoleInput ==  'completewing-backattack'  or RoleInput ==  'completewingback(attack)'  or RoleInput ==  'completewing-back(attack)' or RoleInput ==  'complete-wingback(at)'  or RoleInput ==  'complete-wingbackat'  or RoleInput ==  'complete-wing-backat'  or RoleInput ==  'complete-wingbackattack'  or RoleInput ==  'complete-wing-backattack'  or RoleInput ==  'complete-wingback(attack)'  or RoleInput ==  'complete-wing-back(attack)' :
            CWBatfunc()
            AnotherRoleQ()
        elif RoleInput == 'iwbde'  or RoleInput ==  'iwb(de)' or RoleInput ==  'iwbdefend' or RoleInput ==  'iwb(defend)' or RoleInput ==  'invertedwingback(de)'  or RoleInput ==  'invertedwing-back(de)'  or RoleInput ==  'invertedwingbackde'  or RoleInput ==  'invertedwing-backde'  or RoleInput ==  'invertedwingbackdefend'  or RoleInput ==  'invertedwing-backdefend'  or RoleInput ==  'invertedwingback(defend)'  or RoleInput ==  'invertedwing-back(defend)' or RoleInput ==  'inverted-wingback(de)'  or RoleInput ==  'inverted-wingbackde'  or RoleInput ==  'inverted-wing-backde'  or RoleInput ==  'inverted-wingbackdefend'  or RoleInput ==  'inverted-wing-backdefend'  or RoleInput ==  'inverted-wingback(defend)'  or RoleInput ==  'inverted-wing-back(defend)' :
            IWBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'iwbsu'  or RoleInput ==  'iwb(su)' or RoleInput ==  'iwbsupport' or RoleInput ==  'iwb(support)' or RoleInput ==  'invertedwingback(su)'  or RoleInput ==  'invertedwing-back(su)'  or RoleInput ==  'invertedwingbacksu'  or RoleInput ==  'invertedwing-backsu'  or RoleInput ==  'invertedwingbacksupport'  or RoleInput ==  'invertedwing-backsupport'  or RoleInput ==  'invertedwingback(support)'  or RoleInput ==  'invertedwing-back(support)' or RoleInput ==  'inverted-wingback(su)'  or RoleInput ==  'inverted-wingbacksu'  or RoleInput ==  'inverted-wing-backsu'  or RoleInput ==  'inverted-wingbacksupport'  or RoleInput ==  'inverted-wing-backsupport'  or RoleInput ==  'inverted-wingback(support)'  or RoleInput ==  'inverted-wing-back(support)' :
            IWBsufunc()
            AnotherRoleQ()
        elif RoleInput == 'iwbat'  or RoleInput ==  'iwb(at)' or RoleInput ==  'iwbattack' or RoleInput ==  'iwb(attack)' or RoleInput ==  'invertedwingback(at)'  or RoleInput ==  'invertedwing-back(at)'  or RoleInput ==  'invertedwingbackat'  or RoleInput ==  'invertedwing-backat'  or RoleInput ==  'invertedwingbackattack'  or RoleInput ==  'invertedwing-backattack'  or RoleInput ==  'invertedwingback(attack)'  or RoleInput ==  'invertedwing-back(attack)' or RoleInput ==  'inverted-wingback(at)'  or RoleInput ==  'inverted-wingbackat'  or RoleInput ==  'inverted-wing-backat'  or RoleInput ==  'inverted-wingbackattack'  or RoleInput ==  'inverted-wing-backattack'  or RoleInput ==  'inverted-wingback(attack)'  or RoleInput ==  'inverted-wing-back(attack)' :
            IWBatfunc()
            AnotherRoleQ()
        elif RoleInput == 'ifbde'  or RoleInput ==  'ifb(de)' or RoleInput ==  'ifbdefend' or RoleInput ==  'ifb(defend)' or RoleInput ==  'ifb' or RoleInput ==  'invertedfullback' or RoleInput ==  'invertedfull-back'  or RoleInput ==  'inverted-fullback' or RoleInput ==  'invertedfullback(de)'  or RoleInput ==  'invertedfull-back(de)'  or RoleInput ==  'invertedfullbackde'  or RoleInput ==  'invertedfull-backde'  or RoleInput ==  'invertedfullbackdefend'  or RoleInput ==  'invertedfull-backdefend'  or RoleInput ==  'invertedfullback(defend)'  or RoleInput ==  'invertedfull-back(defend)' or RoleInput ==  'inverted-fullback(de)'  or RoleInput ==  'inverted-fullbackde'  or RoleInput ==  'inverted-full-backde'  or RoleInput ==  'inverted-fullbackdefend'  or RoleInput ==  'inverted-full-backdefend'  or RoleInput ==  'inverted-fullback(defend)'  or RoleInput ==  'inverted-full-back(defend)' :
            IFBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'nnfbde' or RoleInput == 'nnfb(de)' or RoleInput == 'nnfbdefend' or RoleInput == 'nnfb(defend)' or RoleInput == 'nnfb' or RoleInput ==  'nononsensefullback' or RoleInput ==  'nononsensefull-back'  or RoleInput ==  'nononsense-fullback' or RoleInput ==  'no-nonsensefullback' or RoleInput ==  'no-nonsense-fullback' or RoleInput ==  'no-nonsense-full-back' or RoleInput ==  'nononsense-full-back' or RoleInput ==  'no-nonsensefull-back' or RoleInput ==  'nononsensefullback(de)' or RoleInput ==  'nononsensefull-back(de)'  or RoleInput ==  'nononsense-fullback(de)' or RoleInput ==  'no-nonsensefullback(de)' or RoleInput ==  'no-nonsense-fullback(de)' or RoleInput ==  'no-nonsense-full-back(de)' or RoleInput ==  'nononsense-full-back(de)' or RoleInput ==  'no-nonsensefull-back(de)' or RoleInput ==  'nononsensefullback(defend)' or RoleInput ==  'nononsensefull-back(defend)'  or RoleInput ==  'nononsense-fullback(defend)' or RoleInput ==  'no-nonsensefullback(defend)' or RoleInput ==  'no-nonsense-fullback(defend)' or RoleInput ==  'no-nonsense-full-back(defend)' or RoleInput ==  'nononsense-full-back(defend)' or RoleInput ==  'no-nonsensefull-back(defend)' or RoleInput ==  'nononsensefullbackdefend' or RoleInput ==  'nononsensefull-backdefend'  or RoleInput ==  'nononsense-fullbackdefend' or RoleInput ==  'no-nonsensefullbackdefend' or RoleInput ==  'no-nonsense-fullbackdefend' or RoleInput ==  'no-nonsense-full-backdefend' or RoleInput ==  'nononsense-full-backdefend' or RoleInput ==  'no-nonsensefull-backdefend':
            NNFBdefunc()
            AnotherRoleQ()

        # Centre-back roles 

        elif RoleInput == 'wcbde'  or RoleInput ==  'wcbdefend' or RoleInput ==  'wcb(defend)' or RoleInput ==  'wcb(de)' or RoleInput ==  'wcb' or RoleInput ==  'widecentreback' or RoleInput ==  'widecentre-back'  or RoleInput ==  'wide-centreback' or RoleInput ==  'widecentreback(de)'  or RoleInput ==  'widecentre-back(de)'  or RoleInput ==  'widecentrebackde'  or RoleInput ==  'widecentre-backde'  or RoleInput ==  'widecentrebackdefend'  or RoleInput ==  'widecentre-backdefend'  or RoleInput ==  'widecentreback(defend)'  or RoleInput ==  'widecentre-back(defend)' or RoleInput ==  'wide-centreback(de)'  or RoleInput ==  'wide-centrebackde'  or RoleInput ==  'wide-centre-backde'  or RoleInput ==  'wide-centrebackdefend'  or RoleInput ==  'wide-centre-backdefend'  or RoleInput ==  'wide-centreback(defend)'  or RoleInput ==  'wide-centre-back(defend)' :
            WCBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'wcbsu'  or RoleInput ==  'wcbsupport' or RoleInput ==  'wcb(support)' or RoleInput ==  'wcb(su)' or RoleInput ==  'widecentreback(su)'  or RoleInput ==  'widecentre-back(su)'  or RoleInput ==  'widecentrebacksu'  or RoleInput ==  'widecentre-backsu'  or RoleInput ==  'widecentrebacksupport'  or RoleInput ==  'widecentre-backsupport'  or RoleInput ==  'widecentreback(support)'  or RoleInput ==  'widecentre-back(support)' or RoleInput ==  'wide-centreback(su)'  or RoleInput ==  'wide-centrebacksu'  or RoleInput ==  'wide-centre-backsu'  or RoleInput ==  'wide-centrebacksupport'  or RoleInput ==  'wide-centre-backsupport'  or RoleInput ==  'wide-centreback(support)'  or RoleInput ==  'wide-centre-back(support)' :
            WCBsufunc()
            AnotherRoleQ()
        elif RoleInput == 'wcbat'  or RoleInput ==  'wcbattack' or RoleInput ==  'wcb(attack)' or RoleInput ==  'wcb(at)' or RoleInput ==  'widecentreback(at)'  or RoleInput ==  'widecentre-back(at)'  or RoleInput ==  'widecentrebackat'  or RoleInput ==  'widecentre-backat'  or RoleInput ==  'widecentrebackattack'  or RoleInput ==  'widecentre-backattack'  or RoleInput ==  'widecentreback(attack)'  or RoleInput ==  'widecentre-back(attack)' or RoleInput ==  'wide-centreback(at)'  or RoleInput ==  'wide-centrebackat'  or RoleInput ==  'wide-centre-backat'  or RoleInput ==  'wide-centrebackattack'  or RoleInput ==  'wide-centre-backattack'  or RoleInput ==  'wide-centreback(attack)'  or RoleInput ==  'wide-centre-back(attack)' :
            WCBatfunc()
            AnotherRoleQ()
        elif RoleInput == 'cbde' or RoleInput ==  'cbdefend' or RoleInput ==  'cb(defend)' or RoleInput ==  'cb' or RoleInput ==  'centreback' or RoleInput ==  'centre-back' or RoleInput ==  'cb(de)'  or RoleInput ==  'centreback(de)'  or RoleInput ==  'centre-back(de)'  or RoleInput ==  'centrebackde'  or RoleInput ==  'centre-backde'  or RoleInput ==  'centrebackdefend'  or RoleInput ==  'centre-backdefend'  or RoleInput ==  'centreback(defend)'  or RoleInput ==  'centre-back(defend)' :
            CBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'cbst' or RoleInput ==  'cbstopper' or RoleInput ==  'cb(stopper)' or RoleInput ==  'cb(st)'  or RoleInput ==  'centreback(st)'  or RoleInput ==  'centre-back(st)'  or RoleInput ==  'centrebackst'  or RoleInput ==  'centre-backst'  or RoleInput ==  'centrebackstopper'  or RoleInput ==  'centre-backstopper'  or RoleInput ==  'centreback(stopper)'  or RoleInput ==  'centre-back(stopper)' :
            CBstfunc()
            AnotherRoleQ()
        elif RoleInput == 'cbco' or RoleInput ==  'cbcover' or RoleInput ==  'cb(cover)' or RoleInput ==  'cb(co)'  or RoleInput ==  'centreback(co)'  or RoleInput ==  'centre-back(co)'  or RoleInput ==  'centrebackco'  or RoleInput ==  'centre-backco'  or RoleInput ==  'centrebackcover'  or RoleInput ==  'centre-backcover'  or RoleInput ==  'centreback(cover)'  or RoleInput ==  'centre-back(cover)' :
            CBcofunc()
            AnotherRoleQ()
        elif RoleInput == 'nncbde'  or RoleInput ==  'nncb(de)' or RoleInput ==  'nncbdefend' or RoleInput ==  'nncb(defend)' or RoleInput ==  'nncb' or RoleInput ==  'nononsensecentreback' or RoleInput ==  'nononsensecentre-back'  or RoleInput ==  'nononsense-centreback' or RoleInput ==  'no-nonsensecentreback' or RoleInput ==  'no-nonsense-centreback' or RoleInput ==  'no-nonsense-centre-back' or RoleInput ==  'nononsense-centre-back' or RoleInput ==  'no-nonsensecentre-back' or RoleInput ==  'nononsensecentreback(de)' or RoleInput ==  'nononsensecentre-back(de)'  or RoleInput ==  'nononsense-centreback(de)' or RoleInput ==  'no-nonsensecentreback(de)' or RoleInput ==  'no-nonsense-centreback(de)' or RoleInput ==  'no-nonsense-centre-back(de)' or RoleInput ==  'nononsense-centre-back(de)' or RoleInput ==  'no-nonsensecentre-back(de)' or RoleInput ==  'nononsensecentreback(defend)' or RoleInput ==  'nononsensecentre-back(defend)'  or RoleInput ==  'nononsense-centreback(defend)' or RoleInput ==  'no-nonsensecentreback(defend)' or RoleInput ==  'no-nonsense-centreback(defend)' or RoleInput ==  'no-nonsense-centre-back(defend)' or RoleInput ==  'nononsense-centre-back(defend)' or RoleInput ==  'no-nonsensecentre-back(defend)' or RoleInput ==  'nononsensecentrebackdefend' or RoleInput ==  'nononsensecentre-backdefend'  or RoleInput ==  'nononsense-centrebackdefend' or RoleInput ==  'no-nonsensecentrebackdefend' or RoleInput ==  'no-nonsense-centrebackdefend' or RoleInput ==  'no-nonsense-centre-backdefend' or RoleInput ==  'nononsense-centre-backdefend' or RoleInput ==  'no-nonsensecentre-backdefend' :
            NNCBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'bpdde'  or RoleInput ==  'bpddefend' or RoleInput ==  'bpd(defend)' or RoleInput ==  'bpd(de)' or RoleInput ==  'bpd' or RoleInput ==  'ballplayingdefender' or RoleInput ==  'ballplaying-defender'  or RoleInput ==  'ball-playingdefender' or RoleInput ==  'ballplayingdefender(de)'  or RoleInput ==  'ballplaying-defender(de)'  or RoleInput ==  'ballplayingdefenderde'  or RoleInput ==  'ballplaying-defenderde'  or RoleInput ==  'ballplayingdefenderdefend'  or RoleInput ==  'ballplaying-defenderdefend'  or RoleInput ==  'ballplayingdefender(defend)'  or RoleInput ==  'ballplaying-defender(defend)' or RoleInput ==  'ball-playingdefender(de)'  or RoleInput ==  'ball-playingdefenderde'  or RoleInput ==  'ball-playing-defenderde'  or RoleInput ==  'ball-playingdefenderdefend'  or RoleInput ==  'ball-playing-defenderdefend'  or RoleInput ==  'ball-playingdefender(defend)'  or RoleInput ==  'ball-playing-defender(defend)' :
            BPDdefunc()
            AnotherRoleQ()
        elif RoleInput == 'bpdst'  or RoleInput ==  'bpdstopper' or RoleInput ==  'bpd(stopper)' or RoleInput ==  'bpd(st)' or RoleInput ==  'ballplayingdefender(st)'  or RoleInput ==  'ballplaying-defender(st)'  or RoleInput ==  'ballplayingdefenderst'  or RoleInput ==  'ballplaying-defenderst'  or RoleInput ==  'ballplayingdefenderstopper'  or RoleInput ==  'ballplaying-defenderstopper'  or RoleInput ==  'ballplayingdefender(stopper)'  or RoleInput ==  'ballplaying-defender(stopper)' or RoleInput ==  'ball-playingdefender(st)'  or RoleInput ==  'ball-playingdefenderst'  or RoleInput ==  'ball-playing-defenderst'  or RoleInput ==  'ball-playingdefenderstopper'  or RoleInput ==  'ball-playing-defenderstopper'  or RoleInput ==  'ball-playingdefender(stopper)'  or RoleInput ==  'ball-playing-defender(stopper)' :
            BPDstfunc()
            AnotherRoleQ()
        elif RoleInput == 'bpdco'  or RoleInput ==  'bpdcover' or RoleInput ==  'bpd(cover)' or RoleInput ==  'bpd(co)' or RoleInput ==  'ballplayingdefender(co)'  or RoleInput ==  'ballplaying-defender(co)'  or RoleInput ==  'ballplayingdefenderco'  or RoleInput ==  'ballplaying-defenderco'  or RoleInput ==  'ballplayingdefendercover'  or RoleInput ==  'ballplaying-defendercover'  or RoleInput ==  'ballplayingdefender(cover)'  or RoleInput ==  'ballplaying-defender(cover)' or RoleInput ==  'ball-playingdefender(co)'  or RoleInput ==  'ball-playingdefenderco'  or RoleInput ==  'ball-playing-defenderco'  or RoleInput ==  'ball-playingdefendercover'  or RoleInput ==  'ball-playing-defendercover'  or RoleInput ==  'ball-playingdefender(cover)'  or RoleInput ==  'ball-playing-defender(cover)' :
            BPDcofunc()
            AnotherRoleQ()
        elif RoleInput == 'libde'   or RoleInput ==  'lib'   or RoleInput ==  'libero'   or RoleInput ==  'lib(de)'   or RoleInput ==  'libdefend'   or RoleInput ==  'lib(defend)'   or RoleInput ==  'libero(de)'   or RoleInput ==  'liberodefend'   or RoleInput ==  'libero(defend)':
            LIBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'libsu'   or RoleInput ==  'lib(su)'   or RoleInput ==  'libsupport'   or RoleInput ==  'lib(support)'   or RoleInput ==  'libero(su)'   or RoleInput ==  'liberosupport'   or RoleInput ==  'libero(support)':
            LIBsufunc()
            AnotherRoleQ()
        
        # Defensive midfield roles 

        elif RoleInput == 'dlpmde'  or RoleInput ==  'dlpm(de)' or RoleInput ==  'dlpmdefend' or RoleInput ==  'dlpm(defend)' or RoleInput ==  'dlpm' or RoleInput ==  'deeplyingplaymaker' or RoleInput ==  'deeplyingplay-maker'  or RoleInput ==  'deeplying-playmaker' or RoleInput ==  'deep-lyingplaymaker' or RoleInput ==  'deep-lying-playmaker' or RoleInput ==  'deep-lying-play-maker' or RoleInput ==  'deeplying-play-maker' or RoleInput ==  'deep-lyingplay-maker' or RoleInput ==  'deeplyingplaymaker(de)' or RoleInput ==  'deeplyingplay-maker(de)'  or RoleInput ==  'deeplying-playmaker(de)' or RoleInput ==  'deep-lyingplaymaker(de)' or RoleInput ==  'deep-lying-playmaker(de)' or RoleInput ==  'deep-lying-play-maker(de)' or RoleInput ==  'deeplying-play-maker(de)' or RoleInput ==  'deep-lyingplay-maker(de)' or RoleInput ==  'deeplyingplaymaker(defend)' or RoleInput ==  'deeplyingplay-maker(defend)'  or RoleInput ==  'deeplying-playmaker(defend)' or RoleInput ==  'deep-lyingplaymaker(defend)' or RoleInput ==  'deep-lying-playmaker(defend)' or RoleInput ==  'deep-lying-play-maker(defend)' or RoleInput ==  'deeplying-play-maker(defend)' or RoleInput ==  'deep-lyingplay-maker(defend)' or RoleInput ==  'deeplyingplaymakerdefend' or RoleInput ==  'deeplyingplay-makerdefend'  or RoleInput ==  'deeplying-playmakerdefend' or RoleInput ==  'deep-lyingplaymakerdefend' or RoleInput ==  'deep-lying-playmakerdefend' or RoleInput ==  'deep-lying-play-makerdefend' or RoleInput ==  'deeplying-play-makerdefend' or RoleInput ==  'deep-lyingplay-makerdefend' :
            DLPMdefunc()
            AnotherRoleQ()
        elif RoleInput == 'dlpmsu'  or RoleInput ==  'dlpm(su)' or RoleInput ==  'dlpmsupport' or RoleInput ==  'dlpm(support)' or RoleInput ==  'deeplyingplaymaker(su)' or RoleInput ==  'deeplyingplay-maker(su)'  or RoleInput ==  'deeplying-playmaker(su)' or RoleInput ==  'deep-lyingplaymaker(su)' or RoleInput ==  'deep-lying-playmaker(su)' or RoleInput ==  'deep-lying-play-maker(su)' or RoleInput ==  'deeplying-play-maker(su)' or RoleInput ==  'deep-lyingplay-maker(su)' or RoleInput ==  'deeplyingplaymaker(support)' or RoleInput ==  'deeplyingplay-maker(support)'  or RoleInput ==  'deeplying-playmaker(support)' or RoleInput ==  'deep-lyingplaymaker(support)' or RoleInput ==  'deep-lying-playmaker(support)' or RoleInput ==  'deep-lying-play-maker(support)' or RoleInput ==  'deeplying-play-maker(support)' or RoleInput ==  'deep-lyingplay-maker(support)' or RoleInput ==  'deeplyingplaymakersupport' or RoleInput ==  'deeplyingplay-makersupport'  or RoleInput ==  'deeplying-playmakersupport' or RoleInput ==  'deep-lyingplaymakersupport' or RoleInput ==  'deep-lying-playmakersupport' or RoleInput ==  'deep-lying-play-makersupport' or RoleInput ==  'deeplying-play-makersupport' or RoleInput ==  'deep-lyingplay-makersupport' :
            DLPMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'dmde' or RoleInput ==  'dmdefend' or RoleInput ==  'dm(defend)' or RoleInput ==  'dm' or RoleInput ==  'defensivemid' or RoleInput ==  'defensive-mid' or RoleInput ==  'defensivemidfielder' or RoleInput ==  'defensive-midfielder' or RoleInput ==  'dm(de)'  or RoleInput ==  'defensivemid(de)'  or RoleInput ==  'defensivemidfielder(de)'  or RoleInput ==  'defensive-mid(de)'  or RoleInput ==  'defensive-midfielder(de)'  or RoleInput ==  'defensivemid(defend)'  or RoleInput ==  'defensivemidfielder(defend)'  or RoleInput ==  'defensive-mid(defend)'  or RoleInput ==  'defensive-midfielder(defend)'  or RoleInput ==  'defensivemidde'  or RoleInput ==  'defensivemidfielderde'  or RoleInput ==  'defensive-midde'  or RoleInput ==  'defensive-midfielderde'  or RoleInput ==  'defensivemiddefend'  or RoleInput ==  'defensivemidfielderdefend'  or RoleInput ==  'defensive-middefend'  or RoleInput ==  'defensive-midfielderdefend'  :
            DMdefunc()
            AnotherRoleQ()
        elif RoleInput == 'dmsu' or RoleInput ==  'dmsupport' or RoleInput ==  'dm(support)' or RoleInput ==  'dm' or RoleInput ==  'defensivemid' or RoleInput ==  'defensive-mid' or RoleInput ==  'defensivemidfielder' or RoleInput ==  'defensive-midfielder' or RoleInput ==  'dm(su)'  or RoleInput ==  'defensivemid(su)'  or RoleInput ==  'defensivemidfielder(su)'  or RoleInput ==  'defensive-mid(su)'  or RoleInput ==  'defensive-midfielder(su)'  or RoleInput ==  'defensivemid(support)'  or RoleInput ==  'defensivemidfielder(support)'  or RoleInput ==  'defensive-mid(support)'  or RoleInput ==  'defensive-midfielder(support)'  or RoleInput ==  'defensivemidsu'  or RoleInput ==  'defensivemidfieldersu'  or RoleInput ==  'defensive-midsu'  or RoleInput ==  'defensive-midfieldersu'  or RoleInput ==  'defensivemidsupport'  or RoleInput ==  'defensivemidfieldersupport'  or RoleInput ==  'defensive-midsupport'  or RoleInput ==  'defensive-midfieldersupport'  :
            DMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'regsu'   or RoleInput ==  'reg'   or RoleInput ==  'regista'   or RoleInput ==  'reg(su)'   or RoleInput ==  'regsupport'   or RoleInput ==  'reg(support)'   or RoleInput ==  'regista(su)'   or RoleInput ==  'registasupport'   or RoleInput ==  'regista(support)':
            REGsufunc()
            AnotherRoleQ()
        elif RoleInput == 'hb'  or RoleInput ==  'hbdefend' or RoleInput ==  'hb(defend)' or RoleInput ==  'hb(de)' or RoleInput ==  'hbde'  or RoleInput ==  'halfback'  or RoleInput ==  'half-back'  or RoleInput ==  'halfback(de)'  or RoleInput ==  'half-back(de)'  or RoleInput ==  'halfbackde'  or RoleInput ==  'half-backde'  or RoleInput ==  'halfbackdefend'  or RoleInput ==  'half-backdefend':
            HBdefunc()
            AnotherRoleQ()
        elif RoleInput == 'rpmsu' or RoleInput ==  'rpm'  or RoleInput ==  'rpm(su)' or RoleInput ==  'rpmsupport' or RoleInput ==  'rpm(support)' or RoleInput ==  'roamingplaymaker' or RoleInput ==  'roaming-playmaker' or RoleInput ==  'roaming-play-maker' or RoleInput ==  'roamingplay-maker' or RoleInput ==  'roamingplaymaker(su)' or RoleInput ==  'roamingplay-maker(su)'  or RoleInput ==  'roaming-playmaker(su)' or RoleInput ==  'roaming-play-maker(su)' or RoleInput ==  'roamingplaymaker(support)' or RoleInput ==  'roamingplay-maker(support)'  or RoleInput ==  'roaming-playmaker(support)' or RoleInput ==  'roaming-play-maker(support)' or RoleInput ==  'roamingplaymakersupport' or RoleInput ==  'roamingplay-makersupport'  or RoleInput ==  'roaming-playmakersupport' or RoleInput ==  'roaming-play-makersupport' :
            RPMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'ancde'   or RoleInput ==  'anc'   or RoleInput ==  'anchor'   or RoleInput ==  'anc(de)'   or RoleInput ==  'ancdefend'   or RoleInput ==  'anc(defend)'   or RoleInput ==  'anchor(de)'   or RoleInput ==  'anchordefend'   or RoleInput ==  'anchor(defend)':
            ANCdefunc()
            AnotherRoleQ()
        elif RoleInput == 'svsu' or RoleInput ==  'svsupport' or RoleInput ==  'sv(support)' or RoleInput ==  'sv' or RoleInput ==  'segundovolante' or RoleInput ==  'segundo-volante' or RoleInput ==  'sv(su)'  or RoleInput ==  'segundovolante(su)'  or RoleInput ==  'segundo-volante(su)'  or RoleInput ==  'segundovolantesu'  or RoleInput ==  'segundo-volantesu'  or RoleInput ==  'segundovolantesupport'  or RoleInput ==  'segundo-volantesupport'  or RoleInput ==  'segundovolante(support)'  or RoleInput ==  'segundo-volante(support)' :
            SVsufunc()
            AnotherRoleQ()
        elif RoleInput == 'svat' or RoleInput ==  'svattack' or RoleInput ==  'sv(attack)' or RoleInput ==  'sv(at)'  or RoleInput ==  'segundovolante(at)'  or RoleInput ==  'segundo-volante(at)'  or RoleInput ==  'segundovolanteat'  or RoleInput ==  'segundo-volanteat'  or RoleInput ==  'segundovolanteattack'  or RoleInput ==  'segundo-volanteattack'  or RoleInput ==  'segundovolante(attack)'  or RoleInput ==  'segundo-volante(attack)' :
            SVatfunc()
            AnotherRoleQ()
        elif RoleInput == 'bwmde'  or RoleInput ==  'bwm(de)' or RoleInput ==  'bwmdefend' or RoleInput ==  'bwm(defend)' or RoleInput ==  'bwm' or RoleInput ==  'ballwinningmidfielder' or RoleInput ==  'ballwinningmid-fielder'  or RoleInput ==  'ballwinning-midfielder' or RoleInput ==  'ball-winningmidfielder' or RoleInput ==  'ball-winning-midfielder' or RoleInput ==  'ball-winning-mid-fielder' or RoleInput ==  'ballwinning-mid-fielder' or RoleInput ==  'ball-winningmid-fielder' or RoleInput ==  'ballwinningmidfielder(de)' or RoleInput ==  'ballwinningmid-fielder(de)'  or RoleInput ==  'ballwinning-midfielder(de)' or RoleInput ==  'ball-winningmidfielder(de)' or RoleInput ==  'ball-winning-midfielder(de)' or RoleInput ==  'ball-winning-mid-fielder(de)' or RoleInput ==  'ballwinning-mid-fielder(de)' or RoleInput ==  'ball-winningmid-fielder(de)' or RoleInput ==  'ballwinningmidfielder(defend)' or RoleInput ==  'ballwinningmid-fielder(defend)'  or RoleInput ==  'ballwinning-midfielder(defend)' or RoleInput ==  'ball-winningmidfielder(defend)' or RoleInput ==  'ball-winning-midfielder(defend)' or RoleInput ==  'ball-winning-mid-fielder(defend)' or RoleInput ==  'ballwinning-mid-fielder(defend)' or RoleInput ==  'ball-winningmid-fielder(defend)' or RoleInput ==  'ballwinningmidfielderdefend' or RoleInput ==  'ballwinningmid-fielderdefend'  or RoleInput ==  'ballwinning-midfielderdefend' or RoleInput ==  'ball-winningmidfielderdefend' or RoleInput ==  'ball-winning-midfielderdefend' or RoleInput ==  'ball-winning-mid-fielderdefend' or RoleInput ==  'ballwinning-mid-fielderdefend' or RoleInput ==  'ball-winningmid-fielderdefend' :
            BWMdefunc()
            AnotherRoleQ()
        elif RoleInput == 'bwmsu'  or RoleInput ==  'bwm(su)' or RoleInput ==  'bwmsupport' or RoleInput ==  'bwm(support)' or RoleInput ==  'ballwinningmidfielder(su)' or RoleInput ==  'ballwinningmid-fielder(su)'  or RoleInput ==  'ballwinning-midfielder(su)' or RoleInput ==  'ball-winningmidfielder(su)' or RoleInput ==  'ball-winning-midfielder(su)' or RoleInput ==  'ball-winning-mid-fielder(su)' or RoleInput ==  'ballwinning-mid-fielder(su)' or RoleInput ==  'ball-winningmid-fielder(su)' or RoleInput ==  'ballwinningmidfielder(support)' or RoleInput ==  'ballwinningmid-fielder(support)'  or RoleInput ==  'ballwinning-midfielder(support)' or RoleInput ==  'ball-winningmidfielder(support)' or RoleInput ==  'ball-winning-midfielder(support)' or RoleInput ==  'ball-winning-mid-fielder(support)' or RoleInput ==  'ballwinning-mid-fielder(support)' or RoleInput ==  'ball-winningmid-fielder(support)' or RoleInput ==  'ballwinningmidfieldersupport' or RoleInput ==  'ballwinningmid-fieldersupport'  or RoleInput ==  'ballwinning-midfieldersupport' or RoleInput ==  'ball-winningmidfieldersupport' or RoleInput ==  'ball-winning-midfieldersupport' or RoleInput ==  'ball-winning-mid-fieldersupport' or RoleInput ==  'ballwinning-mid-fieldersupport' or RoleInput ==  'ball-winningmid-fieldersupport' :
            BWMsufunc()
            AnotherRoleQ()
        
        # Central midfield roles 

        elif RoleInput == 'cmde' or RoleInput ==  'cmdefend' or RoleInput ==  'cm(defend)' or RoleInput ==  'cm(de)'  or RoleInput ==  'centralmid(de)'  or RoleInput ==  'centralmidfielder(de)'  or RoleInput ==  'central-mid(de)'  or RoleInput ==  'central-midfielder(de)'  or RoleInput ==  'centralmid(defend)'  or RoleInput ==  'centralmidfielder(defend)'  or RoleInput ==  'central-mid(defend)'  or RoleInput ==  'central-midfielder(defend)'  or RoleInput ==  'centralmidde'  or RoleInput ==  'centralmidfielderde'  or RoleInput ==  'central-midde'  or RoleInput ==  'central-midfielderde'  or RoleInput ==  'centralmiddefend'  or RoleInput ==  'centralmidfielderdefend'  or RoleInput ==  'central-middefend'  or RoleInput ==  'central-midfielderdefend'  :
            CMdefunc()
            AnotherRoleQ()
        elif RoleInput == 'cmsu' or RoleInput ==  'cm' or RoleInput ==  'centralmid' or RoleInput ==  'centralmidfielder' or RoleInput ==  'centremid' or RoleInput ==  'centermid' or RoleInput ==  'centermidfielder' or RoleInput ==  'cmsupport' or RoleInput ==  'cm(support)' or RoleInput ==  'cm(su)'  or RoleInput ==  'centralmid(su)'  or RoleInput ==  'centralmidfielder(su)'  or RoleInput ==  'central-mid(su)'  or RoleInput ==  'central-midfielder(su)'  or RoleInput ==  'centralmid(support)'  or RoleInput ==  'centralmidfielder(support)'  or RoleInput ==  'central-mid(support)'  or RoleInput ==  'central-midfielder(support)'  or RoleInput ==  'centralmidsu'  or RoleInput ==  'centralmidfieldersu'  or RoleInput ==  'central-midsu'  or RoleInput ==  'central-midfieldersu'  or RoleInput ==  'centralmidsupport'  or RoleInput ==  'centralmidfieldersupport'  or RoleInput ==  'central-midsupport'  or RoleInput ==  'central-midfieldersupport'  :
            CMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'cmat' or RoleInput ==  'cmdattack' or RoleInput ==  'cm(attack)' or RoleInput ==  'cm(at)'  or RoleInput ==  'centralmid(at)'  or RoleInput ==  'centralmidfielder(at)'  or RoleInput ==  'central-mid(at)'  or RoleInput ==  'central-midfielder(at)'  or RoleInput ==  'centralmid(attack)'  or RoleInput ==  'centralmidfielder(attack)'  or RoleInput ==  'central-mid(attack)'  or RoleInput ==  'central-midfielder(attack)'  or RoleInput ==  'centralmidat'  or RoleInput ==  'centralmidfielderat'  or RoleInput ==  'central-midat'  or RoleInput ==  'central-midfielderat'  or RoleInput ==  'centralmidattack'  or RoleInput ==  'centralmidfielderattack'  or RoleInput ==  'central-midattack'  or RoleInput ==  'central-midfielderattack'  :
            CMatfunc()
            AnotherRoleQ()
        elif RoleInput == 'carsu'   or RoleInput ==  'car'   or RoleInput ==  'carrilero'   or RoleInput ==  'car(su)'   or RoleInput ==  'carsupport'   or RoleInput ==  'car(support)'   or RoleInput ==  'carrilero(su)'   or RoleInput ==  'carrilerosupport'   or RoleInput ==  'carrilero(support)':
            CARsufunc()
            AnotherRoleQ()
        elif RoleInput == 'mezsu'   or RoleInput ==  'mez'   or RoleInput ==  'mezzala'   or RoleInput ==  'mez(su)'   or RoleInput ==  'mezsupport'   or RoleInput ==  'mez(support)'   or RoleInput ==  'mezzala(su)'   or RoleInput ==  'mezzalasupport'   or RoleInput ==  'mezzala(support)':
            MEZsufunc()
            AnotherRoleQ()
        elif RoleInput == 'mezat'   or RoleInput ==  'mez(at)'   or RoleInput ==  'mezattack'   or RoleInput ==  'mez(attack)'   or RoleInput ==  'mezzala(at)'   or RoleInput ==  'mezzalaattack'   or RoleInput ==  'mezzala(attack)':
            MEZatfunc()
            AnotherRoleQ()
        elif RoleInput == 'B2Bsu'   or RoleInput ==  'b2b'   or RoleInput ==  'b2bm'   or RoleInput ==  'b2bmsu'   or RoleInput ==  'b2bm(su)'   or RoleInput ==  'btb'   or RoleInput ==  'btbm'   or RoleInput ==  'btbmsu'   or RoleInput ==  'btbm(su)'   or RoleInput ==  'boxtoboxmidfielder'   or RoleInput ==  'box-toboxmidfielder'   or RoleInput ==  'box-to-boxmidfielder'   or RoleInput ==  'box-to-box-midfielder'   or RoleInput ==  'box-to-box-mid-fielder'   or RoleInput ==  'boxto-box-mid-fielder'   or RoleInput ==  'boxtobox-mid-fielder'   or RoleInput ==  'boxtoboxmid-fielder'   or RoleInput ==  'boxtoboxmid-fielder'   or RoleInput ==  'box-tobox-mid-fielder'   or RoleInput ==  'box-to-boxmid-fielder'   or RoleInput ==  'boxtoboxmidfieldersu'   or RoleInput ==  'box-toboxmidfieldersu'   or RoleInput ==  'box-to-boxmidfieldersu'   or RoleInput ==  'box-to-box-midfieldersu'   or RoleInput ==  'box-to-box-mid-fieldersu'   or RoleInput ==  'boxto-box-mid-fieldersu'   or RoleInput ==  'boxtobox-mid-fieldersu'   or RoleInput ==  'boxtoboxmid-fieldersu'   or RoleInput ==  'boxtoboxmid-fieldersu'   or RoleInput ==  'box-tobox-mid-fieldersu'   or RoleInput ==  'box-to-boxmid-fieldersu'   or RoleInput ==  'boxtoboxmidfielder(su)'   or RoleInput ==  'box-toboxmidfielder(su)'   or RoleInput ==  'box-to-boxmidfielder(su)'   or RoleInput ==  'box-to-box-midfielder(su)'   or RoleInput ==  'box-to-box-mid-fielder(su)'   or RoleInput ==  'boxto-box-mid-fielder(su)'   or RoleInput ==  'boxtobox-mid-fielder(su)'   or RoleInput ==  'boxtoboxmid-fielder(su)'   or RoleInput ==  'boxtoboxmid-fielder(su)'   or RoleInput ==  'box-tobox-mid-fielder(su)'   or RoleInput ==  'box-to-boxmid-fielder(su)'   or RoleInput ==  'boxtoboxmidfieldersupport'   or RoleInput ==  'box-toboxmidfieldersupport'   or RoleInput ==  'box-to-boxmidfieldersupport'   or RoleInput ==  'box-to-box-midfieldersupport'   or RoleInput ==  'box-to-box-mid-fieldersupport'   or RoleInput ==  'boxto-box-mid-fieldersupport'   or RoleInput ==  'boxtobox-mid-fieldersupport'   or RoleInput ==  'boxtoboxmid-fieldersupport'   or RoleInput ==  'boxtoboxmid-fieldersupport'   or RoleInput ==  'box-tobox-mid-fieldersupport'   or RoleInput ==  'box-to-boxmid-fieldersupport'   or RoleInput ==  'boxtoboxmidfielder(support)'   or RoleInput ==  'box-toboxmidfielder(support)'   or RoleInput ==  'box-to-boxmidfielder(support)'   or RoleInput ==  'box-to-box-midfielder(support)'   or RoleInput ==  'box-to-box-mid-fielder(support)'   or RoleInput ==  'boxto-box-mid-fielder(support)'   or RoleInput ==  'boxtobox-mid-fielder(support)'   or RoleInput ==  'boxtoboxmid-fielder(support)'   or RoleInput ==  'boxtoboxmid-fielder(support)'   or RoleInput ==  'box-tobox-mid-fielder(support)'   or RoleInput ==  'box-to-boxmid-fielder(support)':
            B2Bsufunc()
            AnotherRoleQ()
        
        # Wide midfield roles 

        elif RoleInput == 'wpmsu'   or RoleInput ==  'wpm'    or RoleInput ==  'wpm(su)'   or RoleInput ==  'wpmsupport'   or RoleInput ==  'wpm(support)'   or RoleInput ==  'wideplaymaker'   or RoleInput ==  'wide-playmaker'   or RoleInput ==  'wideplay-maker'   or RoleInput ==  'wide-play-maker'   or RoleInput ==  'wideplaymaker(su)'   or RoleInput ==  'wideplay-maker(su)'    or RoleInput ==  'wide-playmaker(su)'   or RoleInput ==  'wide-play-maker(su)'   or RoleInput ==  'wideplaymaker(support)'   or RoleInput ==  'wideplay-maker(support)'    or RoleInput ==  'wide-playmaker(support)'   or RoleInput ==  'wide-play-maker(support)'   or RoleInput ==  'wideplaymakersupport'   or RoleInput ==  'wideplay-makersupport'    or RoleInput ==  'wide-playmakersupport'   or RoleInput ==  'wide-play-makersupport' :
            WPMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'wpmat'   or RoleInput ==  'wpm'    or RoleInput ==  'wpm(at)'   or RoleInput ==  'wpmattack'   or RoleInput ==  'wpm(attack)'   or RoleInput ==  'wideplaymaker(at)'   or RoleInput ==  'wideplay-maker(at)'    or RoleInput ==  'wide-playmaker(at)'   or RoleInput ==  'wide-play-maker(at)'   or RoleInput ==  'wideplaymaker(attack)'   or RoleInput ==  'wideplay-maker(attack)'    or RoleInput ==  'wide-playmaker(attack)'   or RoleInput ==  'wide-play-maker(attack)'   or RoleInput ==  'wideplaymakerattack'   or RoleInput ==  'wideplay-makerattack'    or RoleInput ==  'wide-playmakerattack'   or RoleInput ==  'wide-play-makerattack' :
            WPMatfunc()
            AnotherRoleQ()
        elif RoleInput == 'dwde'  or RoleInput ==  'dw(de)' or RoleInput ==  'dw' or RoleInput ==  'dwdefend' or RoleInput ==  'dw(defend)' or RoleInput ==  'defensivewinger'  or RoleInput ==  'defensive-winger'  or RoleInput ==  'defensivewinger(de)'  or RoleInput ==  'defensive-winger(de)'  or RoleInput ==  'defensivewingerde'  or RoleInput ==  'defensive-wingerde'  or RoleInput ==  'defensivewingerdefend'  or RoleInput ==  'defensive-wingerdefend' or RoleInput ==  'defensivewinger(defend)'  or RoleInput ==  'defensive-winger(defend)' :
            DWdefunc()
            AnotherRoleQ()
        elif RoleInput == 'dwsu'  or RoleInput ==  'dw(su)' or RoleInput ==  'dwsupport' or RoleInput ==  'dw(support)' or RoleInput ==  'defensivewinger(su)'  or RoleInput ==  'defensive-winger(su)'  or RoleInput ==  'defensivewingersu'  or RoleInput ==  'defensive-wingersu'  or RoleInput ==  'defensivewingersupport'  or RoleInput ==  'defensive-wingersupport' or RoleInput ==  'defensivewinger(support)'  or RoleInput ==  'defensive-winger(support)' :
            DWsufunc()
            AnotherRoleQ()
        elif RoleInput == 'wmde' or RoleInput ==  'wmdefend' or RoleInput ==  'wm(defend)' or RoleInput ==  'wm(de)'  or RoleInput ==  'widemid(de)'  or RoleInput ==  'widemidfielder(de)'  or RoleInput ==  'wide-mid(de)'  or RoleInput ==  'wide-midfielder(de)'  or RoleInput ==  'widemid(defend)'  or RoleInput ==  'widemidfielder(defend)'  or RoleInput ==  'wide-mid(defend)'  or RoleInput ==  'wide-midfielder(defend)'  or RoleInput ==  'widemidde'  or RoleInput ==  'widemidfielderde'  or RoleInput ==  'wide-midde'  or RoleInput ==  'wide-midfielderde'  or RoleInput ==  'widemiddefend'  or RoleInput ==  'widemidfielderdefend'  or RoleInput ==  'wide-middefend'  or RoleInput ==  'wide-midfielderdefend'  or RoleInput ==  'widemid-fielder(de)'  or RoleInput ==  'wide-mid(de)'  or RoleInput ==  'wide-mid-fielder(de)'  or RoleInput ==  'widemid(defend)'  or RoleInput ==  'widemid-fielder(defend)'  or RoleInput ==  'wide-mid(defend)'  or RoleInput ==  'wide-mid-fielder(defend)'  or RoleInput ==  'widemidde'  or RoleInput ==  'widemid-fielderde'  or RoleInput ==  'wide-midde'  or RoleInput ==  'wide-mid-fielderde'  or RoleInput ==  'widemiddefend'  or RoleInput ==  'widemid-fielderdefend'  or RoleInput ==  'wide-middefend'  or RoleInput ==  'wide-mid-fielderdefend'  :
            WMdefunc()
            AnotherRoleQ()
        elif RoleInput == 'wmsu' or RoleInput ==  'wm' or RoleInput ==  'widemid' or RoleInput ==  'widemidfielder' or RoleInput ==  'wmsupport' or RoleInput ==  'wm(support)' or RoleInput ==  'wm(su)'  or RoleInput ==  'widemid(su)'  or RoleInput ==  'widemidfielder(su)'  or RoleInput ==  'wide-mid(su)'  or RoleInput ==  'wide-midfielder(su)'  or RoleInput ==  'widemid(support)'  or RoleInput ==  'widemidfielder(support)'  or RoleInput ==  'wide-mid(support)'  or RoleInput ==  'wide-midfielder(support)'  or RoleInput ==  'widemidsu'  or RoleInput ==  'widemidfieldersu'  or RoleInput ==  'wide-midsu'  or RoleInput ==  'wide-midfieldersu'  or RoleInput ==  'widemidsupport'  or RoleInput ==  'widemidfieldersupport'  or RoleInput ==  'wide-midsupport'  or RoleInput ==  'wide-midfieldersupport'  or RoleInput ==  'widemid-fielder(su)'  or RoleInput ==  'wide-mid(su)'  or RoleInput ==  'wide-mid-fielder(su)'  or RoleInput ==  'widemid(support)'  or RoleInput ==  'widemid-fielder(support)'  or RoleInput ==  'wide-mid(support)'  or RoleInput ==  'wide-mid-fielder(support)'  or RoleInput ==  'widemidsu'  or RoleInput ==  'widemid-fieldersu'  or RoleInput ==  'wide-midsu'  or RoleInput ==  'wide-mid-fieldersu'  or RoleInput ==  'widemidsupport'  or RoleInput ==  'widemid-fieldersupport'  or RoleInput ==  'wide-midsupport'  or RoleInput ==  'wide-mid-fieldersupport'  :
            WMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'wmat' or RoleInput ==  'wmattack' or RoleInput ==  'wm(attack)' or RoleInput ==  'wm(at)'  or RoleInput ==  'widemid(at)'  or RoleInput ==  'widemidfielder(at)'  or RoleInput ==  'wide-mid(at)'  or RoleInput ==  'wide-midfielder(at)'  or RoleInput ==  'widemid(attack)'  or RoleInput ==  'widemidfielder(attack)'  or RoleInput ==  'wide-mid(attack)'  or RoleInput ==  'wide-midfielder(attack)'  or RoleInput ==  'widemidat'  or RoleInput ==  'widemidfielderat'  or RoleInput ==  'wide-midat'  or RoleInput ==  'wide-midfielderat'  or RoleInput ==  'widemidattack'  or RoleInput ==  'widemidfielderattack'  or RoleInput ==  'wide-midattack'  or RoleInput ==  'wide-midfielderattack'  or RoleInput ==  'widemid-fielder(at)'  or RoleInput ==  'wide-mid(at)'  or RoleInput ==  'wide-mid-fielder(at)'  or RoleInput ==  'widemid(attack)'  or RoleInput ==  'widemid-fielder(attack)'  or RoleInput ==  'wide-mid(attack)'  or RoleInput ==  'wide-mid-fielder(attack)'  or RoleInput ==  'widemidat'  or RoleInput ==  'widemid-fielderat'  or RoleInput ==  'wide-midat'  or RoleInput ==  'wide-mid-fielderat'  or RoleInput ==  'widemiddefend'  or RoleInput ==  'widemid-fielderattack'  or RoleInput ==  'wide-midattack'  or RoleInput ==  'wide-mid-fielderattack'  :
            WMatfunc()
            AnotherRoleQ()

        # Central attacking midfield roles

        elif RoleInput == 'apmsu' or RoleInput ==  'apm'  or RoleInput ==  'apm(su)' or RoleInput ==  'apmsupport' or RoleInput ==  'apm(support)' or RoleInput ==  'advancedplaymaker' or RoleInput ==  'advanced-playmaker' or RoleInput ==  'advanced-play-maker' or RoleInput ==  'advancedplay-maker' or RoleInput ==  'advancedplaymaker(su)' or RoleInput ==  'advancedplay-maker(su)'  or RoleInput ==  'advanced-playmaker(su)' or RoleInput ==  'advanced-play-maker(su)' or RoleInput ==  'advancedplaymaker(support)' or RoleInput ==  'advancedplay-maker(support)'  or RoleInput ==  'advanced-playmaker(support)' or RoleInput ==  'advanced-play-maker(support)' or RoleInput ==  'advancedplaymakersupport' or RoleInput ==  'advancedplay-makersupport'  or RoleInput ==  'advanced-playmakersupport' or RoleInput ==  'advanced-play-makersupport' :
            APMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'apmat' or RoleInput ==  'apm(at)' or RoleInput ==  'apmattack' or RoleInput ==  'apm(attack)' or RoleInput ==  'advancedplaymaker(at)' or RoleInput ==  'advancedplay-maker(at)'  or RoleInput ==  'advanced-playmaker(at)' or RoleInput ==  'advanced-play-maker(at)' or RoleInput ==  'advancedplaymaker(attack)' or RoleInput ==  'advancedplay-maker(attack)'  or RoleInput ==  'advanced-playmaker(attack)' or RoleInput ==  'advanced-play-maker(attack)' or RoleInput ==  'advancedplaymakerattack' or RoleInput ==  'advancedplay-makerattack'  or RoleInput ==  'advanced-playmakerattack' or RoleInput ==  'advanced-play-makerattack' :
            APMatfunc()
            AnotherRoleQ()
        elif RoleInput == 'amsu' or RoleInput ==  'amsupport' or RoleInput ==  'am(support)' or RoleInput ==  'am' or RoleInput ==  'attackingmid' or RoleInput ==  'attacking-mid' or RoleInput ==  'attackingmidfielder' or RoleInput ==  'attacking-midfielder' or RoleInput ==  'am(su)'  or RoleInput ==  'attackingmid(su)'  or RoleInput ==  'attackingmidfielder(su)'  or RoleInput ==  'attacking-mid(su)'  or RoleInput ==  'attacking-midfielder(su)'  or RoleInput ==  'attackingmid(support)'  or RoleInput ==  'attackingmidfielder(support)'  or RoleInput ==  'attacking-mid(support)'  or RoleInput ==  'attacking-midfielder(support)'  or RoleInput ==  'attackingmidsu'  or RoleInput ==  'attackingmidfieldersu'  or RoleInput ==  'attacking-midsu'  or RoleInput ==  'attacking-midfieldersu'  or RoleInput ==  'attackingmidsupport'  or RoleInput ==  'attackingmidfieldersupport'  or RoleInput ==  'attacking-midsupport'  or RoleInput ==  'attacking-midfieldersupport'  :
            AMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'amat' or RoleInput ==  'amattack' or RoleInput ==  'am(attack)' or RoleInput ==  'am(at)'  or RoleInput ==  'attackingmid(at)'  or RoleInput ==  'attackingmidfielder(at)'  or RoleInput ==  'attacking-mid(at)'  or RoleInput ==  'attacking-midfielder(at)'  or RoleInput ==  'attackingmid(attack)'  or RoleInput ==  'attackingmidfielder(attack)'  or RoleInput ==  'attacking-mid(attack)'  or RoleInput ==  'attacking-midfielder(attack)'  or RoleInput ==  'attackingmidat'  or RoleInput ==  'attackingmidfielderat'  or RoleInput ==  'attacking-midat'  or RoleInput ==  'attacking-midfielderat'  or RoleInput ==  'attackingmidattack'  or RoleInput ==  'attackingmidfielderattack'  or RoleInput ==  'attacking-midattack'  or RoleInput ==  'attacking-midfielderattack'  :
            AMatfunc()
            AnotherRoleQ()
        elif RoleInput == 'ssat'  or RoleInput ==  'ss' or RoleInput ==  'ss(at)' or RoleInput ==  'ssattack' or RoleInput ==  'ss(attack)' or RoleInput ==  'shadowstriker' or RoleInput ==  'shadowstriker(at)'  or RoleInput ==  'shadow-striker(at)'  or RoleInput ==  'shadowstrikerat'  or RoleInput ==  'shadow-striker'  or RoleInput ==  'shadowstrikerattack'  or RoleInput ==  'shadow-strikerattack' or RoleInput ==  'shadowstriker(attack)'  or RoleInput ==  'shadow-striker(attack)' :
            SSatfunc()
            AnotherRoleQ()
        elif RoleInput == 'treat'   or RoleInput ==  'tre'   or RoleInput ==  'tre(at)'   or RoleInput ==  'treattack'   or RoleInput ==  'tre(attack)'   or RoleInput ==  'trequartista'   or RoleInput ==  'trequartista(at)'   or RoleInput ==  'trequartistaattack'   or RoleInput ==  'trequartista(attack)' :
            TREatfunc()
            AnotherRoleQ()
        elif RoleInput == 'engsu'   or RoleInput ==  'eng'   or RoleInput ==  'enganche'   or RoleInput ==  'eng(su)'   or RoleInput ==  'engsupport'   or RoleInput ==  'eng(support)'   or RoleInput ==  'enganche(su)'   or RoleInput ==  'enganchesupport'   or RoleInput ==  'enganche(support)' :
            ENGsufunc()
            AnotherRoleQ()
        
        # Wide attacking midfield roles 

        elif RoleInput == 'iwsu'  or RoleInput ==  'iw' or RoleInput ==  'iw(su)' or RoleInput ==  'iwsupport' or RoleInput ==  'iw(support)' or RoleInput ==  'invertedwinger' or RoleInput ==  'inverted-winger' or RoleInput ==  'invertedwinger(su)'  or RoleInput ==  'inverted-winger(su)'  or RoleInput ==  'invertedwingersu'  or RoleInput ==  'inverted-wingersu'  or RoleInput ==  'invertedwingersupport'  or RoleInput ==  'inverted-wingersupport' or RoleInput ==  'invertedwinger(support)'  or RoleInput ==  'inverted-winger(support)' :
            IWsufunc()
            AnotherRoleQ()
        elif RoleInput == 'iwat'  or RoleInput ==  'iw(at)' or RoleInput ==  'iwattack' or RoleInput ==  'iw(attack)' or RoleInput ==  'invertedwinger(at)'  or RoleInput ==  'inverted-winger(at)'  or RoleInput ==  'invertedwingerat'  or RoleInput ==  'inverted-wingerat'  or RoleInput ==  'invertedwingerattack'  or RoleInput ==  'inverted-wingerattack' or RoleInput ==  'invertedwinger(attack)'  or RoleInput ==  'inverted-winger(attack)' :
            IWatfunc()
            AnotherRoleQ()
        elif RoleInput == 'ifsu'  or RoleInput ==  'if' or RoleInput ==  'if(su)' or RoleInput ==  'ifsupport' or RoleInput ==  'if(support)' or RoleInput ==  'insidewinger' or RoleInput ==  'inside-forward' or RoleInput ==  'insideforward(su)'  or RoleInput ==  'inside-forward(su)'  or RoleInput ==  'insideforwardsu'  or RoleInput ==  'inside-forwardsu'  or RoleInput ==  'insideforwardsupport'  or RoleInput ==  'inside-forwardsupport' or RoleInput ==  'insideforward(support)'  or RoleInput ==  'inside-forward(support)' :
            IFsufunc()
            AnotherRoleQ()
        elif RoleInput == 'ifat'  or RoleInput ==  'if(at)' or RoleInput ==  'ifattack' or RoleInput ==  'if(attack)' or RoleInput ==  'insideforward(at)'  or RoleInput ==  'inside-forward(at)'  or RoleInput ==  'insideforwardat'  or RoleInput ==  'inside-forwardat'  or RoleInput ==  'insideforwardattack'  or RoleInput ==  'inside-forwardattack' or RoleInput ==  'insideforward(attack)'  or RoleInput ==  'inside-forward(attack)' :
            IFatfunc()
            AnotherRoleQ()
        elif RoleInput == 'winsu'   or RoleInput ==  'w'   or RoleInput ==  'wsu'   or RoleInput ==  'w(su)'   or RoleInput ==  'win'   or RoleInput ==  'winger'   or RoleInput ==  'win(su)'   or RoleInput ==  'winsupport'   or RoleInput ==  'win(support)'   or RoleInput ==  'winger(su)'   or RoleInput ==  'wingersupport'   or RoleInput ==  'winger(support)' :
            WINsufunc()
            AnotherRoleQ()
        elif RoleInput == 'winat'   or RoleInput ==  'wat'   or RoleInput ==  'w(at)'   or RoleInput ==  'win(at)'   or RoleInput ==  'winattack'   or RoleInput ==  'win(attack)'   or RoleInput ==  'winger(at)'   or RoleInput ==  'wingerattack'   or RoleInput ==  'winger(attack)' :
            WINatfunc()
            AnotherRoleQ()
        elif RoleInput == 'rmdat'   or RoleInput ==  'rmd'   or RoleInput ==  'rmd(at)'   or RoleInput ==  'rmdattack'   or RoleInput ==  'rmd(attack)'   or RoleInput ==  'raumdeuter'   or RoleInput ==  'raumdeuter(at)'   or RoleInput ==  'raumdeuterattack'   or RoleInput ==  'raumdeuter(attack)' :
            RMDatfunc()
            AnotherRoleQ()
        elif RoleInput == 'wtmsu'   or RoleInput ==  'wtm'    or RoleInput ==  'wtm(su)'   or RoleInput ==  'wtmsupport'   or RoleInput ==  'wtm(support)'   or RoleInput ==  'widetargetman'   or RoleInput ==  'wide-targetman'   or RoleInput ==  'widetarget-man'   or RoleInput ==  'wide-target-man'   or RoleInput ==  'widetargetman(su)'   or RoleInput ==  'widetarget-man(su)'    or RoleInput ==  'wide-targetman(su)'   or RoleInput ==  'wide-target-man(su)'   or RoleInput ==  'widetargetman(support)'   or RoleInput ==  'widetarget-man(support)'    or RoleInput ==  'wide-targetman(support)'   or RoleInput ==  'wide-target-man(support)'   or RoleInput ==  'widetargetmansupport'   or RoleInput ==  'widetarget-mansupport'    or RoleInput ==  'wide-targetmansupport'   or RoleInput ==  'wide-target-mansupport' :
            WTMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'wtmat'   or RoleInput ==  'wtm'    or RoleInput ==  'wtm(at)'   or RoleInput ==  'wtmattack'   or RoleInput ==  'wtm(attack)'   or RoleInput ==  'widetargetman(at)'   or RoleInput ==  'widetarget-man(at)'    or RoleInput ==  'wide-targetman(at)'   or RoleInput ==  'wide-target-man(at)'   or RoleInput ==  'widetargetman(attack)'   or RoleInput ==  'widetarget-man(attack)'    or RoleInput ==  'wide-targetman(attack)'   or RoleInput ==  'wide-target-man(attack)'   or RoleInput ==  'widetargetmanattack'   or RoleInput ==  'widetarget-manattack'    or RoleInput ==  'wide-targetmanattack'   or RoleInput ==  'wide-target-manattack' :
            WTMatfunc()
            AnotherRoleQ()
        
        # Striker roles 

        elif RoleInput == 'afat'  or RoleInput ==  'af' or RoleInput ==  'af(at)' or RoleInput ==  'afattack' or RoleInput ==  'af(attack)' or RoleInput ==  'attackingforward'  or RoleInput ==  'attacking-forward' or RoleInput ==  'attackingforward(at)'  or RoleInput ==  'attacking-forward(at)'  or RoleInput ==  'attackingforwardat'  or RoleInput ==  'attacking-forwardat'  or RoleInput ==  'attackingforwardattack'  or RoleInput ==  'attacking-forwardattack' or RoleInput ==  'attackingforward(attack)'  or RoleInput ==  'attacking-forward(attack)' :
            AFatfunc()
            AnotherRoleQ()
        elif RoleInput == 'cfat'  or RoleInput ==  'cf' or RoleInput ==  'cf(at)' or RoleInput ==  'cfattack' or RoleInput ==  'cf(attack)' or RoleInput ==  'completeforward'  or RoleInput ==  'complete-forward' or RoleInput ==  'completeforward(at)'  or RoleInput ==  'complete-forward(at)'  or RoleInput ==  'completeforwardat'  or RoleInput ==  'complete-forwardat'  or RoleInput ==  'completeforwardattack'  or RoleInput ==  'complete-forwardattack' or RoleInput ==  'completeforward(attack)'  or RoleInput ==  'complete-forward(attack)' :
            CFatfunc()
            AnotherRoleQ()
        elif RoleInput == 'poaat'   or RoleInput ==  'poa'   or RoleInput ==  'poa(at)'   or RoleInput ==  'poaattack'   or RoleInput ==  'poa(attack)'   or RoleInput ==  'poacher'   or RoleInput ==  'poacher(at)'   or RoleInput ==  'poacherattack'   or RoleInput ==  'poacher(attack)' :
            POAatfunc()
            AnotherRoleQ()
        elif RoleInput == 'pfde'  or RoleInput ==  'pf(de)' or RoleInput ==  'pfdefend' or RoleInput ==  'pf(defend)' or RoleInput ==  'pressingforward(de)'  or RoleInput ==  'pressing-forward(de)'  or RoleInput ==  'pressingforwardde'  or RoleInput ==  'pressing-forwardde'  or RoleInput ==  'pressingforwarddefend'  or RoleInput ==  'pressing-forwarddefend' or RoleInput ==  'pressingforward(defend)'  or RoleInput ==  'pressing-forward(defend)' :
            PFdefunc()
            AnotherRoleQ()            
        elif RoleInput == 'pfsu'  or RoleInput ==  'pf' or RoleInput ==  'pf(su)' or RoleInput ==  'pfsupport' or RoleInput ==  'pf(support)' or RoleInput ==  'pressingforward'  or RoleInput ==  'pressing-forward' or RoleInput ==  'pressingforward(su)'  or RoleInput ==  'pressing-forward(su)'  or RoleInput ==  'pressingforwardsu'  or RoleInput ==  'pressing-forwardsu'  or RoleInput ==  'pressingforwardsupport'  or RoleInput ==  'pressing-forwardsupport' or RoleInput ==  'pressingforward(support)'  or RoleInput ==  'pressing-forward(support)' :
            PFsufunc()
            AnotherRoleQ()
        elif RoleInput == 'pfat'  or RoleInput ==  'pf(at)' or RoleInput ==  'pfattack' or RoleInput ==  'pf(attack)' or RoleInput ==  'pressingforward(at)'  or RoleInput ==  'pressing-forward(at)'  or RoleInput ==  'pressingforwardat'  or RoleInput ==  'pressing-forwardat'  or RoleInput ==  'pressingforwardattack'  or RoleInput ==  'pressing-forwardattack' or RoleInput ==  'pressingforward(attack)'  or RoleInput ==  'pressing-forward(attack)' :
            PFatfunc()
            AnotherRoleQ()
        elif RoleInput == 'dlfsu'   or RoleInput ==  'dlf'    or RoleInput ==  'dlf(su)'   or RoleInput ==  'dlfsupport'   or RoleInput ==  'dlf(support)'   or RoleInput ==  'deeplyingforward'   or RoleInput ==  'deep-lyingforward'   or RoleInput ==  'deeplying-forward'   or RoleInput ==  'deep-lying-forward'   or RoleInput ==  'deeplyingforward(su)'   or RoleInput ==  'deeplying-forward(su)'    or RoleInput ==  'deep-lyingforward(su)'   or RoleInput ==  'deep-lying-forward(su)'   or RoleInput ==  'deeplyingforward(support)'   or RoleInput ==  'deeplying-forward(support)'    or RoleInput ==  'deep-lyingforward(support)'   or RoleInput ==  'deep-lying-forward(support)'   or RoleInput ==  'deeplyingforwardsupport'   or RoleInput ==  'deeplying-forwardsupport'    or RoleInput ==  'deep-lyingforwardsupport'   or RoleInput ==  'deep-lying-forwardsupport' :
            DLFsufunc()
            AnotherRoleQ()
        elif RoleInput == 'dlfat'   or RoleInput ==  'dlf(at)'   or RoleInput ==  'dlfattack'   or RoleInput ==  'dlf(attack)'   or RoleInput ==  'deeplyingforward(at)'   or RoleInput ==  'deeplying-forward(at)'    or RoleInput ==  'deep-lyingforward(at)'   or RoleInput ==  'deep-lying-forward(at)'   or RoleInput ==  'deeplyingforward(attack)'   or RoleInput ==  'deeplying-forward(attack)'    or RoleInput ==  'deep-lyingforward(attack)'   or RoleInput ==  'deep-lying-forward(attack)'   or RoleInput ==  'deeplyingforwardattack'   or RoleInput ==  'deeplying-forwardattack'    or RoleInput ==  'deep-lyingforwardattack'   or RoleInput ==  'deep-lying-forwardattack' :
            DLFatfunc()
            AnotherRoleQ()
        elif RoleInput == 'tmsu'  or RoleInput ==  'tm' or RoleInput ==  'tm(su)' or RoleInput ==  'tmsupport' or RoleInput ==  'tm(support)' or RoleInput ==  'targetman'  or RoleInput ==  'target-man' or RoleInput ==  'targetman(su)'  or RoleInput ==  'target-man(su)'  or RoleInput ==  'targetmansu'  or RoleInput ==  'target-mansu'  or RoleInput ==  'targetmansupport'  or RoleInput ==  'target-mansupport' or RoleInput ==  'targetman(support)'  or RoleInput ==  'target-man(support)' :
            TMsufunc()
            AnotherRoleQ()
        elif RoleInput == 'tmat'  or RoleInput ==  'tm(at)' or RoleInput ==  'tmattack' or RoleInput ==  'tm(attack)' or RoleInput ==  'targetman(at)'  or RoleInput ==  'target-man(at)'  or RoleInput ==  'targetmanat'  or RoleInput ==  'target-manat'  or RoleInput ==  'targetmanattack'  or RoleInput ==  'target-manattack' or RoleInput ==  'targetman(attack)'  or RoleInput ==  'target-man(attack)' :
            TMatfunc()
            AnotherRoleQ()
        elif RoleInput == 'f9su'  or RoleInput ==  'f9' or RoleInput ==  'f9(su)' or RoleInput ==  'f9support' or RoleInput ==  'f9(support)' or RoleInput ==  'falsenine'  or RoleInput ==  'false-nine' or RoleInput ==  'falsenine(su)'  or RoleInput ==  'false-nine(su)'  or RoleInput ==  'falseninesu'  or RoleInput ==  'false-ninesu'  or RoleInput ==  'falseninesupport'  or RoleInput ==  'false-ninesupport' or RoleInput ==  'falsenine(support)'  or RoleInput ==  'false-nine(support)' or RoleInput ==  'false9'  or RoleInput ==  'false-9' or RoleInput ==  'false9(su)'  or RoleInput ==  'false-9(su)'  or RoleInput ==  'false9su'  or RoleInput ==  'false-9su'  or RoleInput ==  'false9support'  or RoleInput ==  'false-9support' or RoleInput ==  'false9(support)'  or RoleInput ==  'false-9(support)' :
            F9sufunc()
            AnotherRoleQ()

        else: 
            print(r'''I'm sorry, that role isn't recognised by this program. Try again.''')
    
RoleQs()