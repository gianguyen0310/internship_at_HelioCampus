This repository includes Python script that I wrote during my internship at HelioCampus\
\
The "disk_space_monitor.py" script is used to check disk space usage on a window server, it will automatically check all available drives on a window server and send out Warning email if any drive has its percentage of available space < the alert threshold (15%)\
\
The "the-college-score-card_data-prep.py" script is used to automate the process of download data from The College Scorecard website (3 Field of study files, 23 MERGED files and 1 data dictionary), then clean each data and concatenate 3 field of study data into 1 field_of_study_data_cleaned, concatenate 23 merged data into 1 institution_level_data. Since each of the original MERGED file (institution level data) has 2383 columns > maximum 1600 constrain of Redshift, the "institution_level_data" need to be split into 10 different files based on the data dictionary (each group of columns belong to a category, for example, academics has 247 columns, aid has 108 columns, earnings has 81 columns, etc.), then the cleaned data will be uploaded to AWS S3\
\
The "the-college-score-card_ddl-sql-generate" script is used to generate the DDL SQL "Create Table" command Redshift and also the COPY command to dump data from S3 to Redshift\
\
The "the-college-scorecard_data-dictionary" script is used to prep the data dictionary, concat and prepare it to match the destination table in Redshift, then bulk insert into Redshift table\
\
The "tableau_server_auto_download" script is used to retrieve all available version of Tableau download page, download link, auto download a desired version\
\
The 'ipeds_auto_download" script is used to automate download IPEDS data
