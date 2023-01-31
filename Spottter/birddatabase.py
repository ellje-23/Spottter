import psycopg2

conn = psycopg2.connect(host="database.rhodescs.org", user="ellje-23", password="ellje-23", dbname="practice")
cur = conn.cursor()

# Adding bird color
def add_colors_from_csv(filename):
  with open(filename,'r') as file:
     next(file)
     cur.copy_from(file,'birdcolors', sep=',')
  conn.commit()

def add_birdcolor(species, colorName):
  cur.execute("INSERT INTO birdcolor(species, colorName) Values (%s, %s)",[species, colorName])
  conn.committ()

# Add sighting
def add_sightings_from_csv(sightings):
  with open(sightings,'r') as file:
    next(file)
    cur.copy_from(file,'sightings', sep=',')
  conn.commit()

def add_sighting(email, species, dateTime, longitude, latitude, stateName):
  cur.execute("INSERT INTO sightings(email, species, dateTime, longitude, latitude, stateName) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [email, species, dateTime, longitude, latitude, stateName])
  conn.commit()

# Add group
def add_groups_from_csv(groups):
  with open(groups,'r') as file:
    next(file)
    cur.copy_from(file,'groups',sep=',')
  conn.commit()

def add_group(groupID, numMembers, groupName):
  cur.execute("INSERT INTO groups(groupID, numMembers, groupName) VALUES(%s,%s,%s)",[groupID, numMembers, groupName])
  conn.commit()

# Add bird
def add_birds_from_csv(birds):
  with open(birds,'r') as file:
    next(file)
    cur.copy_from(file,'birds',sep=',')
  conn.commit()

def add_bird(species, genus, commonName, order, family, length, wingspan):
  cur.execute("INSERT INTO birds(species, genus, commonName, order, family, length, wingspan) VALUES(%s,%s,%s, %s,%s,%s, %s)",[species, genus, commonName, order, family, length, wingspan])
  conn.commit()

# Add checklist
def add_checklists_from_csv(checklist):
  with open(checklist,'r') as file:
    next(file)
    cur.copy_from(file,'checklist',sep=',')
  conn.commit()

def add_checklist(species, email, seenNotSeen):
  cur.execute("INSERT INTO groups(species, email, seenNotSeen) VALUES(%s,%s,%s)",[species, email, seenNotSeen])
  conn.commit()

# Add foundIn
def add_foundIn_from_csv(foundin):
  with open(foundin,'r') as file:
    next(file)
    cur.copy_from(file,'foundin',sep=',')
  conn.commit()

def add_foundIn(species, stateName, speciePopulation):
  cur.execute("INSERT INTO groups(species, stateName, speciePopulation) VALUES(%s,%s,%s)",[species, stateName, speciePopulation])
  conn.commit()

# Add meetings
def add_meetings_from_csv(meetings):
  with open(meetings,'r') as file:
    next(file)
    cur.copy_from(file,'meetings',sep=',')
  conn.commit()

def add_meeting(groupID, dateTime, location, state, meetingTopic):
  cur.execute("INSERT INTO groups(groupID, dateTime, location, state, meetingTopic) VALUES(%s,%s,%s,%s, %s)",[groupID, dateTime, location, state, meetingTopic])
  conn.commit()
  
# Add states
def add_states_from_csv(states):
  with open(states,'r') as file:
    next(file)
    cur.copy_from(file,'states',sep=',')
  conn.commit()

def add_state(stateName, region):
  cur.execute("INSERT INTO groups(stateName, region) VALUES(%s,%s)",[stateName, region])
  conn.commit()

# Add user
def add_user_from_csv(users):
  with open(users,'r') as file:
    next(file)
    cur.copy_from(file,'users',sep=',')
  conn.commit()

def add_user(email, firstName, lastName, state, groupID, password):
  cur.execute("INSERT INTO groups(email, firstName, lastName, state, groupID, password) VALUES(%s,%s)",[email, firstName, lastName, state, groupID, password])
  conn.commit()

def main():
  add_colors_from_csv("birdColor.csv")
  add_birds_from_csv("birds.csv")
  add_checklists_from_csv("checklist.csv")
  add_foundIn_from_csv("foundIn.csv")
  add_groups_from_csv("groups.csv")
  add_meetings_from_csv("meetings.csv")
  add_sightings_from_csv("sightings.csv")
  add_states_from_csv("states.csv")
  add_user_from_csv("users.csv")
  

