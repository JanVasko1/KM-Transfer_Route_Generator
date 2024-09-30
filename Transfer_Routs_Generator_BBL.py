import pandas
import pyodbc

def update_string(inset_value):
    try:
        inset_value = str(inset_value).replace(" ", "_")
        return inset_value
    except:
        return inset_value

def Location_Country(Location_first, Location_second, Location_df, In_Transit_Code):
    Location_first_Country_Series = Location_df[(Location_df["Location"] == Location_first)]
    Location_first_Country = Location_first_Country_Series.iloc[0]["Country"]
    Location_second_Country_Series = Location_df[(Location_df["Location"] == Location_second)]
    Location_second_Country = Location_second_Country_Series.iloc[0]["Country"]

    if Location_first_Country == "" or Location_second_Country == "":
        result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;;;;;\n")
    else:
        if Location_first_Country == Location_second_Country:
            result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;;;;;\n")
        else:
            result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
    return str(result)

#--------------------------------------------------------------------Downloader--------------------------------------------------------------------#
Data_NOC = "BBL"
NUS_Version = "NUS3"
Data_System = ""
while Data_System != "QA" and Data_System != "PRD":
    Data_System = update_string(input("Which DB you want to select as data source? [QA/PRD]: "))

# Database connection preparation
if Data_System == "QA":
    server = 'kmnavqdbs03.bs.kme.intern'
else:
    server = 'kmnavpdbs03.bs.kme.intern'

# Database connection
database = update_string(Data_NOC+Data_System)
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
cursor.execute(f'SELECT [Code],[Location Type],[Country_Region Code] FROM [{database}].[{dabase_schama}].[{Company}$Location]')
for row in cursor.fetchall():
    Location_list.append(row)

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
Location_list_all = []
Location_Type_all = []
Location_Country_all = []

for location in Location_list:
    Location_list_all.append(location[0])
    Location_Type_all.append(location[1])
    Location_Country_all.append(location[2])

Location_dict = {
    "Location": Location_list_all,
    "Type": Location_Type_all,
    "Country": Location_Country_all}
Location_df = pandas.DataFrame(data=Location_dict, columns=Location_dict.keys())
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

output = open(f"./Transfer_Rout_result_{update_string(Company)}", "wt", encoding="utf-8", errors='ignore')  

# Combine all types together
for Location_first in Location_list_all:
    for Location_second in Location_list_all:
        Location_first = str(Location_first).rstrip("\n")
        Location_second = str(Location_second).rstrip("\n")
        if (Location_first == Location_second) or (Location_first in In_Transit) or (Location_second in In_Transit):
            continue
        else:
            # Find Correct In Transit Code in Dataframe based on Transfer To Country
            mask1 = Location_df["Location"] == str(Location_second)
            Location_second_country_df = Location_df[mask1]
            Transfer_To_County = Location_second_country_df.iloc[0]["Country"]
            if Transfer_To_County == "LT":
                In_Transit_Code = "50TR"
            elif Transfer_To_County == "LV":
                In_Transit_Code = "5RTR"
            elif Transfer_To_County == "EE":
                In_Transit_Code = "5TTR"
            else:
                In_Transit_Code = ""

            # Trasnfer-From, Transfer-To, In-Transit code, Shipping Agent Code, Shipping Agent Service, Shipment Method, Transaction Type, Tans. Specification, Transport Method, Area
            # Empty
            if (Location_first in Empty) and (Location_second in Empty):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Empty) and (Location_second in Consignment_Stock):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Empty) and (Location_second in Technician):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Empty) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Empty) and (Location_second in Main):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Empty) and (Location_second in On_Board):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Empty) and (Location_second in Returned_Machines):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            
            # Consignemtn Stock
            elif (Location_first in Consignment_Stock) and (Location_second in Empty):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Consignment_Stock) and (Location_second in Consignment_Stock):
                continue
            elif (Location_first in Consignment_Stock) and (Location_second in Technician):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Consignment_Stock) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Consignment_Stock) and (Location_second in Main):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Consignment_Stock) and (Location_second in On_Board):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Consignment_Stock) and (Location_second in Returned_Machines):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)

            # Technician
            elif (Location_first in Technician) and (Location_second in Empty):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Technician) and (Location_second in Consignment_Stock):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Technician) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";OWN;PICKUP;;;;;\n")
            elif (Location_first in Technician) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";OWN;PUTIN;;;;;\n")
            elif (Location_first in Technician) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";OWN;PUTIN;;;;;\n")
            elif (Location_first in Technician) and (Location_second in On_Board):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Technician) and (Location_second in Returned_Machines):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)

            # Sub
            elif (Location_first in Sub) and (Location_second in Empty):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Sub) and (Location_second in Consignment_Stock):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Sub) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";OWN;PICKUP;;;;;\n")
            elif (Location_first in Sub) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Sub) and (Location_second in Main):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Sub) and (Location_second in On_Board):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Sub) and (Location_second in Returned_Machines):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)

            # Main
            elif (Location_first in Main) and (Location_second in Empty):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Main) and (Location_second in Consignment_Stock):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Main) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";VENIPAK;STANDARD;;;;;\n")
            elif (Location_first in Main) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";VENIPAK;STANDARD;;;;;\n")
            elif (Location_first in Main) and (Location_second in Main):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Main) and (Location_second in On_Board):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Main) and (Location_second in Returned_Machines):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)

            # OnBoard
            elif (Location_first in On_Board) and (Location_second in Empty):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
            elif (Location_first in On_Board) and (Location_second in Consignment_Stock):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
            elif (Location_first in On_Board) and (Location_second in Technician):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
            elif (Location_first in On_Board) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in On_Board) and (Location_second in Main):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
            elif (Location_first in On_Board) and (Location_second in On_Board):
                continue
            elif (Location_first in On_Board) and (Location_second in Returned_Machines):
                result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")

            # Return Machine
            elif (Location_first in Returned_Machines) and (Location_second in Empty):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Returned_Machines) and (Location_second in Consignment_Stock):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Returned_Machines) and (Location_second in Technician):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Returned_Machines) and (Location_second in Sub):
                if Location_second == "5RDD" or Location_second == "5TDD":
                    result = str(Location_first+";"+Location_second+";"+In_Transit_Code+";;;DAP;99;DAP;3;\n")
                else:
                    result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Returned_Machines) and (Location_second in Main):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Returned_Machines) and (Location_second in On_Board):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            elif (Location_first in Returned_Machines) and (Location_second in Returned_Machines):
                result = Location_Country(Location_first, Location_second, Location_df, In_Transit_Code)
            else:
                result = str(Location_first+";"+Location_second+";TRANSFER\n")
            output.write(result)

output.close()


Transfer_routes_df = pandas.read_csv(filepath_or_buffer=f"./Transfer_Rout_result_{update_string(Company)}", sep=";", encoding="utf_8", names=["From_Location","To_Location","In_Transit","Shipment Methond","Shipping Agent","Shipping Agent Service","Transaction Type","Trans. Specification","Transport Method","Area"])
for row in Transfer_routes_df.iterrows():
    row_df = pandas.Series(data=row[1])

    # From Location
    From_Location_Mask1 = Location_df["Location"] == row_df["From_Location"]
    From_Location_Country_Series = Location_df[From_Location_Mask1]
    From_Location_Country = From_Location_Country_Series.iloc[0]["Country"]

    # To Location
    To_Location_Mask1 = Location_df["Location"] == row_df["To_Location"]
    To_Location_Country_Series = Location_df[To_Location_Mask1]
    To_Location_Country = To_Location_Country_Series.iloc[0]["Country"]

    #Example of 
    if (From_Location_Country == "LT") and ((To_Location_Country == "LV") or (To_Location_Country == "EE")):
        Transfer_routes_df.at[row[0],"Transaction Type"] = "99"
        Transfer_routes_df.at[row[0],"Trans. Specification"] = "DAP"
        Transfer_routes_df.at[row[0],"Transport Method"] = "3"
    else:
        pass

Transfer_routes_df.to_csv(path_or_buf=f"./Transfer_Rout_result_{update_string(Company)}", sep=";", index=False, header=False)
