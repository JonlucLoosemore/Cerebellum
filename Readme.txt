CEREVELLUM - VERSION 0.2

Introduction
Cerevellum is an AI-driven project that utilizes GPT-J, an advanced language model, to perform various tasks. This version, 0.2, includes initial functionalities and setup guidelines.

Installation Instructions
1. Install Python
Download and Run the Installer:
Download the Python installer compatible with your operating system from python.org.
Double-click the installer to run it.
During installation, ensure to select the option "Add Python X.X to PATH" to add Python to your system's PATH environment variable for easy command-line access.
Click "Install Now" to initiate the installation process.

2. Install Required Python Modules
Install from PIP the modules needed to run the script. If not installed the scripts will fail with error "No Module Named XXX " 

3. Configuration Setup
Update the Configurations (if necessary):

Edit the config.txt file if you need to modify any settings. As of Version 0.2, not all variables are currently utilized in the scripts.
Update Config File Location in model.py:

Navigate to model.py and update the location of the configuration file.
Find Line 36 and modify the path in config.read('location of full path to config.txt') to the full path of your config.txt file. Use double backslashes (\\) for the path (e.g., config.read('C:\\Users\\name\\Cerebellum\\config.txt')).

Note for First-Time Run
The base model requires an initial download of approximately 24GB when running for the first time.