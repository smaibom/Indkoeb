Program for importing hospital specific formated purchase data. Program is written in python 3.10 and file to import nececarry libraries is included in importlibs.ps1

A userguide is found under the word document "Userguide"

The program can import singular or crawl though a directory and attempt to parse any xlsx files or csv files currently. The program requires 2 excel files found in the 
StaticData Folder. The filepath the program loads to these files are found in the constants file under src. Each file must contain a sheet named after the source denoted in the parser static config file explained below
The hospital data file contains 2 columns in each sheet.
    Original : The Identifier found for the source to identify a hospital, can be a number or just a full name
    Translated : The Translated value for the hospital that will show in the parsed sheet values

The category data file contains 3 columns in each sheet. 
    ID : What the source uses to identify each item
    Råvarekategori : Category of the item
    Råvare : Sub category of the category of the item

Parsers uses the Import_Class as its super class. They require a dictionary of static variables found in the constant folder which is indexes 
for where various data is located in columns and the source, also contains the name of the source to be used for the 2 excel files.
Each parser has 2 main functions to call, "load_data" Which will attempt to load in a sheet of a file, if the sheet furfills the criteria of the parser it
stores the data from the sheet in a dataframe in the class and returns the length of data imported. Second is parse_line which will parse the line of a given index 
and return the values to translated form in an array of arrays. Where the sub array is all the column values to the final translated product

Future works:
Move static data from excel files to a database
Interface with more options, ability to look at individual sheets data