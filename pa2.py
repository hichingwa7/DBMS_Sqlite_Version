# date: 3/10/2020
# developer: Humphrey Shikoli
# programming language: Python
# description: program that allows a database user to insert, delete, modify, and query their
# data on basic tables (i.e., no table joins). It is assumed that the database and table structures, that is,
# their metadata, are available

import os 
import csv

f_commands = ['create', 'drop', 'alter', 'use', 'select', 'insert', 'update', 'delete'] # a list of functions used in this program
w_loop = True
current_db = "NOT SELECTED"

def sqlStatements():
    user_input = ""
    while w_loop:  
        try:
            input_raw = input("")
        except EOFError:
            break
        input_raw = user_input + " " + input_raw.lower()
        user_input = input_raw.strip().split()
        user_input = " ".join(user_input)      
        if len(user_input) == 0:
            user_input = ""
            continue      
        elif user_input.strip()[:2] == "--": # removing the hyphen signs in the test file
            user_input = ""
            continue      
        elif user_input.lower() == ".exit": # input query for exiting the program
            break       
        elif user_input[-1] == ";":
            user_input = user_input[:-1] # remove the semicolon and store it in "user_input" variable
            user_input = user_input.lower().split(" ", 3) # input converted to lower-case and split each word by spaces     
            if user_input[0] == f_commands[0]: # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                create(user_input) # calling create function
            elif user_input[0] == f_commands[1]: # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                drop(user_input) # calling drop function               
            elif user_input[0] == f_commands[2] and user_input[1] == "table": # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                alter(user_input[2:]) # calling alter function               
            elif user_input[0] == f_commands[3]: # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                use(user_input) # calling use function               
            elif user_input[0] == f_commands[4]:  # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                select(' '.join(user_input[1:])) # calling select function               
            elif user_input[0] == f_commands[5] and user_input[1] == "into":
                insert(user_input[2], user_input[3])               
            elif user_input[0] == f_commands[6]:
                print()
                update(user_input[1], user_input[2], user_input[3])               
            elif user_input[0] == f_commands[7] and user_input[1] == "from":
                print()
                delete(user_input[2], user_input[3])           
            else:
                print("invalid command") # for an input that is invalid
            user_input = ""         

def create(user_input):
    # function creates a database and table by passing the query as an argument
    if(len(user_input) == 3):
        if(user_input[1] == "database"): # check for the word 'database' in the query
            if not os.path.exists(user_input[2]): # check if the database or directory exists
                os.makedirs(user_input[2]) # create a new directory
                print("Database",user_input[2],"created.")
            else:           
                print("!Failed to create database",user_input[2],"because it already exists.")
    elif(len(user_input) < 3):  # checking if the number of words in the query is less than 3
        print("wrong statement")
    elif(user_input[1] == "table" and len(user_input) > 3): # check for the word 'table' in the query
        if os.path.exists(current_db): # check if the database or directory exists
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'): # check if the table exists
                print("!Failed to create table",user_input[2],"because it already exists.")
            else:
                file = open(current_db+'/'+user_input[2]+".csv", 'w') # create new table
                parseStringForColumnNames(user_input[3], file) # calling function for naming the columns
                print("Table",user_input[2],"created.")
                file.close()                                            
        else:
            print("Valid database is not selected.") # if existing database is not selected
    else:
        print('')      

def drop(user_input):
# function drops a database and table by passing the query as an argument
    if(len(user_input) == 3):
        if(user_input[1] == "database"): # check for the word 'database' in the query
            if os.path.exists(user_input[2]): # check if the database or directory exists
                os.removedirs(user_input[2]) # removing the database
                print("Database",user_input[2],"deleted.")
            else:
                print("!Failed to delete",user_input[2],"because it does not exist.")
        elif user_input[1] == 'table': # check for the word 'table' in the query
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'): # check if the table exists in a database
                os.remove(current_db+'/'+user_input[2]+'.csv') # removing the table
                print("Table",user_input[2],"deleted.")
            else:
                print("!Failed to delete",user_input[2] ,"because it does not exist.")
    elif(len(user_input) < 3): # check if the count of words in the query is less than 3
        print("wrong statement.")
    else:
        print('')

def use(user_input):
    # function definition for selecting a database
    if len(user_input) == 2: # checking if the count of words for the query is 2
        global current_db
        current_db = user_input[1]
        if os.path.exists(user_input[1]): # check if the database or directory exists
            print("Using database",user_input[1],'.')
        else:
            print("Database not available.")
    elif(len(user_input) < 2): # checking if the count of words for the query is less than 2
        print("wrong statement")

def select(user_input):
    # function for selecting columns and rows in a table
    before_from_after = user_input.partition('from')
    select_params = before_from_after[0].split(',')
    if(current_db != 'NOT SELECTED.'):
        if(select_params[0].strip() == '*'):
            if os.path.isfile(current_db+'/'+before_from_after[2].strip()+'.csv'): # check if the file or table exists in the database
                file = open(current_db+'/'+before_from_after[2].strip()+'.csv', 'r')
                for row in file: # iterate each row in the file
                    row = row.strip().replace("\n","")
                    print(row.replace(',', ' | ')) # replaces ',' with ' | '
                file.close()
            else:
                print('!Failed to query table',user_input[2],'because it does not exist.')
        else:
            where_col_ind = []
            where_col_names = []
            where_ops = []
            where_vals = []
            select_col_ind = []
            before_where_after = before_from_after[2].partition('where')
            table_name = before_where_after[0].strip()
            if os.path.isfile(current_db+'/'+table_name+'.csv'): # check if the file or table exists in the database.
                where_params = before_where_after[2].strip().split(' ')
                with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names:
                    reader = csv.reader(read_column_names)
                    columns = next(reader)
                column_names = getOnlyColumnNames(columns) # existing column names are retrieved and stored in a list
                for i in range(len(select_params)):                               
                    if select_params[i].strip() in column_names:
                        select_col_ind.append(column_names.index(select_params[i].strip()))
                    else:
                        print("select column name '",select_params[i],"' doesn't exist.")
                column_datatypes = getColumnDatatypes(columns)
                for word in where_params: # this for loop stores 'where' column names, operators and values in seperate lists
                    if where_params.index(word)%3 == 0:
                        where_col_names.append(word)
                        where_col_ind.append(column_names.index(word.strip()))
                    elif where_params.index(word)%3 == 1:
                        where_ops.append(word.strip())
                    else:
                        where_vals.append(word.strip())
                tot_vals_to_compare_count = 0
                for i in range(len(where_col_ind)):
                    if where_col_names[i] in column_names:
                        tot_vals_to_compare_count += 1
                if tot_vals_to_compare_count == len(where_col_ind):  
                    for i in range(len(select_col_ind)):
                        print(column_names[select_col_ind[i]],column_datatypes[select_col_ind[i]], end=" | ")
                    with open(current_db+'/'+table_name+'.csv', 'r') as read_rows: # this line opens a file with the referred table name in the query
                        next(read_rows) # skip first two rows
                        next(read_rows)
                        for row in read_rows: # iterates through each row 
                            row = row.strip().split(',') # row is split by ',' and stored in a list
                            for i in range(len(where_ops)):
                                if where_ops[i] == '!=': # checks for a '!=' in the query
                                    if row[where_col_ind[i]] not in where_vals: # checks if the query value doesn't match the row value
                                        print()
                                        for i in range(len(select_col_ind)):
                                            print(row[select_col_ind[i]], end=" | ") # prints if the query value doesn't match the row value
                                else:
                                    print("only != works for now.")
                        print()
            else:
                print("!Failed to query table",table_name,"because it does not exist.")
    else:
        print("Database not selected 'use database' statement).")

def alter(user_input):
    # function alters columns in a table
    if os.path.isfile(current_db+'/'+user_input[0]+'.csv'): # check if the file or table exists in a database
        alter_columns = user_input[1].split(' ',1) # get new column name from the query
        if (alter_columns[0] == 'add'): # checking if column should be added
            columns = []
            file = open(current_db+'/'+user_input[0]+'.csv', 'r')
            for row in file:                                
                columns = row.strip().split(',') # get and strip existing columns from the file or table and store in a list variable
                columns.append(alter_columns[1]) # append new column names to the list variable
                columns = ','.join(columns) # join all column names with ','
                file.close()                                                
                break
            with open(current_db+'/'+user_input[0]+'.csv', 'r') as f:        
                lines = f.readlines()                                               
                lines[0] = columns+'\n'                                     # Storing the new column names.
            with open(current_db+'/'+user_input[0]+'.csv', 'w') as f:
                f.writelines(lines)                                         # Writing columns to the file.
                print('Table',user_input[0],'modified.')
    else:
        print('Table does\'nt exist or database not selected.')
def insert(table_name, values):
    if os.path.isfile(current_db+'/'+table_name+'.csv'): # Checks if the table exists
        if values.startswith("values(") and values.endswith(")"):
            values = values[7:-1].split(',') # insertion values are stored in a list
            file = open(current_db+'/'+table_name+'.csv', 'a', newline='')
            for i in range(len(values)): # this for loop eliminates the quotes if present in the values (ex: 'SuperGizmo').
                word = values[i].strip()
                if word.startswith("'") and word.endswith("'"):
                    word = word.replace("'","")
                values[i] = word
                i += 1
            writeRowValues(values, file) # function is called for writing rows with arguments values in a list and opened file object
            file.close()    
        else:
            print("wrong syntax")
    else:
        print('Table doesn\'t exist.')
def update(table_name, set_word, remaining_words):
    column_in_database = True
    if os.path.isfile(current_db+'/'+table_name+'.csv'): # checks if a table or file exists
        update_values = {}
        with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names:  # opens up a table or file for getting column names
            reader = csv.reader(read_column_names)
            columns = next(reader)
        column_names = getOnlyColumnNames(columns)
        column_datatypes = getColumnDatatypes(columns)
        if set_word == 'set':  # checks if the set word is right after the table name
            before_where_after = remaining_words.partition('where')
            before_words = before_where_after[0].split('=') # get all the words before 'where' keyword
            for word in before_words: # this for loop stores the 'set' column names in list
                if before_words.index(word)/2 == 0: # checks if the column names are in the table or file column names
                    before_words[before_words.index(word)] = word.strip()
                    word = word.strip()
                    if word in column_names:
                        set_index = column_names.index(word)
                    else:
                        column_in_database = False
                        print("Entered set column not present in the database.")
                        break
                else:
                    before_words[before_words.index(word)] = word.strip()
                    word = word.strip()
                    if word.startswith("'") and word.endswith("'"):
                        word = word.replace("'","")
                    if ('varchar' in column_datatypes[set_index] or 
                        'char' in column_datatypes[set_index]):
                        if isinstance(word, str):
                            update_values[column_names[set_index]] = word
                        else:
                            print("______________")
                    elif ('float' in column_datatypes[set_index]):
                        if isinstance(word, str):
                            update_values[column_names[set_index]] = word
                        else:
                            print("not string datatype.")
            if bool(update_values):                                                
                after_words = before_where_after[2].split('=')
                for word in after_words: # store each 'where' column names and values in separate lists
                    if after_words.index(word)/2 == 0:
                        after_words[after_words.index(word)] = word.strip()
                        word = word.strip()
                        if word in column_names:
                            where_index = column_names.index(word)
                        else:
                            column_in_database = False
                            print("Entered where column not present in the database.")
                    else:
                        after_words[after_words.index(word)] = word.strip()         
                        word = word.strip()
                        if word.startswith("'") and word.endswith("'"):
                            word = word.replace("'","")
                updateFile(table_name, update_values, set_index, word, column_names[set_index], where_index)    # function call to update file with the passed arguments
        else:
            print("Error in the set name")
    else:
        print('Table does\'nt exist or database not selected.')
def delete(table_name, contents):
    if os.path.isfile(current_db+'/'+table_name+'.csv'):
        with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names: # opens a file and gets column names
            reader = csv.reader(read_column_names)
            columns = next(reader)
        column_names = getOnlyColumnNames(columns)
        contents = contents.split(' ', 1)
        if contents[0].strip() == 'where':
            contents = contents[1].split(' ')
            delete_col_indexes = []
            delete_col_values = []
            delete_col_operators = []
            delete_col_dtypes = []
            for word in contents: # stores 'delete' column names, operators and values in seperate lists
                if contents.index(word)%3 == 0: # check if the mentioned column names in the query are present in the existing table or file column names
                    if word.strip() in column_names:
                        delete_col_indexes.append(column_names.index(word.strip()))
                        delete_col_dtypes.append(column_names.index(word.strip()))
                    else:
                        print('Entered column name(where) not present in the table.')
                        break
                elif contents.index(word) %3 == 1:
                    delete_col_operators.append(word.strip())
                else:
                    word = word.strip()
                    if word.startswith('"') and word.endswith('"'):
                        word = word.replace('"',"")
                    delete_col_values.append(word)
            deleteWriteRows(table_name, delete_col_indexes, delete_col_values, delete_col_dtypes, delete_col_operators)  # fuction is called with arguments as table name, delete column names, operators and values for deletion.
        else:
            print("Table '",table_name,"'doesn't exist.")

def parseStringForColumnNames(input_string, file):
# function parses column names from the input query
    columns = []
    if input_string.startswith("(") and input_string.endswith(")"): # checking for open and close brackets.
        for column in input_string[1:-1].split(','): # cxclude "(" & ")" and splitting at "," for column names.
            column = column.strip()                                     
            columns.append(column) # appending column names to the list variable
        writer = csv.writer(file)
        writer.writerow(columns)
    else:
        print('error in open or close brackets.')
        
def writeRowValues(values, file):
    writer = csv.writer(file)
    writer.writerow(values)
    print('1 new record inserted.')
    
def getOnlyColumnNames(columns):
    names = []
    for i in range(len(columns)):
        single_column_name = columns[i].rsplit(' ',1)
        names.append(single_column_name[0]);
    return names
def getColumnDatatypes(columns):
    
    names = []
    for i in range(len(columns)):
        single_column_name = columns[i].rsplit(' ',1)
        names.append(single_column_name[1]);
    return names

def updateFile(table_name, update_values, set_index, word, column_name, where_index):   
# function replaces values stored in update_values list by comparing values stored in word with each row in a table
    count = 0;                                                                              
    with open(current_db+'/'+table_name+'.csv', 'r') as rf:
        lines = rf.readlines()
    for i in range(len(lines)):
        values = lines[i].strip().split(',')
        if values: # checking if list is not empty
            if word in values:
                values[set_index] = update_values[column_name]
                count += 1
                for w in values:
                    lines[i] = ",".join(values)+"\n"
        else:
            print('line empty')
    with open(current_db+'/'+table_name+'.csv', 'w') as wf:
        wf.writelines(lines)
        if count == 1:
            print(count,'record modified.')
        elif count > 1:
            print(count,'records modified.')
            
def deleteWriteRows(table_name, col_indexes, change_values, delete_col_dtypes, operators):   
# function deletes a row if present and adjusts empty lines if present after deletion
    found = False 
    records_modified = 0;
    with open(current_db+'/'+table_name+'.csv', 'r') as rf:
        lines = rf.readlines()
    for i in range(len(lines)):
        found_int = 0
        values = lines[i].strip().split(',')
        if i > 0 and values:
            for j in range(len(col_indexes)):
                value = change_values[j]
                if value.startswith('\'') and value.endswith('\''):
                    value = value.replace('\'', "")
                if(operators[j] == '='):
                    if values[col_indexes[j]] == value:
                        found_int += 1
                        records_modified += 1
                elif(operators[j] == '>'):
                    if float(values[col_indexes[j]]) > float(change_values[j]):
                        found_int += 1
                        records_modified += 1
            if found:
                lines[i-1] = ",".join(values)+"\n"
                lines[i] = ""
                found = False
            if found_int == len(change_values):
                found = True
                if(i == len(lines) - 1):
                    lines[i] = ""
                i = i-1
    with open(current_db+'/'+table_name+'.csv', 'w') as wf:
        wf.writelines(lines)
        print(records_modified,'records deleted.')
sqlStatements()
print('All done.')