_amol is **very** hot_

### Following are the required pre-requisites:
The following libraries can also be found in `requirements.txt` by running the following command:
`pip install -r requirements.txt`

`gspread` - `pip install gspread`  
`dotenv` - `pip install python-dotenv`
`discord.py` - `pip install discord.py`  
`discord.py-pagination` - `pip install discord.py-pagination`
`pretty-help` - `pip install discord-pretty-help`
    
### Account details for the Google Sheets:  
ID: dasabot1@gmail.com  
Password: Discord@123  

---

# Summary

## Code Breakdown:

### connectRankDB.py

1. The script imports the necessary libraries, `gspread` for interacting with Google Sheets, as well as `os` and `pathlib` for getting filepaths etc.
2. The script establishes a data connection to Google Sheets using the `service_account` method from `gspread`. It loads the service account credentials from a JSON file named `"DASABot/db_key.json"`.
4. It then opens a specific google sheet using its key, and then gets all the worksheets present and adds it to an object variable called `worksheets`
5. The script retrieves all the values from the worksheet using the `get_all_values` method and stores them in the `worksheet_data` variable in the form of a nested list. Since the data is static, the program operates based on list indexes.

Upon this, there are multiple methods to execute specific functions:

- `get_sheet` searches the worksheet containing the cutoffs of a specific year and round
- `request_college_list` returns a list of colleges participating in DASA counselling in a specific year and round
- `nick_to_college` converts any college nickname to its full name and returns it
- `request_branch_list` returns a list of valid branches under a college depending on whether the student qualifies for ciwg or not
- `get_statistics` returns a list of the cutoff ranks for a specific branch under a college
- `get_statistics_for_all` returns a list of cutoff ranks for all branches under a specified college (using `get_statistics`)
- `reverse_engine` returns a list of colleges which has a closing rank cutoff closest to the rank given by the user
- `analysis` returns three lists each containing the names of colleges filtered out by the difference between the user's CRL and college's Round 3 JEE Closing cutoff

NOTE: The code assumes the presence of the `gspread` library and a valid service account JSON file with the appropriate access to the Google Sheet.
