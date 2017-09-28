# Account_Password_Manager
A python GUI for managing your accounts and passwords.

As a result that tha database only store encrypted accounts and passwords, the security of the database are guaranteed.

## Requirements
To use this GUI, one has to install **python 2** program as well as **PyQt4** and **Crypto** libraries that is compatible with your python version. An easy way for doing this is to install the Anaconda package with the following procedures: 

1. Download and install Anaconda package by following the instructions in [Anaconda's web site](https://docs.continuum.io/anaconda/install). 

2. Open terminal (or cmd if you use windows) and type `conda install pyqt=4.11.4` (you may need to type `sudo conda install pyqt=4.11.4` for linux based OS). 

3. Same procedure as 2., but use `conda install crypto` to install Crypto library.

If 2. is failed or you have anaconda with python3 installed, it is strongly recommended to use the [virtual environment](https://docs.continuum.io/anaconda/install) for the installation. To create a virtual environment, for example of name "myenv", with python2 and pyqt4 installed, one can use `conda create -n myenv python=2 pyqt=4`. Then, use `activate myenv`(windows) or `source activate myenv`(linux based OS) to enter the environment myenv. As long as you have entered myenv, you just need to do 3. and everything should work nicely.


Before using the GUI, one has to do one more step for setting the icon files. This can be done by `pyrcc4 -o icons.py icons.qrc`.

Finally, one can start the GUI by `python account_password_manager.py`.


## Usage
### Add a set of account and password for a particular service into database

1. Fill the **Magic Number** field with a secret code defined and remembered by yourself. 
2. Fill the **Service** field for indicating what is this set of account and password for.
3. Fill the account in the **AC or its hint** field.
4. Fill the password in the **PW or its hint** field.
5. Press **Add** button to add data into database shown in the right dock-widget.

### Look up the account and password for a particular service from the database

1. Fill the **Magic Number** field with the secret code that you used while saving the corresponding data into the database.
2. Fill the service field by either typing or clicking the service shown in the right dock-widget.
3. Press **Find** button to find the account and password of the service(you get garbles if the magic-number does not match the one while saving).


### Remove the account and password for a particular service in the database

1. Fill the service field by either typing or clicking the service shown in the right dock-widget.
2. Press **Remove** button to remove the data for the corresponding service.


### Save the database

1. Save to the current databse: Press **File** -> **Save** or the corresponding icon in the toolbar.
2. Save as a new database: Press **File** -> **Save As** or the corresponding icon in the toolbar.
### Open the database

1. Open an existing databse: Press **File** -> **Open** or the corresponding icon in the toolbar.
2. Open an empty database: Press **File** -> **New** or the corresponding icon in the toolbar.



