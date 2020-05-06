# date: 05/04/2020
# developer: Humphrey Shikoli
# programming language: Python
# description: program that allows allows a database user to make queries over multiple tables

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
        user_input = ' '.join(user_input)
        if len(user_input) == 0:
            user_input = ""
            continue
        elif(user_input.strip()[:2] == "--"): # removing the hyphen signs in the test file
            user_input = ""
            continue
        elif(user_input.lower() == '.exit'): # input query for exiting the program
            print("\nAll done.")
            break     
        elif(user_input[-1] is ';'):
            user_input = user_input[:-1] # remove the semicolon and store it in "user_input" variable
            user_input = user_input.lower().split(' ', 3)  # input converted to lower-case and split each word by spaces       
            if(user_input[0] == f_commands[0]): # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                create(user_input) # calling create function
            elif(user_input[0] == f_commands[1]): # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                drop(user_input) # calling drop function               
            elif(user_input[0] == f_commands[2] and user_input[1] == 'table'): # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                alter(user_input[2:]) # calling alter function           
            elif(user_input[0] == f_commands[3]): # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                use(user_input) # calling use function               
            elif(user_input[0] == f_commands[4]): # crosscheck the first word of input with the contents of the "f_commands list"
                print()
                select(' '.join(user_input[1:])) # calling select function
            elif(user_input[0] == f_commands[5] and user_input[1] == 'into'):
                insert(user_input[2], user_input[3])
            elif(user_input[0] == f_commands[6]):
                print()
                update(user_input[1], user_input[2], user_input[3])
            elif(user_input[0] == f_commands[7] and user_input[1] == "from"):
                print()
                delete(user_input[2], user_input[3])
            else:
                print("\ninvalid command") # for an input that is invalid
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
    elif(len(user_input) < 3): # checking if the number of words in the query is less than 3
        print("Wrong statement.")
    elif(user_input[1].lower() == "table" and len(user_input) > 3): # check for the word 'table' in the query
        user_input = ' '.join(user_input)
        user_input = user_input.split(' ', 2)
        user_input = user_input[2].partition('(')
        user_input = list(user_input)
        if os.path.exists(current_db): # check if the database or directory exists
            if os.path.isfile(current_db+'/'+user_input[0].strip()+'.csv'): # check if the table exists
                print("!Failed to create table",user_input[0].strip(),"because it already exists.")
            else:
                file = open(current_db+'/'+user_input[0].strip()+'.csv', 'w') # create new table
                parse_string_for_column_names(user_input[2], file) # calling function for naming the columns
                print("Table",user_input[0],"created.")
                file.close()                                            
        else:
            print("Valid database is not selected.") # if existing database is not selected
    else:
        print('')

def drop(user_input):
    # function drops a database and table by passing the query as an argument
    if(len(user_input) == 3):
        if(user_input[1].lower() == "database"): # check for the word 'database' in the query
            if os.path.exists(user_input[2]): # check if the database or directory exists
                os.removedirs(user_input[2]) # remove the database
                print("Database",user_input[2],"deleted.")
            else:
                print("!Failed to delete",user_input[2],"because it does not exist.")
        elif user_input[1].lower() == "table": # check for the word 'table' in the query
            if os.path.isfile(current_db+'/'+user_input[2]+'.csv'): # check if the table exists in a database
                os.remove(current_db+'/'+user_input[2]+'.csv') # remove the table
                print("Table",user_input[2],"deleted.")
            else:
                print("!Failed to delete",user_input[2] ,"because it does not exist.")
    elif(len(user_input) < 3): # check if the count of words in the query is less than 3
        print("Wrong Statement.")
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
        print("Wrong Statement.")

def select(user_input):
    # function for selecting columns and rows in a table
    if 'from' in user_input.lower():
        ind = user_input.lower().index('from')
        user_input = user_input[:ind]+"from"+user_input[ind+4:]
    before_from_after = user_input.partition('from')
    select_params = before_from_after[0].split(',')
    where_col_ind = []
    where_col_names = []
    where_ops = []
    where_vals = []
    existing_table_col_names = {}
    if(current_db != "NOT SELECTED."):
        if(select_params[0].strip() == '*'):
            where_vals_ind = []
            table_aliases = []
            allColumns = []
            if 'where' in before_from_after[2].lower():   
                ind = before_from_after[2].lower().index('where')
                before_from_after = list(before_from_after)
                before_from_after[2] = before_from_after[2][:ind]+"where"+before_from_after[2][ind+5:]
                before_where_after = before_from_after[2].partition('where') # partitioing query before and after 'before' keyword
                table_names = before_where_after[0].split(',')
                after_where = before_where_after[2].strip().split(' ')
                getTableNamesAndAliases(table_names, table_aliases) # call method for table names and their aliases
                getExistingColumnNames(table_names, existing_table_col_names, allColumns)
                getAllOtherLists(after_where, table_aliases, existing_table_col_names, table_names, where_col_ind, where_ops, where_vals_ind)
                printSelectWhereOrOnQuery(table_names, where_ops, where_vals_ind, where_col_ind, 'where', allColumns)      
            elif 'on' in before_from_after[2]:
                before_on_after = before_from_after[2].strip().partition('on')
                if 'inner join' in before_on_after[0]:
                    join_name = 'inner join'
                    table_names = before_on_after[0].split(join_name)
                elif 'left outer join' in before_on_after[0]:
                    join_name = 'left outer join'
                    table_names = before_on_after[0].split(join_name)
                getTableNamesAndAliases(table_names, table_aliases)
                getExistingColumnNames(table_names, existing_table_col_names, allColumns)
                getAllOtherLists(before_on_after[2].strip().split(' '), table_aliases, existing_table_col_names, table_names, where_col_ind, where_ops, where_vals_ind)
                printSelectWhereOrOnQuery(table_names, where_ops, where_vals_ind, where_col_ind, join_name, allColumns)
            else:
                if os.path.isfile(current_db+'/'+before_from_after[2].strip()+'.csv'): # check if the file or table exists in a database
                    file = open(current_db+'/'+before_from_after[2].strip()+'.csv', 'r') # open table or file in readable mode
                    for row in file: # iterate each row in the file
                        row = row.strip().replace("\n","")
                        print(row.replace(',', ' | ')) # replace ',' to ' | '
                    file.close() # closing file.
                else:
                    print("!Failed to query table", before_from_after[2], "because it does not exist.")
        else:
            select_col_ind = []
            before_where_after = before_from_after[2].partition("where")
            table_name = before_where_after[0].strip()
            if os.path.isfile(current_db+'/'+table_name+'.csv'): # check if the file or table exists in a database
                where_params = before_where_after[2].strip().split(' ')
                with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names:
                    reader = csv.reader(read_column_names)
                    columns = next(reader)
                column_names = get_only_column_names(columns) # existing column names are retrieved and stored in a list
                for i in range(len(select_params)):                               
                    if select_params[i].strip() in column_names:
                        select_col_ind.append(column_names.index(select_params[i].strip()))
                    else:
                        print("select column name '",select_params[i],"' doesn't exist.")
                column_datatypes = get_column_datatypes(columns)
                for word in where_params: # this for loop stores 'where' column names, operators and values in seperate lists
                    if where_params.index(word) % 3 == 0:
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
                    with open(current_db+'/'+table_name+'.csv', 'r') as read_rows: # open file with the mentioned table name in the query
                        next(read_rows) # skip first two rows
                        next(read_rows)
                        for row in read_rows: # iterate through each row
                            row = row.strip().split(',') # row split by ',' and stored in a list
                            for i in range(len(where_ops)):
                                if where_ops[i] == '!=': # checks for a '!=' in the query
                                    if row[where_col_ind[i]] not in where_vals:  # checks if the query value doesn't match the row value
                                        print()
                                        for i in range(len(select_col_ind)):
                                            print(row[select_col_ind[i]], end = " | ") # prints if the query value doesn't match the row value
                                else:
                                    print("only != works for now.")
                        print()
            else:
                print("!Failed to query table", table_name, "because it does not exist.")
    else:
        print("Database not selected ('use database' statement).")

def getTableNamesAndAliases(table_names, table_aliases):
    
    i = 0
    for word in table_names:
        # get table names and their aliases in different lists using this loop
        word = word.strip().split(' ')
        table_aliases.append(word[1])
        table_names[i] = word[0]
        i += 1
        
def getExistingColumnNames(table_names, existing_table_col_names, allColumns):
    
    for i in range(len(table_names)): 
        # store existing table column names in dictionaries using this loop
        with open(current_db+'/'+table_names[i]+'.csv', 'r') as read_column_names:
            reader = csv.reader(read_column_names)
            columns = next(reader)
            allColumns.append(columns)
            column_names = get_only_column_names(columns) # existing column names are retrieved and stored in a list
            existing_table_col_names[table_names[i]] = column_names
            
def getAllOtherLists(after_on_or_where, table_aliases, existing_table_col_names, table_names, where_col_ind, where_ops, where_vals_ind):
    
    for word in after_on_or_where: 
        # for loop for getting where comparision values and operators in seperate lists
        if after_on_or_where.index(word) % 3 == 0:
            if '.' in word:
                table_and_column_names = word.split('.')
                if table_and_column_names[0] in table_aliases:
                    temp_cols = existing_table_col_names[table_names[table_aliases.index(table_and_column_names[0])]]
                    where_col_ind.append(temp_cols.index(table_and_column_names[1]))
        elif after_on_or_where.index(word) % 3 == 1:
            where_ops.append(word.strip())
        else:
            if '.' in word:
                table_and_column_names = word.split('.')
                if table_and_column_names[0] in table_aliases:
                    temp_cols = existing_table_col_names[table_names[table_aliases.index(table_and_column_names[0])]]
                    where_vals_ind.append(temp_cols.index(table_and_column_names[1]))
                    
def printSelectWhereOrOnQuery(table_names, where_ops, where_vals_ind, where_col_ind, join_name, allColumns):
    
    if len(table_names) == 2:
        print(','.join(allColumns[0]).replace(',','|'),end="|",flush = True)
        print(','.join(allColumns[1]).replace(',','|'))
        with open(current_db+'/'+table_names[0]+'.csv', 'r') as read_rows_table1: # opens a file with the mentioned table name in the query
            next(read_rows_table1)
            for row_tb1 in read_rows_table1:
                row_tb1 = row_tb1.strip().split(',')
                count = 0;
                with open(current_db+'/'+table_names[1]+'.csv', 'r') as read_rows_table2: # opens a file with the mentioned table name in the query
                    next(read_rows_table2)
                    for row_tb2 in read_rows_table2:  
                        row_tb2 = row_tb2.strip().split(',')
                        for i in range(len(where_ops)):
                            if(where_ops[i] == '='):
                                if row_tb1[where_col_ind[i]] == row_tb2[where_vals_ind[i]]:
                                    temp1 = ','.join(row_tb1)
                                    temp2 = ','.join(row_tb2)
                                    count += 1
                                    print(temp1.replace(',','|'),'|',temp2.replace(',','|'))
                    if(join_name == 'left outer join' and count == 0):
                        print(','.join(row_tb1).replace(',','|'), end = '', flush = True)
                        temp2 = temp2.split(',')
                        for i in range(len(temp2)):
                            print('|', end='')
                        print()
    else:
        print("Error. More than 2 table names in query.")

def alter(user_input):
    # function alters columns in a table
    if os.path.isfile(current_db+'/'+user_input[0]+'.csv'): # check if the table or file exists in a database
        alter_columns = user_input[1].split(' ',1) # get new column name from the query
        if (alter_columns[0].lower() == 'add'): # check if the column has to be added
            columns = []
            file = open(current_db+'/'+user_input[0]+'.csv', 'r')  # open the file in readable mode
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
                f.writelines(lines) # write columns to the file
                print("Table", user_input[0],"modified.")
    else:
        print("Table does\'nt exist or database not selected.")

def insert(table_name, values):
    
    if os.path.isfile(current_db+'/'+table_name+'.csv'): # checks if a table exists
        if values.startswith("values(") and values.endswith(")"):
            values = values[7:-1].split(',') # insertion values are stored in a list
            file = open(current_db+'/'+table_name+'.csv', 'a', newline='') # table or file is opened
            for i in range(len(values)): 
                # for loop eliminates the quotes if present in the values
                word = values[i].strip()
                if word.startswith("'") and word.endswith("'"):
                    word = word.replace("'","")
                values[i] = word
                i += 1
            write_row_values(values, file) # function call for writing rows with arguments values in a list and opened file object
            file.close()
        else:
            print("wrong syntax.")
    else:
        print('Table doesn\'t exist.')

def update(table_name, set_word, remaining_words):
    
    column_in_database = True
    if os.path.isfile(current_db+'/'+table_name+'.csv'): # checks if a table or file exists
        update_values = {}
        with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names: # open a table or file for getting column names
            reader = csv.reader(read_column_names)
            columns = next(reader)
        column_names = get_only_column_names(columns)
        column_datatypes = get_column_datatypes(columns)
        if set_word == 'set': # checks if the set word is right after the table name
            before_where_after = remaining_words.partition('where')
            before_words = before_where_after[0].split('=') # retrieves all the words before a 'where' keyword
            for word in before_words: # this for loop stores the 'set' column names in list
                if before_words.index(word)/2 == 0: # and checks if those column names are in the file or table column names
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
                for word in after_words: # loop stores 'where' column names and values each in separate lists
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
                update_to_file(table_name, update_values, set_index, word, column_names[set_index], where_index) # function call to update file with arguments as table name, set column names & values, where column names, operators and values
        else:
            print("Error in the set name")
    else:
        print("Table does\'nt exist or database not selected.")
        
def delete(table_name, contents):
    
    if os.path.isfile(current_db+'/'+table_name+'.csv'):
        with open(current_db+'/'+table_name+'.csv', 'r') as read_column_names: # opens a file and get column names
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
            for word in contents: 
                # for loop stores 'delete' column names, operators and values in seperate lists
                # and checks if the mentioned column names in the query are present in the existing table or file column names
                if contents.index(word)%3 == 0:
                    if word.strip() in column_names:
                        delete_col_indexes.append(column_names.index(word.strip()))
                        delete_col_dtypes.append(column_names.index(word.strip()))
                    else:
                        print("Entered column name(where) not present in the table.")
                        break
                elif contents.index(word)%3 == 1:
                    delete_col_operators.append(word.strip())
                else:
                    word = word.strip()
                    if word.startswith('"') and word.endswith('"'):
                        word = word.replace('"',"")
                    delete_col_values.append(word)
            deleteAndWriteRows(table_name, delete_col_indexes, delete_col_values, delete_col_dtypes, delete_col_operators) # fuction call with arguments as table name, delete column names, operators and values for deletion
        else:
            print("Table '",table_name,"'doesn't exist.")

def parse_string_for_column_names(input_string, file):
    # function is used to parse column names from the input query
    columns = []
    input_string = '(' + input_string
    if input_string.startswith("(") and input_string.endswith(")"): # check for open and close brackets
        for column in input_string[1:-1].split(','): # exclude "(" & ")" and splitting at "," for column names
            column = column.strip() # strip column names
            columns.append(column) # append column names to the list variable
        writer = csv.writer(file) # create a csv writer object
        writer.writerow(columns) # write columns into the table or file
    else:
        print("Error in open or close brackets.")
        
def write_row_values(values, file):
    
    writer = csv.writer(file)
    writer.writerow(values)
    print("1 new record inserted.")
    
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

def update_to_file(table_name, update_values, set_index, word, column_name, where_index):   
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
            print("empty line")
    with open(current_db+'/'+table_name+'.csv', 'w') as wf:
        wf.writelines(lines)
        if count == 1:
            print(count,"record modified.")
        elif count > 1:
            print(count,"records modified.")
            
def deleteAndWriteRows(table_name, col_indexes, change_values, delete_col_dtypes, operators):   
    # function deletes a row if present and adjusts empty lines if present after deletion
    found = False
    records_modified = 0;
    with open(current_db+'/'+table_name+'.csv', 'r') as rf:
        lines = rf.readlines()
    for i in range(len(lines)):
        found_int = 0
        values = lines[i].strip().split(',')
        if i > 1 and values:
            for j in range(len(col_indexes)):
                if(operators[j] == '='):
                    if values[col_indexes[j]] == change_values[j]:
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
        if records_modified == 1:
            print(records_modified,'record deleted.')
        elif records_modified > 1:
            print(records_modified,'records deleted.')
sqlStatements()