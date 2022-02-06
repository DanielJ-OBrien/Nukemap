5#To do:
#Incorp arbitrary sorting e.g with markers being added
#Incorp more classes?
#Make radiation ring staggered?
#Graph future populations
#double counting? ✓
#Better markers

import folium as fl
import pandas as pd
import os
import json
import sqlite3
import codecs
import csv
import setup
import hashlib
import tkinter as tk
from tkinter import *

def login():
    try:
        loginroot.destroy()
    except:
        pass
    try:
        root.destroy()
    except:
        pass
    def logininfo():
        loginbutton.pack_forget()
        signupbutton.pack_forget()
        #Asks for username, and queries database for the username
        def loginaction(username, password):
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute(("SELECT password FROM Users WHERE username = ?"), (username,))
            #Takes the hashed password, and strips it so it does not have unneeded brackets
            hashedpass = c.fetchall()
            hashedpasses = []
            for x in range(0, int(len(hashedpass))):
                hashedpassclean = hashedpass[0]
                hashedpassclean = str(hashedpassclean)
                hashedpassclean = hashedpassclean.strip("[(,')]")
                hashedpasses.append(hashedpassclean)
                del hashedpass[0]
            #Hashes the provided password
            password = hashlib.md5(password.encode())
            password = password.hexdigest()
            #If the two hashed passwords are the same, you log in
            n = 0
            try:
                while n == 0:
                        if password == hashedpasses[0]:
                            c.execute(("SELECT uid FROM Users WHERE password = ?"), (password,))
                            global uid
                            uid = c.fetchall()
                            uid = str(uid)
                            uid = uid.strip("[(,')]")
                            loginroot.destroy()
                            loginwindow.destroy()
                            return uid
                            n+=1
                            break
                        elif password != hashedpasses[0]:
                            del hashedpasses[0]
                            loginroot.destroy()
                        elif int(len(hashedpasses)) == 0:
                                 usernameentry.pack_forget()
                                 passwordentry.pack_forget()
                                 submitusername.pack_forget()
                                 loginroot.destroy()
                                 logininfo()
            except IndexError:
                #sends you back to the start
                usernameentry.pack_forget()
                passwordentry.pack_forget()
                submitusername.pack_forget()
                loginroot.destroy()
                login()
        def submitusernamef(username, password):
            #puts the users username and passwords into passable variables
            username = usernameentry.get()
            password = passwordentry.get()
            loginaction(username, password)
        #Creates UI for entering & submitting username and password
        loginwindow = Tk()
        usernameentry = Entry(loginwindow, width=50)
        usernameentry.pack()
        usernameentry.insert(0, "Enter username:")
        passwordentry = Entry(loginwindow, width=50)
        passwordentry.pack()
        passwordentry.insert(0, "Enter password:")
        submitusername = Button(loginwindow, text="Submit", command= lambda: submitusernamef(usernameentry, passwordentry))
        submitusername.pack()

    def signupinfo():    
        loginbutton.pack_forget()
        signupbutton.pack_forget()
        def signup(newusername, newusername2, newpassword, newpassword2):
            if newusername == newusername2:
                pass
            else:
                login()
            if newpassword == newpassword2:
                #Hashes the password
                hashedpassword = hashlib.md5(newpassword.encode())
                hashedpassword = hashedpassword.hexdigest()
                conn = sqlite3.connect('Database.db')
                c = conn.cursor()
                #Generates a userID from the first 3 letters and the username length
                userlen = len(newusername)
                uid = newusername[0:2] + str(userlen)
                def register(newusername, hashedpassword, uid, userlen):
                    try:
                        #Adds the uid, username, and encrypted password to the database
                        c.execute(("INSERT INTO Users VALUES(?, ?, ?)"), (newusername, hashedpassword, uid,))
                    except sqlite3.IntegrityError:
                        #If the username is in use, then the user ID is increased by one, to allow both people to use it
                        int(userlen)
                        userlen +=1
                        uid = newusername[0:2] + str(userlen)
                        register(newusername, hashedpassword, uid, userlen)
                register(newusername, hashedpassword, uid, userlen)
                #Saves
                conn.commit()
                #Sends you to the login page
                usernameentry.pack_forget()
                usernameentry2.pack_forget()
                passwordentry.pack_forget()
                passwordentry2.pack_forget()
                submitusername.pack_forget()
                signupwindow.destroy()
                login()
            else:
                #Passwords do not match
                logininfo()
        def submitpasswordf(usernameentry, usernameentry2, passwordentry, passwordentry2):
            #Once again turns the user inputs into passable variables, and calls the signup function
            newusername = usernameentry.get()
            newusername2 = usernameentry2.get()
            password = passwordentry.get()
            password2 = passwordentry2.get()
            loginroot.destroy()
            signup(newusername, newusername2, password, password2)
        #Creates UI for inserting two sets of username and password
        signupwindow = Tk()
        usernameentry = Entry(signupwindow, width=50)
        usernameentry.pack()
        usernameentry.insert(0, "Enter username:")
        usernameentry2 = Entry(signupwindow, width=50)
        usernameentry2.pack()
        usernameentry2.insert(0, "Confirm username:")
        passwordentry = Entry(signupwindow, width=50)
        passwordentry.pack()
        passwordentry.insert(0, "Enter password:")
        passwordentry2 = Entry(signupwindow, width=50)
        passwordentry2.pack()
        passwordentry2.insert(0, "Confirm password:")
        submitusername = Button(signupwindow, text="Submit", command= lambda: submitpasswordf(usernameentry, usernameentry2, passwordentry, passwordentry2))
        submitusername.pack()
    loginroot = Tk()
    loginroot.geometry("500x500") 
    loginbutton = Button(loginroot, text="Log in", command=logininfo, height=3, width=40)
    signupbutton = Button(loginroot, text="Register", command=signupinfo, height=3, width=40)
    title = Label(loginroot, text = "Login or Sign-up", font=("Arial", 35))
    title2 = Label(loginroot, text = """    If you have used this previously, please
    log in to your account. Otherwise, press
    press "Register" to get started""", font=("Arial", 10))
    title.place(x=78, y=50)
    title2.place(x=100, y=175)
    loginbutton.place(x=100, y=300) 
    signupbutton.place(x=100, y=400)

#Technically the begining of the program. Initializes Tkinter and sends you to the login page.
root = tk.Tk()
root.geometry("500x500")
title = Label(root, text = "The Cost of", font=("Arial", 25)) 
title2 = Label(root, text = "Global Thermonuclear War", font=("Arial", 25)) 
startbutton = Button(root, text="Shall we play a game?", command= login)
startimg = PhotoImage(file = r"nukeimg.png") 
startimg = startimg.subsample(3, 3) 
title.place(x=150, y=20) 
title2.place(x=50, y=70) 
Label(root, image = startimg).place(x=95, y=140)
startbutton.place(x=180, y=458) 
root.mainloop()
        

#Reads a text file. If it says 0, its runs a asetup file that creates databases. Otherwise, it just passes.
setupcheck = open("setupcheck.txt", "r")
setupvar = setupcheck.read()
if setupvar == "0":
    setup()
    pass
else:
    pass


#Decides where to start on the map
m = fl.Map(
    location=[0, 0],
    zoom_start=2
)

#Connects to our database containing all relevant info

conn = sqlite3.connect('Database.db')
c = conn.cursor()

def pickyear():
    pickroot = Tk()
    #We will now choose which year to get our data from
    year = range(1799, 2020)
    YearList = []
    start = 1799
    for x in range(1799, 2020):
        #Generates a list of values to use as a year to pick, because tkinter doesnt let you do anything simple like a number range to create a dropdown list
        YearList.append(start)
        start+=1
    def setyear():
        global chosenyear #shhh this isnt real
        chosenyear = variable.get()
        chosenyear = int(chosenyear)
        if chosenyear in range(1799, 2020):
            #Takes the year, and uses it to take relevent data from the database
            chosenyearmenu.pack_forget()
            submityear.pack_forget()
            chosenyear = str(chosenyear)
            ChosenData = c.execute(('SELECT name, Code, Year, Population FROM Populations WHERE Year = ?'), (chosenyear,))
            rows = c.fetchall()
            with open("population.csv", "w") as write_file:
                #Creates a CSV file with all data for the selected year. This is essential when using Pandas
                headers = ("name","Code","Year","Population")
                obj = csv.writer(write_file)
                obj.writerow(headers)
                for row in c.execute(('SELECT * FROM Populations WHERE Year = ?'), (chosenyear,)):
                    writer = csv.writer(write_file)
                    writer.writerows(rows)
            pickroot.destroy()
        else:
            chosenyearmenu.pack_forget()
            submityear.pack_forget()
    #Creates dropdown menu with submit button. Contains all approriate years.
    variable = StringVar(pickroot)
    variable.set("2019") # default value
    chosenyearmenu = OptionMenu(pickroot, variable, *YearList)
    chosenyearmenu.pack()
    submityear = Button(pickroot, text="Submit", command= setyear)
    submityear.pack()
    pickroot.mainloop()
markers = []
markers2 = []

def prepnuke():
    #Names nuke and takes megatons, before sending to the nuke class for processing
    global uid #This one isnt real either
    counter1 = 0
    def makenuke():
        def save(nameinput, yieldinput):
            #If the button is ticked, then this will run and add the values to the database.
            c.execute(("INSERT INTO Nukes VALUES(?, ?, ?)"), (nameinput, yieldinput, uid,))
            conn.commit()
        def submit():
            #Turns the data in to passable variables (this happens a fair amount)
            nameinput = namebox.get()
            yieldinput = yieldbox.get()
            nukeinputs.destroy()
            saveornott = saveornot.get()
            if saveornott == 1:
                save(nameinput, yieldinput)
            else:
                pass
            placemarker(markers, markers2, counter1, nameinput, yieldinput)
        #Creates UI with space for nuke name and yield, as well as the option to save the nuke.
        nukeroot.destroy()
        nukeinputs = Tk()
        namebox = Entry(nukeinputs, text="Nuke name:", width=50)
        namebox.pack()
        yieldbox = Entry(nukeinputs, text="Nuke yield (Megatons)", width=50)
        yieldbox.pack()
        saveornot= IntVar(nukeinputs)
        savebox = Checkbutton(nukeinputs, text="Save?", variable=saveornot, onvalue=1, offvalue=0)
        savebox.pack()
        submitbutton = Button(nukeinputs, text="Submit", command = submit).pack()
        
    def loadnuke():
        def picknuke(nukeyield, nukevalues):
            #Data to passing variable AGAIN, but this time it has to remove all the extra commas and whatnot because it was pulled from a database
            nukevaluesget = nukeyield.get()
            nukevaluessplit = nukevaluesget.split(",")
            nameinput = nukevaluessplit[0]
            nameinput = nameinput.strip("([',])")
            yieldinput = nukevaluessplit[1]
            yieldinput = yieldinput.strip("([',])")
            loadroot.destroy()
            placemarker(markers, markers2, counter1, nameinput, yieldinput)
        #Takes nukes saved to the current users uid, and puts them in a selectable list
        c.execute(('SELECT name, yield FROM Nukes WHERE uid = ?'), (uid,))
        nukevalues = c.fetchall()
        nukeroot.destroy()
        loadroot = Tk()
        nukeyield = StringVar(loadroot)
        nukelist = OptionMenu(loadroot, nukeyield, *nukevalues)
        nukelist.pack()
        nukesubmit = Button(loadroot, text="Submit", command= lambda: picknuke(nukeyield, nukevalues))
        nukesubmit.pack()

    def placemarker(markers, markers2, counter1, nameinput,yieldinput):
        currentnuke = MyNukes(nameinput,yieldinput)
        #Has user input a 3 character code
        def processcharcode(markers, markers2, counter1):
            pickedc = pickedctk.get()
             #Makes key variable combining the input of the code and selected year
            key = pickedc + str(chosenyear)
            #Selects latitude from database with the same key
            c.execute(('SELECT lat FROM Citycoords WHERE key = ?'), (key,))
            #Takes the key and removes excess brackets and commas
            lat = c.fetchall()
            lat = str(lat)
            lat = lat.strip("[(,)]")
            #Repeated
            c.execute(('SELECT long FROM Citycoords WHERE key = ?'), (key,))
            long = c.fetchall()
            long = str(long)
            long = long.strip("[(,)]")
            #Adds the latitude, longditude, and various blast radius's to a set of arrays
            markers.insert(int(counter1), [lat, long, currentnuke.nukeblastrad, currentnuke.nukethermrad, currentnuke.nukeionrad])
            markers2.insert(int(counter1), [lat, long, currentnuke.nukeblastrad, currentnuke.nukethermrad, currentnuke.nukeionrad])
            counter1+=1
            
            def placemarkerpick(markers, markers2, counter1):
                placeroot.destroy()
                markerchoice = Tk()
                def placeagain():
                    markerchoice.destroy()
                    prepnuke()
                def addmarkers():
                    w = 0
                    while w == 0:
                        try:
                            #Adds marker to map by taking the coords and radiuses from the array
                            fl.Marker([markers[0][0], markers[0][1]],
                                        popup='Nuke location').add_to(m)
                            fl.Circle([markers[0][0], markers[0][1]],
                                    fill = True,
                                    fill_color = '#28f209',
                                    fill_opacity = 0.2,
                                            radius=float(markers[0][4])).add_to(m)
                            fl.Circle([markers[0][0], markers[0][1]],
                                    fill = True,
                                    fill_color = '#f29c09',
                                    fill_opacity = 0.4,
                                            radius=float(markers[0][3])).add_to(m)
                            fl.Circle([markers[0][0], markers[0][1]],
                                    fill = True,
                                    fill_color = '#FF0000',
                                    fill_opacity = 0.6,
                                            radius=float(markers[0][2])).add_to(m)
                            #Removes the front value from the queue
                            del markers[0]
                        except IndexError:
                            #Lets the code continue when the queue is empty
                            counter1 = 0
                            w+=1
                        except ValueError:
                            #Removes any invalid locations
                            del markers[0]
                            pass
                def printmarkers():
                    markerprint = Tk()
                    markertext = Text(markerprint)
                    markertext.insert(INSERT, markers)
                    markertext.pack()
                def closebutton():
                        markerchoice.destroy()
                #Creates four buttons, the all call its own subroutine
                placeagainbutton = Button(markerchoice, text="Prepare another marker", command= placeagain)
                placeagainbutton.pack()
                addbutton = Button(markerchoice, text="Add all markers to the map", command= addmarkers)
                addbutton.pack()
                printbutton = Button(markerchoice, text="Print all marker data", command= printmarkers)
                printbutton.pack()
                exitbutton = Button(markerchoice, text="Close tab", command= closebutton)
                exitbutton.pack()
            placemarkerpick(markers, markers2, counter1)
        #Creates a text box where the user puts the code
        placeroot = Tk()
        pickedctk = Entry(placeroot, width=50)
        pickedctk.insert(0, "Type 3 character code of desired country")
        pickedctk.pack()
        pickedcretrieve = Button(placeroot, text="Submit", command=lambda : processcharcode(markers, markers2, counter1))
        pickedcretrieve.pack()
    #creates a box with two buttons, that load the relevent subroutines
    nukeroot = Tk()
    makebutton = Button(nukeroot, text="Create new nuke", command= makenuke)
    loadbutton = Button(nukeroot, text="Load saved nuke", command= loadnuke)
    makebutton.pack()
    loadbutton.pack()

#Makes variables hold data on both the borders of countries and their respective populations
world = os.path.join('world-countries.json')
population = pd.read_csv('population.csv')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT! A single coordinate increase is equal to 111195m
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Creates map & overlay, linking relevant data
def generatemap():
    m.choropleth(
        geo_data=world,#Uses world variable set earlier of the GeoJSON file to make borders for the choropleth map
        name=('choropleth'),
        data = population,#Uses the data variable for picking the year and data
        columns = ['name', 'Population'],
        key_on="name",
        fill_color = ("RdYlGn"),
        bins = [100, 1000, 10000, 100000, 1000000, 10000000, 50000000, 70000000, 90000000, 100000000, 1500000000],
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=("population")
    )
    #Generates HTML file 
    fl.LayerControl().add_to(m)
    m.save('map2.html')
    os.system("start map2.html")

def losses(markers2):
    #oh boy
    latdistance = markers2[0][0]
    longdistance = markers2[0][1]
    #this one will take the blast radius from that big array we made earlier
    nukeblastrad = markers2[0][2]
    #We then divide the number by 10000 because it has to be converted into coordinate values
    nukeblastrad = float(nukeblastrad) / 10000
    nukethermrad = markers2[0][3]
    nukethermrad = float(nukethermrad) / 10000
    nukeionrad = markers2[0][4]
    #We do it more to this one so it doesnt cover the entire map WHY???
    nukeionrad = float(nukeionrad) / 100000
    #We then find the minimum and maximum measurements for the nukes blast radius
    latmax = float(latdistance) + float(nukeblastrad)
    latmin = float(latdistance) - float(nukeblastrad)
    longmax = float(longdistance) + float(nukeblastrad)
    longmin = float(longdistance) - float(nukeblastrad)
    #c.execute(('SELECT lat, long, key FROM Citycoords WHERE instr(key, ?) AND lat BETWEEN ? AND ? AND long BETWEEN ? AND ?'), (chosenyear, latmin, latmax, longmin, longmax,))
    #Will use later for more accurate losses
    #nope
    #This find the coords within that ring, and takes their keys.
    c.execute(('SELECT key FROM Citycoords WHERE instr(key, ?) AND lat BETWEEN ? AND ? AND long BETWEEN ? AND ?'), (chosenyear, latmin, latmax, longmin, longmax,))
    popkey = c.fetchall()
    popsdead = []
    n = 0
    popsdeadblast = []
    while n == 0:
        try:
            #This will select the population from each country via its key, and adds it to the big list(tm)
            c.execute(('SELECT Population FROM Populations WHERE instr(key, ?)'), (popkey[0][0],))
            popstemp = c.fetchall()
            popstemp = str(popstemp)
            popstemp = popstemp.strip("[(,)]")
            popstemp = int(popstemp)
            popsdeadblast.append(popstemp)
            del popkey[0]

        except IndexError:
            #When its out of stuff to throw in the big list(tm) it creates a total death count out everything in popsdead
            popsdeadtotal = sum(popsdead)
            break
    #I then copy and pasted that block two more times, so there is one per blast effect - this is probably a terrible way of implementing this. Too bad!
    latmax = float(latdistance) + float(nukethermrad)
    latmin = float(latdistance) - float(nukethermrad)
    longmax = float(longdistance) + float(nukethermrad)
    longmin = float(longdistance) - float(nukethermrad)
    c.execute(('SELECT key FROM Citycoords WHERE instr(key, ?) AND lat BETWEEN ? AND ? AND long BETWEEN ? AND ?'), (chosenyear, latmin, latmax, longmin, longmax,))
    popkey = c.fetchall()
    m = 0
    popsdeadtherm = []
    while m == 0:
        try:
            c.execute(('SELECT Population FROM Populations WHERE instr(key, ?)'), (popkey[0][0],))
            popstemp = c.fetchall()
            popstemp = str(popstemp)
            popstemp = popstemp.strip("[(,)]")
            popstemp = int(popstemp)
            popsdeadtherm.append(popstemp)
            del popkey[0]

        except IndexError:
            popsdeadtotal = sum(popsdead)
            break

    latmax = float(latdistance) + float(nukeionrad)
    latmin = float(latdistance) - float(nukeionrad)
    longmax = float(longdistance) + float(nukeionrad)
    longmin = float(longdistance) - float(nukeionrad)
    c.execute(('SELECT key FROM Citycoords WHERE instr(key, ?) AND lat BETWEEN ? AND ? AND long BETWEEN ? AND ?'), (chosenyear, latmin, latmax, longmin, longmax,))
    popkey = c.fetchall()
    l = 0
    popsdeadion = []
    while l == 0:
        try:
            c.execute(('SELECT Population FROM Populations WHERE instr(key, ?)'), (popkey[0][0],))
            popstemp = c.fetchall()
            popstemp = str(popstemp)
            popstemp = popstemp.strip("[(,)]")
            popstemp = int(popstemp)
            popsdeadion.append(popstemp)
            del popkey[0]

        except IndexError:
            #Finally, we reach the last calculation
            #This adds all of the numbers we collected together, and puts them into a single variable
            print("before", popsdeadion)
            popsdeadion = list(set(popsdeadion))
            print("after", popsdeadion)
            popsdeadblastsum = sum(popsdeadblast)
            popsdeadthermsum = sum(popsdeadtherm)
            popsdeadionsum = sum(popsdeadion)
            #We then divide the numbers for what amount will be fatalities, or other cool stuff like cancer deaths
            popsdeadblastsum = popsdeadblastsum / 13.512369
            popsdeadthermsum = float(popsdeadthermsum) / 1253
            popsdeadionsum = popsdeadionsum / 19234
            popsdeadcancer = popsdeadionsum / 14
            popsdeadtotal =  float(popsdeadblastsum) + float(popsdeadthermsum) + float(popsdeadionsum)
            #Assigns that text to variables
            blast = int(popsdeadblastsum), "people died from the nukes blast pressures, which vapourised much of its surroundings."
            therm = int(popsdeadthermsum), "people died from the nukes thermal radiation, instantly burning those outside the blast areas."
            ion = int(popsdeadionsum), "people died from the nukes ionic radiation, which spreads incredibly far."
            cancer = int(popsdeadcancer), "People will likely die early, developing cancer in their later life"
            total = int(popsdeadtotal), "people died overall."
            #Creates one last box of text, that prints the bit above with the correct numbers
            deathcountroot = Tk()
            deathtextblast = Text(deathcountroot, height=5)
            deathtexttherm = Text(deathcountroot, height=5)
            deathtextion = Text(deathcountroot, height=5)
            deathtexttotal = Text(deathcountroot, height=5)
            deathtextcancer = Text(deathcountroot, height=5)
            deathtextblast.insert(INSERT, blast)
            deathtexttherm.insert(INSERT, therm)
            deathtextion.insert(INSERT, ion)
            deathtexttotal.insert(INSERT, total)
            deathtextcancer.insert(INSERT, cancer)
            deathtextblast.pack()
            deathtexttherm.pack()
            deathtextion.pack()
            deathtexttotal.pack()
            deathtextcancer.pack()
            break

#Use the nuke class to make an easier custom datatype to use
class Nukes: 
    def __init__(self,nukename,nukeyield):
        self.nukename = nukename
        self.nukeyield = float(nukeyield)
    
    def calc(self):
        pass

#Inheritance marks
class MyNukes(Nukes):
    def __init__(self,nukename,nukeyield):
            #Inherits values from parent class
            Nukes.__init__(self,nukename,nukeyield)
            #calculate other attributes from given yield
            self.calc() 

    def calc(self):
            #Using the yield, calculates the various radiuses
            self.nukethermrad = self.nukeyield ** 0.41 * 1.20 * 1000
            self.nukeblastrad = self.nukeyield ** 0.33 * 2.2 * 1000
            self.nukeionrad = self.nukeyield ** 0.19 * 1000 * 1000

#Generates a main menu that lets you pick whatever stuff you want to do in any order. Except you seriously need to pick a year first.
mainmenu = Tk()
yearbutton = Button(mainmenu, text="Pick year first", command= pickyear)
yearbutton.pack()
nukebutton = Button(mainmenu, text="Create a nuke", command= prepnuke)
nukebutton.pack()
mapbutton = Button(mainmenu, text="Open the map", command= generatemap)
mapbutton.pack()
lossesbutton = Button(mainmenu, text="Calculate losses", command= lambda: losses(markers2))
lossesbutton.pack()
root.mainloop()


