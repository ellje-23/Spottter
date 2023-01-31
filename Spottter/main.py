# Blog Flask application
import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, render_template, g, current_app, session
from flask.cli import with_appcontext
import click
import birddatabase
from datetime import datetime
# initialize Flask
app = Flask(__name__)
app.secret_key = "rhodesedudatabaseproject"
####################################################
# Routes 

@app.route("/", methods= ['get','post'])
def home():
 if "step" not in request.form:     
  return render_template('home.html', step="compose_entry")
 elif request.form["step"] == "check":
   conn = get_db()
   cursor = conn.cursor()
   cursor.execute("select count(*) from users where email=%s and password=%s", [request.form["email"], request.form["password"]])
   count=cursor.fetchone();
   if(count == [1]):
     email = request.form["email"]
     session["email"] = email
     return render_template("homeMain.html", step = "true")
   else:
    return render_template("home.html", step = "false")
     
@app.route("/signup", methods=["get","post"])    
def signup():
  if "step" not in request.form:
    return render_template('signup.html', step="compose_signup")
  elif request.form["step"] == "signup":
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("insert into users(email,firstname,lastname,statename,password) values (%s,%s,%s,%s,%s)", [request.form["email"], request.form["fname"], request.form["lname"], request.form["hstate"], request.form["password"]])
    conn.commit()
    return render_template("signup.html", step = "done" )

@app.route("/modify", methods=["get", "post"])
def modify():
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("select firstName, lastName, email from users where email=%s", [session.get("email",None)])#how to store the email to retrieve info
    row = cursor.fetchone()
    return render_template('modify.html', step="make_edit", info = row)
    
  elif request.form["step"] == "update":
    conn =get_db()
    cursor = conn.cursor()
    cursor.execute("update users set firstName=%s, lastName=%s where email=%s",[request.form["fname"], request.form["lname"], request.form["email"]])
    conn.commit()
    email = request.form["email"]
    session["email"] = email
    print(session.get("email",None))
    return render_template("modify.html", step="update_complete")

@app.route("/home", methods=["get","post"])
def homeMain():
    return render_template("homeMain.html")    

@app.route("/searchColor", methods=["get","post"])    
def searchByColor():
  if "step" not in request.form:
    return render_template("searchByColor.html", step = "select_colors")
  elif request.form["step"] == "list_birds":
    conn = get_db()
    cursor = conn.cursor()
    listColors = request.form.getlist("color")
    cursor.execute("select distinct species, colorname from birdcolors where colorname=ANY(%s)", [listColors])
    allBirds = cursor.fetchall()
    conn.commit()
    return render_template("searchByColor.html", step = "list_birds", birdList = allBirds)

@app.route("/searchAttribute", methods=["get","post"])    
def searchByAttribute():
    if "step" not in request.form:
        print("yes")
        return render_template("searchByAttribute.html", step = "specify_attribute")
    elif request.form["step"] == "list_birds":
        conn = get_db()
        cursor = conn.cursor()
        wingspan = int(request.form.get("wingspan"))
        wingspanUpper = wingspan + 3
        wingspanLower = wingspan - 3
        length = int(request.form.get("length"))
        lengthUpper = length + 3
        lengthLower = length - 3
        cursor.execute("select species, commonname, wingspan, length from birds where wingspan>=%s and wingspan<%s and length>=%s and length<%s", [wingspanLower, wingspanUpper, lengthLower, lengthUpper])
        allBirds = cursor.fetchall()
        conn.commit()
        return render_template("searchByAttribute.html", step = "list_birds", birdList = allBirds)

@app.route("/searchRegion", methods=["get","post"])    
def searchByRegion():
  if "step" not in request.form:
    return render_template("searchByRegion.html", step = "select_region")
  elif request.form["step"] == "list_birds":
    conn = get_db()
    cursor = conn.cursor()
    region = request.form.get("region")
    cursor.execute("select distinct species, stateName, speciepopulation, region from states natural join foundIn where region=%s", [region])
    allBirds = cursor.fetchall()
    conn.commit()
    return render_template("searchByRegion.html", step = "list_birds", birdList = allBirds)

@app.route("/searchSpecie", methods=["get","post"])    
def searchBySpecies():
  if "step" not in request.form:
    return render_template("searchBySpecies.html", step = "select_specie")
  elif request.form["step"] == "list_specie":
    conn = get_db()
    cursor = conn.cursor()
    specie = request.form["specie"]
    cursor.execute("select * from birds where species=%s", [specie])
    birdSpecie = cursor.fetchone()
    conn.commit()
    return render_template("searchBySpecies.html", step = "list_specie", bird = birdSpecie)

@app.route("/addSighting", methods=['get', 'post'])
def addSighting():
    if "step" not in request.form:     
        return render_template('addSighting.html', step="compose_sighting")
    elif request.form["step"] == "add_entry":
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("insert into sightings (email, species, dateTime, longitude, latitude, stateName) values (%s, %s, %s, %s, %s, %s)",
                   [session.get("email"), request.form['species'], request.form['dateTime'], request.form['longitude'], request.form['latitude'], request.form['stateName']])
        conn.commit()
        return render_template("addSighting.html", step="add_sighting")

@app.route("/viewSighting", methods=['get', 'post'])
def viewSighting():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("select * from sightings where email=%s", [session.get("email")])
    listSightings = cursor.fetchall()
    conn.commit()
    return render_template("viewSighting.html", sightings = listSightings)

@app.route("/editSighting", methods=['get', 'post'])
def editSighting():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("select email, species, dateTime, longitude, latitude, stateName from sightings where email=%s", [session.get("email",None)])
        rowlist = cursor.fetchall()
        return render_template('editSighting.html', step="display_sightings", entries=rowlist)   
    elif request.form["step"] == "make_edits":
        conn = get_db()
        cursor = conn.cursor()
        
        choice = request.form["choice"]
        twoVars = choice.split("|")
        dateTimeStr = twoVars[0]
        dateTime = datetime.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")
        species = twoVars[1]

        cursor.execute("select email, species, dateTime, longitude, latitude, stateName from sightings where email=%s and species=%s and dateTime = %s", [session.get("email",None), species, dateTime])
        row = cursor.fetchone()
        conn.commit()     
        return render_template("editSighting.html", step="make_edits", entry=row, oldSpecies=species, oldDateTime=dateTime)

    elif request.form["step"] == "update_database":
        conn = get_db()
        cursor = conn.cursor()

        species = request.form["species"]
        dateTime = request.form["dateTime"]
        longitude = request.form["longitude"]
        latitude = request.form["latitude"]
        stateName = request.form["stateName"]

        speciesOld = request.form["speciesOld"]
        dateTimeOld = request.form["dateTimeOld"]
    
        cursor.execute("update sightings set email=%s, species=%s ,dateTime=%s, longitude=%s,latitude=%s,stateName=%s where email=%s and species=%s and dateTime = %s", [session.get("email",None), species, dateTime, longitude, latitude, stateName, session.get("email",None), speciesOld, dateTimeOld])
        conn.commit()
        return render_template("editSighting.html", step="update_database")

@app.route("/deleteSighting", methods=['get', 'post'])
def deleteSighting():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("select email, species, dateTime, longitude, latitude, stateName from sightings where email=%s", [session.get("email",None)])
        rowlist = cursor.fetchall()
        return render_template('deleteSighting.html', step="display_sightings", entries=rowlist)

    elif request.form["step"] == "delete_sighting":
        conn = get_db()
        cursor = conn.cursor()

        choice = request.form["choice"]
        twoVars = choice.split("|")
        dateTimeStr = twoVars[0]
        dateTime = datetime.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")
        species = twoVars[1]

        cursor.execute("delete from sightings where email=%s and species=%s and dateTime = %s", [session.get("email",None), species, dateTime])
        conn.commit()
        return render_template("deleteSighting.html", step="delete_sighting")

@app.route("/browseSighting", methods=["get","post"])
def browseSighting():
    if "step" not in request.form:
        return render_template("browseSighting.html", step = "select_search")
    elif request.form["step"] == "list_sightings":
        conn = get_db()
        cursor = conn.cursor()
        species = request.form["species"]
        state = request.form["stateName"]
        cursor.execute("select email, species, dateTime, longitude, latitude, stateName from sightings where species=%s and stateName=%s", [species, state])
        allSightings = cursor.fetchall()
        conn.commit()
        return render_template("browseSighting.html", step = "list_sightings", entries = allSightings)
  
#Shows groups the user is a part of, as well as upcoming meetings for those groups
@app.route("/mygroup")
def mygroup():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID, groupName, numMembers from groups natural join users where email=%s', [session.get("email",None)])
        myGroupData = cursor.fetchall()

        if not len(myGroupData): #if myGroupData is empty, length is False
            return render_template('mygroup.html', mygroup=[])
            
        else: 
            cursor.execute('select email, firstName, lastName from users where groupID=(select groupID from users where email=%s)', [session.get("email",None)])
            groupMembers = cursor.fetchall()

            cursor.execute('select meetingTopic, groupID, dateTime, location, stateName from meetings where groupID=(select groupID from users where email=%s) order by dateTime', [session.get("email",None)])
            meetingsData = cursor.fetchall()
    
            return render_template('mygroup.html', mygroup=myGroupData[0], meetings=meetingsData, members=groupMembers)

#Browse all groups and their information; join a new group.
@app.route("/browsegroups", methods=["get","post"])
def browsegroups():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID, groupName, numMembers from groups')
        groupsData = cursor.fetchall()
        cursor.execute('select groupID, groupName, numMembers from groups natural join users where email=%s', [session.get("email",None)])
        mygroup = cursor.fetchall()
        return render_template('browsegroups.html', step="select_group", mygroup=mygroup, groups=groupsData)
        
    elif request.form["step"] == "groupinfo":
        conn = get_db()
        cursor = conn.cursor()
        viewGroupID = request.form["groupID"]
        
        cursor.execute('select groupID, groupName, numMembers from groups where groupID=%s', [viewGroupID])
        viewgroup = cursor.fetchall()
        cursor.execute('select groupID, groupName, numMembers from groups')
        groupsData = cursor.fetchall()
        cursor.execute('select meetingTopic, groupID, dateTime from meetings where groupID=%s order by dateTime' % (viewGroupID))
        meetingsData = cursor.fetchall()

        cursor.execute('select email, firstName, lastName from users where groupID=%s',[viewGroupID])
        groupMembers = cursor.fetchall()
        return render_template('browsegroups.html', step="groupinfo", viewgroup=viewgroup[0], groups=groupsData, meetings=meetingsData, members=groupMembers)

    elif request.form["step"] == "joingroup":
        conn = get_db()
        cursor = conn.cursor()
        myemail = session.get("email")
        cursor.execute("update users set groupID=%s where email=%s", [request.form["newgroupID"], myemail])
        conn.commit()
        return render_template('browsegroups.html', step="joingroup",)
    

@app.route("/addmeeting", methods=["get","post"])
def addmeeting():
    if "step" not in request.form:     
        return render_template('addMeeting.html', step="compose_meeting")
    elif request.form["step"] == "add_entry":
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID from users where email=%s', [session.get("email",None)])
        myGroupID = cursor.fetchone()
        
        cursor.execute("insert into meetings (groupID, dateTime, location, stateName, meetingTopic) values (%s, %s, %s, %s, %s)",
                   [myGroupID[0], request.form['dateTime'], request.form['location'], request.form['stateName'], request.form['meetingTopic']]) #sometimes myGroupID.groupID returns a type error hence the index
        conn.commit()
        return render_template("addMeeting.html", step="add_meeting")


@app.route("/deletemeeting", methods=["get","post"])
def deletemeeting():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID from users where email=%s', [session.get("email",None)])
        myGroupID = cursor.fetchone()
        
        cursor.execute("select groupID, dateTime, location, stateName, meetingTopic from meetings where groupID=%s", [myGroupID[0]])
        rowlist = cursor.fetchall()
        return render_template('deletemeeting.html', step="display_meetings", entries=rowlist)   
    elif request.form["step"] == "delete_meeting":
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID from users where email=%s', [session.get("email",None)])
        myGroupID = cursor.fetchone()

        choiceInfo = request.form["chosenMeetingKeys"]
        choiceInfo = choiceInfo.split("|")
        dateTimeStr = choiceInfo[0]
        dateTime = datetime.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")
        location = choiceInfo[1]

        cursor.execute("delete from meetings where groupID=%s and dateTime=%s and location=%s", [myGroupID[0], dateTime, location])
        
        conn.commit() 
        return render_template("deletemeeting.html", step="delete_meeting")
    
    
@app.route("/editmeeting", methods=["get","post"])
def editmeeting():
    if "step" not in request.form:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID from users where email=%s', [session.get("email",None)])
        myGroupID = cursor.fetchone()
        
        cursor.execute("select groupID, dateTime, location, stateName, meetingTopic from meetings where groupID=%s", [myGroupID[0]])
        rowlist = cursor.fetchall()
        return render_template('editMeeting.html', step="display_meetings", entries=rowlist)   
    elif request.form["step"] == "make_edits":
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID from users where email=%s', [session.get("email",None)])
        myGroupID = cursor.fetchone()

        choiceInfo = request.form["chosenMeetingKeys"]
        choiceInfo = choiceInfo.split("|")
        dateTimeStr = choiceInfo[0]
        dateTime = datetime.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")
        location = choiceInfo[1]

        cursor.execute("select groupID, dateTime, location, stateName, meetingTopic from meetings where groupID=%s and dateTime=%s and location=%s", [myGroupID[0], dateTime, location])
        
        row = cursor.fetchone()
        conn.commit()     
        return render_template("editMeeting.html", step="make_edits", entry=row, oldLocation=location, oldDateTime=dateTime)

        
    elif request.form["step"] == "update_database":
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('select groupID from users where email=%s', [session.get("email",None)])
        myGroupID = cursor.fetchone()

        
        meetingTopic = request.form["meetingTopic"]
        dateTime = request.form["dateTime"]
        location = request.form["location"]
        stateName = request.form["stateName"]

        locationOld = request.form["locationOld"]
        dateTimeOld = request.form["dateTimeOld"]
        
        cursor.execute("update meetings set groupID=%s, dateTime=%s, location=%s, meetingTopic=%s, stateName=%s where groupID=%s and dateTime=%s", [myGroupID[0], dateTime, location, meetingTopic, stateName, myGroupID[0], dateTimeOld])
        
        conn.commit()
        return render_template("editMeeting.html", step="update_database")





    
        

@app.route("/checklist", methods=['post','get'])
def checklist():
  if "step" not in request.form:
    conn=get_db()
    cursor = conn.cursor()
    cursor.execute('select checklist.species, commonname, seen from checklist natural join birds where email=%s',[session.get("email",None)])
    rowlist = cursor.fetchall()
    return render_template('checklist.html', step = "user_checklist", entries=rowlist)
    
  elif request.form["step"] == "Spotted":
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("update checklist set seen = 'TRUE' where email=%s and species=%s",[session.get("email",None),request.form["species"]])
    print("ran")
    conn.commit()
    cursor.execute('select checklist.species, commonname, seen from checklist natural join birds where email=%s',[session.get("email",None)])
    rowlist = cursor.fetchall()
    return render_template('checklist.html',step = "user_checklist", entries=rowlist)
    
  elif request.form["step"] == "Delete":
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("delete from checklist where email=%s and species=%s",[session.get("email",None),request.form["species"]])
    conn.commit()
    cursor.execute('select checklist.species, commonname, seen from checklist natural join birds where email=%s',[session.get("email",None)])
    rowlist = cursor.fetchall()
    return render_template('checklist.html',step = "user_checklist", entries=rowlist)

@app.route("/addtochecklist", methods=['post','get'])
def addtochecklist():
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("select stateName from states")
    row = cursor.fetchall()
    cursor.execute("select birds.family from birds group by family")
    familylist= cursor.fetchall()
    return render_template('addtochecklist.html',step="add", familydata = familylist, entries = row)

  elif request.form["step"] == "getbirds":
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("select species, commonname from birds natural join foundin where stateName=%s and family=%s",[request.form["state"],request.form["family"]])
    entries = cursor.fetchall()
    return render_template('addtochecklist.html', step="show_list", entries = entries)

  elif request.form["step"] == "add_to":
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO checklist(species, email, seen) VALUES(%s,%s,%s)",[request.form["species"],session.get("email",None),"FALSE"])
    conn.commit()
    return render_template('addtochecklist.html', step = "done")
    
    
    
#####################################################
# Database handling 
  
def connect_db():
    """Connects to the database."""
    debug("Connecting to DB.")
    conn = psycopg2.connect(host="database.rhodescs.org", user="ellje-23", password="ellje-23", dbname="practice", 
        cursor_factory=psycopg2.extras.DictCursor)
    return conn
    
def get_db():
    """Retrieve the database connection or initialize it. The connection
    is unique for each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = connect_db()
    return g.db
    
@app.teardown_appcontext
def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
        debug("Closing DB")
    
#####################################################
# Debugging

def debug(s):
    """Prints a message to the screen (not web browser) 
    if debugging is turned on."""
    if app.config['DEBUG']:
        print(s)

#####################################################
# App begins running here:

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)  # can turn off debugging with False