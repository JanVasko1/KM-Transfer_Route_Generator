import pandas
import pyodbc
import os

def update_string(inset_value):
    try:
        inset_value = str(inset_value).replace(" ", "_")
        return inset_value
    except:
        return inset_value

File_path = os.path.dirname(os.path.abspath(__file__))
output = open(f"{File_path}/Transfer_Rout_result", "wt", encoding="utf-8", errors='ignore')  


#--------------------------------------------------------------------Downloader--------------------------------------------------------------------#
# Data downloaded from DB
NUS2_NOC_list = ["NAV2009", "BBG", "BBL", "BCZ", "BFI", "BGR", "BHN", "BNO", "BPT", "BRO", "BSK", "BSW", "BTR", "BUR"]
NUS3_NOC_list = ["COREQA", "BDK", "BPL", "BHR", "BSL", "BIH", "BRS", "BR"]

NUS_Version = ""
while NUS_Version != "NUS2" and NUS_Version != "NUS3":
    NUS_Version = update_string(input("Which NUS Version you want to select as data source? [NUS2/NUS3]: "))
Data_System = ""
while Data_System != "QA" and Data_System != "PRD":
    Data_System = update_string(input("Which DB you want to select as data source? [QA/PRD]: "))

if NUS_Version == "NUS2":
    Data_NOC = ""
    while Data_NOC not in NUS2_NOC_list:
        Data_NOC = update_string(input(f"Which NOC you want to select? {NUS2_NOC_list} [Code]: "))
elif NUS_Version == "NUS3":
    Data_NOC = ""
    while Data_NOC not in NUS3_NOC_list:
        Data_NOC = update_string(input(f"Which NOC you want to select? {NUS3_NOC_list} [Code]: "))
else:
    pass

# Database connection preparation
if NUS_Version == "NUS2":
    if Data_System == "QA":
        server = 'kmnus2qadbs01.erp.kme.intern'
    else:
        server = 'kmnus2prddbs01.erp.kme.intern'
elif NUS_Version == "NUS3":
    if Data_System == "QA":
        server = 'kmnavqdbs03.bs.kme.intern'
    else:
        server = 'kmnavpdbs03.bs.kme.intern'
else:
    print("No NUS Version selected")
    exit

# Database connection
database = update_string(Data_NOC+Data_System)
if Data_NOC == "NAV2009" or Data_NOC == "COREQA":
    database = update_string(Data_NOC)
dabase_schama = "dbo"
Connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'
cnxn = pyodbc.connect(Connection_string, autocommit=True)
cursor = cnxn.cursor()

# Company Selection
company_list = []
cursor.execute(f'SELECT [Name] FROM [{database}].[{dabase_schama}].[Company]')
for row in cursor.fetchall():
    company_list.append(row[0])
Company = ""
while Company not in company_list:
    Company = str(input(f"Select Company you want {company_list}: "))

Location_list = []
Location_list_all = []

# NUS3 Location List
if NUS_Version == "NUS3":
    cursor.execute(f'SELECT [Code],[Location Type] FROM [{database}].[{dabase_schama}].[{Company}$Location]')
    for row in cursor.fetchall():
        Location_list.append(row)
elif NUS_Version == "NUS2":
    cursor.execute(f'SELECT [Code],[Location Type],[Use As In-Transit] FROM [{database}].[{dabase_schama}].[{Company}$Location]')
    for row in cursor.fetchall():
        Location_list.append(row)
else:
    pass

cnxn.commit()
cursor.close()

Empty = []
Consignment_Stock = []
Technician = []
Sub = []
Main = []
On_Board = []
In_Transit = []
Returned_Machines = []

#--------------------------------------------------------------------Prepare Transfer Rout Import--------------------------------------------------------------------#
# List of all Locations:
for location in Location_list:
    Location_list_all.append(location[0])
Location_list_all = list(set(Location_list_all))
# Location Types:
# NUS3
"""
0 - Empty
1 - Consignment Stock
2 - Technician
3 - Sub
4 - Main 
5 - On Board 
6 - In Transit
7 - Returned Machines
"""
# NUS2
"""
0 - Empty
1 - Consignment Stock
3 - Technician
4 - Sub
5 - Main
6 - On Board
"""
if NUS_Version == "NUS3":
    for location in Location_list:
        if location[1] == 0:
            Empty.append(str(location[0]))
        elif location[1] == 1:
            Consignment_Stock.append(str(location[0]))
        elif location[1] == 2:
            Technician.append(str(location[0]))
        elif location[1] == 3:
            Sub.append(str(location[0]))
        elif location[1] == 4:
            Main.append(str(location[0]))
        elif location[1] == 5:
            On_Board.append(str(location[0]))
        elif location[1] == 6:
            In_Transit.append(str(location[0]))
        elif location[1] == 7:
            Returned_Machines.append(str(location[0]))
        else:
            print("Not Supported Locaton Type")
elif NUS_Version == "NUS2":
    for location in Location_list:
        if location[2] == 0:
            if location[1] == 0:
                Empty.append(str(location[0]))
            elif location[1] == 1:
                Consignment_Stock.append(str(location[0]))
            elif location[1] == 3:
                Technician.append(str(location[0]))
            elif location[1] == 4:
                Sub.append(str(location[0]))
            elif location[1] == 5:
                Main.append(str(location[0]))
            elif location[1] == 6:
                On_Board.append(str(location[0]))
            else:
                print("Not Supported Locaton Type")
        else:
            In_Transit.append(str(location[0]))
else:
    pass

# Combine all types together
for Location_first in Location_list_all:
    for Location_second in Location_list_all:
        Location_first = str(Location_first).rstrip("\n")
        Location_second = str(Location_second).rstrip("\n")
        if (Location_first == Location_second) or (Location_first in In_Transit) or (Location_second in In_Transit):
            continue
        else:
            # Data Format
            if (Location_first in Empty) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Empty) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Empty) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Empty) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Empty) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Empty) and (Location_second in On_Board):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Empty) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")
            
            elif (Location_first in Consignment_Stock) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Consignment_Stock):
                continue
            elif (Location_first in Consignment_Stock) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in On_Board):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")

            elif (Location_first in Technician) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Technician) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Technician) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Technician) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Technician) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Technician) and (Location_second in On_Board):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Technician) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")

            elif (Location_first in Sub) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Sub) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Sub) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Sub) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Sub) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Sub) and (Location_second in On_Board):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Sub) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")

            elif (Location_first in Main) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Main) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Main) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Main) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Main) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Main) and (Location_second in On_Board):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Main) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")

            elif (Location_first in On_Board) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in On_Board) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in On_Board) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in On_Board) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in On_Board) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in On_Board) and (Location_second in On_Board):
                continue
            elif (Location_first in On_Board) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")

            elif (Location_first in Returned_Machines) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Sub):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in On_Board):
                result = str(Location_first+";"+Location_second+";;;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";;;;\n")
            else:
                result = str(Location_first+";"+Location_second+";TRANSFER\n")
            output.write(result)

output.close()