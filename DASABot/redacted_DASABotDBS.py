import gspread
import re

## some weird ass thing i ripped off of stack overflow dont question it ##

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

## Establishing Data connection between Python and Cloud ##

connserv = gspread.service_account(filename=r"DASABot/dasa-bot-dbs-244b38b1da22.json")
connsheet = connserv.open("DASA 2022 Round 1")
wks= connsheet.worksheet("DASA 2022 Round 1 General")

## Retrieving all data from database onto python envionment ##

data = (wks.get_all_values())
newdat = []

## Defining functions to append college info based on CIWG status to newdat ##

def ciwg(a):
    if (i[1] == a) and ("1" in i[2]):
        newdat.append(i)
        return newdat
    elif findWholeWord(a)(i[8]) and ("1" in i[2]):
        newdat.append(i)
        return newdat
        
def nri(a):
     if (i[1] == a) and ("1" not in i[2]):
            newdat.append(i)
            return newdat
     elif findWholeWord(a)(i[8]) and ("1" not in i[2]):
        newdat.append(i)
        return newdat

## Initial loop taking in user input to filter out data based om college name and ciwg status ##

while True:
    loop_breaker1= False #resetting loop breaker status
    clg_name = input("Enter college name: ")
    ciwg_status = input("Is user CIWG? (Y/N): ")
    for i in data:
        if ciwg_status.lower() == "y":
            ciwg(clg_name)
        elif ciwg_status.lower() == "n":
            nri(clg_name)
        else:
             loop_breaker1 = True #to break out of inner loop
             break
    if loop_breaker1 == True: #to break out of outer loop
        print("Invalid Input try again")
        continue
    if newdat==[]:
         print("College not found in database")
         continue
    
    ## Displaying available majors based on user provided criteria ##

    print("Majors for the selected school are: ")

    for i in range (len(newdat)):
         course_code = newdat[i][2]
         course_name = newdat[i][3]
         print("Code:", course_code+",", course_name)

    ## Recieving user prompt to display cutoffs of a specific branch ##

    user_code = input("Please enter the Course Code to view cutoffs: ")
    for i in range (len(newdat)):
         if user_code.upper() == newdat[i][2]:
              print("\n"+ "Statistics for", newdat[i][1],"\n")
              print("JEE Opening Rank:", newdat[i][4])
              print("JEE Closing Rank:", newdat[i][5])
              print("DASA Opening Rank:", newdat[i][6])
              print("DASA Opening Rank:", newdat[i][7])

    ## Flag to continue pulling out data ##

    ans = input("Do you want to continue?: ")
    if ans.lower() == "y":
        newdat=[]
        continue
    else:
        break
