import os
import time
from redshift_auto_schema import RedshiftAutoSchema

start= time.time() # set a start point to measure the elapsed time it take to run script

## NOTE: change the 5 variables below
input_path= r'D:\Users\sample-user\CollegeScorecard_Raw_Data_01192021\Cleaned Data Files' # input directory
schema_name= 'sample_schema' # schema name in Redshift
s3_bucket= 's3://sample-bucket/' # bucket name in S3
access_key_id= 'sample-access-key-id' # access_key_id in Redshift
secret_access_key= 'sample-secret-access-key' # secret_access_key in Redshift

for subdir, dirs, files in os.walk(input_path):
    for file in files:
        if file.endswith('.parquet'):
            file_name= os.path.splitext(file)[0]

            # Generate CREATE TABLE command from parquet files
            create_table_command= RedshiftAutoSchema(file= f'{input_path}\\{file}', schema= schema_name, table= file_name).generate_table_ddl()

            # Generate COPY command from csv files (not sure why this not work for parquet files!!!)
            copy_command= f'''COPY {schema_name}.{file_name}
FROM '{s3_bucket}{file_name}.csv'
ACCESS_KEY_ID '{access_key_id}'
SECRET_ACCESS_KEY '{secret_access_key}'
FORMAT AS csv
DELIMITER ','
IGNOREHEADER AS 1
'''
            drop_table_command= f'DROP TABLE IF EXISTS {file_name}'

            # Convert some incorrect variable type
            string_variables= ['ACAD_YR', 'UNITID', 'OPEID', 'OPEID6', 'CIPCODE', 'ZIP']
            for i in string_variables:
                create_table_command = create_table_command.replace(f'"{i}" float8', f'"{i}" varchar(32)')
                create_table_command = create_table_command.replace(f'"{i}" varchar(256)', f'"{i}" varchar(32)')

            float_variables= ["DEBT_ALL_PP_ANY_MDN10YRPAY", "DEBT_ALL_PP_EVAL_MDN10YRPAY", "DEBT_ALL_STGP_ANY_MDN10YRPAY", "DEBT_ALL_STGP_EVAL_MDN10YRPAY",
                              "SATVR25", "SATVR75", "SATMT25", "SATMT75", "SATWR25", "SATWR75", "SATVRMID", "SATMTMID", "SATWRMID", "ACTCM25", "ACTCM75","ACTEN25", "ACTEN75" , "ACTMT25" , "ACTMT75" , "ACTWR25" , "ACTWR75" , "ACTCMMID" , "ACTENMID" , "ACTMTMID" , "ACTWRMID" , "SAT_AVG" , "SAT_AVG_ALL",
                              "D200_4", "D200_L4", "MN_EARN_WNE_INC1_P6", "MN_EARN_WNE_INC2_P6", "MN_EARN_WNE_INC3_P6" , "MN_EARN_WNE_INDEP0_INC1_P6", "MN_EARN_WNE_INDEP0_P6", "MN_EARN_WNE_INDEP1_P6", "MN_EARN_WNE_MALE0_P6", "MN_EARN_WNE_MALE1_P6",
                              "BBRR1_FED_GRCOMP_DFLT", "BBRR1_FED_GRNOCOMP_DFLT", "CUML_DEBT_N"
                              ]
            for i in float_variables:
                create_table_command = create_table_command.replace(f'"{i}" int4', f'"{i}" float8')
                create_table_command = create_table_command.replace(f'"{i}" varchar(256)', f'"{i}" float8')

            integer_variables= ['COUNT_ED']
            for i in integer_variables:
                create_table_command = create_table_command.replace(f'"{i}" varchar(256)', f'"{i}" int4')

            create_table_command = create_table_command.replace('bool', 'int4')
            create_table_command = create_table_command.replace('date', 'varchar(32)')

            # Write to a SQL file
            with open(f"{input_path}\\the-college-score-card_generate-DDL.sql", "a") as f:
                print(f'--{drop_table_command};', file= f)
                print(f'{create_table_command};', file= f)
                print(f'{copy_command};', file= f)

end= time.time() # set an end point to measure the elapsed time it took to run script
time_to_run= time.gmtime(end- start) # time to run the script in seconds
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run)) # 30 seconds
