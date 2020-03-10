# date: 3/10/2020
# developer: Humphrey Shikoli
# programming language: Python
# description: program that allows a database user to insert, delete, modify, and query their
# data on basic tables (i.e., no table joins). It is assumed that the database and table structures 
# that is, their metadata are available

import os 
import csv

in_loop = True
current_db = 'NOT SELECTED.'
command = ['create', 'drop', 'alter', 'use', 'select', 'insert', 'update', 'delete']          # List of functions

def sqlStatements():
    user_input = ""
    while in_loop:  
        try:
            input_raw = input('')
        except EOFError:
            break
        input_raw = user_input + " " + input_raw.lower()
        user_input = input_raw.strip().split()
        user_input = ' '.join(user_input)      
        if len(user_input) == 0:
            user_input = ""
            continue      
        elif user_input.strip()[:2] == "--":
            user_input = ""
            continue      
        elif user_input.lower() == '.exit':      # Checking the input query for exiting the program.
            break       
        elif user_input[-1] is ';':
            user_input = user_input[:-1]                    # Removing the semicolon and storing it in "user_input" variable.
            user_input = user_input.lower().split(' ', 3)   # Converting the input into lower case and splitting each word by spaces.     
            if user_input[0] == command[0]:    # Comparing the first word of input with the contents of the list "command".
                print()
                create(user_input)              # calling create function
            elif user_input[0] == command[1]:  # Comparing the first word of input with the contents of the list "command".
                print()
                drop(user_input)                # calling drop function               
            elif user_input[0] == command[2] and user_input[1] == 'table':     # Comparing the first word of input with the contents of the list "command".
                print()
                alter(user_input[2:])                                           # calling alter function               
            elif user_input[0] == command[3]:  # Comparing the first word of input with the contents of the list "command".
                print()
                use(user_input)                 # calling use function               
            elif user_input[0] == command[4]:  # Comparing the first word of input with the contents of the list "command".
                print()
                select(' '.join(user_input[1:]))          # calling select function               
            elif user_input[0] == command[5] and user_input[1] == 'into':
                insert(user_input[2], user_input[3])               
            elif user_input[0] == command[6]:
                print()
                update(user_input[1], user_input[2], user_input[3])               
            elif user_input[0] == command[7] and user_input[1] == 'from':
                print()
                delete(user_input[2], user_input[3])           
            else:
                print('\ncommand invalid.')       # If the input is invalid.
            user_input = ""         
#   Below function is used to create a database and table by passing the query as an argument.     
def create(user_input):
    if(len(user_input) == 3):
        if(user_input[1] == 'database'):            # Check for the word 'database' in the query.
            if not os.path.exists(user_input[2]):   # Check if the directory/database exists.
                os.makedirs(user_input[2])          # Creating a new directory.
                print('Database',user_input[2],'created.')
            else:           
                print("!Failed to create database",user_input[2],"because it already exists.")
    elif(len(user_input) < 3):                                  # Checking if the number of words in the query is less than 3.
        print("Statement wrong.")
    elif(user_input[1] == 'table' and len(user_input) > 3):             # Check for the word 'table' in the query.
        if os.path.exists(current_db):                                  # Check if the directory/database exists.
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'):     # Check if the table exists.
                print('!Failed to create table',user_input[2],'because it already exists.')
            else:
                file = open(current_db+'/'+user_input[2]+'.csv', 'w')   # Creating new table.
                parse_string_for_column_names(user_input[3], file)      # Calling function for naming the columns.
                print('Table',user_input[2],'created.')
                file.close()                                            
        else:
            print('Valid database is not selected.')                    # If existing database is not selected.
    else:
        print('')      
#   Below function is used to drop a database and table by passing the query as an argument.
def drop(user_input):
    if(len(user_input) == 3):
        if(user_input[1] == 'database'):        # Check for the word 'database' in the query.
            if os.path.exists(user_input[2]):   # Check if the directory/database exists.
                os.removedirs(user_input[2])    # Removing the database.
                print('Database',user_input[2],'deleted.')
            else:
                print('!Failed to delete',user_input[2],'because it does not exist.')
        elif user_input[1] == 'table':                                  # Check for the word 'table' in the query.
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'):     # Check if the table exists in a database.
                os.remove(current_db+'/'+user_input[2]+'.csv')          # Removing the table.
                print('Table',user_input[2],'deleted.')
            else:
                print('!Failed to delete',user_input[2] ,'because it does not exist.')
    elif(len(user_input) < 3):                                          # Checking if the query consists less than 3 words.
        print("Statement wrong.")
    else:
        print('')
#   Below function is used for selecting a database.
def use(user_input):
    if len(user_input) == 2:                            # Checking if length(words) of the query is 2.
        global current_db
        current_db = user_input[1]
        if os.path.exists(user_input[1]):               # Check if the directory/database exists.
            print('Using database',user_input[1],'.')
        else:
            print('Database not available.')
    elif(len(user_input) < 2):                          # Checking if length(words) of the query is less than 2.
        print("Statement wrong.")
#   Below function is used to select columns and rows in a table.
def select(user_input):
    before_from_after = user_input.partition('from')
    select_params = before_from_after[0].split(',')
    if(current_db != 'NOT SELECTED.'):
        if(select_params[0].strip() == '*'):
            if os.path.isfile(current_db+'/'+before_from_after[2].strip()+'.csv'):             # Check if the table/file exists in a database.
                file = open(current_db+'/'+before_from_after[2].strip()+'.csv', 'r')       # Opening file/table in readable mode.
                for row in file:                                            # Iterating each row in the file.
                    row = row.strip().replace("\n","")
                    print(row.replace(',', ' | '))                          # To replace ',' to ' | ' and printing.
                file.close()                                                # Closing file.
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
            if os.path.isfile(current_db+'/'+table_name+'.csv'):             # Check if the table/file exists in a database.
                where_params = before_where_after[2].strip().split(' ')
                with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names:
                    reader = csv.reader(read_column_names)
                    columns = next(reader)
                column_names = get_only_column_names(columns)                # Existing column names are retrieved and stored in a list.
                for i in range(len(select_params)):                               
                    if select_params[i].strip() in column_names:
                        select_col_ind.append(column_names.index(select_params[i].strip()))
                    else:
                        print("select column name '",select_params[i],"' doesn't exist.")
                column_datatypes = get_column_datatypes(columns)
                for word in where_params:                                    # This for loop stores 'where' column names, operators and values in seperate lists.
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
                    with open(current_db+'/'+table_name+'.csv', 'r') as read_rows:                               # This line opens a file with the mentioned table name in the query.
                        next(read_rows)                                                                          # First two rows are skipped.
                        next(read_rows)
                        for row in read_rows:                                                                    # Iterates through each row. 
                            row = row.strip().split(',')                                                         # Row is split by ',' and stored in a list.
                            for i in range(len(where_ops)):
                                if where_ops[i] == '!=':                                                         # Checks for a '!=' in the query.
                                    if row[where_col_ind[i]] not in where_vals:                                  # Checks if the query value doesn't match the row value.
                                        print()
                                        for i in range(len(select_col_ind)):
                                            print(row[select_col_ind[i]], end=" | ")                             # Prints if the query value doesn't match the row value.
                                else:
                                    print("only != works for now.")
                        print()
            else:
                print('!Failed to query table',table_name,'because it does not exist.')
    else:
        print('Database not selected("use database" statement).')
#   Below function is used to alter columns in a table.
def alter(user_input):
    if os.path.isfile(current_db+'/'+user_input[0]+'.csv'):                 # Check if the table/file exists in a database.
        alter_columns = user_input[1].split(' ',1)                          # Getting new column name from the query.
        if (alter_columns[0] == 'add'):                                     # Checking if column has to be added.
            columns = []
            file = open(current_db+'/'+user_input[0]+'.csv', 'r')           # Opening the file in readable mode.
            for row in file:                                
                columns = row.strip().split(',')                            # Getting and striping existing columns from the table/file and storing in a list variable.
                columns.append(alter_columns[1])                            # Appending new column names to the list variable.
                columns = ','.join(columns)                                 # Joining all column names with ','.
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
    if os.path.isfile(current_db+'/'+table_name+'.csv'):                    # Checks table existance.
        if values.startswith("values(") and values.endswith(")"):
            values = values[7:-1].split(',')                                # Insertion values are stored in a list.
            file = open(current_db+'/'+table_name+'.csv', 'a', newline='')  # File/Table is opened.
            for i in range(len(values)):                                    # This for loop eliminates the quotes if present in the values (ex: 'SuperGizmo').
                word = values[i].strip()
                if word.startswith("'") and word.endswith("'"):
                    word = word.replace("'","")
                values[i] = word
                i += 1
            write_row_values(values, file)                                  # function is called for writing rows with arguments values in a list and opened file object.
            file.close()    
        else:
            print('values syntax wrong.')
    else:
        print('Table doesn\'t exist.')
def update(table_name, set_word, remaining_words):
    column_in_database = True
    if os.path.isfile(current_db+'/'+table_name+'.csv'):                        # Checks if a file/table exist.
        update_values = {}
        with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names:  # opens up a file/table for getting columns names.
            reader = csv.reader(read_column_names)
            columns = next(reader)
        column_names = get_only_column_names(columns)
        column_datatypes = get_column_datatypes(columns)
        if set_word == 'set':                                                   # Checks if the set word is right after the table name.
            before_where_after = remaining_words.partition('where')
            before_words = before_where_after[0].split('=')                     # Retrieves all the words before a 'where' keyword.
            for word in before_words:                                           # This for loop stores the 'set' column names in list
                if before_words.index(word)/2 == 0:                             # and checks if those column names are in the file/table column names.
                    before_words[before_words.index(word)] = word.strip()       #  
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
                for word in after_words:                                            # This for loop stores 'where' column names and values each
                    if after_words.index(word)/2 == 0:                              # in separate lists.
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
                update_to_file(table_name, update_values, set_index, word, column_names[set_index], where_index)    # Function is called to update file with arguments as table name, set column names & values, where column names, operators and values.
        else:
            print("Error in the set name")
    else:
        print('Table does\'nt exist or database not selected.')
def delete(table_name, contents):
    if os.path.isfile(current_db+'/'+table_name+'.csv'):
        with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names:          # These lines opens a file and get column names.
            reader = csv.reader(read_column_names)
            columns = next(reader)
        column_names = get_only_column_names(columns)
        contents = contents.split(' ', 1)
        if contents[0].strip() == 'where':
            contents = contents[1].split(' ')
            delete_col_indexes = []
            delete_col_values = []
            delete_col_operators = []
            delete_col_dtypes = []
            for word in contents:                                                       # This for loop stores 'delete' column names, operators and values in seperate lists.
                if contents.index(word)%3 == 0:                                         # And checks if the mentioned column names in the query are present in the existing
                    if word.strip() in column_names:                                    # table/file column names.
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
            deleteAndWriteRows(table_name, delete_col_indexes, delete_col_values, delete_col_dtypes, delete_col_operators)  # fuction is called with arguments as table name, delete column names, operators and values for deletion.
        else:
            print("Table '",table_name,"'doesn't exist.")
#   Below function is used to parse column names from the input query.
def parse_string_for_column_names(input_string, file):
    columns = []
    if input_string.startswith("(") and input_string.endswith(")"):     # Checking for open and close brackets.
        for column in input_string[1:-1].split(','):                    # Excluding "(" & ")" and splitting at "," for column names.
            column = column.strip()                                     # Striping column names.
            columns.append(column)                                      # Appending column names to the list variable.
        writer = csv.writer(file)                                       # Creating a csv writer object.
        writer.writerow(columns)                                        # Writing columns into the file/table.
    else:
        print('error in open or close brackets.')
def write_row_values(values, file):
    writer = csv.writer(file)
    writer.writerow(values)
    print('1 new record inserted.')
def get_only_column_names(columns):
    names = []
    for i in range(len(columns)):
        single_column_name = columns[i].rsplit(' ',1)
        names.append(single_column_name[0]);
    return names
def get_column_datatypes(columns):
    names = []
    for i in range(len(columns)):
        single_column_name = columns[i].rsplit(' ',1)
        names.append(single_column_name[1]);
    return names
def update_to_file(table_name, update_values, set_index, word, column_name, where_index):   # This function replaces values stored in update_values list 
    count = 0;                                                                              # by comparing values stored in word with each row in a table.
    with open(current_db+'/'+table_name+'.csv', 'r') as rf:
        lines = rf.readlines()
    for i in range(len(lines)):
        values = lines[i].strip().split(',')
        if values:                                      # Checking if list is not empty
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
def deleteAndWriteRows(table_name, col_indexes, change_values, delete_col_dtypes, operators):   # This function deletes a row if present and adjusts empty lines 
    found = False                                                                               # if present after deletion.
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