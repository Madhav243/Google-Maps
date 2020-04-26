import urllib.request, urllib.parse, urllib.error,webbrowser
import http,sqlite3,json,time,codecs,os

from tkinter import *

def showloc():
    serviceurl = "http://py4e-data.dr-chuck.net/json?"

    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Locations;
    CREATE TABLE Locations (address TEXT, geodata TEXT)''')


    fh = open("where.data",'w')
    fh.write(loc_field.get())
    fh.close()

    fh=open("where.data")
    for line in fh:
            address = line.strip()
            parms = dict()
            parms["address"] = address
            parms['key'] = 42
            url = serviceurl + urllib.parse.urlencode(parms)
            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            try:
                js = json.loads(data)
            except:
                print(data)

            if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
                break

            cur.execute('''INSERT INTO Locations (address, geodata)
                    VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
            conn.commit()

    fh.close()

    cur.execute('SELECT * FROM Locations')
    fhand = codecs.open('where.js', 'w', "utf-8")
    fhand.write("myData = [\n")
    count = 0
    for row in cur :
        data = str(row[1].decode())
        try: js = json.loads(str(data))
        except: continue

        if not('status' in js and js['status'] == 'OK') : continue

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        if lat == 0 or lng == 0 : continue
        where = js['results'][0]['formatted_address']
        where = where.replace("'", "")
        try :

            count = count + 1
            if count > 1 : fhand.write(",\n")
            output = "["+str(lat)+","+str(lng)+", '"+where+"']"
            fhand.write(output)
        except:
            continue

    fhand.write("\n];\n")
    cur.close()
    fhand.close()
    path=os.getcwd().replace("\\","/")
    url = "file://"+path+"/where.html"
    webbrowser.open(url,new=2)




if __name__=='__main__':
    gui=Tk()
    gui.config(background='white')
    gui.title("Google Maps")
    gui.geometry("250x140")
    cal=Label(gui,text="Google Maps",bg="dark grey",font=("times",28,'bold'))
    location=Label(gui,text="Enter Location",bg="light green")
    loc_field=Entry(gui)
    Show=Button(gui,text="Show location",fg="black",bg="red",command=showloc)
    Exit=Button(gui,text="Exit",fg="black",bg="Red",command=exit)
    cal.grid(row=1,column=1)
    location.grid(row=2,column=1)
    loc_field.grid(row=3,column=1)
    Show.grid(row=4,column=1)
    Exit.grid(row=6,column=1)
    gui.mainloop()
