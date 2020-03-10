# date: 2/20/2020
# developer: Humphrey Shikoli
# programming language: Python
# description: program that allows a database user to manage the metadata of
# their relational data. Metadata here refers to the database's own information
# and the properties of the tables

import os 
import csv

f_commands = ['create', 'drop', 'alter', 'use', 'select'] # a list of functions used in this program
w_loop = True
current_db = 'NOT SELECTED.'

def sqlStatements():
    while w_loop:
        try:
            user_input = input()              
            if(user_input.lower() == '.exit'): # input query for exiting the program
                print('All done.')
                break
            elif(user_input.startswith('--')): # removing the hyphen signs in the test file
                continue
            elif(not user_input.strip()): # escapes blank line from the input
                continue
            elif(user_input[-1] == ';'):
                user_input = user_input[:-1] # remove the semicolon and store it in "user_input" variable
                user_input = user_input.lower().split(' ', 3) # input converted to lower-case and split each word by spaces
                if(user_input[0] == f_commands[0]): # crosscheck the first word of input with the contents of the "f_commands list"
                    create(user_input)              
                elif(user_input[0] == f_commands[1]): # crosscheck the first word of input with the contents of the "f_commands list"
                    drop(user_input)
                elif(user_input[0] == f_commands[2] and user_input[1] == 'table'): # crosscheck the first word of input with the contents of the "f_commands list"
                    alter(user_input[2:])
                elif(user_input[0] == f_commands[3]):  # crosscheck the first word of input with the contents of the "f_commands list"
                    use(user_input)
                elif(user_input[0] == f_commands[4]):  # crosscheck the first word of input with the contents of the "f_commands list"
                    select(user_input[1:])
                else:
                    print('invalid command.')
            else:
                print('missing semicolon.') #if semicolon is missing in the sql statement                
        except(EOFError): # program exits after output is displayed
            break

def create(user_input):
    # function creates a database and table by passing the query as an argument
    if(len(user_input) == 3):
        if(user_input[1] == 'database'): # check for the word 'database' in the query
            if not os.path.exists(user_input[2]): # check if the database or directory exists
                os.makedirs(user_input[2]) # create a new directory
                print('Database',user_input[2],'created.')
            else:           
                print("!Failed to create database",user_input[2],"because it already exists.")
    elif(len(user_input) < 3): # checking if the count of words in the query is less than 3
        print("wrong statement.")
    elif(user_input[1] == 'table' and len(user_input) > 3): # check for the word 'table' in the query
        if os.path.exists(current_db): # check if the database or directory exists
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'): # check if the table exists
                print('!Failed to create table',user_input[2],'because it already exists.')
            else:
                file = open(current_db+'/'+user_input[2]+'.csv', 'w') # create new table
                parse_string_for_column_names(user_input[3], file) # calling function for naming the columns
                print('Table',user_input[2],'created.')
                file.close()
        else:
            print('Valid database is not selected.') # if existing database is not selected
    else:
        print('')

def drop(user_input):
    # function drops a database and table by passing the query as an argument
    if(len(user_input) == 3):
        if(user_input[1] == 'database'): # check for the word 'database' in the query
            if os.path.exists(user_input[2]): # check if the database or directory exists
                os.removedirs(user_input[2])  # remove the database
                print('Database',user_input[2],'deleted.')
            else:
                print('!Failed to delete',user_input[2],'because it does not exist.')

        elif user_input[1] == 'table': # check for the word 'table' in the query
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'): # check if the table exists in a database
                os.remove(current_db+'/'+user_input[2]+'.csv') # remove the table
                print('Table',user_input[2],'deleted.')
            else:
                print('!Failed to delete',user_input[2] ,'because it does not exist.')

    elif(len(user_input) < 3): # check if the count of words in the query is less than s3
        print("wrong statement.")
    else:
        print('')

def use(user_input):
    # function definition for selecting a database
    if len(user_input) == 2: # checking if the count of words for the query is 2
        global current_db
        current_db = user_input[1]
        if os.path.exists(user_input[1]): # check if the database or directory exists
            print('Using database',user_input[1],'.')
        else:
            print('Database not available.')
    elif(len(user_input) < 2): # checking if the count of words for the query is less than 2

        print("wrong statement.")
        
def select(user_input):
    # function for selecting columns and rows in a table
    if(current_db != 'NOT SELECTED.'):
        if os.path.isfile(current_db+'/'+user_input[2]+'.csv'): # check if the file or table exists in the database
            if(user_input[0] == '*'):
                file = open(current_db+'/'+user_input[2]+'.csv', 'r')
                for row in file: # iterate each row in the file
                    print(row.replace(',', ' | ')) # replaces ',' with ' | '
                file.close()
            else:
                print('currently the symbol " * " only works in the select statement')
        else:
            print('!Failed to query table',user_input[2],'because it does not exist.')
    else:
        print('Database not selected. Hint: "use database" statement).')

def alter(user_input):
    # function alters columns in a table
    if os.path.isfile(current_db+'/'+user_input[0]+'.csv'): # checks if the file or table exists in the database
        alter_columns = user_input[1].split(' ',1) # new column name
        if (alter_columns[0] == 'add'): # check if column needs to be added
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
                lines[0] = columns+'\n' # store the new column names
            with open(current_db+'/'+user_input[0]+'.csv', 'w') as f:
                f.writelines(lines) # Writing columns to the file
                print('Table',user_input[0],'modified.')
    else:
        print('Table does\'nt exist or database not selected.')
        
def parse_string_for_column_names(input_string, file):
    # function parses column names from the input query
    columns = []
    if input_string.startswith("(") and input_string.endswith(")"): # checking for open and close brackets
        for column in input_string[1:-1].split(','): # exclude "(" & ")" and split at "," for column names
            column = column.strip() # strip column names
            columns.append(column)  # append column names to the list variable
        writer = csv.writer(file)
        writer.writerow(columns) # write columns into the table or file
    else:
        print('error in open or close brackets.')
            
sqlStatements()