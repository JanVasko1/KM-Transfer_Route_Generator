# Transfer Rout Setup
This program was developed because of an need to create Transfer Routs during migration phase of implementation project.

# Setup
### <span style="color:blue;">Installation</span>
1. Install [Python 3.11.2](https://www.python.org/downloads/release/python-3112/) - recomended or higher
    - install it as "Run as Administrator"
    - on pop-up page mark "Add Python to PATH" and unmark "Instal launcher for all users" (if possible)
2. Run `Installation_libs.ps1` code (reflect correct path to your python installation)
3. Update `HQ_Data_Generator.bat` to reflect correct path to your python installation

# Operation
### <span style="color:blue;">Process</span></span>
![Process](https://github.com/JanVasko1/KM-Transfer_Route_Generator/blob/master/Lib/Readme/HQ_Test_Examples_Generator_Map.png?raw=true
 "Overal process")

- red --> manual steps
- green --> automatic steps

### <span style="color:blue;">Dowloader</span>
- there is an need to select
    1. NOC 
    2. Company
    --> as these entity fully describe pure data source
- downloads all Locations Codes and Location type to enable logic inside

### <span style="color:blue;">Read .csv files</span>
- addtional infromation which cannot be downloaded from NAV are maintained in .csv files [Link](https://github.com/JanVasko1/KM-Transfer_Route_Generator/tree/master/Lib/Defaults)
    1. Shipping Agent
    2. Shipping Agent Services
    3. Shipment Methods

### <span style="color:blue;">Main function</span>
- creates and full combination of all location and map it according to .csv files 

### <span style="color:blue;">Export</span>
- program will exports data to .csv file and prints it