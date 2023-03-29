# CZ4031-DBMS-Group-37
Project repository for CZ4031 Database System Design

# Members
> Ng Chi Hui <br>
> Goh Shan Ying <br>
> Malcolm Tan Wei Zhang <br>
> Shannen Lee Xuan Ning<br>


# Running the code


## Prerequisites
You can create a virtual environment to make running of the code easier

1. Create a virtual environment

For Mac Users:
Create a new virtual environment
```
python3 -m venv myenv
```
2. Activate your virtual environment
```
source myenv/bin/activate
```
<br><br>
For Windows user
1. Create a virtual environment
```
python -m venv myenv
```
2. Activate your virtual environment

```
myenv\Scripts\activate
```

2. Install the modules required to run the code
```
pip install -r requirements.txt
```

3. Create a `config.json` file like below and place it in same directory as `preprocecssing.py` 

**Database Connection Settings**
Set your database connection parameter in the `config.py` file. 
  ```json
  {
    "host": "localhost",
    "port": "5432",
    "database": "your db name",
    "user": "postgres",
    "password": "your password" 	
  }
  ```

*** pushing the config file for now will be adding to git ignore later on

3. Run the project 
```
python project.py
```
