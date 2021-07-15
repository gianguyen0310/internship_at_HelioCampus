import awswrangler as wr
import pandas as pd
pd.options.display.width=None
import redshift_connector
import time
import numpy as np
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.max_colwidth', 100)


start= time.time() # set a start point to measure the elapsed time it take to run script

# NOTE: change 9 variables below if necessary
db_host= 'sample-host.us-east-1.redshift.amazonaws.com'
db_name= 'sample_db'
user= 'sample_user'
password= 'sample_password'
path_to_data_dictionary= r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\collegescorecarddatadictionary_2021-04-01.xlsx'
corresponding_redshift_table_for_field_of_study_data_dictionary= 'tcsc_field_of_study'
corresponding_redshift_table_institution_level_data_dictionary= 'tcsc_institution_level'
write_to_schema= 'sample_schema'
write_to_table= 'sample_table'

# Create a Redshift connection
con_redshift = redshift_connector.connect(host= db_host, database= db_name, user= user, password= password)

# Read the "data_definitions" table in the "edwutil" schema
data_definitions = wr.redshift.read_sql_table(table="sample_table",
                                              schema="sample_schema",
                                              con= con_redshift
                                             )

# Read 2 data dictionaries from local file
field_of_study_data_dictionary= pd.read_excel(path_to_data_dictionary, sheet_name= 'FieldOfStudy_data_dictionary', engine= 'openpyxl',
                                              usecols= ['NAME OF DATA ELEMENT', 'VARIABLE NAME', 'VALUE', 'LABEL'],
                                              #dtype= {'NAME OF DATA ELEMENT': str, 'VARIABLE NAME': str, 'VALUE': 'Int64', 'LABEL': str}
                                              )
institution_level_data_dictionary= pd.read_excel(path_to_data_dictionary, sheet_name= 'institution_data_dictionary', engine= 'openpyxl',
                                                 usecols= ['NAME OF DATA ELEMENT', 'VARIABLE NAME', 'VALUE', 'LABEL'],
                                                 #dtype={'NAME OF DATA ELEMENT': str, 'VARIABLE NAME': str, 'VALUE': 'Int64', 'LABEL': str}
                                                 )

# Forward fill to eliminate NaN
field_of_study_data_dictionary['VARIABLE NAME']= field_of_study_data_dictionary['VARIABLE NAME'].fillna(method= 'ffill')
field_of_study_data_dictionary['NAME OF DATA ELEMENT']= field_of_study_data_dictionary['NAME OF DATA ELEMENT'].fillna(method= 'ffill')

institution_level_data_dictionary['VARIABLE NAME']= institution_level_data_dictionary['VARIABLE NAME'].fillna(method= 'ffill')
institution_level_data_dictionary['NAME OF DATA ELEMENT']= institution_level_data_dictionary['NAME OF DATA ELEMENT'].fillna(method= 'ffill')

# Replace weird string format
string1= institution_level_data_dictionary.iloc[15,0]
string2= institution_level_data_dictionary.iloc[20,0]
institution_level_data_dictionary['NAME OF DATA ELEMENT']= institution_level_data_dictionary['NAME OF DATA ELEMENT'].replace(string1, string1.split("\n")[0])
institution_level_data_dictionary['NAME OF DATA ELEMENT']= institution_level_data_dictionary['NAME OF DATA ELEMENT'].replace(string2, string2.split("\n")[0])

## OPTION 1: Create 1 record for each VALUE
# For example: CONTROL -- Control of institution. 1: Public,
#              CONTROL -- Control of institution. 2: Private nonprofit
#              CONTROL -- Control of institution. 3: Private for-profit

# Combine "NAME OF DATA ELEMENT", "VALUE", "LABEL" into one "DESCRIPTION" column
# If there are VALUE or LABEL, then DESCRIPTION= NAME OF DATA ELEMENT+ VALUE+ LABEL, else DESCRIPTION= NAME OF DATA ELEMENT
# field_of_study_data_dictionary['DESCRIPTION'] = np.where(field_of_study_data_dictionary['VALUE'].isnull(),
#                                                          field_of_study_data_dictionary['NAME OF DATA ELEMENT'],
#                                                          field_of_study_data_dictionary['NAME OF DATA ELEMENT'] + '. ' + \
#                                                          field_of_study_data_dictionary['VALUE'].astype(str)+ ': ' +\
#                                                          field_of_study_data_dictionary['LABEL']
#                                                          )
#
# institution_level_data_dictionary['DESCRIPTION'] = np.where(institution_level_data_dictionary['VALUE'].isnull(),
#                                                          institution_level_data_dictionary['NAME OF DATA ELEMENT'],
#                                                          institution_level_data_dictionary['NAME OF DATA ELEMENT'] + '. ' + \
#                                                          institution_level_data_dictionary['VALUE'].astype(str)+ ': ' +\
#                                                          institution_level_data_dictionary['LABEL']
#                                                          )



## OPTION 2: Create only 1 record per VARIABLE
# For example: CONTROL -- Control of institution [1: Public, 2: Private nonprofit, 3: Private for-profit]
#              MAIN -- Flag for main campus [0: Not main campus, 1: Main campus]

# Create a VALUE-LABEL column combine VALUE and LABEL
field_of_study_data_dictionary['VALUE-LABEL']= np.where(field_of_study_data_dictionary['VALUE'].isna(),
                                                        np.nan,
                                                        field_of_study_data_dictionary['VALUE'].astype('Int64').astype(str) + ': ' + field_of_study_data_dictionary['LABEL'],
                                                        )

field_of_study_data_dictionary = field_of_study_data_dictionary.fillna('NaN').groupby(['VARIABLE NAME', 'NAME OF DATA ELEMENT'], sort= False)['VALUE-LABEL'].apply('| '.join).reset_index()
field_of_study_data_dictionary['DESCRIPTION']= np.where(field_of_study_data_dictionary['VALUE-LABEL'].str.contains('NaN'),
                                                        field_of_study_data_dictionary['NAME OF DATA ELEMENT'],
                                                        field_of_study_data_dictionary['NAME OF DATA ELEMENT'] + ' [' + field_of_study_data_dictionary['VALUE-LABEL'] + ']')



institution_level_data_dictionary['VALUE-LABEL']= np.where(institution_level_data_dictionary['VALUE'].isna(),
                                                           np.nan,
                                                           institution_level_data_dictionary['VALUE'].astype(str) + ': ' + institution_level_data_dictionary['LABEL'],
                                                           )

institution_level_data_dictionary = institution_level_data_dictionary.fillna('NaN').groupby(['VARIABLE NAME', 'NAME OF DATA ELEMENT'], sort= False)['VALUE-LABEL'].apply('| '.join).reset_index()
institution_level_data_dictionary['DESCRIPTION']= np.where(institution_level_data_dictionary['VALUE-LABEL'].str.contains('NaN'),
                                                           institution_level_data_dictionary['NAME OF DATA ELEMENT'],
                                                           institution_level_data_dictionary['NAME OF DATA ELEMENT'] + ' [' + institution_level_data_dictionary['VALUE-LABEL'] + ']')

# --------------------------- end of OPTION 2 ----------------------------


# Create a "from_table" column for 2 data dictionary
field_of_study_data_dictionary['from_table']= corresponding_redshift_table_for_field_of_study_data_dictionary
institution_level_data_dictionary['from_table']= corresponding_redshift_table_institution_level_data_dictionary

#print(data_definitions.shape)
#print(field_of_study_data_dictionary.shape)
#print(institution_level_data_dictionary.shape)

#print(field_of_study_data_dictionary)
#print(institution_level_data_dictionary)

# Concat "field_of_study_data_dictionary" and "institution_level_data_dictionary" into 1 data_dictionary
data_dictionary= pd.concat([field_of_study_data_dictionary, institution_level_data_dictionary], ignore_index= True, axis= 0)

# Drop duplicates between 2 data dictionary
# print(data_dictionary[data_dictionary.duplicated(keep=False)])
data_dictionary.drop_duplicates(ignore_index= True, inplace= True)

#print(data_dictionary)
#print(data_dictionary.shape)


# Rename the columns in "data_dictionary" data frame to match the columns name in "data_definition" table
data_dictionary= data_dictionary.rename(columns={'from_table': 'perseus_table','VARIABLE NAME': 'perseus_column',
                                                 'DESCRIPTION': 'functional_definition'})

# Keep only 3 columns 'perseus_table','perseus_column','functional_definition'
data_dictionary= data_dictionary[['perseus_table','perseus_column','functional_definition']]
#print(data_dictionary)

# Check if the new data_dictionary has any duplicated VARIABLEs with current data_definition table
#print(data_definitions.merge(data_dictionary, indicator = True, how='inner').loc[lambda x : x['_merge']!='both'])

# Write records in the "data_dictionary" data frame to table "edwutil.data_definitions_third_party" in Redshift
wr.redshift.to_sql(df= data_dictionary,
                   table= write_to_table,
                   schema= write_to_schema,
                   con= con_redshift,
                   mode= 'overwrite',
                   index= False,
                   dtype= {'perseus_table': 'VARCHAR(256)', 'perseus_column': 'VARCHAR(512)', 'functional_definition': 'VARCHAR(max)'}
                   )


end= time.time() # set an end point to measure the elapsed time it took to run script
time_to_run= time.gmtime(end- start) # time to run the script in seconds
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run)) # 30 seconds


