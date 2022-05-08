# EGM722 Assignment
## 1. Getting started
Conda and Git must be installed first. The instructions for installing Git can be found in https://git-scm.com/downloads (Github 2022), and Anaconda installation on this link https://docs.anaconda.com/anaconda/install/.

## 2. Download/clone the repository
Once Conda and Git installed, the repository should be cloned to the user’s local machine by following the below method:
In GitHub Desktop, select File > Clone Repository. Select the URL tab, then enter the URL for this report’s repository https://github.com/Waddahismail/EGM722_Assignment , and the local repository path in the local machine must be specified. Alternatively, you can execute the following command from Git Bash on the start menu: git clone https://github.com/Waddahismail/EGM722_Assignment, you need to open the directory where the file will be saved first using the command cd, for example cd documents will open the documents folder. 
Once the Github directory is cloned, all sample data, script, and environments will be downloaded to the local machine.
 

## 3. Create a conda environment
Once the repository is successfully cloned, you can then create a Conda environment using the environment.yml file provided in the repository. This can be done by  selecting Import from the bottom of the Environments panel in Anaconda Navigator (https://docs.anaconda.com/anaconda/navigator/index.html).

## 4. Installing PyCharm (optional)
The script does not require any changes by the user, I recommend using PyCharm to run the script, the installation guide can be found in this link https://www.jetbrains.com/pycharm/download/#section=windows, make sure to download the Community edition.
All the required packages to run the script are included in the environment.yml file, but you can install them manually within PyCharm by following the instruction on this link https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#packages-tool-window

## 5. Troubleshooting
The user can change the data_path variable to the location where the shapefiles are saved, sample data for the project can be found on the Github directory “github.com/Waddahismail/WGM722_assignment”.
Properties sample data projected to UTM zone 37 is provided in the sample data folder, this is for the user to test the projection step in the code, the user can point the properties layer to this feature instead, to check if the statement will execute correctly.
If the user requires to replicate or use their own data for similar project, “land_id” and “station” fields in the properties feature must be numeric fields. “road_type” field in Roads feature is a text field to identify the type/category of each road.
A user input is required for compensation and buffer values, this cannot be blank otherwise the script will produce an error message, if the value is zero, then the user must input “0”.

