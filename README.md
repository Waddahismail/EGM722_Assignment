# EGM722 Assignment
## 1. Getting started
You'll need to install both git and conda on your computer. You can follow the instructions for installing git from https://git-scm.com/downloads, and Anaconda from https://docs.anaconda.com/anaconda/install/.

## 2. Download/clone the repository
Once you have these installed, clone this repository to your computer by doing one of the following things:

Open GitHub Desktop and select File > Clone Repository. Select the URL tab, then enter the URL for this repository.
Open Git Bash (from the Start menu), then navigate to your folder. Now, execute the following command: git clone https://github.com/Waddahismail/EGM722_Assignment. You should see some messages about downloading/unpacking files, and the repository should be set up.
You can also clone this repository by clicking the green "clone or download" button above, and select "download ZIP" at the bottom of the menu. Once it's downloaded, unzip the file and move on to the next step. Once you clone the github directory, you should have all the sample data downloaded to your computer. 

## 3. Create a conda environment
Once you have successfully cloned the repository, you can then create a conda environment.

To do this, use the environment.yml file provided in the repository. If you have Anaconda Navigator installed, you can do this by selecting Import from the bottom of the Environments panel.

Otherwise, you can open a command prompt (on Windows, you may need to select an Anaconda command prompt). Navigate to the folder where you cloned this repository and run the following command:

C:\Users\(your machine user name)> conda env create -f environment.yml
This will probably take some time.

## 4. Installing PyCharm (optional)
The script does not require any changes by the user, I recommend using PyCharm to run the script, the installation guide can be found in this link https://www.jetbrains.com/pycharm/download/#section=windows, make sure to download the Community edition.
All the required packages to run the script are included in the environment.yml file, but you can install them manually within PyCharm by following the instruction on this link https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#packages-tool-window
## 5. Troubleshooting
The user can change the data_path variable to the location where the shapefiles are saved, sample data for the project can be found on the Github directory “github.com/Waddahismail/WGM722_assignment”.
If the user requires to replicate or use their own data for similar project, “land_id” and “station” fields in the properties feature must be numeric fields. “road_type” field in Roads feature is a text field to identify the type/category of each road.
A user input is required for compensation and buffer values, this cannot be blank otherwise the cript will produce an error message, if the value is zero, then the user must input “0”.

