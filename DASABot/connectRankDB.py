'''

'''

import gspread
import os
import pathlib
from dotenv import load_dotenv

class connectDB:
    '''
    formats:

    WORKSHEET NAME FORMAT: DASA_YYYY_Rx

    WORKSHEET DATA FORMAT:

    [index, college_name, course_code, course_name, or_jee, cr_jee, or_dasa, cr_dasa, nicknames, ciwg_status]
       0         1             2            3          4       5       6        7         8           9

    where: or stands for opening rank
           cr stands for closing rank

    '''

    '''

    TO DO: 
    
    '''


    # constants, try not to change
    DB_KEY_FILENAME = "DASABot/db_key.json"
    RANK_SPREADSHEET_KEY = os.getenv("RANK_SPREADSHEET_KEY")


    # function to get sheet data for a specific year and round
    def get_sheet(self, year : str, round : str):

        # try to find a worksheet for respective year and round, raises value error if not found 
        sheet_name = f'DASA_{year}_R{round}' 
        try:   
            sheet_index = self.worksheet_names.index(sheet_name) 
        except ValueError: 
            raise ValueError("Invalid year / round")
            return
        
        wksdat = self.worksheet_data[sheet_index]
        return wksdat[2:]


    # function to request a list of colleges for a specific year and round
    def request_college_list(self, year : str, round : str): 
         
        current_sheet = connectDB.get_sheet(self, year, round)  # stores all values for current year and round    
        
        college_list = []
        for row in current_sheet:
            if row[1] not in college_list:
                college_list.append(row[1])
        
        return college_list[2:]


    # function to convert a college nickname to the original college name
    def nick_to_college(self, year : str, round : str, college_nick : str):
        current_sheet = connectDB.get_sheet(self, year, round)
        college_list = connectDB.request_college_list(self, year, round)    

        if college_nick in college_list: return college_nick

        for row in current_sheet:
            if college_nick in row[8]:
                return row[1]

        raise ValueError("Invalid college name")
        return
        

    # function to request a list of branches for a specific year, round and college
    def request_branch_list(self, year : str, round : str, college_name : str, ciwg : bool):
        current_sheet = connectDB.get_sheet(self, year, round)

        college_name = connectDB.nick_to_college(self, year, round, college_name)

        branch_list = []
        for row in current_sheet:
            if row[1] != college_name: continue ## skips any irrelevant college names 
            if not ciwg and row[9] == '1': continue ## checks for non-ciwg
            
            if row[2] not in branch_list:
                branch_list.append(row[2])

        return branch_list


    # functions to get rank statistics
    def get_statistics(self, year : str, round : str, college_name : str, branch_code : str, ciwg : bool):
        current_sheet = connectDB.get_sheet(self, year, round)
        branch_list = connectDB.request_branch_list(self, year, round, college_name, ciwg)
        code = branch_code.upper()

        # checks if branch is valid 
        if code not in branch_list:
            raise ValueError("Invalid branch name")
            return
        
        for row in current_sheet:
            if row[1] != college_name: continue
            if row[2] != branch_code: continue
            
            return row[4:8] # jee_or, jee_cr, dasa_or, dasa_cr
    

    #function to return 3 lists of colleges based on user's CRL and cutoff    
    def analysis(self, rank: int, ciwg: bool, branch: str = None):
        current_sheet = connectDB.get_sheet(self, "2022", "3")
        highclg = []
        midclg = []
        lowclg = []
        for row in current_sheet:
            val = int(row[5])
            if not ciwg and row[9] == '1':
                continue
            closing_rank = f"{row[1]} {row[2]} Closing rank: {row[5]}"
            if val - rank < 0:
                pass
            elif val - rank < 50000:
                lowclg.append(closing_rank)
            elif val - rank < 100000:
                midclg.append(closing_rank)
            if val - rank > 100000:
                highclg.append(closing_rank)

        if branch:
            lowclg = [clg for clg in lowclg if branch.lower() in clg.lower()]
            midclg = [clg for clg in midclg if branch.lower() in clg.lower()]
            highclg = [clg for clg in highclg if branch.lower() in clg.lower()]

        return lowclg, midclg, highclg



    '''
    ## testing function
    def testing(self):
        userinput= input("Please enter your selection \n1. Retrieve college rankings\n2. Enter JEE Rank to determine college chances\n")
        if userinput == "1":
            while True:
                year = input("Enter year: ")
                round = input("Enter round: ")
                
                current_sheet = connectDB.get_sheet(self, year, round)
                college_list = connectDB.request_college_list(self, year, round)
                
                print("\nChoose a college from below: ")
                for college in college_list:
                    print(college)

                breaker = True
                while breaker:
                    breaker = False
                    try:
                        college = input("\n")
                        college = connectDB.nick_to_college(self, year, round, college)
                    except ValueError:
                        print("Invalid college name, re-enter")
                        breaker = True

            
                ciwg_yn = input("Are you CIWG? (Y/N) ")
                ciwg = ciwg_yn.lower() == 'y'

                branch_list = connectDB.request_branch_list(self, year, round, college, ciwg)

                print(f"\nAvailable branches for {college}: " )
                for branch in branch_list:
                    print(branch)

                branch = input("\n")
                truebranch = branch.upper()
                while truebranch not in branch_list:
                    print("Invalid branch name, re-enter")
                    branch = input()

                
                stats = connectDB.get_statistics(self, year, round, college, truebranch, ciwg)
                print(f"""
                    \nStatistics for {college}, {truebranch}
                    \nJEE Opening Rank: {stats[0]}
                    \nJEE Closing Rank: {stats[1]}
                    \nDASA Opening Rank: {stats[2]}
                    \nDASA Closing Rank: {stats[3]}
                """)  

        elif userinput == "2":
            rank = int(input("Enter JEE Rank: "))
            ciwg_yn = input("Are you CIWG?(Y/N): ")
            ciwg = ciwg_yn.lower() == 'y'
            branch_yn = input("Which Branch?: ")
            branch = branch_yn.upper()
            lowclg, midclg, highclg = connectDB.analysis(self, rank, ciwg, branch)
            print("\n\nLow chances in: \n\n")
            for row in lowclg:
                print(row) 
            print("\n\nMid chances in: \n\n")
            for row in midclg:
                print(row)
            print("\n\nHigh chances in: \n\n")
            for row in highclg:
                print(row) 

        else: 
            print("Invalid input please try again") 
    '''


    # initialisation function 
    def __init__(self):
        load_dotenv()
        connectDB.RANK_SPREADSHEET_KEY = os.getenv("RANK_SPREADSHEET_KEY")
        self.cwd_path = os.getcwd()

        # connects to DB
        
        db_key_path = os.path.abspath(connectDB.DB_KEY_FILENAME)  # gets path name of db_key.json
        gc = gspread.service_account(filename = f'{db_key_path}')  # connects to service account

        self.database = gc.open_by_key(connectDB.RANK_SPREADSHEET_KEY) # connects to excel sheet

        self.worksheets = self.database.worksheets() # gets all the worksheets
        self.worksheet_names = [worksheet.title for worksheet in self.worksheets] # gets names of worksheets

        self.worksheet_data = [worksheet.get_all_values() for worksheet in self.worksheets]


obj = connectDB()
#obj.testing()

#changed so that branch input isnt case sensitive
#enabled user to enter nicknames of college to pull out data from dbs

#Changed so that getsheet() only returns values from row two onwards so that rankings data type can be changed from str to int for relational executions (omits headers of db)
#Implemented analysis() to return 3 lists, each list holding college name, branch and round 3 cutoff of 2022 of colleges based on the difference of user inputted CRL and round 3 cutoff
#Analysis takes in 2 arguments, rank and ciwg status but ciwg is still non functional. Arguments passed for get_sheet() are hard-coded onto analysis(), ie; year 2022 and round 3
#Edited testing() to allow user to choose between two functions, one forward engine and one reverse engine
#testing webhook again
