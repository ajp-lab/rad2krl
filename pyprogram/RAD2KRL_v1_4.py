#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#AP (C) 07/2009 - FILE I/O
#Version v1.4 - 20.07.09
#HYPERMESH Exports (.rad) - KRL (.src) INTERFACE
#reads a number of .rad Files - XYZ-coordinate lists
#supports currently .rad exports from Hypermesh v9.0
#converts .rad files into .src/KRL sourcecode files
#commandline and gui support

#v1.4 - 20.07.09 improvements
# works now for windows nt and unix derivatives

#imports
import os, string, math, shutil, time, sys
from datetime import datetime, date
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

#FUNCTIONS------------------

#current functions:
# setcwdtohome() - work with home dir
# sleepcount3() - sleep and count 3 secs
# hints() - important hints
# isReal() - check if number is real
# listAllRadFiles() - return all rad files from cwd
# newSrcFilename() - generate new filename for src files
# readRadFiles() - read rad files
# writeSrcFiles() - write src files
# createSrcFolder() - create folder for new src files
# startRad2Krl() - start program
#menu functions:
# about
# tips


#check homedir and set cwd to homedir, works with all winnt, unix, mac osx...
def setcwdtohome():
    homepath=os.path.expanduser("~")
    if os.access(homepath, os.W_OK) is True:
        os.chdir(homepath)
    else:
        print("***ERROR: Programm RAD2KRL ist mangels Schreib- und Leserechten auf Homeverzeichnissen nicht ausführbar!"+
              "\nBitte Home-Verzeichnissen Schreibrechte erteilen!")
        messagebox.showerror("Programm nicht ausführbar","Programm RAD2KRL ist mangels Schreib- und Leserechten auf Homeverzeichnissen nicht ausführbar!"+
                             "\nBitte Home-Verzeichnissen Schreibrechte erteilen!")
        sys.exit("Programm RAD2KRL ist mangels Schreib- und Leserechten auf Homeverzeichnissen nicht ausführbar!")    

#count and sleep for 3 secs
def sleepcount3():
    for i in range(1, 4):
        print(i)
        time.sleep(1)
    print("...GO")

#hints before program starts
def hints():
    print("WELCOME USER, TO THE PROGRAM RAD2KRL...\n"+
          "-----------------------------------------------------------------------\n"+
          "This program is written in Python 3 and converts .rad files from Hypermesh (v9.0) to\n"+
          "sourcecode files (.src) for the KRC2 interpreter from KUKA robot model KR140 L100\n"+
          "Version 1.4, Jul 2009. Author: A. Pucher\n"+
          "-----------------------------------------------------------------------\n")
    #sleep and count
    sleepcount3()
    print("Achtung... folgendes durchchecken, so dass das PYTHON-Programm korrekt funktioniert:\n"+
      "1) Wurde Hypermesh v9 zum Extrahieren der Punkte verwendet? Programm ist auf Version 9 optimiert!\n"+
      "2) Wurden die Punkte der Linien fuer das Prueffeld in 10 MM Abstaenden in ein .rad File extrahiert?\n"+
      "   OPTIMAL = 10 mm, max. Abstand = 20mm, ab >20mm werden nur mehr Punkte einzeln abgefahren!!!")
    time.sleep(5)
    print("------------------------------------------------------------------------\n"+
          "...OK...PYTHON PROGRAM RAD2KRL STARTS TO READ .rad Files IN 3 SECONDS...\n")
    #sleep and count
    sleepcount3()

#check if obj is a real number
def isReal(txt):
    try:
        float(txt)
        return True
    except ValueError:
        return False

#returns all .rad files from a directory
def listAllRadFiles():
    #decl
    radFileList=[]
    #prints current working directory
    print ("INFO: Current Working Directory is... "+ os.getcwd())
    print ("-----------------------------------------------------------------")

    #ask for directory, where the .rad files are
    while True:
        folderOfRadfiles = filedialog.askdirectory(initialdir="./", title="Bitte Ordner der zu konvertierenden .RAD Dateien auswaehlen...")
        #if "cancel" - end program
        if len(folderOfRadfiles)==0:
            messagebox.showwarning("Achtung", "Sie haben die Ordnerauswahl abgebrochen! Programm wird "+
                                       "dadurch beendet und es werden keine .rad Dateien eingelesen!")
            break
        else:       
            print ("INFO: You chose directory "+folderOfRadfiles)
            
        #list all files of folderOfRadfiles
        for datei in os.listdir(folderOfRadfiles):
            #erase whitespaces
            datei.strip()
            print ("INFO: File: "+ datei)    
            #list all .rad files of folderOfRadfiles, append radFiles to list
            if datei.endswith(".rad"):
                radFileList.append(datei)
                print ("-----------------------------------------------------------------")
                print ("INFO:  ===> .RAD FILE *** "+datei+" *** FOUND !!!")
                print ("-----------------------------------------------------------------")
                    
        print ("-----------------------------------------------------------------")
        if len(radFileList)== 0:
            print ("***WARNING: NO '.rad' files identified in the directory " + folderOfRadfiles+" !!!")
            messagebox.showwarning("Keine .rad Dateien", "Achtung, KEINE .rad Dateien gefunden - neues Verzeichnis auswählen!!!")
        else:
            print ("INFO: %dx '.RAD' file export(s) from Hypermesh format found." %(len(radFileList)))
            break
        print ("-----------------------------------------------------------------")
        print ("-----------------------------------------------------------------")
    
    #sleep and count
    sleepcount3()
    #return list of radFiles AND folderOfRadfiles
    return radFileList, folderOfRadfiles
    

#generate new filename for .src/KRL file (KRL = KUKA Roboter Language)
def newSrcFilename(radFileList):
    #decl
    srcFileList=[]
    for f_index, srcFilename in enumerate(radFileList):
        #adept filename from .rad export for .src file (line_filename.src)
        srcFilename = "KRL_"+srcFilename[:-4]
        #erase whitespaces from srcFilename
        srcFilename = srcFilename.strip()
        #new src filename - not more than <24 char - KRL limitation AND exact identification of each filename if is too long
        if len(srcFilename) > 23:
            #srcFilename = srcFilename[:23]
            srcFilename = srcFilename[:21] + "_" + str(f_index+1)
        print ("INFO: Old .rad-filename was %s, new .src-filename output is %s.src!" % (radFileList[f_index], srcFilename))
        #append the new srcFilenames to a list
        srcFileList.append(srcFilename)        
    #sleep and count
    sleepcount3()    
    return srcFileList

#read input from .rad FileList
def readRadFiles(radFileList, folderOfRadfiles):

    #decl dictionary mdict
    mdict = {}

    for rfl_item in radFileList:
	#input from .rad file
        try:
            file_rad = open(folderOfRadfiles + "/" + rfl_item)
        except:
            messagebox.showerror("Schwerwiegender Fehler!", "Einlesen des Files "+rfl_item+".rad funktioniert nicht. Programm endet!")
            print("***ERROR: Schwerwiegender Fehler! Einlesen des Files "+rfl_item+".rad funktioniert nicht. Programm endet!")
            sys.exit()

        #decl parameters new
        lineAusgabe=[]
        i=0
        #coords/rot
        ID=[]
        X=[]
        Y=[]
        Z=[]
        B=[]
        C=[]
        #math
        dAlpha=0
        vekLaengePkt=0
        #decl rotation standard, starting pos (no rotation) => B = 0°, C = 90°
        standardB = 0
        standardC = 90
        #flag vekLaenge
        vLTooLong=False
	
	#lese zeilenweise aus datei
        for line in file_rad:
				
	    #Einzulesende kartesische Koordinatenliste von file_rad darf max aus 4 Elementen bestehen (ID, X, Y, Z)
            if len(line.split())==4 and isReal(line.split()[0]) and isReal(line.split()[1]) and isReal(line.split()[2]) and isReal(line.split()[3]):
                print("INFO: LINE PROBABLY OK - exactly 4 elements (ID, X, Y, Z) and each element is a real number. Elements: %d" % (len(line.split())))
									
                ID.append(int(line.split()[0]))
                X.append(float(line.split()[1]))
                Y.append(float(line.split()[2]))
                Z.append(float(line.split()[3]))
		
                #coord check
                print("ID: %d" %(ID[i]))
                print("X: %f" %(X[i]))
                print("Y: %f" %(Y[i]))
                print("Z: %f" %(Z[i]))

		#Winkel ausrechnen - normal zur Fronthaube (Kruemmungen..)
		#nur wenn mehr als 1 Pkt
                if(i >= 1):
		    #Vektor (3D) d zwischen 2 Pkt
                    vekLaengePkt = math.sqrt(math.pow(X[i-1]-X[i], 2) + math.pow(Y[i-1]-Y[i], 2) + math.pow(Z[i-1]-Z[i], 2))

                    #check ob vekLaengePkt = 0 (avoid #DIV/0)
                    if (vekLaengePkt == 0):
                        #B, C Standard: keine Rotation
                        B.append(float(standardB))
                        C.append(float(standardC))                        
                        print("***ERROR: Something wrong - distance between 2 points is 0!!!")
                        messagebox.showerror("Keine Distanz zwischen 2 Punkten!", ("Distanz zwischen ersten Punkt mit der ID %d und \n"+
                                             "zweiten Punkt mit der ID %d ist NULL!\n\nLetzter Punkt wird geloescht.") % (ID[i-1], ID[i]))
                        #del last element from lineAusgabe (eliminate one of the points where the distance is 0)
                        lineAusgabe.pop()
                        #sleep and count
                        sleepcount3()
                        
                    #check ob vekLaengePkt - Punkte laenger als 20mm? (max) auseinanderliegen - zurueck auf HOME POS - Achtung Testbetrieb
                    elif (vekLaengePkt >20):
                        #flag to check if vekLaengePkt was once too long (>20)
                        vLTooLong=True
                        
                        #B, C Standard: keine Rotation
                        B.append(float(standardB))
                        C.append(float(standardC))
                        
                        print("INFO: Distance between 2 points > 20mm!!! - Drive back to HOME POS! OPTIMAL IS 10 MM!!!")
                        messagebox.showinfo("Distanz zwischen 2 Punkten ist >20mm", ("Da die Distanz zwischen ersten Punkt mit der ID %d und \n"+
                                            "zweiten Punkt mit der ID %d groesser als 20mm ist, wird eine Befehlszeile eingefuegt, sodass der Roboter\n"+
                                            "dazwischen auf die Startposition faehrt. Punktedistanz betraegt = %f mm.\n\n"+
                                            "Ideal dafuer, dass nur Punkte einzeln abgefahren und keine Linien dazwischen eingezeichnet werden.\n"+
                                            "Sollen Linien eingezeichnet werden, MUSS der Punkteabstand zw. 2 Punkten kleiner als 20mm sein!") % (ID[i-1], ID[i], float(vekLaengePkt)))
                        #app HOME POS
                        lineAusgabe.append("PTP HOME ;drive back to HOME POS - distance between the 2 points >20mm \n")
                        
                    else:                        
                        #Winkel - Z-Unterschied/Ebene
                        #1 Drehung per Pn..Pn+1 - Vektorlänge/Winkel auf Z-Ebene um XY-Achse wg. Fronthaubenkruemmungen
                        #wenn Z von P1 und P2 = 0 (ebene Fläche) entsteht keine B oder C Rotation
                        #wenn dAlpha positiv = Z-Steigung, negativ = Z-Senkung
                        dAlpha = math.asin((Z[i]-Z[i-1])/vekLaengePkt)
                        #Bogenmass in Gradmass umrechnen
                        dAlphaGrad = (dAlpha*180)/math.pi
                        #Standard-Normalwert A 90°, B 0°, C 90° (KUKA-spezifisch) Stift normal auf XY-Achse (in Z-Achse liegend)                    
                        #A/B/C = KUKA-Pos. - dAlphaGrad (pos. Richtung Uhrzeigersinn, neg. gegen Uhrzg.)
                        #A = Rotation um Z-Achse - in dem Fall unerheblich, Stift dreht sich nur um eig. Z-Achse 
                        #B = Rotation um X-Achse: 0 Standard = Sueden, Westen: -90, Osten: 90
                        #C = Rotation um Y-Achse:  90 Standard=Sueden, Westen: 180, Osten: 0

                        #Rotation Info
                        print("dAlphaGrad/Rotation is: %f °" % (dAlphaGrad))

                        #Rotation um Y-Achse = C, wenn X von Pkt 1 kleiner als von Pkt 2 = Bewegung Richtung X positiv, umgekehrt negative Richtung
                        if(X[i-1]<X[i]):
                            C.append(float(standardC - dAlphaGrad))
                        elif(X[i-1]>X[i]):
                            C.append(float(standardC + dAlphaGrad))                            
                        else:
                            C.append(float(standardC))
                        #Rotation um X-Achse = B, wenn Y von Pkt 1 kleiner als von Pkt 2 = Bewegung Richtung Y positiv, umgekehrt negative Richtung
                        if(Y[i-1]<Y[i]):
                            B.append(float(standardB - dAlphaGrad))
                        elif(Y[i-1]>Y[i]):
                            B.append(float(standardB + dAlphaGrad))
                        else:
                            B.append(float(standardB))
                else:
		    #A/B/C Standard - ebene Flaeche (keine Rotation)
                    B.append(float(standardB))
                    C.append(float(standardC))

		#Hinzufuegen einer LIN-Zeile(KRL)
                lineAusgabe.append("LIN {X %f,Y %f, Z %f,A 90, B %f, C %f} C_DIS\n" % (float(X[i]), float(Y[i]), float(Z[i]), float(B[i]), float(C[i])))

		#Count i 1up
                i+=1
			
            else:
                print("INFO: line --- %s --- hasnt been read!" % (line))

        print("***END: %d NODES/POINTS HAVE BEEN READ FROM FILE --- %s --- !!!" % (len(lineAusgabe), rfl_item))

        #sleep and count
        sleepcount3()

	#schließe datei, zeilenweise lesen ende
        file_rad.close()

        #Option YES/NO um Linie(n) dieses aktuell eingelesenen .rad Files strichliert zeichnen zu koennen, nur wenn Punkte in richtigem Abstand (<20mm)
        if vLTooLong == False:
            answ= messagebox.askyesno("Linie strichliert zeichnen?", "Optimal. Kein Punkteabstand"+
                            " der Linienpunkte des Files '"+rfl_item+".rad' betraegt mehr als 20mm.\n\n"+
                            "Soll(en) diese Linie(n) strichliert gezeichnet werden? (z.B. notwendig bei einem ENCAP-Prueffeld)")
            if answ == True:
                #del 2 linepoints every 2 linepoints
                for delpos in range(0, len(lineAusgabe), 2):
                    del lineAusgabe[delpos+2:delpos+4]
                #insert ptp home - drive back home pos every two line points
                #decl inspos
                inspos = 0
                while inspos <= len(lineAusgabe)-1:
                    lineAusgabe.insert(inspos+2, "PTP HOME ;Back to home position - strichliert zeichnen\n")
                    inspos += 3
                print("INFO: Sie haben JA gewaehlt. Linienpunkte des Files "+rfl_item+" werden als Linie strichliert eingezeichnet!")
            else:
                print("INFO: Sie haben NEIN gewaehlt. Linienpunkte des Files "+rfl_item+" werden als Linie nicht strichliert und normal eingezeichnet!")
        else:
            print("INFO: Linie(n) des Files " + rfl_item+" koennen nicht strichliert eingezeichnet werden, da ein oder\n"+
                  " mehrere Punkteabstaende auf den/der Linie(n) >20mm sind!")

        #save lineAusgabe in m-dim list/dict
        mdict[rfl_item] = lineAusgabe
        
        #clear/del parameters
        del lineAusgabe, ID, X, Y, Z, B, C, i, dAlpha, vekLaengePkt
    
    #return dict mdict
    return mdict

#write output from lineAusgabeList into .src files
def writeSrcFiles(radFileList, srcFileList, mdict):

    #decl key index for iterating through radFileList which is in dict mdict
    key_i=0
    
    for sfl_item in srcFileList:
        #---------printout KRL----------------
        #open new krl file for output
        try:
            file_src = open (sfl_item+".src", "w")
        except:
            messagebox.showerror("Schwerwiegender Fehler!", "Schreiben des Files "+sfl_item+".src funktioniert nicht. Programm endet!")
            print("***ERROR: Schwerwiegender Fehler! Schreiben des Files "+sfl_item+".src funktioniert nicht. Programm endet!")
            sys.exit()
            
        #begin
        file_src.write("DEF %s()\n\n" %(sfl_item))
        #comment
        file_src.write(";Job name: Erzeuge Linie(n) aus File "+ sfl_item+".rad\n"
                       ";Product : "+sfl_item+".src (KUKA KRL Kuka Roboter Language) Programmdatei \n"
                       ";Date: Erzeugt am "+datetime.now().strftime("%d.%m.%y, %H:%M:%S")+"\n"
                       ";Project name: RAD2KRL v1.4 - Erzeuge KUKA KRL Sourcecode aus .rad Dateien von Hypermesh v9.0\n"
                       ";Author: A. Pucher\n"
                       ";Company: Magna Steyr Engineering - Vehicle Safety\n"
                       ";Division: Pedestrian Safety\n\n")
        #decl
        file_src.write(";FOLD DECLARE\n"+
                           ";--------- Deklarationsteil ---------\n"+
                           "EXT BAS (BAS_COMMAND :IN,REAL :IN )\n"+
                           "DECL AXIS HOME\n"+
                           ";ENDFOLD\n\n")
        #init
        file_src.write(";FOLD INITIAL\n"+
                           ";---------- Initialisierung ---------\n"+
                           "INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )\n"+
                           "INTERRUPT ON 3\n"+
                           "BAS (#INITMOV,0 ) ;Initialisierung von Geschwindigkeiten,\n"+
                           ";Geschwindigkeiten, Beschleunigungen, $BASE, $TOOL, etc.\n"+
                           "HOME={AXIS: A1 30,A2 -130,A3 100,A4 100,A5 -20,A6 -20} ;mom. ohne Probleme (Singularitaet)\n"+
                           "bSolldatenOK=FALSE\n"+
                           ";Hier stoppt Programm bis bSolldaten=True d.h. bis Eingaben Tool-Nr und Base-Nr OK sind\n"+
                           "WAIT FOR bSolldatenOK==TRUE\n"+
                           "$BASE = BASE_DATA[nBase]\n"+
                           "$TOOL = TOOL_DATA[nTool]\n"+
                           "$VEL.CP=2 ;Anfahrgeschwindigkeit\n"+
                           "$APO.CDIS = 2.5 ;LIN/LIN Ueberschleifen - fuer Abstaende von 10mm: 2.5mm optimal\n"+
                           ";ENDFOLD\n\n")
        #main part
        file_src.write(";---------- Start - Go ---------\n"+
                           "PTP HOME ;SAK-Fahrt\n")
            
        for la_item in mdict[radFileList[key_i]]:
            file_src.write(la_item)

        #count key_i 1up, for next key element (which is a .rad file)
        key_i +=1

        #last PTP-Home, EOF
        file_src.write("PTP HOME\n"+
                           "END\n")
        #---------EOF KRL/SRC FILE------------
        file_src.flush()
        file_src.close()

        print("INFO: File for KUKA (KRL) "+ sfl_item+" has been SUCCESSFULLY created!!!")
        
    #sleep and count
    sleepcount3()

#create new folder and move all .src (KRL) files from cwd into it
def createSrcFolder(srcFileList):
    #generate name of new src folder from current date and time
    srcFolderName = datetime.now().strftime("srcFiles_%d%m%y_%H%M%S")
    
    #ask where the new src files should be saved, check write permission
    while True:
        folderOfSrcfiles = filedialog.askdirectory(initialdir="./", title="Wohin sollen die neuen .SRC Dateien gespielt werden?")
        if os.access(folderOfSrcfiles, os.W_OK) is True and len(folderOfSrcfiles)>0:
            print ("INFO: Verzeichnis "+folderOfSrcfiles+" erfolgreich ausgewählt!")
            break
        #if "cancel" - default => to cwd
        elif len(folderOfSrcfiles)==0:
            folderOfSrcfiles = os.getcwd()
            messagebox.showwarning("Achtung", "Sie haben die Ordnerauswahl abgebrochen! Neue '.SRC' Dateien werden\n"+
                                   "in einen neuen Unterordner des Home-Verzeichnisses "+folderOfSrcfiles+" kopiert.")
            break
        else:
            messagebox.showerror("Achtung, keine Schreibrechte!", "Sie haben für das Verzeichnis "+folderOfSrcfiles+" keine Schreibrechte!\n"+
                                   "Bitte anderes Verzeichnis auswählen!") 

    #create new src folder
    try:
        os.mkdir(folderOfSrcfiles+"/"+srcFolderName)
        print("INFO: Neuer Ordner "+srcFolderName+" erstellt.")
    except:
        print("***ERROR: Ordner "+srcFolderName+" erstellen hat nicht funktioniert! Programm endet!")
        messagebox.showerror("Fehler beim Erstellen eines Ordners!", "Ordner "+srcFolderName+" erstellen hat nicht funktioniert! Programm endet!")
        sys.exit()

    #move all .src files to new folder
    for datei in os.listdir(os.getcwd()):
        #list all new created .src files of cwd and checks if the .src file is in filelist of created .src files
        if datei.endswith(".src") and datei[:-4] in srcFileList:
            shutil.move(datei, folderOfSrcfiles+"/"+srcFolderName)
            print ("-----------------------------------------------------------------")
            print ("INFO:  ===> NEW .SRC (KUKA KRL) FILE *** "+datei+" *** FOUND !!!")
            print ("INFO:  ===> .SRC (KUKA KRL) FILE MOVED TO NEW SUBFOLDER --- "+srcFolderName+" --- !!!")
            print ("-----------------------------------------------------------------")
    messagebox.showinfo("Ende", "Neue .SRC Dateien wurden generiert und in das Verzeichnis \n"+
                        folderOfSrcfiles+" in den neuen Unterordner "+srcFolderName+" gespielt.\n"+
                        "Programm endet. Bis zum naechsten Mal.\n\n"+
                        "Weitere Schritte:\n"+
                        "Ordner mit den neuen .src (KUKA KRL) Programmdateien auf einen USB-Stick od. Diskette spielen,\n"+
                        "und in das Dateisystem der Robotersteuerung kopieren und Programmdateien starten.")
    #sleep and count
    sleepcount3()
    print("PROGRAM ENDS HERE. GOOD BYE!")


#start main program---------------------------------------------
def startRad2Krl():
    #for avoiding errors give over copies of lists as parameters
    #decl
    radfilelist = []
    srcfilelist = []
    mdimlineausg = {}

    #start main
    #-----------
    #set cwd to home dir of user
    setcwdtohome()
    #hints
    hints()
    #get rad files and folderOfRadfiles
    radfilelist, radfolder = listAllRadFiles()    
    #quit if radfilelist contains no files!
    if len(radfilelist)>0:
        #generate new src filenames for converted rad files
        srcfilelist = newSrcFilename(radfilelist[:])
        #save return value from generated 'LIN' Commands (lineAusgabe) in a dict, radfolder
        mdimlineausg = readRadFiles(radfilelist[:], radfolder)
        print("INFO: Eingelesene .rad files waren: %s"%(list(mdimlineausg.keys())))
        #write krl/src files from generated input
        writeSrcFiles(radfilelist[:], srcfilelist[:], mdimlineausg)
        #create new src folder for generated .src/krl files
        createSrcFolder(srcfilelist[:])
    else:
        messagebox.showwarning("Keine .RAD Files gefunden", "Es wurde abgebrochen - Programm endet!")
        print("INFO: Programm endet. Keine .rad Dateien gefunden. GOOD BYE!")

    #End program
    root.quit()

#menu functions
def about():
    messagebox.showinfo("About", "Tool 'RAD2KRL' wurde programmiert in Python 3.\n"+
                        "Informationen ueber Python auf www.python.org\n\n"+
                        "Konvertiert .rad Files in .src Files fuer Kuka Roboter Control.\n"+
                        "Programmiert im Rahmen einer Diplomarbeit (Dauer von Jan 09 - Jul 09) \n"+
                        "fuer den Einsatz bei MS-Engineering, Fahrzeugsicherheit, \n"+
                        "Fussgaengerschutz um automatisiert Prueffelder (PHASE I, II, ENCAP)\n"+
                        "auf eine Fahrzeugfront zu uebertragen.\n\n"+
                        "Erstellung: Juli 2009, Version 1.4\n"+
                        "Betreuer FH Joanneum: DI John Feiner\n"+
                        "Firmenbetreuer: DI Dr Heribert Kassegger\n"+
                        "Author/Programmierer: Alfred Pucher\n"+
                        "Mail: alfred.pucher.itm05@fh-joanneum.at od. alfred.pucher@gmail.com\n"+
                        "Hotline: Bei Problemen bitte Tel.-Nr. +43 676 917 22 03 anrufen.")

def tips():
    messagebox.showinfo("Tips", "Wichtiges zum Ablauf des Programms und zur Programmbenutzung:\n\n"+
                        "Das Programm bietet die Moeglichkeit, einen Ordner auszuwaehlen, wo die zu\n"+
                        "konvertierenden .rad Files liegen. Diese .rad Files werden eingelesen und\n"+
                        "und in .src Files konvertiert (Dateiname: KRL/KUKA seitig beschraenkt auf max. 24 Zeichen).\n"+
                        "Das Format fuer neue, konvertierte .src Files ist 'krl_+alter Filename' von .rad.\n"+
                        "Der Dateiname vom .rad File wird als Dateiname fuer das .src File uebernommen, ist dieser laenger als \n"+
                        "24 Zeichen wird dieser automatisch auf unter 24 Zeichen gekuerzt.\n"+
                        "Die neuen .src Files werden automatisch in einem Unterordner in einem ebenfalls selbst\n"+
                        "gewaehlten Verzeichnis kopiert. Dieser Ordner bekommt automatisch den Namen \n"+
                        "im Format 'srcFolder_ddmmyy_hhmmss' zugewiesen, um die Eindeutigkeit des Ordners\n"+
                        "sicherzustellen (d=Tag, m=Monat, y=Jahr, h=Std, m=Min, s=Sec). In diesem Ordner\n"+
                        "liegen nun die neuen, generierten .src Files fuer die Robotersteuerung des KUKA-Roboters.\n"+
                        "Diese .src/bzw. Programmfiles sind nun in das Filesystem des Roboters/der Robotersteuerung\n"+
                        "zu kopieren und das Programmfile kann gestartet werden. Der Roboter sollte nun die Bewegungs-\n"+
                        "anweisungen nach den exportierten Punkten des/der .rad File/s durchfuehren.\n"+
                        "Die Rotationen um die XYZ-Achsen, so dass der Lackstifts immer flaechennormal zeichnet,\n"+
                        "werden autmatisch berechnet. (z.B. bei Kruemmungen der Fronthaube)\n"+
                        "Das Programm kann natuerlich nur genau die Punkte abfahren, die auch in das .rad File mithilfe von\n"+
                        "Hypermesh exportiert worden sind, z.B. ein ganzes Prueffeld oder auch nur einzelne Linien eines Prueffelds...\n\n"+
                        "WICHTIG:\n"+
                        "Das Programm ist darauf ausgelegt, eine Punkteliste von optimal 10mm Abstaenden zu verarbeiten.\n"+
                        "Nur dann werden Linien optimal, rund und moeglichst genau eingezeichnet.\n"+
                        "Ab Abstaenden von 20mm werden Punkte nur mehr einzeln abgefahren, ohne Linieneinzeichnung, \n"+
                        "das Programm schaltet in den Punktemodus.\n"+
                        "Wenn gewuenscht, kann eine Linie auch strichliert eingezeichnet werden (z.B. bei ENCAP-Prueffeld).\n"+
                        "Dazu ist es noetig, die Linien eines Prueffelds einzeln zu extrahieren und beim Einlesen des .rad-Files\n"+
                        "in dem die Koordinaten der strichlierten Linie sind, 'Linie strichliert zeichnen?' mit 'JA' zu bestaetigen.\n"+
                        "Sinnvoll ist es, den Dateinamen des extrahierten .rad Files mit z.B. 'strichliert' zu kennzeichnen,\n"+
                        "um die Punkteliste der Linie bzw. das .rad File selbst leichter zu erkennen, das strichliert werden soll.\n"+
                        "Die Luecken auf der strichlierten Linie entsprechen einem doppelten Punkteabstand.\n\n"+
                        "Folgende Optionen sind also moeglich:\n"+
                        "1) Linien normal einzeichnen (Export der Linienpunkte in Hypermesh im Bereich von [min. 1mm bis max: 20 mm] - optimal sind 10 mm!\n"+
                        "2) Linien strichliert einzeichnen (.rad Dateiname umbenennen/kennzeichnen mit z.B. 'strichliert' und mit 'JA' bestaetigen)\n"+
                        "3) Punkte abfahren - es werden keine Linien eingezeichnet, sondern nur einzeln Punkte abgefahren - dazu ist es noetig,\n"+
                        "   die Punkte im Abstand von groesser als >20mm zu exportieren.\n\n"+
                        "Bei 2) innerhalb der strichlierten Linie und bei 3) zwischen den einzelnen Punkten verfaehrt der Roboter immer wieder auf die\n"+
                        "HOME-Position und wieder zurueck, fuer Anfangskalibrierung und bei Ende auch - das bei 1), 2) und 3).")


#END FUNCTIONS--------------


#MAIN GUI-------------
#GUI for rad2krl

root = Tk()

#canvas
canvas= Canvas(width= 640, height = 360, bg="black")
canvas.pack(expand=YES, fill=BOTH)
#text
canvas.create_text(235,20,text="Dieses Tool ist kompatibel mit Altair HYPERMESH v9.0 & KUKA Roboter Modell KR140 L100.\n", fill="white")
canvas.create_rectangle(10, 40, 630, 30, fill="red", outline="white", width=0)
canvas.create_text(325,180, text="INFORMATION\n\n"+
                   "-Dieses Tool erzeugt KRL(Kuka Roboter Language) Code bzw. Bewegungsanweisungen, damit Prueffeldlinien\n"+
                   " von Prueffeldern wie Phase I, II und ENCAP autmatisiert auf eine beliebige Fahrzeugfront uebertragen"+
                   " werden koennen.\n"+
                   "-Es dient als Schnittstelle zwischen dem Programm Hypermesh von Altair am Rechner und der Robotersteuerung (KRC2),\n"+
                   " die die zu zeichnenden Prueffeldlinien als Bewegungsanweisungen fuer den verwendeten KUKA-Roboter interpretieren muss.\n"+
                   "-Aus Hypermesh werden ausgehend von dem Konstruktionsmodell des Fahrzeugs die Linienpunkte des Prueffelds als Punkte in\n"+
                   " der Form P: (X,Y,Z) in einem Abstand von (EMPFEHLENSWERT: 10 MM) in ein Plaintext-File (Endung '.rad') exportiert.\n"+
                   "-Dieses Tool konvertiert jedes exportierte .rad-File in einen für die Robotersteuerung verständlichen KRL-Code, d.h.\n"+
                   " in ein Programmfile (mit Endung '.src'), das nach erfolgter Konvertierung in das Filesystem der Robotersteuerung kopiert wird.\n"+
                   "-Damit laesst sich nun am Roboter das kopierte KRL-Programfile starten und der Roboter fuehrt Bewegungsanweisungen in der\n"+
                   " Reihenfolge der exportierten Punkteliste durch. Mit dem am Roboterarm/Effektor angebrachten Lackstifthalterung lassen sich die\n"+
                   " Linien einzeichnen. Voraussetzung dafuer ist, dass man sich mit dem Roboter korrekt in das Base-(Fahrzeug)und das Tool-(Lackstift)\n"+
                   " Koordinatensystem eingemessen hat.\n\n"+
                   "-Schnittstellen: Rechner(Hypermesh) <= Rechner(Tool) => Roboter(KUKA/KRL)bzw. Robotersteuerung(KRC2) - Fahrzeug\n"+
                   "-Konvertierungsprozess: Hypermesh (.rad File) => Tool => KRL Programmfile (.src File) - Kopie des/der .src File(s) in das Filesystem\n"+
                   " der Robotersteuerung mittels USB, Ethernet, Diskette."+
                   "\n\n", fill="white")
canvas.create_rectangle(10, 310, 630, 300, fill="red", outline="white", width=0)
canvas.create_text(290, 330, text="Programmiert fuer MAGNA STEYR Engineering Graz, Abt. FGS-I, Fahrzeugsicherheit - Fussgaengerschutz, "+
                   "Jul 2009, v1.4", fill="white")


#create a menu
menu = Menu(root)
root.config(menu=menu)
root.title("RAD2KRL v1.4")
root.resizable(width=0, height=0)

#menu items
startmenu = Menu(menu)
menu.add_cascade(label="START", menu=startmenu)
startmenu.add_command(label="Start RAD2KRL...", command=startRad2Krl)

startmenu = Menu(menu)
menu.add_cascade(label="EXIT", menu=startmenu)
startmenu.add_command(label="Exit/Cancel RAD2KRL", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="HELP", menu=helpmenu)
helpmenu.add_command(label="Tips", command=tips)
helpmenu.add_command(label="About", command=about)

#statusbar
status = Label(root, text="RAD2KRL (C) by A.P., v1.4, Jul 2009 - Python 3. OS: "+str(os.name.upper()), bd=1, relief=SUNKEN, anchor=W)
status.pack(side=RIGHT)

mainloop()

#END MAIN GUI-------------------

#---------EOF------------------
