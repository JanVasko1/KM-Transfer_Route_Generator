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
output = open(f"{File_path}/BRO_2nd_wave.csv", "wt", encoding="utf-8", errors='ignore')  

Location_list_all = []
Empty = ["5110", "5120", "5130", "5140", "5160", "5170", "5180", "5190", "51C0", "51D0", "51E0", "51H0", "51K0", "51M0", "51R0", "51S0", "51U0", "51V0", "5310", "5330", "5430", "5440", "5480", "54E0", "5510", "5550", "5570", "5590", "55M0", "5630", "5670", "5680", "5690", "56B0", "5710", "5730", "5790", "57C0", "5830", "5860", "5890", "5970", "5MA0", "5150", "5A50", "5C10", "5C30", "5C40"]
Technician = ["T5200", "T5210", "T5220", "T5230", "T5240", "T5250", "T5260", "T5280", "T5290", "T52B0", "T52C0", "T52D0", "T52E0", "T52F0", "T52H0", "T52K0", "T52M0", "T52N0", "T52P0", "T52R0", "T52T0", "T52U0", "T52V0", "T52X0", "T5320", "T5340", "T5380", "T5410", "T5420", "T5450", "T5490", "T5520", "T5540", "T5560", "T5580", "T55C0", "T55E0", "T55F0", "T55G0", "T55H0", "T55K0", "T55N0", "T55P0", "T55S0", "T5610", "T5620", "T5640", "T5650", "T5660", "T56A0", "T5720", "T5750", "T5760", "T5780", "T57B0", "T57D0", "T5810", "T5820", "T5840", "T5850", "T5870", "T5880", "T5920", "T5930", "T5950"]
Sub = ["5020", "5030", "5040", "5050", "5060", "5070", "5080", "5090", "50A0", "5300", "5400", "5500", "5600", "5700", "5800", "5900", "5C50", "5D00"]
Main = ["5000", "5010", "5A20"]
Consignment_Stock = ["MT_DDL"]
On_Board = ["ON-BOARD"]
In_Transit = ["IN-TRANSIT"]
Returned_Machines = []


Location_list_all.extend(Empty)
Location_list_all.extend(Consignment_Stock)
Location_list_all.extend(Technician)
Location_list_all.extend(Sub)
Location_list_all.extend(Main)
Location_list_all.extend(On_Board)
Location_list_all.extend(In_Transit)
Location_list_all.extend(Returned_Machines)

#--------------------------------------------------------------------Prepare Transfer Rout Import--------------------------------------------------------------------#
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
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Empty) and (Location_second in Consignment_Stock):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Empty) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in Empty) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Empty) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Empty) and (Location_second in On_Board):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Empty) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            
            elif (Location_first in Consignment_Stock) and (Location_second in Empty):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Consignment_Stock):
                continue
            elif (Location_first in Consignment_Stock) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in On_Board):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Consignment_Stock) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")

            elif (Location_first in Technician) and (Location_second in Empty):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PUTIN;\n")
            elif (Location_first in Technician) and (Location_second in Consignment_Stock):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PUTIN;\n")
            elif (Location_first in Technician) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in Technician) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PUTIN;\n")
            elif (Location_first in Technician) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PUTIN;\n")
            elif (Location_first in Technician) and (Location_second in On_Board):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PUTIN;\n")
            elif (Location_first in Technician) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PUTIN;\n")

            elif (Location_first in Sub) and (Location_second in Empty):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Sub) and (Location_second in Consignment_Stock):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Sub) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in Sub) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Sub) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Sub) and (Location_second in On_Board):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Sub) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")

            elif (Location_first in Main) and (Location_second in Empty):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Main) and (Location_second in Consignment_Stock):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Main) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in Main) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Main) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Main) and (Location_second in On_Board):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Main) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")

            elif (Location_first in On_Board) and (Location_second in Empty):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in On_Board) and (Location_second in Consignment_Stock):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in On_Board) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in On_Board) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in On_Board) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in On_Board) and (Location_second in On_Board):
                continue
            elif (Location_first in On_Board) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")

            elif (Location_first in Returned_Machines) and (Location_second in Empty):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Consignment_Stock):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Technician):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};OWN;PICKUP;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Sub):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Main):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in On_Board):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            elif (Location_first in Returned_Machines) and (Location_second in Returned_Machines):
                result = str(f"{Location_first};{Location_second};{In_Transit[0]};;;\n")
            else:
                result = str(Location_first+";"+Location_second+";TRANSFER\n")
            output.write(result)

output.close()