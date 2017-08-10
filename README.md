# Account_Password_Manager
A python GUI for managing your accounts and passwords.

As a result that tha database only save encrypted accounts and passwords, the security for the saving data are guaranteed.

## Requirements
To use this GUI, one has to install **python 2** program as well as **PyQt4** and **Crypto** libraries that is compatible with your python version. An easy way for doing this is to install the Anaconda package. An example for the procedures would be the following: 

1. Download and install Anaconda package by following the instructions in [Anaconda's web site](https://docs.continuum.io/anaconda/install). 

2. Open terminal (or cmd if you use windows) and type `conda install pyqt=4.11.4` (you may need to type `sudo conda install pyqt=4.11.4` for linux based OS). 

3. Same procedure as 2., but use `conda install crypto` to install Crypto library. 

Finally, one can start the GUI by `python ac_pw_manager.py`.

## Usage
### Add a set of account and password for a particular service

1. Fill the **Magic Number** field with a secret code defined and remembered by yourself. 
2. Fill the **Service** field for indicating what is this set of account and password for.
3. Fill the account (or its hint) in the **AC or its hint** field.
4. Fill the password (or its hint) in the **PW or its hint** field.
5. Press **Add** button to add data into database (appear as **database.txt** in the same directory).

### Look up the account and password for a particular service

First way:
1. Fill the **Magic Number** field with the secret code that you used while saving the corresponding data into the database.
2. Fill the service you wnat to look up in the **Service** field (have to match the one you input).
3. Press **Find** button to check the account and password of the service.

Second way:
1. Fill the **Magic Number** field with the secret code that you used while saving the corresponding data into the database.
2. Press **Display** button and check the services saved in the database from the poped window. 
3. Click the service you want to look up in the poped window.
4. Press **Find** button to check the account and password of the service.


### Remove the account and password for a particular service

First way:
1. Fill the name of service you wnat to look up in the **Service** field (have to match the one you input).
2. Press **Remove** button to remove the data for the corresponding service.

Second way:
1. Press **Display** button and check the services saved in the database from the poped window. 
2. Click the service you want to remove in the poped window.
3. Press **Remove** button to remove the data for the corresponding service.
