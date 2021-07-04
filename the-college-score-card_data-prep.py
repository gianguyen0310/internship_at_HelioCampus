import pandas as pd
import numpy as np
pd.options.display.width=None
pd.options.mode.chained_assignment = None
import glob
import re
import time
import os
import boto3

start= time.time() # set a start point to measure the elapsed time it take to run script

### NOTE: CHANGE THE INPUT and OUTPUT directory at line 15, 21 as well as the path to the data dictionary at line 18

# Path to the folder that contains raw data (Raw Data Files)
input_path = r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\Raw Data Files'

# Path to the data dictionary (the data dictionary would be downloaded separately, not in the raw data Zip file)
path_to_data_dictionary= r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\collegescorecarddatadictionary_2021-04-01.xlsx'

# Create a folder named "Cleaned Data Files" to store output files
output_path= r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\Cleaned Data Files'
if not os.path.exists(output_path):
    os.mkdir(output_path)

# Create files list for FieldOfStudyData (data by field of study) and MERGED data (data by institution_level)
field_of_study_files = glob.glob(input_path + r'\FieldOfStudyData*.csv')
institution_level_files= glob.glob(input_path + r'\MERGED*.csv')



## Read all the "FieldOfStudy" files (data by field of study) and concat into one data frame
field_of_study_list = [] # create an empty list to store all field of study data frame

for filename in field_of_study_files:
    temp_df = pd.read_csv(filename, low_memory=False, index_col=False, na_values= ['NULL','PrivacySuppressed'],
                          dtype={'ACAD_YR': str, 'UNITID': str, 'OPEID6': str, 'INSTNM': str, 'CONTROL': str, 'MAIN': 'Int64',
                                'CIPCODE': str, 'CIPDESC': str, 'CREDLEV': 'Int64', 'CREDDESC': str, 'IPEDSCOUNT1': 'Int64', 'IPEDSCOUNT2': 'Int64',
                                'DEBT_ALL_STGP_ANY_N': 'Int64', 'DEBT_ALL_STGP_ANY_MEAN': 'Int64', 'DEBT_ALL_STGP_ANY_MDN': 'Int64', 'DEBT_ALL_STGP_EVAL_N': 'Int64', 'DEBT_ALL_STGP_EVAL_MEAN': 'Int64', 'DEBT_ALL_STGP_EVAL_MDN': 'Int64', 'DEBT_ALL_PP_ANY_N': 'Int64', 'DEBT_ALL_PP_ANY_MEAN': 'Int64', 'DEBT_ALL_PP_ANY_MDN': 'Int64', 'DEBT_ALL_PP_EVAL_N': 'Int64', 'DEBT_ALL_PP_EVAL_MEAN': 'Int64', 'DEBT_ALL_PP_EVAL_MDN': 'Int64', 'DEBT_MALE_STGP_ANY_N': 'Int64', 'DEBT_MALE_STGP_ANY_MEAN': 'Int64', 'DEBT_MALE_STGP_ANY_MDN': 'Int64', 'DEBT_MALE_STGP_EVAL_N': 'Int64', 'DEBT_MALE_STGP_EVAL_MEAN': 'Int64', 'DEBT_MALE_STGP_EVAL_MDN': 'Int64', 'DEBT_MALE_PP_ANY_N': 'Int64', 'DEBT_MALE_PP_ANY_MEAN': 'Int64', 'DEBT_MALE_PP_ANY_MDN': 'Int64', 'DEBT_MALE_PP_EVAL_N': 'Int64', 'DEBT_MALE_PP_EVAL_MEAN': 'Int64', 'DEBT_MALE_PP_EVAL_MDN': 'Int64', 'DEBT_NOTMALE_STGP_ANY_N': 'Int64', 'DEBT_NOTMALE_STGP_ANY_MEAN': 'Int64', 'DEBT_NOTMALE_STGP_ANY_MDN': 'Int64', 'DEBT_NOTMALE_STGP_EVAL_N': 'Int64', 'DEBT_NOTMALE_STGP_EVAL_MEAN': 'Int64', 'DEBT_NOTMALE_STGP_EVAL_MDN': 'Int64', 'DEBT_NOTMALE_PP_ANY_N': 'Int64', 'DEBT_NOTMALE_PP_ANY_MEAN': 'Int64', 'DEBT_NOTMALE_PP_ANY_MDN': 'Int64', 'DEBT_NOTMALE_PP_EVAL_N': 'Int64', 'DEBT_NOTMALE_PP_EVAL_MEAN': 'Int64', 'DEBT_NOTMALE_PP_EVAL_MDN': 'Int64', 'DEBT_PELL_STGP_ANY_N': 'Int64', 'DEBT_PELL_STGP_ANY_MEAN': 'Int64', 'DEBT_PELL_STGP_ANY_MDN': 'Int64', 'DEBT_PELL_STGP_EVAL_N': 'Int64', 'DEBT_PELL_STGP_EVAL_MEAN': 'Int64', 'DEBT_PELL_STGP_EVAL_MDN': 'Int64', 'DEBT_PELL_PP_ANY_N': 'Int64', 'DEBT_PELL_PP_ANY_MEAN': 'Int64', 'DEBT_PELL_PP_ANY_MDN': 'Int64', 'DEBT_PELL_PP_EVAL_N': 'Int64', 'DEBT_PELL_PP_EVAL_MEAN': 'Int64', 'DEBT_PELL_PP_EVAL_MDN': 'Int64', 'DEBT_NOPELL_STGP_ANY_N': 'Int64', 'DEBT_NOPELL_STGP_ANY_MEAN': 'Int64', 'DEBT_NOPELL_STGP_ANY_MDN': 'Int64', 'DEBT_NOPELL_STGP_EVAL_N': 'Int64', 'DEBT_NOPELL_STGP_EVAL_MEAN': 'Int64', 'DEBT_NOPELL_STGP_EVAL_MDN': 'Int64', 'DEBT_NOPELL_PP_ANY_N': 'Int64', 'DEBT_NOPELL_PP_ANY_MEAN': 'Int64', 'DEBT_NOPELL_PP_ANY_MDN': 'Int64', 'DEBT_NOPELL_PP_EVAL_N': 'Int64', 'DEBT_NOPELL_PP_EVAL_MEAN': 'Int64', 'DEBT_NOPELL_PP_EVAL_MDN': 'Int64',
                                'DEBT_ALL_PP_ANY_MDN10YRPAY': float, 'DEBT_ALL_PP_EVAL_MDN10YRPAY': float, 'DEBT_ALL_STGP_ANY_MDN10YRPAY': float, 'DEBT_ALL_STGP_EVAL_MDN10YRPAY': float,
                                'EARN_COUNT_NWNE_HI_1YR': 'Int64', 'EARN_CNTOVER150_HI_1YR': 'Int64', 'EARN_COUNT_WNE_HI_1YR': 'Int64', 'EARN_MDN_HI_1YR': 'Int64', 'EARN_COUNT_NWNE_HI_2YR': 'Int64', 'EARN_CNTOVER150_HI_2YR': 'Int64', 'EARN_COUNT_WNE_HI_2YR': 'Int64', 'EARN_MDN_HI_2YR': 'Int64',
                                'BBRR2_FED_COMP_N': 'Int64', 'BBRR2_FED_COMP_DFLT': float, 'BBRR2_FED_COMP_DLNQ': float, 'BBRR2_FED_COMP_FBR': float, 'BBRR2_FED_COMP_DFR': float, 'BBRR2_FED_COMP_NOPROG': float, 'BBRR2_FED_COMP_MAKEPROG': float, 'BBRR2_FED_COMP_PAIDINFULL': float, 'BBRR2_FED_COMP_DISCHARGE': float
                                }
                          )

    # create an indicator column named "ACAD_YR" to identify where rows originate from
    temp_df['ACAD_YR'] = re.findall(r'\d+_\d+', filename)[0]

    # shift column 'ACAD_YR' to first position
    first_column = temp_df.pop('ACAD_YR')
    temp_df.insert(0, 'ACAD_YR', first_column)

    # append all temp_df into one list
    field_of_study_list.append(temp_df)

# Concat 3 data frames into one data frame "field_of_study_data"
field_of_study_data = pd.concat(field_of_study_list, axis=0, ignore_index=True)

# Write to a csv file
field_of_study_data.to_csv(f'{output_path}/field_of_study_data.csv', index= False, header= True)



## Read all the "MERGED" files (data by institution level) and concat into one data frame
institution_level_list = [] # create an empty list to store all institution level data frame

# Keep only 1527 columns ['VARIABLE NAME'], exclude 875 columns
columns_to_read= """
                UNITID
                OPEID
                OPEID6
                INSTNM
                CITY
                STABBR
                ZIP
                ACCREDAGENCY
                SCH_DEG
                HCM2
                MAIN
                NUMBRANCH
                PREDDEG
                HIGHDEG
                CONTROL
                ST_FIPS
                REGION
                LOCALE
                CCBASIC
                CCUGPROF
                CCSIZSET
                HBCU
                PBI
                ANNHI
                TRIBAL
                AANAPII
                HSI
                NANTI
                MENONLY
                WOMENONLY
                RELAFFIL
                ADM_RATE
                ADM_RATE_ALL
                SATVR25
                SATVR75
                SATMT25
                SATMT75
                SATWR25
                SATWR75
                SATVRMID
                SATMTMID
                SATWRMID
                ACTCM25
                ACTCM75
                ACTEN25
                ACTEN75
                ACTMT25
                ACTMT75
                ACTWR25
                ACTWR75
                ACTCMMID
                ACTENMID
                ACTMTMID
                ACTWRMID
                SAT_AVG
                SAT_AVG_ALL
                PCIP01
                PCIP03
                PCIP04
                PCIP05
                PCIP09
                PCIP10
                PCIP11
                PCIP12
                PCIP13
                PCIP14
                PCIP15
                PCIP16
                PCIP19
                PCIP22
                PCIP23
                PCIP24
                PCIP25
                PCIP26
                PCIP27
                PCIP29
                PCIP30
                PCIP31
                PCIP38
                PCIP39
                PCIP40
                PCIP41
                PCIP42
                PCIP43
                PCIP44
                PCIP45
                PCIP46
                PCIP47
                PCIP48
                PCIP49
                PCIP50
                PCIP51
                PCIP52
                PCIP54
                CIP01CERT1
                CIP01CERT2
                CIP01ASSOC
                CIP01CERT4
                CIP01BACHL
                CIP03CERT1
                CIP03CERT2
                CIP03ASSOC
                CIP03CERT4
                CIP03BACHL
                CIP04CERT1
                CIP04CERT2
                CIP04ASSOC
                CIP04CERT4
                CIP04BACHL
                CIP05CERT1
                CIP05CERT2
                CIP05ASSOC
                CIP05CERT4
                CIP05BACHL
                CIP09CERT1
                CIP09CERT2
                CIP09ASSOC
                CIP09CERT4
                CIP09BACHL
                CIP10CERT1
                CIP10CERT2
                CIP10ASSOC
                CIP10CERT4
                CIP10BACHL
                CIP11CERT1
                CIP11CERT2
                CIP11ASSOC
                CIP11CERT4
                CIP11BACHL
                CIP12CERT1
                CIP12CERT2
                CIP12ASSOC
                CIP12CERT4
                CIP12BACHL
                CIP13CERT1
                CIP13CERT2
                CIP13ASSOC
                CIP13CERT4
                CIP13BACHL
                CIP14CERT1
                CIP14CERT2
                CIP14ASSOC
                CIP14CERT4
                CIP14BACHL
                CIP15CERT1
                CIP15CERT2
                CIP15ASSOC
                CIP15CERT4
                CIP15BACHL
                CIP16CERT1
                CIP16CERT2
                CIP16ASSOC
                CIP16CERT4
                CIP16BACHL
                CIP19CERT1
                CIP19CERT2
                CIP19ASSOC
                CIP19CERT4
                CIP19BACHL
                CIP22CERT1
                CIP22CERT2
                CIP22ASSOC
                CIP22CERT4
                CIP22BACHL
                CIP23CERT1
                CIP23CERT2
                CIP23ASSOC
                CIP23CERT4
                CIP23BACHL
                CIP24CERT1
                CIP24CERT2
                CIP24ASSOC
                CIP24CERT4
                CIP24BACHL
                CIP25CERT1
                CIP25CERT2
                CIP25ASSOC
                CIP25CERT4
                CIP25BACHL
                CIP26CERT1
                CIP26CERT2
                CIP26ASSOC
                CIP26CERT4
                CIP26BACHL
                CIP27CERT1
                CIP27CERT2
                CIP27ASSOC
                CIP27CERT4
                CIP27BACHL
                CIP29CERT1
                CIP29CERT2
                CIP29ASSOC
                CIP29CERT4
                CIP29BACHL
                CIP30CERT1
                CIP30CERT2
                CIP30ASSOC
                CIP30CERT4
                CIP30BACHL
                CIP31CERT1
                CIP31CERT2
                CIP31ASSOC
                CIP31CERT4
                CIP31BACHL
                CIP38CERT1
                CIP38CERT2
                CIP38ASSOC
                CIP38CERT4
                CIP38BACHL
                CIP39CERT1
                CIP39CERT2
                CIP39ASSOC
                CIP39CERT4
                CIP39BACHL
                CIP40CERT1
                CIP40CERT2
                CIP40ASSOC
                CIP40CERT4
                CIP40BACHL
                CIP41CERT1
                CIP41CERT2
                CIP41ASSOC
                CIP41CERT4
                CIP41BACHL
                CIP42CERT1
                CIP42CERT2
                CIP42ASSOC
                CIP42CERT4
                CIP42BACHL
                CIP43CERT1
                CIP43CERT2
                CIP43ASSOC
                CIP43CERT4
                CIP43BACHL
                CIP44CERT1
                CIP44CERT2
                CIP44ASSOC
                CIP44CERT4
                CIP44BACHL
                CIP45CERT1
                CIP45CERT2
                CIP45ASSOC
                CIP45CERT4
                CIP45BACHL
                CIP46CERT1
                CIP46CERT2
                CIP46ASSOC
                CIP46CERT4
                CIP46BACHL
                CIP47CERT1
                CIP47CERT2
                CIP47ASSOC
                CIP47CERT4
                CIP47BACHL
                CIP48CERT1
                CIP48CERT2
                CIP48ASSOC
                CIP48CERT4
                CIP48BACHL
                CIP49CERT1
                CIP49CERT2
                CIP49ASSOC
                CIP49CERT4
                CIP49BACHL
                CIP50CERT1
                CIP50CERT2
                CIP50ASSOC
                CIP50CERT4
                CIP50BACHL
                CIP51CERT1
                CIP51CERT2
                CIP51ASSOC
                CIP51CERT4
                CIP51BACHL
                CIP52CERT1
                CIP52CERT2
                CIP52ASSOC
                CIP52CERT4
                CIP52BACHL
                CIP54CERT1
                CIP54CERT2
                CIP54ASSOC
                CIP54CERT4
                CIP54BACHL
                DISTANCEONLY
                UGDS
                UG
                UGDS_WHITE
                UGDS_BLACK
                UGDS_HISP
                UGDS_ASIAN
                UGDS_AIAN
                UGDS_NHPI
                UGDS_2MOR
                UGDS_NRA
                UGDS_UNKN
                UGDS_WHITENH
                UGDS_BLACKNH
                UGDS_API
                UGDS_AIANOLD
                UGDS_HISPOLD
                UG_NRA
                UG_UNKN
                UG_WHITENH
                UG_BLACKNH
                UG_API
                UG_AIANOLD
                UG_HISPOLD
                PPTUG_EF
                PPTUG_EF2
                CURROPER
                NPT4_PUB
                NPT4_PRIV
                NPT4_PROG
                NPT4_OTHER
                NPT41_PUB
                NPT42_PUB
                NPT43_PUB
                NPT44_PUB
                NPT45_PUB
                NPT41_PRIV
                NPT42_PRIV
                NPT43_PRIV
                NPT44_PRIV
                NPT45_PRIV
                NPT41_PROG
                NPT42_PROG
                NPT43_PROG
                NPT44_PROG
                NPT45_PROG
                NPT41_OTHER
                NPT42_OTHER
                NPT43_OTHER
                NPT44_OTHER
                NPT45_OTHER
                NPT4_048_PUB
                NPT4_048_PRIV
                NPT4_048_PROG
                NPT4_048_OTHER
                NPT4_3075_PUB
                NPT4_3075_PRIV
                NPT4_75UP_PUB
                NPT4_75UP_PRIV
                NPT4_3075_PROG
                NPT4_3075_OTHER
                NPT4_75UP_PROG
                NPT4_75UP_OTHER
                NUM4_PUB
                NUM4_PRIV
                NUM4_PROG
                NUM4_OTHER
                NUM41_PUB
                NUM42_PUB
                NUM43_PUB
                NUM44_PUB
                NUM45_PUB
                NUM41_PRIV
                NUM42_PRIV
                NUM43_PRIV
                NUM44_PRIV
                NUM45_PRIV
                NUM41_PROG
                NUM42_PROG
                NUM43_PROG
                NUM44_PROG
                NUM45_PROG
                NUM41_OTHER
                NUM42_OTHER
                NUM43_OTHER
                NUM44_OTHER
                NUM45_OTHER
                COSTT4_A
                COSTT4_P
                TUITIONFEE_IN
                TUITIONFEE_OUT
                TUITIONFEE_PROG
                TUITFTE
                INEXPFTE
                AVGFACSAL
                PFTFAC
                PCTPELL
                C150_4
                C150_L4
                C150_4_POOLED
                C150_L4_POOLED
                POOLYRS
                PFTFTUG1_EF
                C150_4_WHITE
                C150_4_BLACK
                C150_4_HISP
                C150_4_ASIAN
                C150_4_AIAN
                C150_4_NHPI
                C150_4_2MOR
                C150_4_NRA
                C150_4_UNKN
                C150_4_WHITENH
                C150_4_BLACKNH
                C150_4_API
                C150_4_AIANOLD
                C150_4_HISPOLD
                C150_L4_WHITE
                C150_L4_BLACK
                C150_L4_HISP
                C150_L4_ASIAN
                C150_L4_AIAN
                C150_L4_NHPI
                C150_L4_2MOR
                C150_L4_NRA
                C150_L4_UNKN
                C150_L4_WHITENH
                C150_L4_BLACKNH
                C150_L4_API
                C150_L4_AIANOLD
                C150_L4_HISPOLD
                C200_4
                C200_L4
                D200_4
                D200_L4
                RET_FT4
                RET_FTL4
                RET_PT4
                RET_PTL4
                C200_4_POOLED
                C200_L4_POOLED
                POOLYRS200
                PCTFLOAN
                UG25ABV
                CDR2
                CDR3
                DEATH_YR2_RT
                COMP_ORIG_YR2_RT
                COMP_4YR_TRANS_YR2_RT
                COMP_2YR_TRANS_YR2_RT
                WDRAW_ORIG_YR2_RT
                WDRAW_4YR_TRANS_YR2_RT
                WDRAW_2YR_TRANS_YR2_RT
                ENRL_ORIG_YR2_RT
                ENRL_4YR_TRANS_YR2_RT
                ENRL_2YR_TRANS_YR2_RT
                UNKN_ORIG_YR2_RT
                UNKN_4YR_TRANS_YR2_RT
                UNKN_2YR_TRANS_YR2_RT
                LO_INC_DEATH_YR2_RT
                LO_INC_COMP_ORIG_YR2_RT
                LO_INC_COMP_4YR_TRANS_YR2_RT
                LO_INC_COMP_2YR_TRANS_YR2_RT
                LO_INC_WDRAW_ORIG_YR2_RT
                LO_INC_WDRAW_4YR_TRANS_YR2_RT
                LO_INC_WDRAW_2YR_TRANS_YR2_RT
                LO_INC_ENRL_ORIG_YR2_RT
                LO_INC_ENRL_4YR_TRANS_YR2_RT
                LO_INC_ENRL_2YR_TRANS_YR2_RT
                LO_INC_UNKN_ORIG_YR2_RT
                LO_INC_UNKN_4YR_TRANS_YR2_RT
                LO_INC_UNKN_2YR_TRANS_YR2_RT
                MD_INC_DEATH_YR2_RT
                MD_INC_COMP_ORIG_YR2_RT
                MD_INC_COMP_4YR_TRANS_YR2_RT
                MD_INC_COMP_2YR_TRANS_YR2_RT
                MD_INC_WDRAW_ORIG_YR2_RT
                MD_INC_WDRAW_4YR_TRANS_YR2_RT
                MD_INC_WDRAW_2YR_TRANS_YR2_RT
                MD_INC_ENRL_ORIG_YR2_RT
                MD_INC_ENRL_4YR_TRANS_YR2_RT
                MD_INC_ENRL_2YR_TRANS_YR2_RT
                MD_INC_UNKN_ORIG_YR2_RT
                MD_INC_UNKN_4YR_TRANS_YR2_RT
                MD_INC_UNKN_2YR_TRANS_YR2_RT
                HI_INC_DEATH_YR2_RT
                HI_INC_COMP_ORIG_YR2_RT
                HI_INC_COMP_4YR_TRANS_YR2_RT
                HI_INC_COMP_2YR_TRANS_YR2_RT
                HI_INC_WDRAW_ORIG_YR2_RT
                HI_INC_WDRAW_4YR_TRANS_YR2_RT
                HI_INC_WDRAW_2YR_TRANS_YR2_RT
                HI_INC_ENRL_ORIG_YR2_RT
                HI_INC_ENRL_4YR_TRANS_YR2_RT
                HI_INC_ENRL_2YR_TRANS_YR2_RT
                HI_INC_UNKN_ORIG_YR2_RT
                HI_INC_UNKN_4YR_TRANS_YR2_RT
                HI_INC_UNKN_2YR_TRANS_YR2_RT
                DEP_DEATH_YR2_RT
                DEP_COMP_ORIG_YR2_RT
                DEP_COMP_4YR_TRANS_YR2_RT
                DEP_COMP_2YR_TRANS_YR2_RT
                DEP_WDRAW_ORIG_YR2_RT
                DEP_WDRAW_4YR_TRANS_YR2_RT
                DEP_WDRAW_2YR_TRANS_YR2_RT
                DEP_ENRL_ORIG_YR2_RT
                DEP_ENRL_4YR_TRANS_YR2_RT
                DEP_ENRL_2YR_TRANS_YR2_RT
                DEP_UNKN_ORIG_YR2_RT
                DEP_UNKN_4YR_TRANS_YR2_RT
                DEP_UNKN_2YR_TRANS_YR2_RT
                IND_DEATH_YR2_RT
                IND_COMP_ORIG_YR2_RT
                IND_COMP_4YR_TRANS_YR2_RT
                IND_COMP_2YR_TRANS_YR2_RT
                IND_WDRAW_ORIG_YR2_RT
                IND_WDRAW_4YR_TRANS_YR2_RT
                IND_WDRAW_2YR_TRANS_YR2_RT
                IND_ENRL_ORIG_YR2_RT
                IND_ENRL_4YR_TRANS_YR2_RT
                IND_ENRL_2YR_TRANS_YR2_RT
                IND_UNKN_ORIG_YR2_RT
                IND_UNKN_4YR_TRANS_YR2_RT
                IND_UNKN_2YR_TRANS_YR2_RT
                FEMALE_DEATH_YR2_RT
                FEMALE_COMP_ORIG_YR2_RT
                FEMALE_COMP_4YR_TRANS_YR2_RT
                FEMALE_COMP_2YR_TRANS_YR2_RT
                FEMALE_WDRAW_ORIG_YR2_RT
                FEMALE_WDRAW_4YR_TRANS_YR2_RT
                FEMALE_WDRAW_2YR_TRANS_YR2_RT
                FEMALE_ENRL_ORIG_YR2_RT
                FEMALE_ENRL_4YR_TRANS_YR2_RT
                FEMALE_ENRL_2YR_TRANS_YR2_RT
                FEMALE_UNKN_ORIG_YR2_RT
                FEMALE_UNKN_4YR_TRANS_YR2_RT
                FEMALE_UNKN_2YR_TRANS_YR2_RT
                MALE_DEATH_YR2_RT
                MALE_COMP_ORIG_YR2_RT
                MALE_COMP_4YR_TRANS_YR2_RT
                MALE_COMP_2YR_TRANS_YR2_RT
                MALE_WDRAW_ORIG_YR2_RT
                MALE_WDRAW_4YR_TRANS_YR2_RT
                MALE_WDRAW_2YR_TRANS_YR2_RT
                MALE_ENRL_ORIG_YR2_RT
                MALE_ENRL_4YR_TRANS_YR2_RT
                MALE_ENRL_2YR_TRANS_YR2_RT
                MALE_UNKN_ORIG_YR2_RT
                MALE_UNKN_4YR_TRANS_YR2_RT
                MALE_UNKN_2YR_TRANS_YR2_RT
                PELL_DEATH_YR2_RT
                PELL_COMP_ORIG_YR2_RT
                PELL_COMP_4YR_TRANS_YR2_RT
                PELL_COMP_2YR_TRANS_YR2_RT
                PELL_WDRAW_ORIG_YR2_RT
                PELL_WDRAW_4YR_TRANS_YR2_RT
                PELL_WDRAW_2YR_TRANS_YR2_RT
                PELL_ENRL_ORIG_YR2_RT
                PELL_ENRL_4YR_TRANS_YR2_RT
                PELL_ENRL_2YR_TRANS_YR2_RT
                PELL_UNKN_ORIG_YR2_RT
                PELL_UNKN_4YR_TRANS_YR2_RT
                PELL_UNKN_2YR_TRANS_YR2_RT
                NOPELL_DEATH_YR2_RT
                NOPELL_COMP_ORIG_YR2_RT
                NOPELL_COMP_4YR_TRANS_YR2_RT
                NOPELL_COMP_2YR_TRANS_YR2_RT
                NOPELL_WDRAW_ORIG_YR2_RT
                NOPELL_WDRAW_4YR_TRANS_YR2_RT
                NOPELL_WDRAW_2YR_TRANS_YR2_RT
                NOPELL_ENRL_ORIG_YR2_RT
                NOPELL_ENRL_4YR_TRANS_YR2_RT
                NOPELL_ENRL_2YR_TRANS_YR2_RT
                NOPELL_UNKN_ORIG_YR2_RT
                NOPELL_UNKN_4YR_TRANS_YR2_RT
                NOPELL_UNKN_2YR_TRANS_YR2_RT
                FIRSTGEN_DEATH_YR2_RT
                FIRSTGEN_COMP_ORIG_YR2_RT
                FIRSTGEN_COMP_4YR_TRANS_YR2_RT
                FIRSTGEN_COMP_2YR_TRANS_YR2_RT
                FIRSTGEN_WDRAW_ORIG_YR2_RT
                FIRSTGEN_WDRAW_4YR_TRANS_YR2_RT
                FIRSTGEN_WDRAW_2YR_TRANS_YR2_RT
                FIRSTGEN_ENRL_ORIG_YR2_RT
                FIRSTGEN_ENRL_4YR_TRANS_YR2_RT
                FIRSTGEN_ENRL_2YR_TRANS_YR2_RT
                FIRSTGEN_UNKN_ORIG_YR2_RT
                FIRSTGEN_UNKN_4YR_TRANS_YR2_RT
                FIRSTGEN_UNKN_2YR_TRANS_YR2_RT
                NOT1STGEN_DEATH_YR2_RT
                NOT1STGEN_COMP_ORIG_YR2_RT
                NOT1STGEN_COMP_4YR_TRANS_YR2_RT
                NOT1STGEN_COMP_2YR_TRANS_YR2_RT
                NOT1STGEN_WDRAW_ORIG_YR2_RT
                NOT1STGEN_WDRAW_4YR_TRANS_YR2_RT
                NOT1STGEN_WDRAW_2YR_TRANS_YR2_RT
                NOT1STGEN_ENRL_ORIG_YR2_RT
                NOT1STGEN_ENRL_4YR_TRANS_YR2_RT
                NOT1STGEN_ENRL_2YR_TRANS_YR2_RT
                NOT1STGEN_UNKN_ORIG_YR2_RT
                NOT1STGEN_UNKN_4YR_TRANS_YR2_RT
                NOT1STGEN_UNKN_2YR_TRANS_YR2_RT
                DEATH_YR3_RT
                COMP_ORIG_YR3_RT
                COMP_4YR_TRANS_YR3_RT
                COMP_2YR_TRANS_YR3_RT
                WDRAW_ORIG_YR3_RT
                WDRAW_4YR_TRANS_YR3_RT
                WDRAW_2YR_TRANS_YR3_RT
                ENRL_ORIG_YR3_RT
                ENRL_4YR_TRANS_YR3_RT
                ENRL_2YR_TRANS_YR3_RT
                UNKN_ORIG_YR3_RT
                UNKN_4YR_TRANS_YR3_RT
                UNKN_2YR_TRANS_YR3_RT
                LO_INC_DEATH_YR3_RT
                LO_INC_COMP_ORIG_YR3_RT
                LO_INC_COMP_4YR_TRANS_YR3_RT
                LO_INC_COMP_2YR_TRANS_YR3_RT
                LO_INC_WDRAW_ORIG_YR3_RT
                LO_INC_WDRAW_4YR_TRANS_YR3_RT
                LO_INC_WDRAW_2YR_TRANS_YR3_RT
                LO_INC_ENRL_ORIG_YR3_RT
                LO_INC_ENRL_4YR_TRANS_YR3_RT
                LO_INC_ENRL_2YR_TRANS_YR3_RT
                LO_INC_UNKN_ORIG_YR3_RT
                LO_INC_UNKN_4YR_TRANS_YR3_RT
                LO_INC_UNKN_2YR_TRANS_YR3_RT
                MD_INC_DEATH_YR3_RT
                MD_INC_COMP_ORIG_YR3_RT
                MD_INC_COMP_4YR_TRANS_YR3_RT
                MD_INC_COMP_2YR_TRANS_YR3_RT
                MD_INC_WDRAW_ORIG_YR3_RT
                MD_INC_WDRAW_4YR_TRANS_YR3_RT
                MD_INC_WDRAW_2YR_TRANS_YR3_RT
                MD_INC_ENRL_ORIG_YR3_RT
                MD_INC_ENRL_4YR_TRANS_YR3_RT
                MD_INC_ENRL_2YR_TRANS_YR3_RT
                MD_INC_UNKN_ORIG_YR3_RT
                MD_INC_UNKN_4YR_TRANS_YR3_RT
                MD_INC_UNKN_2YR_TRANS_YR3_RT
                HI_INC_DEATH_YR3_RT
                HI_INC_COMP_ORIG_YR3_RT
                HI_INC_COMP_4YR_TRANS_YR3_RT
                HI_INC_COMP_2YR_TRANS_YR3_RT
                HI_INC_WDRAW_ORIG_YR3_RT
                HI_INC_WDRAW_4YR_TRANS_YR3_RT
                HI_INC_WDRAW_2YR_TRANS_YR3_RT
                HI_INC_ENRL_ORIG_YR3_RT
                HI_INC_ENRL_4YR_TRANS_YR3_RT
                HI_INC_ENRL_2YR_TRANS_YR3_RT
                HI_INC_UNKN_ORIG_YR3_RT
                HI_INC_UNKN_4YR_TRANS_YR3_RT
                HI_INC_UNKN_2YR_TRANS_YR3_RT
                DEP_DEATH_YR3_RT
                DEP_COMP_ORIG_YR3_RT
                DEP_COMP_4YR_TRANS_YR3_RT
                DEP_COMP_2YR_TRANS_YR3_RT
                DEP_WDRAW_ORIG_YR3_RT
                DEP_WDRAW_4YR_TRANS_YR3_RT
                DEP_WDRAW_2YR_TRANS_YR3_RT
                DEP_ENRL_ORIG_YR3_RT
                DEP_ENRL_4YR_TRANS_YR3_RT
                DEP_ENRL_2YR_TRANS_YR3_RT
                DEP_UNKN_ORIG_YR3_RT
                DEP_UNKN_4YR_TRANS_YR3_RT
                DEP_UNKN_2YR_TRANS_YR3_RT
                IND_DEATH_YR3_RT
                IND_COMP_ORIG_YR3_RT
                IND_COMP_4YR_TRANS_YR3_RT
                IND_COMP_2YR_TRANS_YR3_RT
                IND_WDRAW_ORIG_YR3_RT
                IND_WDRAW_4YR_TRANS_YR3_RT
                IND_WDRAW_2YR_TRANS_YR3_RT
                IND_ENRL_ORIG_YR3_RT
                IND_ENRL_4YR_TRANS_YR3_RT
                IND_ENRL_2YR_TRANS_YR3_RT
                IND_UNKN_ORIG_YR3_RT
                IND_UNKN_4YR_TRANS_YR3_RT
                IND_UNKN_2YR_TRANS_YR3_RT
                FEMALE_DEATH_YR3_RT
                FEMALE_COMP_ORIG_YR3_RT
                FEMALE_COMP_4YR_TRANS_YR3_RT
                FEMALE_COMP_2YR_TRANS_YR3_RT
                FEMALE_WDRAW_ORIG_YR3_RT
                FEMALE_WDRAW_4YR_TRANS_YR3_RT
                FEMALE_WDRAW_2YR_TRANS_YR3_RT
                FEMALE_ENRL_ORIG_YR3_RT
                FEMALE_ENRL_4YR_TRANS_YR3_RT
                FEMALE_ENRL_2YR_TRANS_YR3_RT
                FEMALE_UNKN_ORIG_YR3_RT
                FEMALE_UNKN_4YR_TRANS_YR3_RT
                FEMALE_UNKN_2YR_TRANS_YR3_RT
                MALE_DEATH_YR3_RT
                MALE_COMP_ORIG_YR3_RT
                MALE_COMP_4YR_TRANS_YR3_RT
                MALE_COMP_2YR_TRANS_YR3_RT
                MALE_WDRAW_ORIG_YR3_RT
                MALE_WDRAW_4YR_TRANS_YR3_RT
                MALE_WDRAW_2YR_TRANS_YR3_RT
                MALE_ENRL_ORIG_YR3_RT
                MALE_ENRL_4YR_TRANS_YR3_RT
                MALE_ENRL_2YR_TRANS_YR3_RT
                MALE_UNKN_ORIG_YR3_RT
                MALE_UNKN_4YR_TRANS_YR3_RT
                MALE_UNKN_2YR_TRANS_YR3_RT
                PELL_DEATH_YR3_RT
                PELL_COMP_ORIG_YR3_RT
                PELL_COMP_4YR_TRANS_YR3_RT
                PELL_COMP_2YR_TRANS_YR3_RT
                PELL_WDRAW_ORIG_YR3_RT
                PELL_WDRAW_4YR_TRANS_YR3_RT
                PELL_WDRAW_2YR_TRANS_YR3_RT
                PELL_ENRL_ORIG_YR3_RT
                PELL_ENRL_4YR_TRANS_YR3_RT
                PELL_ENRL_2YR_TRANS_YR3_RT
                PELL_UNKN_ORIG_YR3_RT
                PELL_UNKN_4YR_TRANS_YR3_RT
                PELL_UNKN_2YR_TRANS_YR3_RT
                NOPELL_DEATH_YR3_RT
                NOPELL_COMP_ORIG_YR3_RT
                NOPELL_COMP_4YR_TRANS_YR3_RT
                NOPELL_COMP_2YR_TRANS_YR3_RT
                NOPELL_WDRAW_ORIG_YR3_RT
                NOPELL_WDRAW_4YR_TRANS_YR3_RT
                NOPELL_WDRAW_2YR_TRANS_YR3_RT
                NOPELL_ENRL_ORIG_YR3_RT
                NOPELL_ENRL_4YR_TRANS_YR3_RT
                NOPELL_ENRL_2YR_TRANS_YR3_RT
                NOPELL_UNKN_ORIG_YR3_RT
                NOPELL_UNKN_4YR_TRANS_YR3_RT
                NOPELL_UNKN_2YR_TRANS_YR3_RT
                FIRSTGEN_DEATH_YR3_RT
                FIRSTGEN_COMP_ORIG_YR3_RT
                FIRSTGEN_COMP_4YR_TRANS_YR3_RT
                FIRSTGEN_COMP_2YR_TRANS_YR3_RT
                FIRSTGEN_WDRAW_ORIG_YR3_RT
                FIRSTGEN_WDRAW_4YR_TRANS_YR3_RT
                FIRSTGEN_WDRAW_2YR_TRANS_YR3_RT
                FIRSTGEN_ENRL_ORIG_YR3_RT
                FIRSTGEN_ENRL_4YR_TRANS_YR3_RT
                FIRSTGEN_ENRL_2YR_TRANS_YR3_RT
                FIRSTGEN_UNKN_ORIG_YR3_RT
                FIRSTGEN_UNKN_4YR_TRANS_YR3_RT
                FIRSTGEN_UNKN_2YR_TRANS_YR3_RT
                NOT1STGEN_DEATH_YR3_RT
                NOT1STGEN_COMP_ORIG_YR3_RT
                NOT1STGEN_COMP_4YR_TRANS_YR3_RT
                NOT1STGEN_COMP_2YR_TRANS_YR3_RT
                NOT1STGEN_WDRAW_ORIG_YR3_RT
                NOT1STGEN_WDRAW_4YR_TRANS_YR3_RT
                NOT1STGEN_WDRAW_2YR_TRANS_YR3_RT
                NOT1STGEN_ENRL_ORIG_YR3_RT
                NOT1STGEN_ENRL_4YR_TRANS_YR3_RT
                NOT1STGEN_ENRL_2YR_TRANS_YR3_RT
                NOT1STGEN_UNKN_ORIG_YR3_RT
                NOT1STGEN_UNKN_4YR_TRANS_YR3_RT
                NOT1STGEN_UNKN_2YR_TRANS_YR3_RT
                DEATH_YR4_RT
                COMP_ORIG_YR4_RT
                COMP_4YR_TRANS_YR4_RT
                COMP_2YR_TRANS_YR4_RT
                WDRAW_ORIG_YR4_RT
                WDRAW_4YR_TRANS_YR4_RT
                WDRAW_2YR_TRANS_YR4_RT
                ENRL_ORIG_YR4_RT
                ENRL_4YR_TRANS_YR4_RT
                ENRL_2YR_TRANS_YR4_RT
                UNKN_ORIG_YR4_RT
                UNKN_4YR_TRANS_YR4_RT
                UNKN_2YR_TRANS_YR4_RT
                LO_INC_DEATH_YR4_RT
                LO_INC_COMP_ORIG_YR4_RT
                LO_INC_COMP_4YR_TRANS_YR4_RT
                LO_INC_COMP_2YR_TRANS_YR4_RT
                LO_INC_WDRAW_ORIG_YR4_RT
                LO_INC_WDRAW_4YR_TRANS_YR4_RT
                LO_INC_WDRAW_2YR_TRANS_YR4_RT
                LO_INC_ENRL_ORIG_YR4_RT
                LO_INC_ENRL_4YR_TRANS_YR4_RT
                LO_INC_ENRL_2YR_TRANS_YR4_RT
                LO_INC_UNKN_ORIG_YR4_RT
                LO_INC_UNKN_4YR_TRANS_YR4_RT
                LO_INC_UNKN_2YR_TRANS_YR4_RT
                MD_INC_DEATH_YR4_RT
                MD_INC_COMP_ORIG_YR4_RT
                MD_INC_COMP_4YR_TRANS_YR4_RT
                MD_INC_COMP_2YR_TRANS_YR4_RT
                MD_INC_WDRAW_ORIG_YR4_RT
                MD_INC_WDRAW_4YR_TRANS_YR4_RT
                MD_INC_WDRAW_2YR_TRANS_YR4_RT
                MD_INC_ENRL_ORIG_YR4_RT
                MD_INC_ENRL_4YR_TRANS_YR4_RT
                MD_INC_ENRL_2YR_TRANS_YR4_RT
                MD_INC_UNKN_ORIG_YR4_RT
                MD_INC_UNKN_4YR_TRANS_YR4_RT
                MD_INC_UNKN_2YR_TRANS_YR4_RT
                HI_INC_DEATH_YR4_RT
                HI_INC_COMP_ORIG_YR4_RT
                HI_INC_COMP_4YR_TRANS_YR4_RT
                HI_INC_COMP_2YR_TRANS_YR4_RT
                HI_INC_WDRAW_ORIG_YR4_RT
                HI_INC_WDRAW_4YR_TRANS_YR4_RT
                HI_INC_WDRAW_2YR_TRANS_YR4_RT
                HI_INC_ENRL_ORIG_YR4_RT
                HI_INC_ENRL_4YR_TRANS_YR4_RT
                HI_INC_ENRL_2YR_TRANS_YR4_RT
                HI_INC_UNKN_ORIG_YR4_RT
                HI_INC_UNKN_4YR_TRANS_YR4_RT
                HI_INC_UNKN_2YR_TRANS_YR4_RT
                DEP_DEATH_YR4_RT
                DEP_COMP_ORIG_YR4_RT
                DEP_COMP_4YR_TRANS_YR4_RT
                DEP_COMP_2YR_TRANS_YR4_RT
                DEP_WDRAW_ORIG_YR4_RT
                DEP_WDRAW_4YR_TRANS_YR4_RT
                DEP_WDRAW_2YR_TRANS_YR4_RT
                DEP_ENRL_ORIG_YR4_RT
                DEP_ENRL_4YR_TRANS_YR4_RT
                DEP_ENRL_2YR_TRANS_YR4_RT
                DEP_UNKN_ORIG_YR4_RT
                DEP_UNKN_4YR_TRANS_YR4_RT
                DEP_UNKN_2YR_TRANS_YR4_RT
                IND_DEATH_YR4_RT
                IND_COMP_ORIG_YR4_RT
                IND_COMP_4YR_TRANS_YR4_RT
                IND_COMP_2YR_TRANS_YR4_RT
                IND_WDRAW_ORIG_YR4_RT
                IND_WDRAW_4YR_TRANS_YR4_RT
                IND_WDRAW_2YR_TRANS_YR4_RT
                IND_ENRL_ORIG_YR4_RT
                IND_ENRL_4YR_TRANS_YR4_RT
                IND_ENRL_2YR_TRANS_YR4_RT
                IND_UNKN_ORIG_YR4_RT
                IND_UNKN_4YR_TRANS_YR4_RT
                IND_UNKN_2YR_TRANS_YR4_RT
                FEMALE_DEATH_YR4_RT
                FEMALE_COMP_ORIG_YR4_RT
                FEMALE_COMP_4YR_TRANS_YR4_RT
                FEMALE_COMP_2YR_TRANS_YR4_RT
                FEMALE_WDRAW_ORIG_YR4_RT
                FEMALE_WDRAW_4YR_TRANS_YR4_RT
                FEMALE_WDRAW_2YR_TRANS_YR4_RT
                FEMALE_ENRL_ORIG_YR4_RT
                FEMALE_ENRL_4YR_TRANS_YR4_RT
                FEMALE_ENRL_2YR_TRANS_YR4_RT
                FEMALE_UNKN_ORIG_YR4_RT
                FEMALE_UNKN_4YR_TRANS_YR4_RT
                FEMALE_UNKN_2YR_TRANS_YR4_RT
                MALE_DEATH_YR4_RT
                MALE_COMP_ORIG_YR4_RT
                MALE_COMP_4YR_TRANS_YR4_RT
                MALE_COMP_2YR_TRANS_YR4_RT
                MALE_WDRAW_ORIG_YR4_RT
                MALE_WDRAW_4YR_TRANS_YR4_RT
                MALE_WDRAW_2YR_TRANS_YR4_RT
                MALE_ENRL_ORIG_YR4_RT
                MALE_ENRL_4YR_TRANS_YR4_RT
                MALE_ENRL_2YR_TRANS_YR4_RT
                MALE_UNKN_ORIG_YR4_RT
                MALE_UNKN_4YR_TRANS_YR4_RT
                MALE_UNKN_2YR_TRANS_YR4_RT
                PELL_DEATH_YR4_RT
                PELL_COMP_ORIG_YR4_RT
                PELL_COMP_4YR_TRANS_YR4_RT
                PELL_COMP_2YR_TRANS_YR4_RT
                PELL_WDRAW_ORIG_YR4_RT
                PELL_WDRAW_4YR_TRANS_YR4_RT
                PELL_WDRAW_2YR_TRANS_YR4_RT
                PELL_ENRL_ORIG_YR4_RT
                PELL_ENRL_4YR_TRANS_YR4_RT
                PELL_ENRL_2YR_TRANS_YR4_RT
                PELL_UNKN_ORIG_YR4_RT
                PELL_UNKN_4YR_TRANS_YR4_RT
                PELL_UNKN_2YR_TRANS_YR4_RT
                NOPELL_DEATH_YR4_RT
                NOPELL_COMP_ORIG_YR4_RT
                NOPELL_COMP_4YR_TRANS_YR4_RT
                NOPELL_COMP_2YR_TRANS_YR4_RT
                NOPELL_WDRAW_ORIG_YR4_RT
                NOPELL_WDRAW_4YR_TRANS_YR4_RT
                NOPELL_WDRAW_2YR_TRANS_YR4_RT
                NOPELL_ENRL_ORIG_YR4_RT
                NOPELL_ENRL_4YR_TRANS_YR4_RT
                NOPELL_ENRL_2YR_TRANS_YR4_RT
                NOPELL_UNKN_ORIG_YR4_RT
                NOPELL_UNKN_4YR_TRANS_YR4_RT
                NOPELL_UNKN_2YR_TRANS_YR4_RT
                FIRSTGEN_DEATH_YR4_RT
                FIRSTGEN_COMP_ORIG_YR4_RT
                FIRSTGEN_COMP_4YR_TRANS_YR4_RT
                FIRSTGEN_COMP_2YR_TRANS_YR4_RT
                FIRSTGEN_WDRAW_ORIG_YR4_RT
                FIRSTGEN_WDRAW_4YR_TRANS_YR4_RT
                FIRSTGEN_WDRAW_2YR_TRANS_YR4_RT
                FIRSTGEN_ENRL_ORIG_YR4_RT
                FIRSTGEN_ENRL_4YR_TRANS_YR4_RT
                FIRSTGEN_ENRL_2YR_TRANS_YR4_RT
                FIRSTGEN_UNKN_ORIG_YR4_RT
                FIRSTGEN_UNKN_4YR_TRANS_YR4_RT
                FIRSTGEN_UNKN_2YR_TRANS_YR4_RT
                NOT1STGEN_DEATH_YR4_RT
                NOT1STGEN_COMP_ORIG_YR4_RT
                NOT1STGEN_COMP_4YR_TRANS_YR4_RT
                NOT1STGEN_COMP_2YR_TRANS_YR4_RT
                NOT1STGEN_WDRAW_ORIG_YR4_RT
                NOT1STGEN_WDRAW_4YR_TRANS_YR4_RT
                NOT1STGEN_WDRAW_2YR_TRANS_YR4_RT
                NOT1STGEN_ENRL_ORIG_YR4_RT
                NOT1STGEN_ENRL_4YR_TRANS_YR4_RT
                NOT1STGEN_ENRL_2YR_TRANS_YR4_RT
                NOT1STGEN_UNKN_ORIG_YR4_RT
                NOT1STGEN_UNKN_4YR_TRANS_YR4_RT
                NOT1STGEN_UNKN_2YR_TRANS_YR4_RT
                DEATH_YR6_RT
                COMP_ORIG_YR6_RT
                COMP_4YR_TRANS_YR6_RT
                COMP_2YR_TRANS_YR6_RT
                WDRAW_ORIG_YR6_RT
                WDRAW_4YR_TRANS_YR6_RT
                WDRAW_2YR_TRANS_YR6_RT
                ENRL_ORIG_YR6_RT
                ENRL_4YR_TRANS_YR6_RT
                ENRL_2YR_TRANS_YR6_RT
                UNKN_ORIG_YR6_RT
                UNKN_4YR_TRANS_YR6_RT
                UNKN_2YR_TRANS_YR6_RT
                LO_INC_DEATH_YR6_RT
                LO_INC_COMP_ORIG_YR6_RT
                LO_INC_COMP_4YR_TRANS_YR6_RT
                LO_INC_COMP_2YR_TRANS_YR6_RT
                LO_INC_WDRAW_ORIG_YR6_RT
                LO_INC_WDRAW_4YR_TRANS_YR6_RT
                LO_INC_WDRAW_2YR_TRANS_YR6_RT
                LO_INC_ENRL_ORIG_YR6_RT
                LO_INC_ENRL_4YR_TRANS_YR6_RT
                LO_INC_ENRL_2YR_TRANS_YR6_RT
                LO_INC_UNKN_ORIG_YR6_RT
                LO_INC_UNKN_4YR_TRANS_YR6_RT
                LO_INC_UNKN_2YR_TRANS_YR6_RT
                MD_INC_DEATH_YR6_RT
                MD_INC_COMP_ORIG_YR6_RT
                MD_INC_COMP_4YR_TRANS_YR6_RT
                MD_INC_COMP_2YR_TRANS_YR6_RT
                MD_INC_WDRAW_ORIG_YR6_RT
                MD_INC_WDRAW_4YR_TRANS_YR6_RT
                MD_INC_WDRAW_2YR_TRANS_YR6_RT
                MD_INC_ENRL_ORIG_YR6_RT
                MD_INC_ENRL_4YR_TRANS_YR6_RT
                MD_INC_ENRL_2YR_TRANS_YR6_RT
                MD_INC_UNKN_ORIG_YR6_RT
                MD_INC_UNKN_4YR_TRANS_YR6_RT
                MD_INC_UNKN_2YR_TRANS_YR6_RT
                HI_INC_DEATH_YR6_RT
                HI_INC_COMP_ORIG_YR6_RT
                HI_INC_COMP_4YR_TRANS_YR6_RT
                HI_INC_COMP_2YR_TRANS_YR6_RT
                HI_INC_WDRAW_ORIG_YR6_RT
                HI_INC_WDRAW_4YR_TRANS_YR6_RT
                HI_INC_WDRAW_2YR_TRANS_YR6_RT
                HI_INC_ENRL_ORIG_YR6_RT
                HI_INC_ENRL_4YR_TRANS_YR6_RT
                HI_INC_ENRL_2YR_TRANS_YR6_RT
                HI_INC_UNKN_ORIG_YR6_RT
                HI_INC_UNKN_4YR_TRANS_YR6_RT
                HI_INC_UNKN_2YR_TRANS_YR6_RT
                DEP_DEATH_YR6_RT
                DEP_COMP_ORIG_YR6_RT
                DEP_COMP_4YR_TRANS_YR6_RT
                DEP_COMP_2YR_TRANS_YR6_RT
                DEP_WDRAW_ORIG_YR6_RT
                DEP_WDRAW_4YR_TRANS_YR6_RT
                DEP_WDRAW_2YR_TRANS_YR6_RT
                DEP_ENRL_ORIG_YR6_RT
                DEP_ENRL_4YR_TRANS_YR6_RT
                DEP_ENRL_2YR_TRANS_YR6_RT
                DEP_UNKN_ORIG_YR6_RT
                DEP_UNKN_4YR_TRANS_YR6_RT
                DEP_UNKN_2YR_TRANS_YR6_RT
                IND_DEATH_YR6_RT
                IND_COMP_ORIG_YR6_RT
                IND_COMP_4YR_TRANS_YR6_RT
                IND_COMP_2YR_TRANS_YR6_RT
                IND_WDRAW_ORIG_YR6_RT
                IND_WDRAW_4YR_TRANS_YR6_RT
                IND_WDRAW_2YR_TRANS_YR6_RT
                IND_ENRL_ORIG_YR6_RT
                IND_ENRL_4YR_TRANS_YR6_RT
                IND_ENRL_2YR_TRANS_YR6_RT
                IND_UNKN_ORIG_YR6_RT
                IND_UNKN_4YR_TRANS_YR6_RT
                IND_UNKN_2YR_TRANS_YR6_RT
                FEMALE_DEATH_YR6_RT
                FEMALE_COMP_ORIG_YR6_RT
                FEMALE_COMP_4YR_TRANS_YR6_RT
                FEMALE_COMP_2YR_TRANS_YR6_RT
                FEMALE_WDRAW_ORIG_YR6_RT
                FEMALE_WDRAW_4YR_TRANS_YR6_RT
                FEMALE_WDRAW_2YR_TRANS_YR6_RT
                FEMALE_ENRL_ORIG_YR6_RT
                FEMALE_ENRL_4YR_TRANS_YR6_RT
                FEMALE_ENRL_2YR_TRANS_YR6_RT
                FEMALE_UNKN_ORIG_YR6_RT
                FEMALE_UNKN_4YR_TRANS_YR6_RT
                FEMALE_UNKN_2YR_TRANS_YR6_RT
                MALE_DEATH_YR6_RT
                MALE_COMP_ORIG_YR6_RT
                MALE_COMP_4YR_TRANS_YR6_RT
                MALE_COMP_2YR_TRANS_YR6_RT
                MALE_WDRAW_ORIG_YR6_RT
                MALE_WDRAW_4YR_TRANS_YR6_RT
                MALE_WDRAW_2YR_TRANS_YR6_RT
                MALE_ENRL_ORIG_YR6_RT
                MALE_ENRL_4YR_TRANS_YR6_RT
                MALE_ENRL_2YR_TRANS_YR6_RT
                MALE_UNKN_ORIG_YR6_RT
                MALE_UNKN_4YR_TRANS_YR6_RT
                MALE_UNKN_2YR_TRANS_YR6_RT
                PELL_DEATH_YR6_RT
                PELL_COMP_ORIG_YR6_RT
                PELL_COMP_4YR_TRANS_YR6_RT
                PELL_COMP_2YR_TRANS_YR6_RT
                PELL_WDRAW_ORIG_YR6_RT
                PELL_WDRAW_4YR_TRANS_YR6_RT
                PELL_WDRAW_2YR_TRANS_YR6_RT
                PELL_ENRL_ORIG_YR6_RT
                PELL_ENRL_4YR_TRANS_YR6_RT
                PELL_ENRL_2YR_TRANS_YR6_RT
                PELL_UNKN_ORIG_YR6_RT
                PELL_UNKN_4YR_TRANS_YR6_RT
                PELL_UNKN_2YR_TRANS_YR6_RT
                NOPELL_DEATH_YR6_RT
                NOPELL_COMP_ORIG_YR6_RT
                NOPELL_COMP_4YR_TRANS_YR6_RT
                NOPELL_COMP_2YR_TRANS_YR6_RT
                NOPELL_WDRAW_ORIG_YR6_RT
                NOPELL_WDRAW_4YR_TRANS_YR6_RT
                NOPELL_WDRAW_2YR_TRANS_YR6_RT
                NOPELL_ENRL_ORIG_YR6_RT
                NOPELL_ENRL_4YR_TRANS_YR6_RT
                NOPELL_ENRL_2YR_TRANS_YR6_RT
                NOPELL_UNKN_ORIG_YR6_RT
                NOPELL_UNKN_4YR_TRANS_YR6_RT
                NOPELL_UNKN_2YR_TRANS_YR6_RT
                FIRSTGEN_DEATH_YR6_RT
                FIRSTGEN_COMP_ORIG_YR6_RT
                FIRSTGEN_COMP_4YR_TRANS_YR6_RT
                FIRSTGEN_COMP_2YR_TRANS_YR6_RT
                FIRSTGEN_WDRAW_ORIG_YR6_RT
                FIRSTGEN_WDRAW_4YR_TRANS_YR6_RT
                FIRSTGEN_WDRAW_2YR_TRANS_YR6_RT
                FIRSTGEN_ENRL_ORIG_YR6_RT
                FIRSTGEN_ENRL_4YR_TRANS_YR6_RT
                FIRSTGEN_ENRL_2YR_TRANS_YR6_RT
                FIRSTGEN_UNKN_ORIG_YR6_RT
                FIRSTGEN_UNKN_4YR_TRANS_YR6_RT
                FIRSTGEN_UNKN_2YR_TRANS_YR6_RT
                NOT1STGEN_DEATH_YR6_RT
                NOT1STGEN_COMP_ORIG_YR6_RT
                NOT1STGEN_COMP_4YR_TRANS_YR6_RT
                NOT1STGEN_COMP_2YR_TRANS_YR6_RT
                NOT1STGEN_WDRAW_ORIG_YR6_RT
                NOT1STGEN_WDRAW_4YR_TRANS_YR6_RT
                NOT1STGEN_WDRAW_2YR_TRANS_YR6_RT
                NOT1STGEN_ENRL_ORIG_YR6_RT
                NOT1STGEN_ENRL_4YR_TRANS_YR6_RT
                NOT1STGEN_ENRL_2YR_TRANS_YR6_RT
                NOT1STGEN_UNKN_ORIG_YR6_RT
                NOT1STGEN_UNKN_4YR_TRANS_YR6_RT
                NOT1STGEN_UNKN_2YR_TRANS_YR6_RT
                RPY_1YR_RT
                COMPL_RPY_1YR_RT
                NONCOM_RPY_1YR_RT
                LO_INC_RPY_1YR_RT
                MD_INC_RPY_1YR_RT
                HI_INC_RPY_1YR_RT
                DEP_RPY_1YR_RT
                IND_RPY_1YR_RT
                PELL_RPY_1YR_RT
                NOPELL_RPY_1YR_RT
                FEMALE_RPY_1YR_RT
                MALE_RPY_1YR_RT
                FIRSTGEN_RPY_1YR_RT
                NOTFIRSTGEN_RPY_1YR_RT
                RPY_3YR_RT
                COMPL_RPY_3YR_RT
                NONCOM_RPY_3YR_RT
                LO_INC_RPY_3YR_RT
                MD_INC_RPY_3YR_RT
                HI_INC_RPY_3YR_RT
                DEP_RPY_3YR_RT
                IND_RPY_3YR_RT
                PELL_RPY_3YR_RT
                NOPELL_RPY_3YR_RT
                FEMALE_RPY_3YR_RT
                MALE_RPY_3YR_RT
                FIRSTGEN_RPY_3YR_RT
                NOTFIRSTGEN_RPY_3YR_RT
                RPY_5YR_RT
                COMPL_RPY_5YR_RT
                NONCOM_RPY_5YR_RT
                LO_INC_RPY_5YR_RT
                MD_INC_RPY_5YR_RT
                HI_INC_RPY_5YR_RT
                DEP_RPY_5YR_RT
                IND_RPY_5YR_RT
                PELL_RPY_5YR_RT
                NOPELL_RPY_5YR_RT
                FEMALE_RPY_5YR_RT
                MALE_RPY_5YR_RT
                FIRSTGEN_RPY_5YR_RT
                NOTFIRSTGEN_RPY_5YR_RT
                RPY_7YR_RT
                COMPL_RPY_7YR_RT
                NONCOM_RPY_7YR_RT
                LO_INC_RPY_7YR_RT
                MD_INC_RPY_7YR_RT
                HI_INC_RPY_7YR_RT
                DEP_RPY_7YR_RT
                IND_RPY_7YR_RT
                PELL_RPY_7YR_RT
                NOPELL_RPY_7YR_RT
                FEMALE_RPY_7YR_RT
                MALE_RPY_7YR_RT
                FIRSTGEN_RPY_7YR_RT
                NOTFIRSTGEN_RPY_7YR_RT
                INC_PCT_LO
                DEP_STAT_PCT_IND
                IND_INC_PCT_LO
                DEP_INC_PCT_LO
                PAR_ED_PCT_1STGEN
                INC_PCT_M1
                INC_PCT_M2
                INC_PCT_H1
                INC_PCT_H2
                DEP_INC_PCT_M1
                DEP_INC_PCT_M2
                DEP_INC_PCT_H1
                DEP_INC_PCT_H2
                IND_INC_PCT_M1
                IND_INC_PCT_M2
                IND_INC_PCT_H1
                IND_INC_PCT_H2
                PAR_ED_PCT_MS
                PAR_ED_PCT_HS
                PAR_ED_PCT_PS
                DEP_INC_AVG
                IND_INC_AVG
                OVERALL_YR2_N
                LO_INC_YR2_N
                MD_INC_YR2_N
                HI_INC_YR2_N
                DEP_YR2_N
                IND_YR2_N
                FEMALE_YR2_N
                MALE_YR2_N
                PELL_YR2_N
                NOPELL_YR2_N
                LOAN_YR2_N
                NOLOAN_YR2_N
                FIRSTGEN_YR2_N
                NOT1STGEN_YR2_N
                OVERALL_YR3_N
                LO_INC_YR3_N
                MD_INC_YR3_N
                HI_INC_YR3_N
                DEP_YR3_N
                IND_YR3_N
                FEMALE_YR3_N
                MALE_YR3_N
                PELL_YR3_N
                NOPELL_YR3_N
                LOAN_YR3_N
                NOLOAN_YR3_N
                FIRSTGEN_YR3_N
                NOT1STGEN_YR3_N
                OVERALL_YR4_N
                LO_INC_YR4_N
                MD_INC_YR4_N
                HI_INC_YR4_N
                DEP_YR4_N
                IND_YR4_N
                FEMALE_YR4_N
                MALE_YR4_N
                PELL_YR4_N
                NOPELL_YR4_N
                LOAN_YR4_N
                NOLOAN_YR4_N
                FIRSTGEN_YR4_N
                NOT1STGEN_YR4_N
                OVERALL_YR6_N
                LO_INC_YR6_N
                MD_INC_YR6_N
                HI_INC_YR6_N
                DEP_YR6_N
                IND_YR6_N
                FEMALE_YR6_N
                MALE_YR6_N
                PELL_YR6_N
                NOPELL_YR6_N
                LOAN_YR6_N
                NOLOAN_YR6_N
                FIRSTGEN_YR6_N
                NOT1STGEN_YR6_N
                DEBT_MDN
                GRAD_DEBT_MDN
                WDRAW_DEBT_MDN
                LO_INC_DEBT_MDN
                MD_INC_DEBT_MDN
                HI_INC_DEBT_MDN
                DEP_DEBT_MDN
                IND_DEBT_MDN
                PELL_DEBT_MDN
                NOPELL_DEBT_MDN
                FEMALE_DEBT_MDN
                MALE_DEBT_MDN
                FIRSTGEN_DEBT_MDN
                NOTFIRSTGEN_DEBT_MDN
                DEBT_N
                GRAD_DEBT_N
                WDRAW_DEBT_N
                LO_INC_DEBT_N
                MD_INC_DEBT_N
                HI_INC_DEBT_N
                DEP_DEBT_N
                IND_DEBT_N
                PELL_DEBT_N
                NOPELL_DEBT_N
                FEMALE_DEBT_N
                MALE_DEBT_N
                FIRSTGEN_DEBT_N
                NOTFIRSTGEN_DEBT_N
                GRAD_DEBT_MDN10YR
                CUML_DEBT_N
                CUML_DEBT_P90
                CUML_DEBT_P75
                CUML_DEBT_P25
                CUML_DEBT_P10
                INC_N
                DEP_INC_N
                IND_INC_N
                DEP_STAT_N
                PAR_ED_N
                APPL_SCH_N
                REPAY_DT_MDN
                SEPAR_DT_MDN
                REPAY_DT_N
                SEPAR_DT_N
                RPY_1YR_N
                COMPL_RPY_1YR_N
                NONCOM_RPY_1YR_N
                LO_INC_RPY_1YR_N
                MD_INC_RPY_1YR_N
                HI_INC_RPY_1YR_N
                DEP_RPY_1YR_N
                IND_RPY_1YR_N
                PELL_RPY_1YR_N
                NOPELL_RPY_1YR_N
                FEMALE_RPY_1YR_N
                MALE_RPY_1YR_N
                FIRSTGEN_RPY_1YR_N
                NOTFIRSTGEN_RPY_1YR_N
                RPY_3YR_N
                COMPL_RPY_3YR_N
                NONCOM_RPY_3YR_N
                LO_INC_RPY_3YR_N
                MD_INC_RPY_3YR_N
                HI_INC_RPY_3YR_N
                DEP_RPY_3YR_N
                IND_RPY_3YR_N
                PELL_RPY_3YR_N
                NOPELL_RPY_3YR_N
                FEMALE_RPY_3YR_N
                MALE_RPY_3YR_N
                FIRSTGEN_RPY_3YR_N
                NOTFIRSTGEN_RPY_3YR_N
                RPY_5YR_N
                COMPL_RPY_5YR_N
                NONCOM_RPY_5YR_N
                LO_INC_RPY_5YR_N
                MD_INC_RPY_5YR_N
                HI_INC_RPY_5YR_N
                DEP_RPY_5YR_N
                IND_RPY_5YR_N
                PELL_RPY_5YR_N
                NOPELL_RPY_5YR_N
                FEMALE_RPY_5YR_N
                MALE_RPY_5YR_N
                FIRSTGEN_RPY_5YR_N
                NOTFIRSTGEN_RPY_5YR_N
                COUNT_ED
                LOAN_EVER
                PELL_EVER
                AGE_ENTRY
                AGEGE24
                FEMALE
                MARRIED
                DEPENDENT
                VETERAN
                FIRST_GEN
                FAMINC
                MD_FAMINC
                FAMINC_IND
                PCT_WHITE
                PCT_BLACK
                PCT_ASIAN
                PCT_HISPANIC
                PCT_BA
                PCT_GRAD_PROF
                PCT_BORN_US
                MEDIAN_HH_INC
                POVERTY_RATE
                UNEMP_RATE
                COUNT_NWNE_P6
                COUNT_WNE_P6
                MN_EARN_WNE_P6
                MD_EARN_WNE_P6
                PCT10_EARN_WNE_P6
                PCT25_EARN_WNE_P6
                PCT75_EARN_WNE_P6
                PCT90_EARN_WNE_P6
                SD_EARN_WNE_P6
                COUNT_WNE_INC1_P6
                COUNT_WNE_INC2_P6
                COUNT_WNE_INC3_P6
                COUNT_WNE_INDEP0_INC1_P6
                COUNT_WNE_INDEP0_P6
                COUNT_WNE_INDEP1_P6
                COUNT_WNE_MALE0_P6
                COUNT_WNE_MALE1_P6
                GT_25K_P6
                GT_28K_P6
                MN_EARN_WNE_INC1_P6
                MN_EARN_WNE_INC2_P6
                MN_EARN_WNE_INC3_P6
                MN_EARN_WNE_INDEP0_INC1_P6
                MN_EARN_WNE_INDEP0_P6
                MN_EARN_WNE_INDEP1_P6
                MN_EARN_WNE_MALE0_P6
                MN_EARN_WNE_MALE1_P6
                DEBT_MDN_SUPP
                GRAD_DEBT_MDN_SUPP
                GRAD_DEBT_MDN10YR_SUPP
                C150_L4_POOLED_SUPP
                C150_4_POOLED_SUPP
                C200_L4_POOLED_SUPP
                C200_4_POOLED_SUPP
                ALIAS
                C100_4
                D100_4
                C100_L4
                D100_L4
                TRANS_4
                DTRANS_4
                TRANS_L4
                ICLEVEL
                UGDS_MEN
                UGDS_WOMEN
                CDR2_DENOM
                CDR3_DENOM
                OPENADMP
                UGNONDS
                GRADS
                ACCREDCODE
                T4APPROVALDATE
                RET_FT4_POOLED
                RET_FTL4_POOLED
                RET_PT4_POOLED
                RET_PTL4_POOLED
                POOLYRSRET_FT
                POOLYRSRET_PT
                RET_FT4_POOLED_SUPP
                RET_FTL4_POOLED_SUPP
                RET_PT4_POOLED_SUPP
                RET_PTL4_POOLED_SUPP
                TRANS_4_POOLED
                TRANS_L4_POOLED
                DTRANS_4_POOLED
                DTRANS_L4_POOLED
                TRANS_4_POOLED_SUPP
                TRANS_L4_POOLED_SUPP
                C100_4_POOLED
                C100_L4_POOLED
                D100_4_POOLED
                D100_L4_POOLED
                POOLYRS100
                C100_4_POOLED_SUPP
                C100_L4_POOLED_SUPP
                C150_4_PELL
                D150_4_PELL
                C150_L4_PELL
                D150_L4_PELL
                C150_4_LOANNOPELL
                D150_4_LOANNOPELL
                C150_L4_LOANNOPELL
                D150_L4_LOANNOPELL
                C150_4_NOLOANNOPELL
                D150_4_NOLOANNOPELL
                C150_L4_NOLOANNOPELL
                D150_L4_NOLOANNOPELL
                OMACHT6_FTFT_POOLED
                SCHTYPE
                OPEFLAG
                PRGMOFR
                CIPCODE1
                CIPTITLE1
                CIPTFBS1
                CIPTFBSANNUAL1
                MTHCMP1
                FTFTPCTPELL
                FTFTPCTFLOAN
                UG12MN
                G12MN
                POOLYRS_FTFTAIDPCT
                FTFTPCTPELL_POOLED_SUPP
                FTFTPCTFLOAN_POOLED_SUPP
                POOLYRS_PLUSPCT
                PLUS_DEBT_INST_N
                PLUS_DEBT_INST_MD
                PLUS_DEBT_ALL_N
                PLUS_DEBT_ALL_MD
                PLUS_DEBT_INST_COMP_N
                PLUS_DEBT_INST_COMP_MD
                PLUS_DEBT_INST_COMP_MDPAY10
                PLUS_DEBT_INST_COMP_MD_SUPP
                PLUS_DEBT_INST_COMP_MDPAY10_SUPP
                PLUS_DEBT_ALL_COMP_N
                PLUS_DEBT_ALL_COMP_MD
                PLUS_DEBT_ALL_COMP_MDPAY10
                PLUS_DEBT_ALL_COMP_MD_SUPP
                PLUS_DEBT_ALL_COMP_MDPAY10_SUPP
                PLUS_DEBT_INST_NOCOMP_N
                PLUS_DEBT_INST_NOCOMP_MD
                PLUS_DEBT_ALL_NOCOMP_N
                PLUS_DEBT_ALL_NOCOMP_MD
                PLUS_DEBT_INST_MALE_N
                PLUS_DEBT_INST_MALE_MD
                PLUS_DEBT_ALL_MALE_N
                PLUS_DEBT_ALL_MALE_MD
                PLUS_DEBT_INST_NOMALE_N
                PLUS_DEBT_INST_NOMALE_MD
                PLUS_DEBT_ALL_NOMALE_N
                PLUS_DEBT_ALL_NOMALE_MD
                PLUS_DEBT_INST_PELL_N
                PLUS_DEBT_INST_PELL_MD
                PLUS_DEBT_ALL_PELL_N
                PLUS_DEBT_ALL_PELL_MD
                PLUS_DEBT_INST_NOPELL_N
                PLUS_DEBT_INST_NOPELL_MD
                PLUS_DEBT_ALL_NOPELL_N
                PLUS_DEBT_ALL_NOPELL_MD
                COUNT_NWNE_3YR
                COUNT_WNE_3YR
                CNTOVER150_3YR
                BBRR1_FED_UG_N
                BBRR1_FED_UG_DFLT
                BBRR1_FED_UG_DLNQ
                BBRR1_FED_UG_FBR
                BBRR1_FED_UG_DFR
                BBRR1_FED_UG_NOPROG
                BBRR1_FED_UG_MAKEPROG
                BBRR1_FED_UG_PAIDINFULL
                BBRR1_FED_UG_DISCHARGE
                BBRR1_FED_UGCOMP_N
                BBRR1_FED_UGCOMP_DFLT
                BBRR1_FED_UGCOMP_DLNQ
                BBRR1_FED_UGCOMP_FBR
                BBRR1_FED_UGCOMP_DFR
                BBRR1_FED_UGCOMP_NOPROG
                BBRR1_FED_UGCOMP_MAKEPROG
                BBRR1_FED_UGCOMP_PAIDINFULL
                BBRR1_FED_UGCOMP_DISCHARGE
                BBRR1_FED_UGNOCOMP_N
                BBRR1_FED_UGNOCOMP_DFLT
                BBRR1_FED_UGNOCOMP_DLNQ
                BBRR1_FED_UGNOCOMP_FBR
                BBRR1_FED_UGNOCOMP_DFR
                BBRR1_FED_UGNOCOMP_NOPROG
                BBRR1_FED_UGNOCOMP_MAKEPROG
                BBRR1_FED_UGNOCOMP_PAIDINFULL
                BBRR1_FED_UGNOCOMP_DISCHARGE
                BBRR1_FED_UGUNK_N
                BBRR1_FED_UGUNK_DFLT
                BBRR1_FED_UGUNK_DLNQ
                BBRR1_FED_UGUNK_FBR
                BBRR1_FED_UGUNK_DFR
                BBRR1_FED_UGUNK_NOPROG
                BBRR1_FED_UGUNK_MAKEPROG
                BBRR1_FED_UGUNK_PAIDINFULL
                BBRR1_FED_UGUNK_DISCHARGE
                BBRR1_FED_GR_N
                BBRR1_FED_GR_DFLT
                BBRR1_FED_GR_DLNQ
                BBRR1_FED_GR_FBR
                BBRR1_FED_GR_DFR
                BBRR1_FED_GR_NOPROG
                BBRR1_FED_GR_MAKEPROG
                BBRR1_FED_GR_PAIDINFULL
                BBRR1_FED_GR_DISCHARGE
                BBRR1_FED_GRCOMP_N
                BBRR1_FED_GRCOMP_DFLT
                BBRR1_FED_GRCOMP_DLNQ
                BBRR1_FED_GRCOMP_FBR
                BBRR1_FED_GRCOMP_DFR
                BBRR1_FED_GRCOMP_NOPROG
                BBRR1_FED_GRCOMP_MAKEPROG
                BBRR1_FED_GRCOMP_PAIDINFULL
                BBRR1_FED_GRCOMP_DISCHARGE
                BBRR1_FED_GRNOCOMP_N
                BBRR1_FED_GRNOCOMP_DFLT
                BBRR1_FED_GRNOCOMP_DLNQ
                BBRR1_FED_GRNOCOMP_FBR
                BBRR1_FED_GRNOCOMP_DFR
                BBRR1_FED_GRNOCOMP_NOPROG
                BBRR1_FED_GRNOCOMP_MAKEPROG
                BBRR1_FED_GRNOCOMP_PAIDINFULL
                BBRR1_FED_GRNOCOMP_DISCHARGE
                LPSTAFFORD_CNT
                LPSTAFFORD_AMT
                LPPPLUS_CNT
                LPPPLUS_AMT
                LPGPLUS_CNT
                LPGPLUS_AMT
                FEDSCHCD
                """
# Put these "columns_to_read" above into a list
columns_to_read_list = []
for line in columns_to_read.split("\n"):
    if not line.strip():
        continue
    columns_to_read_list.append(line.lstrip())

# Read all the "institution_level" data
for filename in institution_level_files:
    # TypeError: cannot safely cast non-equivalent float64 to int64
    temp_df = pd.read_csv(filename, low_memory=False, index_col=False, usecols=columns_to_read_list, na_values= ['NULL','PrivacySuppressed'],
                          dtype={'ACAD_YR': str, 'UNITID': str, 'OPEID': str, 'OPEID6': str, 'INSTNM': str, 'CITY': str, 'STABBR': str, 'ZIP': str, 'ACCREDAGENCY': str,
                                'SCH_DEG': 'Int64', 'HCM2': 'Int64', 'MAIN': 'Int64', 'NUMBRANCH': 'Int64', 'PREDDEG': 'Int64', 'HIGHDEG': 'Int64', 'CONTROL': 'Int64', 'ST_FIPS': 'Int64', 'REGION': 'Int64', 'LOCALE': 'Int64', 'CCBASIC': 'Int64', 'CCUGPROF': 'Int64', 'CCSIZSET': 'Int64', 'HBCU': 'Int64', 'PBI': 'Int64', 'ANNHI': 'Int64', 'TRIBAL': 'Int64', 'AANAPII': 'Int64', 'HSI': 'Int64', 'NANTI': 'Int64', 'MENONLY': 'Int64', 'WOMENONLY': 'Int64', 'RELAFFIL': 'Int64',
                                'ADM_RATE': float, 'ADM_RATE_ALL': float, 'SATVR25': float, 'SATVR75': float, 'SATMT25': float, 'SATMT75': float, 'SATWR25': float, 'SATWR75': float, 'SATVRMID': float, 'SATMTMID': float, 'SATWRMID': float, 'ACTCM25': float, 'ACTCM75': float, 'ACTEN25': float, 'ACTEN75': float, 'ACTMT25': float, 'ACTMT75': float, 'ACTWR25': float, 'ACTWR75': float, 'ACTCMMID': float, 'ACTENMID': float, 'ACTMTMID': float, 'ACTWRMID': float, 'SAT_AVG': float, 'SAT_AVG_ALL': float, 'PCIP01': float, 'PCIP03': float, 'PCIP04': float, 'PCIP05': float, 'PCIP09': float, 'PCIP10': float, 'PCIP11': float, 'PCIP12': float, 'PCIP13': float, 'PCIP14': float, 'PCIP15': float, 'PCIP16': float, 'PCIP19': float, 'PCIP22': float, 'PCIP23': float, 'PCIP24': float, 'PCIP25': float, 'PCIP26': float, 'PCIP27': float, 'PCIP29': float, 'PCIP30': float, 'PCIP31': float, 'PCIP38': float, 'PCIP39': float, 'PCIP40': float, 'PCIP41': float, 'PCIP42': float, 'PCIP43': float, 'PCIP44': float, 'PCIP45': float, 'PCIP46': float, 'PCIP47': float, 'PCIP48': float, 'PCIP49': float, 'PCIP50': float, 'PCIP51': float, 'PCIP52': float, 'PCIP54': float,
                                'CIP01CERT1': 'Int64', 'CIP01CERT2': 'Int64', 'CIP01ASSOC': 'Int64', 'CIP01CERT4': 'Int64', 'CIP01BACHL': 'Int64', 'CIP03CERT1': 'Int64', 'CIP03CERT2': 'Int64', 'CIP03ASSOC': 'Int64', 'CIP03CERT4': 'Int64', 'CIP03BACHL': 'Int64', 'CIP04CERT1': 'Int64', 'CIP04CERT2': 'Int64', 'CIP04ASSOC': 'Int64', 'CIP04CERT4': 'Int64', 'CIP04BACHL': 'Int64', 'CIP05CERT1': 'Int64', 'CIP05CERT2': 'Int64', 'CIP05ASSOC': 'Int64', 'CIP05CERT4': 'Int64', 'CIP05BACHL': 'Int64', 'CIP09CERT1': 'Int64', 'CIP09CERT2': 'Int64', 'CIP09ASSOC': 'Int64', 'CIP09CERT4': 'Int64', 'CIP09BACHL': 'Int64', 'CIP10CERT1': 'Int64', 'CIP10CERT2': 'Int64', 'CIP10ASSOC': 'Int64', 'CIP10CERT4': 'Int64', 'CIP10BACHL': 'Int64', 'CIP11CERT1': 'Int64', 'CIP11CERT2': 'Int64', 'CIP11ASSOC': 'Int64', 'CIP11CERT4': 'Int64', 'CIP11BACHL': 'Int64', 'CIP12CERT1': 'Int64', 'CIP12CERT2': 'Int64', 'CIP12ASSOC': 'Int64', 'CIP12CERT4': 'Int64', 'CIP12BACHL': 'Int64', 'CIP13CERT1': 'Int64', 'CIP13CERT2': 'Int64', 'CIP13ASSOC': 'Int64', 'CIP13CERT4': 'Int64', 'CIP13BACHL': 'Int64', 'CIP14CERT1': 'Int64', 'CIP14CERT2': 'Int64', 'CIP14ASSOC': 'Int64', 'CIP14CERT4': 'Int64', 'CIP14BACHL': 'Int64', 'CIP15CERT1': 'Int64', 'CIP15CERT2': 'Int64', 'CIP15ASSOC': 'Int64', 'CIP15CERT4': 'Int64', 'CIP15BACHL': 'Int64', 'CIP16CERT1': 'Int64', 'CIP16CERT2': 'Int64', 'CIP16ASSOC': 'Int64', 'CIP16CERT4': 'Int64', 'CIP16BACHL': 'Int64', 'CIP19CERT1': 'Int64', 'CIP19CERT2': 'Int64', 'CIP19ASSOC': 'Int64', 'CIP19CERT4': 'Int64', 'CIP19BACHL': 'Int64', 'CIP22CERT1': 'Int64', 'CIP22CERT2': 'Int64', 'CIP22ASSOC': 'Int64', 'CIP22CERT4': 'Int64', 'CIP22BACHL': 'Int64', 'CIP23CERT1': 'Int64', 'CIP23CERT2': 'Int64', 'CIP23ASSOC': 'Int64', 'CIP23CERT4': 'Int64', 'CIP23BACHL': 'Int64', 'CIP24CERT1': 'Int64', 'CIP24CERT2': 'Int64', 'CIP24ASSOC': 'Int64', 'CIP24CERT4': 'Int64', 'CIP24BACHL': 'Int64', 'CIP25CERT1': 'Int64', 'CIP25CERT2': 'Int64', 'CIP25ASSOC': 'Int64', 'CIP25CERT4': 'Int64', 'CIP25BACHL': 'Int64', 'CIP26CERT1': 'Int64', 'CIP26CERT2': 'Int64', 'CIP26ASSOC': 'Int64', 'CIP26CERT4': 'Int64', 'CIP26BACHL': 'Int64', 'CIP27CERT1': 'Int64', 'CIP27CERT2': 'Int64', 'CIP27ASSOC': 'Int64', 'CIP27CERT4': 'Int64', 'CIP27BACHL': 'Int64', 'CIP29CERT1': 'Int64', 'CIP29CERT2': 'Int64', 'CIP29ASSOC': 'Int64', 'CIP29CERT4': 'Int64', 'CIP29BACHL': 'Int64', 'CIP30CERT1': 'Int64', 'CIP30CERT2': 'Int64', 'CIP30ASSOC': 'Int64', 'CIP30CERT4': 'Int64', 'CIP30BACHL': 'Int64', 'CIP31CERT1': 'Int64', 'CIP31CERT2': 'Int64', 'CIP31ASSOC': 'Int64', 'CIP31CERT4': 'Int64', 'CIP31BACHL': 'Int64', 'CIP38CERT1': 'Int64', 'CIP38CERT2': 'Int64', 'CIP38ASSOC': 'Int64', 'CIP38CERT4': 'Int64', 'CIP38BACHL': 'Int64', 'CIP39CERT1': 'Int64', 'CIP39CERT2': 'Int64', 'CIP39ASSOC': 'Int64', 'CIP39CERT4': 'Int64', 'CIP39BACHL': 'Int64', 'CIP40CERT1': 'Int64', 'CIP40CERT2': 'Int64', 'CIP40ASSOC': 'Int64', 'CIP40CERT4': 'Int64', 'CIP40BACHL': 'Int64', 'CIP41CERT1': 'Int64', 'CIP41CERT2': 'Int64', 'CIP41ASSOC': 'Int64', 'CIP41CERT4': 'Int64', 'CIP41BACHL': 'Int64', 'CIP42CERT1': 'Int64', 'CIP42CERT2': 'Int64', 'CIP42ASSOC': 'Int64', 'CIP42CERT4': 'Int64', 'CIP42BACHL': 'Int64', 'CIP43CERT1': 'Int64', 'CIP43CERT2': 'Int64', 'CIP43ASSOC': 'Int64', 'CIP43CERT4': 'Int64', 'CIP43BACHL': 'Int64', 'CIP44CERT1': 'Int64', 'CIP44CERT2': 'Int64', 'CIP44ASSOC': 'Int64', 'CIP44CERT4': 'Int64', 'CIP44BACHL': 'Int64', 'CIP45CERT1': 'Int64', 'CIP45CERT2': 'Int64', 'CIP45ASSOC': 'Int64', 'CIP45CERT4': 'Int64', 'CIP45BACHL': 'Int64', 'CIP46CERT1': 'Int64', 'CIP46CERT2': 'Int64', 'CIP46ASSOC': 'Int64', 'CIP46CERT4': 'Int64', 'CIP46BACHL': 'Int64', 'CIP47CERT1': 'Int64', 'CIP47CERT2': 'Int64', 'CIP47ASSOC': 'Int64', 'CIP47CERT4': 'Int64', 'CIP47BACHL': 'Int64', 'CIP48CERT1': 'Int64', 'CIP48CERT2': 'Int64', 'CIP48ASSOC': 'Int64', 'CIP48CERT4': 'Int64', 'CIP48BACHL': 'Int64', 'CIP49CERT1': 'Int64', 'CIP49CERT2': 'Int64', 'CIP49ASSOC': 'Int64', 'CIP49CERT4': 'Int64', 'CIP49BACHL': 'Int64', 'CIP50CERT1': 'Int64', 'CIP50CERT2': 'Int64', 'CIP50ASSOC': 'Int64', 'CIP50CERT4': 'Int64', 'CIP50BACHL': 'Int64', 'CIP51CERT1': 'Int64', 'CIP51CERT2': 'Int64', 'CIP51ASSOC': 'Int64', 'CIP51CERT4': 'Int64', 'CIP51BACHL': 'Int64', 'CIP52CERT1': 'Int64', 'CIP52CERT2': 'Int64', 'CIP52ASSOC': 'Int64', 'CIP52CERT4': 'Int64', 'CIP52BACHL': 'Int64', 'CIP54CERT1': 'Int64', 'CIP54CERT2': 'Int64', 'CIP54ASSOC': 'Int64', 'CIP54CERT4': 'Int64', 'CIP54BACHL': 'Int64', 'DISTANCEONLY': 'Int64', 'UGDS': 'Int64', 'UG': 'Int64',
                                'UGDS_WHITE': float, 'UGDS_BLACK': float, 'UGDS_HISP': float, 'UGDS_ASIAN': float, 'UGDS_AIAN': float, 'UGDS_NHPI': float, 'UGDS_2MOR': float, 'UGDS_NRA': float, 'UGDS_UNKN': float, 'UGDS_WHITENH': float, 'UGDS_BLACKNH': float, 'UGDS_API': float, 'UGDS_AIANOLD': float, 'UGDS_HISPOLD': float, 'UG_NRA': float, 'UG_UNKN': float, 'UG_WHITENH': float, 'UG_BLACKNH': float, 'UG_API': float, 'UG_AIANOLD': float, 'UG_HISPOLD': float, 'PPTUG_EF': float, 'PPTUG_EF2': float,
                                'CURROPER': 'Int64', 'NPT4_PUB': 'Int64', 'NPT4_PRIV': 'Int64', 'NPT4_PROG': 'Int64', 'NPT4_OTHER': 'Int64', 'NPT41_PUB': 'Int64', 'NPT42_PUB': 'Int64', 'NPT43_PUB': 'Int64', 'NPT44_PUB': 'Int64', 'NPT45_PUB': 'Int64', 'NPT41_PRIV': 'Int64', 'NPT42_PRIV': 'Int64', 'NPT43_PRIV': 'Int64', 'NPT44_PRIV': 'Int64', 'NPT45_PRIV': 'Int64', 'NPT41_PROG': 'Int64', 'NPT42_PROG': 'Int64', 'NPT43_PROG': 'Int64', 'NPT44_PROG': 'Int64', 'NPT45_PROG': 'Int64', 'NPT41_OTHER': 'Int64', 'NPT42_OTHER': 'Int64', 'NPT43_OTHER': 'Int64', 'NPT44_OTHER': 'Int64', 'NPT45_OTHER': 'Int64', 'NPT4_048_PUB': 'Int64', 'NPT4_048_PRIV': 'Int64', 'NPT4_048_PROG': 'Int64', 'NPT4_048_OTHER': 'Int64', 'NPT4_3075_PUB': 'Int64', 'NPT4_3075_PRIV': 'Int64', 'NPT4_75UP_PUB': 'Int64', 'NPT4_75UP_PRIV': 'Int64', 'NPT4_3075_PROG': 'Int64', 'NPT4_3075_OTHER': 'Int64', 'NPT4_75UP_PROG': 'Int64', 'NPT4_75UP_OTHER': 'Int64', 'NUM4_PUB': 'Int64', 'NUM4_PRIV': 'Int64', 'NUM4_PROG': 'Int64', 'NUM4_OTHER': 'Int64', 'NUM41_PUB': 'Int64', 'NUM42_PUB': 'Int64', 'NUM43_PUB': 'Int64', 'NUM44_PUB': 'Int64', 'NUM45_PUB': 'Int64', 'NUM41_PRIV': 'Int64', 'NUM42_PRIV': 'Int64', 'NUM43_PRIV': 'Int64', 'NUM44_PRIV': 'Int64', 'NUM45_PRIV': 'Int64', 'NUM41_PROG': 'Int64', 'NUM42_PROG': 'Int64', 'NUM43_PROG': 'Int64', 'NUM44_PROG': 'Int64', 'NUM45_PROG': 'Int64', 'NUM41_OTHER': 'Int64', 'NUM42_OTHER': 'Int64', 'NUM43_OTHER': 'Int64', 'NUM44_OTHER': 'Int64', 'NUM45_OTHER': 'Int64', 'COSTT4_A': 'Int64', 'COSTT4_P': 'Int64', 'TUITIONFEE_IN': 'Int64', 'TUITIONFEE_OUT': 'Int64', 'TUITIONFEE_PROG': 'Int64', 'TUITFTE': 'Int64', 'INEXPFTE': 'Int64', 'AVGFACSAL': 'Int64',
                                'PFTFAC': float, 'PCTPELL': float, 'C150_4': float, 'C150_L4': float, 'C150_4_POOLED': float, 'C150_L4_POOLED': float, 'POOLYRS': 'Int64', 'PFTFTUG1_EF': float, 'C150_4_WHITE': float, 'C150_4_BLACK': float, 'C150_4_HISP': float, 'C150_4_ASIAN': float, 'C150_4_AIAN': float, 'C150_4_NHPI': float, 'C150_4_2MOR': float, 'C150_4_NRA': float, 'C150_4_UNKN': float, 'C150_4_WHITENH': float, 'C150_4_BLACKNH': float, 'C150_4_API': float, 'C150_4_AIANOLD': float, 'C150_4_HISPOLD': float, 'C150_L4_WHITE': float, 'C150_L4_BLACK': float, 'C150_L4_HISP': float, 'C150_L4_ASIAN': float, 'C150_L4_AIAN': float, 'C150_L4_NHPI': float, 'C150_L4_2MOR': float, 'C150_L4_NRA': float, 'C150_L4_UNKN': float, 'C150_L4_WHITENH': float, 'C150_L4_BLACKNH': float, 'C150_L4_API': float, 'C150_L4_AIANOLD': float, 'C150_L4_HISPOLD': float, 'C200_4': float, 'C200_L4': float, 'D200_4': float, 'D200_L4': float, 'RET_FT4': float, 'RET_FTL4': float, 'RET_PT4': float, 'RET_PTL4': float, 'C200_4_POOLED': float, 'C200_L4_POOLED': float, 'POOLYRS200': 'Int64', 'PCTFLOAN': float, 'UG25ABV': float, 'CDR2': float, 'CDR3': float, 'DEATH_YR2_RT': str, 'COMP_ORIG_YR2_RT': str, 'COMP_4YR_TRANS_YR2_RT': str, 'COMP_2YR_TRANS_YR2_RT': str, 'WDRAW_ORIG_YR2_RT': str, 'WDRAW_4YR_TRANS_YR2_RT': str, 'WDRAW_2YR_TRANS_YR2_RT': str, 'ENRL_ORIG_YR2_RT': str, 'ENRL_4YR_TRANS_YR2_RT': str, 'ENRL_2YR_TRANS_YR2_RT': str, 'UNKN_ORIG_YR2_RT': str, 'UNKN_4YR_TRANS_YR2_RT': str, 'UNKN_2YR_TRANS_YR2_RT': str, 'LO_INC_DEATH_YR2_RT': str, 'LO_INC_COMP_ORIG_YR2_RT': str, 'LO_INC_COMP_4YR_TRANS_YR2_RT': str, 'LO_INC_COMP_2YR_TRANS_YR2_RT': str, 'LO_INC_WDRAW_ORIG_YR2_RT': str, 'LO_INC_WDRAW_4YR_TRANS_YR2_RT': str, 'LO_INC_WDRAW_2YR_TRANS_YR2_RT': str, 'LO_INC_ENRL_ORIG_YR2_RT': str, 'LO_INC_ENRL_4YR_TRANS_YR2_RT': str, 'LO_INC_ENRL_2YR_TRANS_YR2_RT': str, 'LO_INC_UNKN_ORIG_YR2_RT': str, 'LO_INC_UNKN_4YR_TRANS_YR2_RT': str, 'LO_INC_UNKN_2YR_TRANS_YR2_RT': str, 'MD_INC_DEATH_YR2_RT': str, 'MD_INC_COMP_ORIG_YR2_RT': str, 'MD_INC_COMP_4YR_TRANS_YR2_RT': str, 'MD_INC_COMP_2YR_TRANS_YR2_RT': str, 'MD_INC_WDRAW_ORIG_YR2_RT': str, 'MD_INC_WDRAW_4YR_TRANS_YR2_RT': str, 'MD_INC_WDRAW_2YR_TRANS_YR2_RT': str, 'MD_INC_ENRL_ORIG_YR2_RT': str, 'MD_INC_ENRL_4YR_TRANS_YR2_RT': str, 'MD_INC_ENRL_2YR_TRANS_YR2_RT': str, 'MD_INC_UNKN_ORIG_YR2_RT': str, 'MD_INC_UNKN_4YR_TRANS_YR2_RT': str, 'MD_INC_UNKN_2YR_TRANS_YR2_RT': str, 'HI_INC_DEATH_YR2_RT': str, 'HI_INC_COMP_ORIG_YR2_RT': str, 'HI_INC_COMP_4YR_TRANS_YR2_RT': str, 'HI_INC_COMP_2YR_TRANS_YR2_RT': str, 'HI_INC_WDRAW_ORIG_YR2_RT': str, 'HI_INC_WDRAW_4YR_TRANS_YR2_RT': str, 'HI_INC_WDRAW_2YR_TRANS_YR2_RT': str, 'HI_INC_ENRL_ORIG_YR2_RT': str, 'HI_INC_ENRL_4YR_TRANS_YR2_RT': str, 'HI_INC_ENRL_2YR_TRANS_YR2_RT': str, 'HI_INC_UNKN_ORIG_YR2_RT': str, 'HI_INC_UNKN_4YR_TRANS_YR2_RT': str, 'HI_INC_UNKN_2YR_TRANS_YR2_RT': str, 'DEP_DEATH_YR2_RT': str, 'DEP_COMP_ORIG_YR2_RT': str, 'DEP_COMP_4YR_TRANS_YR2_RT': str, 'DEP_COMP_2YR_TRANS_YR2_RT': str, 'DEP_WDRAW_ORIG_YR2_RT': str, 'DEP_WDRAW_4YR_TRANS_YR2_RT': str, 'DEP_WDRAW_2YR_TRANS_YR2_RT': str, 'DEP_ENRL_ORIG_YR2_RT': str, 'DEP_ENRL_4YR_TRANS_YR2_RT': str, 'DEP_ENRL_2YR_TRANS_YR2_RT': str, 'DEP_UNKN_ORIG_YR2_RT': str, 'DEP_UNKN_4YR_TRANS_YR2_RT': str, 'DEP_UNKN_2YR_TRANS_YR2_RT': str, 'IND_DEATH_YR2_RT': str, 'IND_COMP_ORIG_YR2_RT': str, 'IND_COMP_4YR_TRANS_YR2_RT': str, 'IND_COMP_2YR_TRANS_YR2_RT': str, 'IND_WDRAW_ORIG_YR2_RT': str, 'IND_WDRAW_4YR_TRANS_YR2_RT': str, 'IND_WDRAW_2YR_TRANS_YR2_RT': str, 'IND_ENRL_ORIG_YR2_RT': str, 'IND_ENRL_4YR_TRANS_YR2_RT': str, 'IND_ENRL_2YR_TRANS_YR2_RT': str, 'IND_UNKN_ORIG_YR2_RT': str, 'IND_UNKN_4YR_TRANS_YR2_RT': str, 'IND_UNKN_2YR_TRANS_YR2_RT': str, 'FEMALE_DEATH_YR2_RT': str, 'FEMALE_COMP_ORIG_YR2_RT': str, 'FEMALE_COMP_4YR_TRANS_YR2_RT': str, 'FEMALE_COMP_2YR_TRANS_YR2_RT': str, 'FEMALE_WDRAW_ORIG_YR2_RT': str, 'FEMALE_WDRAW_4YR_TRANS_YR2_RT': str, 'FEMALE_WDRAW_2YR_TRANS_YR2_RT': str, 'FEMALE_ENRL_ORIG_YR2_RT': str, 'FEMALE_ENRL_4YR_TRANS_YR2_RT': str, 'FEMALE_ENRL_2YR_TRANS_YR2_RT': str, 'FEMALE_UNKN_ORIG_YR2_RT': str, 'FEMALE_UNKN_4YR_TRANS_YR2_RT': str, 'FEMALE_UNKN_2YR_TRANS_YR2_RT': str, 'MALE_DEATH_YR2_RT': str, 'MALE_COMP_ORIG_YR2_RT': str, 'MALE_COMP_4YR_TRANS_YR2_RT': str, 'MALE_COMP_2YR_TRANS_YR2_RT': str, 'MALE_WDRAW_ORIG_YR2_RT': str, 'MALE_WDRAW_4YR_TRANS_YR2_RT': str, 'MALE_WDRAW_2YR_TRANS_YR2_RT': str, 'MALE_ENRL_ORIG_YR2_RT': str, 'MALE_ENRL_4YR_TRANS_YR2_RT': str, 'MALE_ENRL_2YR_TRANS_YR2_RT': str, 'MALE_UNKN_ORIG_YR2_RT': str, 'MALE_UNKN_4YR_TRANS_YR2_RT': str, 'MALE_UNKN_2YR_TRANS_YR2_RT': str, 'PELL_DEATH_YR2_RT': str, 'PELL_COMP_ORIG_YR2_RT': str, 'PELL_COMP_4YR_TRANS_YR2_RT': str, 'PELL_COMP_2YR_TRANS_YR2_RT': str, 'PELL_WDRAW_ORIG_YR2_RT': str, 'PELL_WDRAW_4YR_TRANS_YR2_RT': str, 'PELL_WDRAW_2YR_TRANS_YR2_RT': str, 'PELL_ENRL_ORIG_YR2_RT': str, 'PELL_ENRL_4YR_TRANS_YR2_RT': str, 'PELL_ENRL_2YR_TRANS_YR2_RT': str, 'PELL_UNKN_ORIG_YR2_RT': str, 'PELL_UNKN_4YR_TRANS_YR2_RT': str, 'PELL_UNKN_2YR_TRANS_YR2_RT': str, 'NOPELL_DEATH_YR2_RT': str, 'NOPELL_COMP_ORIG_YR2_RT': str, 'NOPELL_COMP_4YR_TRANS_YR2_RT': str, 'NOPELL_COMP_2YR_TRANS_YR2_RT': str, 'NOPELL_WDRAW_ORIG_YR2_RT': str, 'NOPELL_WDRAW_4YR_TRANS_YR2_RT': str, 'NOPELL_WDRAW_2YR_TRANS_YR2_RT': str, 'NOPELL_ENRL_ORIG_YR2_RT': str, 'NOPELL_ENRL_4YR_TRANS_YR2_RT': str, 'NOPELL_ENRL_2YR_TRANS_YR2_RT': str, 'NOPELL_UNKN_ORIG_YR2_RT': str, 'NOPELL_UNKN_4YR_TRANS_YR2_RT': str, 'NOPELL_UNKN_2YR_TRANS_YR2_RT': str, 'FIRSTGEN_DEATH_YR2_RT': str, 'FIRSTGEN_COMP_ORIG_YR2_RT': str, 'FIRSTGEN_COMP_4YR_TRANS_YR2_RT': str, 'FIRSTGEN_COMP_2YR_TRANS_YR2_RT': str, 'FIRSTGEN_WDRAW_ORIG_YR2_RT': str, 'FIRSTGEN_WDRAW_4YR_TRANS_YR2_RT': str, 'FIRSTGEN_WDRAW_2YR_TRANS_YR2_RT': str, 'FIRSTGEN_ENRL_ORIG_YR2_RT': str, 'FIRSTGEN_ENRL_4YR_TRANS_YR2_RT': str, 'FIRSTGEN_ENRL_2YR_TRANS_YR2_RT': str, 'FIRSTGEN_UNKN_ORIG_YR2_RT': str, 'FIRSTGEN_UNKN_4YR_TRANS_YR2_RT': str, 'FIRSTGEN_UNKN_2YR_TRANS_YR2_RT': str, 'NOT1STGEN_DEATH_YR2_RT': str, 'NOT1STGEN_COMP_ORIG_YR2_RT': str, 'NOT1STGEN_COMP_4YR_TRANS_YR2_RT': str, 'NOT1STGEN_COMP_2YR_TRANS_YR2_RT': str, 'NOT1STGEN_WDRAW_ORIG_YR2_RT': str, 'NOT1STGEN_WDRAW_4YR_TRANS_YR2_RT': str, 'NOT1STGEN_WDRAW_2YR_TRANS_YR2_RT': str, 'NOT1STGEN_ENRL_ORIG_YR2_RT': str, 'NOT1STGEN_ENRL_4YR_TRANS_YR2_RT': str, 'NOT1STGEN_ENRL_2YR_TRANS_YR2_RT': str, 'NOT1STGEN_UNKN_ORIG_YR2_RT': str, 'NOT1STGEN_UNKN_4YR_TRANS_YR2_RT': str, 'NOT1STGEN_UNKN_2YR_TRANS_YR2_RT': str, 'DEATH_YR3_RT': str, 'COMP_ORIG_YR3_RT': str, 'COMP_4YR_TRANS_YR3_RT': str, 'COMP_2YR_TRANS_YR3_RT': str, 'WDRAW_ORIG_YR3_RT': str, 'WDRAW_4YR_TRANS_YR3_RT': str, 'WDRAW_2YR_TRANS_YR3_RT': str, 'ENRL_ORIG_YR3_RT': str, 'ENRL_4YR_TRANS_YR3_RT': str, 'ENRL_2YR_TRANS_YR3_RT': str, 'UNKN_ORIG_YR3_RT': str, 'UNKN_4YR_TRANS_YR3_RT': str, 'UNKN_2YR_TRANS_YR3_RT': str, 'LO_INC_DEATH_YR3_RT': str, 'LO_INC_COMP_ORIG_YR3_RT': str, 'LO_INC_COMP_4YR_TRANS_YR3_RT': str, 'LO_INC_COMP_2YR_TRANS_YR3_RT': str, 'LO_INC_WDRAW_ORIG_YR3_RT': str, 'LO_INC_WDRAW_4YR_TRANS_YR3_RT': str, 'LO_INC_WDRAW_2YR_TRANS_YR3_RT': str, 'LO_INC_ENRL_ORIG_YR3_RT': str, 'LO_INC_ENRL_4YR_TRANS_YR3_RT': str, 'LO_INC_ENRL_2YR_TRANS_YR3_RT': str, 'LO_INC_UNKN_ORIG_YR3_RT': str, 'LO_INC_UNKN_4YR_TRANS_YR3_RT': str, 'LO_INC_UNKN_2YR_TRANS_YR3_RT': str, 'MD_INC_DEATH_YR3_RT': str, 'MD_INC_COMP_ORIG_YR3_RT': str, 'MD_INC_COMP_4YR_TRANS_YR3_RT': str, 'MD_INC_COMP_2YR_TRANS_YR3_RT': str, 'MD_INC_WDRAW_ORIG_YR3_RT': str, 'MD_INC_WDRAW_4YR_TRANS_YR3_RT': str, 'MD_INC_WDRAW_2YR_TRANS_YR3_RT': str, 'MD_INC_ENRL_ORIG_YR3_RT': str, 'MD_INC_ENRL_4YR_TRANS_YR3_RT': str, 'MD_INC_ENRL_2YR_TRANS_YR3_RT': str, 'MD_INC_UNKN_ORIG_YR3_RT': str, 'MD_INC_UNKN_4YR_TRANS_YR3_RT': str, 'MD_INC_UNKN_2YR_TRANS_YR3_RT': str, 'HI_INC_DEATH_YR3_RT': str, 'HI_INC_COMP_ORIG_YR3_RT': str, 'HI_INC_COMP_4YR_TRANS_YR3_RT': str, 'HI_INC_COMP_2YR_TRANS_YR3_RT': str, 'HI_INC_WDRAW_ORIG_YR3_RT': str, 'HI_INC_WDRAW_4YR_TRANS_YR3_RT': str, 'HI_INC_WDRAW_2YR_TRANS_YR3_RT': str, 'HI_INC_ENRL_ORIG_YR3_RT': str, 'HI_INC_ENRL_4YR_TRANS_YR3_RT': str, 'HI_INC_ENRL_2YR_TRANS_YR3_RT': str, 'HI_INC_UNKN_ORIG_YR3_RT': str, 'HI_INC_UNKN_4YR_TRANS_YR3_RT': str, 'HI_INC_UNKN_2YR_TRANS_YR3_RT': str, 'DEP_DEATH_YR3_RT': str, 'DEP_COMP_ORIG_YR3_RT': str, 'DEP_COMP_4YR_TRANS_YR3_RT': str, 'DEP_COMP_2YR_TRANS_YR3_RT': str, 'DEP_WDRAW_ORIG_YR3_RT': str, 'DEP_WDRAW_4YR_TRANS_YR3_RT': str, 'DEP_WDRAW_2YR_TRANS_YR3_RT': str, 'DEP_ENRL_ORIG_YR3_RT': str, 'DEP_ENRL_4YR_TRANS_YR3_RT': str, 'DEP_ENRL_2YR_TRANS_YR3_RT': str, 'DEP_UNKN_ORIG_YR3_RT': str, 'DEP_UNKN_4YR_TRANS_YR3_RT': str, 'DEP_UNKN_2YR_TRANS_YR3_RT': str, 'IND_DEATH_YR3_RT': str, 'IND_COMP_ORIG_YR3_RT': str, 'IND_COMP_4YR_TRANS_YR3_RT': str, 'IND_COMP_2YR_TRANS_YR3_RT': str, 'IND_WDRAW_ORIG_YR3_RT': str, 'IND_WDRAW_4YR_TRANS_YR3_RT': str, 'IND_WDRAW_2YR_TRANS_YR3_RT': str, 'IND_ENRL_ORIG_YR3_RT': str, 'IND_ENRL_4YR_TRANS_YR3_RT': str, 'IND_ENRL_2YR_TRANS_YR3_RT': str, 'IND_UNKN_ORIG_YR3_RT': str, 'IND_UNKN_4YR_TRANS_YR3_RT': str, 'IND_UNKN_2YR_TRANS_YR3_RT': str, 'FEMALE_DEATH_YR3_RT': str, 'FEMALE_COMP_ORIG_YR3_RT': str, 'FEMALE_COMP_4YR_TRANS_YR3_RT': str, 'FEMALE_COMP_2YR_TRANS_YR3_RT': str, 'FEMALE_WDRAW_ORIG_YR3_RT': str, 'FEMALE_WDRAW_4YR_TRANS_YR3_RT': str, 'FEMALE_WDRAW_2YR_TRANS_YR3_RT': str, 'FEMALE_ENRL_ORIG_YR3_RT': str, 'FEMALE_ENRL_4YR_TRANS_YR3_RT': str, 'FEMALE_ENRL_2YR_TRANS_YR3_RT': str, 'FEMALE_UNKN_ORIG_YR3_RT': str, 'FEMALE_UNKN_4YR_TRANS_YR3_RT': str, 'FEMALE_UNKN_2YR_TRANS_YR3_RT': str, 'MALE_DEATH_YR3_RT': str, 'MALE_COMP_ORIG_YR3_RT': str, 'MALE_COMP_4YR_TRANS_YR3_RT': str, 'MALE_COMP_2YR_TRANS_YR3_RT': str, 'MALE_WDRAW_ORIG_YR3_RT': str, 'MALE_WDRAW_4YR_TRANS_YR3_RT': str, 'MALE_WDRAW_2YR_TRANS_YR3_RT': str, 'MALE_ENRL_ORIG_YR3_RT': str, 'MALE_ENRL_4YR_TRANS_YR3_RT': str, 'MALE_ENRL_2YR_TRANS_YR3_RT': str, 'MALE_UNKN_ORIG_YR3_RT': str, 'MALE_UNKN_4YR_TRANS_YR3_RT': str, 'MALE_UNKN_2YR_TRANS_YR3_RT': str, 'PELL_DEATH_YR3_RT': str, 'PELL_COMP_ORIG_YR3_RT': str, 'PELL_COMP_4YR_TRANS_YR3_RT': str, 'PELL_COMP_2YR_TRANS_YR3_RT': str, 'PELL_WDRAW_ORIG_YR3_RT': str, 'PELL_WDRAW_4YR_TRANS_YR3_RT': str, 'PELL_WDRAW_2YR_TRANS_YR3_RT': str, 'PELL_ENRL_ORIG_YR3_RT': str, 'PELL_ENRL_4YR_TRANS_YR3_RT': str, 'PELL_ENRL_2YR_TRANS_YR3_RT': str, 'PELL_UNKN_ORIG_YR3_RT': str, 'PELL_UNKN_4YR_TRANS_YR3_RT': str, 'PELL_UNKN_2YR_TRANS_YR3_RT': str, 'NOPELL_DEATH_YR3_RT': str, 'NOPELL_COMP_ORIG_YR3_RT': str, 'NOPELL_COMP_4YR_TRANS_YR3_RT': str, 'NOPELL_COMP_2YR_TRANS_YR3_RT': str, 'NOPELL_WDRAW_ORIG_YR3_RT': str, 'NOPELL_WDRAW_4YR_TRANS_YR3_RT': str, 'NOPELL_WDRAW_2YR_TRANS_YR3_RT': str, 'NOPELL_ENRL_ORIG_YR3_RT': str, 'NOPELL_ENRL_4YR_TRANS_YR3_RT': str, 'NOPELL_ENRL_2YR_TRANS_YR3_RT': str, 'NOPELL_UNKN_ORIG_YR3_RT': str, 'NOPELL_UNKN_4YR_TRANS_YR3_RT': str, 'NOPELL_UNKN_2YR_TRANS_YR3_RT': str, 'FIRSTGEN_DEATH_YR3_RT': str, 'FIRSTGEN_COMP_ORIG_YR3_RT': str, 'FIRSTGEN_COMP_4YR_TRANS_YR3_RT': str, 'FIRSTGEN_COMP_2YR_TRANS_YR3_RT': str, 'FIRSTGEN_WDRAW_ORIG_YR3_RT': str, 'FIRSTGEN_WDRAW_4YR_TRANS_YR3_RT': str, 'FIRSTGEN_WDRAW_2YR_TRANS_YR3_RT': str, 'FIRSTGEN_ENRL_ORIG_YR3_RT': str, 'FIRSTGEN_ENRL_4YR_TRANS_YR3_RT': str, 'FIRSTGEN_ENRL_2YR_TRANS_YR3_RT': str, 'FIRSTGEN_UNKN_ORIG_YR3_RT': str, 'FIRSTGEN_UNKN_4YR_TRANS_YR3_RT': str, 'FIRSTGEN_UNKN_2YR_TRANS_YR3_RT': str, 'NOT1STGEN_DEATH_YR3_RT': str, 'NOT1STGEN_COMP_ORIG_YR3_RT': str, 'NOT1STGEN_COMP_4YR_TRANS_YR3_RT': str, 'NOT1STGEN_COMP_2YR_TRANS_YR3_RT': str, 'NOT1STGEN_WDRAW_ORIG_YR3_RT': str, 'NOT1STGEN_WDRAW_4YR_TRANS_YR3_RT': str, 'NOT1STGEN_WDRAW_2YR_TRANS_YR3_RT': str, 'NOT1STGEN_ENRL_ORIG_YR3_RT': str, 'NOT1STGEN_ENRL_4YR_TRANS_YR3_RT': str, 'NOT1STGEN_ENRL_2YR_TRANS_YR3_RT': str, 'NOT1STGEN_UNKN_ORIG_YR3_RT': str, 'NOT1STGEN_UNKN_4YR_TRANS_YR3_RT': str, 'NOT1STGEN_UNKN_2YR_TRANS_YR3_RT': str, 'DEATH_YR4_RT': str, 'COMP_ORIG_YR4_RT': str, 'COMP_4YR_TRANS_YR4_RT': str, 'COMP_2YR_TRANS_YR4_RT': str, 'WDRAW_ORIG_YR4_RT': str, 'WDRAW_4YR_TRANS_YR4_RT': str, 'WDRAW_2YR_TRANS_YR4_RT': str, 'ENRL_ORIG_YR4_RT': str, 'ENRL_4YR_TRANS_YR4_RT': str, 'ENRL_2YR_TRANS_YR4_RT': str, 'UNKN_ORIG_YR4_RT': str, 'UNKN_4YR_TRANS_YR4_RT': str, 'UNKN_2YR_TRANS_YR4_RT': str, 'LO_INC_DEATH_YR4_RT': str, 'LO_INC_COMP_ORIG_YR4_RT': str, 'LO_INC_COMP_4YR_TRANS_YR4_RT': str, 'LO_INC_COMP_2YR_TRANS_YR4_RT': str, 'LO_INC_WDRAW_ORIG_YR4_RT': str, 'LO_INC_WDRAW_4YR_TRANS_YR4_RT': str, 'LO_INC_WDRAW_2YR_TRANS_YR4_RT': str, 'LO_INC_ENRL_ORIG_YR4_RT': str, 'LO_INC_ENRL_4YR_TRANS_YR4_RT': str, 'LO_INC_ENRL_2YR_TRANS_YR4_RT': str, 'LO_INC_UNKN_ORIG_YR4_RT': str, 'LO_INC_UNKN_4YR_TRANS_YR4_RT': str, 'LO_INC_UNKN_2YR_TRANS_YR4_RT': str, 'MD_INC_DEATH_YR4_RT': str, 'MD_INC_COMP_ORIG_YR4_RT': str, 'MD_INC_COMP_4YR_TRANS_YR4_RT': str, 'MD_INC_COMP_2YR_TRANS_YR4_RT': str, 'MD_INC_WDRAW_ORIG_YR4_RT': str, 'MD_INC_WDRAW_4YR_TRANS_YR4_RT': str, 'MD_INC_WDRAW_2YR_TRANS_YR4_RT': str, 'MD_INC_ENRL_ORIG_YR4_RT': str, 'MD_INC_ENRL_4YR_TRANS_YR4_RT': str, 'MD_INC_ENRL_2YR_TRANS_YR4_RT': str, 'MD_INC_UNKN_ORIG_YR4_RT': str, 'MD_INC_UNKN_4YR_TRANS_YR4_RT': str, 'MD_INC_UNKN_2YR_TRANS_YR4_RT': str, 'HI_INC_DEATH_YR4_RT': str, 'HI_INC_COMP_ORIG_YR4_RT': str, 'HI_INC_COMP_4YR_TRANS_YR4_RT': str, 'HI_INC_COMP_2YR_TRANS_YR4_RT': str, 'HI_INC_WDRAW_ORIG_YR4_RT': str, 'HI_INC_WDRAW_4YR_TRANS_YR4_RT': str, 'HI_INC_WDRAW_2YR_TRANS_YR4_RT': str, 'HI_INC_ENRL_ORIG_YR4_RT': str, 'HI_INC_ENRL_4YR_TRANS_YR4_RT': str, 'HI_INC_ENRL_2YR_TRANS_YR4_RT': str, 'HI_INC_UNKN_ORIG_YR4_RT': str, 'HI_INC_UNKN_4YR_TRANS_YR4_RT': str, 'HI_INC_UNKN_2YR_TRANS_YR4_RT': str, 'DEP_DEATH_YR4_RT': str, 'DEP_COMP_ORIG_YR4_RT': str, 'DEP_COMP_4YR_TRANS_YR4_RT': str, 'DEP_COMP_2YR_TRANS_YR4_RT': str, 'DEP_WDRAW_ORIG_YR4_RT': str, 'DEP_WDRAW_4YR_TRANS_YR4_RT': str, 'DEP_WDRAW_2YR_TRANS_YR4_RT': str, 'DEP_ENRL_ORIG_YR4_RT': str, 'DEP_ENRL_4YR_TRANS_YR4_RT': str, 'DEP_ENRL_2YR_TRANS_YR4_RT': str, 'DEP_UNKN_ORIG_YR4_RT': str, 'DEP_UNKN_4YR_TRANS_YR4_RT': str, 'DEP_UNKN_2YR_TRANS_YR4_RT': str, 'IND_DEATH_YR4_RT': str, 'IND_COMP_ORIG_YR4_RT': str, 'IND_COMP_4YR_TRANS_YR4_RT': str, 'IND_COMP_2YR_TRANS_YR4_RT': str, 'IND_WDRAW_ORIG_YR4_RT': str, 'IND_WDRAW_4YR_TRANS_YR4_RT': str, 'IND_WDRAW_2YR_TRANS_YR4_RT': str, 'IND_ENRL_ORIG_YR4_RT': str, 'IND_ENRL_4YR_TRANS_YR4_RT': str, 'IND_ENRL_2YR_TRANS_YR4_RT': str, 'IND_UNKN_ORIG_YR4_RT': str, 'IND_UNKN_4YR_TRANS_YR4_RT': str, 'IND_UNKN_2YR_TRANS_YR4_RT': str, 'FEMALE_DEATH_YR4_RT': str, 'FEMALE_COMP_ORIG_YR4_RT': str, 'FEMALE_COMP_4YR_TRANS_YR4_RT': str, 'FEMALE_COMP_2YR_TRANS_YR4_RT': str, 'FEMALE_WDRAW_ORIG_YR4_RT': str, 'FEMALE_WDRAW_4YR_TRANS_YR4_RT': str, 'FEMALE_WDRAW_2YR_TRANS_YR4_RT': str, 'FEMALE_ENRL_ORIG_YR4_RT': str, 'FEMALE_ENRL_4YR_TRANS_YR4_RT': str, 'FEMALE_ENRL_2YR_TRANS_YR4_RT': str, 'FEMALE_UNKN_ORIG_YR4_RT': str, 'FEMALE_UNKN_4YR_TRANS_YR4_RT': str, 'FEMALE_UNKN_2YR_TRANS_YR4_RT': str, 'MALE_DEATH_YR4_RT': str, 'MALE_COMP_ORIG_YR4_RT': str, 'MALE_COMP_4YR_TRANS_YR4_RT': str, 'MALE_COMP_2YR_TRANS_YR4_RT': str, 'MALE_WDRAW_ORIG_YR4_RT': str, 'MALE_WDRAW_4YR_TRANS_YR4_RT': str, 'MALE_WDRAW_2YR_TRANS_YR4_RT': str, 'MALE_ENRL_ORIG_YR4_RT': str, 'MALE_ENRL_4YR_TRANS_YR4_RT': str, 'MALE_ENRL_2YR_TRANS_YR4_RT': str, 'MALE_UNKN_ORIG_YR4_RT': str, 'MALE_UNKN_4YR_TRANS_YR4_RT': str, 'MALE_UNKN_2YR_TRANS_YR4_RT': str, 'PELL_DEATH_YR4_RT': str, 'PELL_COMP_ORIG_YR4_RT': str, 'PELL_COMP_4YR_TRANS_YR4_RT': str, 'PELL_COMP_2YR_TRANS_YR4_RT': str, 'PELL_WDRAW_ORIG_YR4_RT': str, 'PELL_WDRAW_4YR_TRANS_YR4_RT': str, 'PELL_WDRAW_2YR_TRANS_YR4_RT': str, 'PELL_ENRL_ORIG_YR4_RT': str, 'PELL_ENRL_4YR_TRANS_YR4_RT': str, 'PELL_ENRL_2YR_TRANS_YR4_RT': str, 'PELL_UNKN_ORIG_YR4_RT': str, 'PELL_UNKN_4YR_TRANS_YR4_RT': str, 'PELL_UNKN_2YR_TRANS_YR4_RT': str, 'NOPELL_DEATH_YR4_RT': str, 'NOPELL_COMP_ORIG_YR4_RT': str, 'NOPELL_COMP_4YR_TRANS_YR4_RT': str, 'NOPELL_COMP_2YR_TRANS_YR4_RT': str, 'NOPELL_WDRAW_ORIG_YR4_RT': str, 'NOPELL_WDRAW_4YR_TRANS_YR4_RT': str, 'NOPELL_WDRAW_2YR_TRANS_YR4_RT': str, 'NOPELL_ENRL_ORIG_YR4_RT': str, 'NOPELL_ENRL_4YR_TRANS_YR4_RT': str, 'NOPELL_ENRL_2YR_TRANS_YR4_RT': str, 'NOPELL_UNKN_ORIG_YR4_RT': str, 'NOPELL_UNKN_4YR_TRANS_YR4_RT': str, 'NOPELL_UNKN_2YR_TRANS_YR4_RT': str, 'FIRSTGEN_DEATH_YR4_RT': str, 'FIRSTGEN_COMP_ORIG_YR4_RT': str, 'FIRSTGEN_COMP_4YR_TRANS_YR4_RT': str, 'FIRSTGEN_COMP_2YR_TRANS_YR4_RT': str, 'FIRSTGEN_WDRAW_ORIG_YR4_RT': str, 'FIRSTGEN_WDRAW_4YR_TRANS_YR4_RT': str, 'FIRSTGEN_WDRAW_2YR_TRANS_YR4_RT': str, 'FIRSTGEN_ENRL_ORIG_YR4_RT': str, 'FIRSTGEN_ENRL_4YR_TRANS_YR4_RT': str, 'FIRSTGEN_ENRL_2YR_TRANS_YR4_RT': str, 'FIRSTGEN_UNKN_ORIG_YR4_RT': str, 'FIRSTGEN_UNKN_4YR_TRANS_YR4_RT': str, 'FIRSTGEN_UNKN_2YR_TRANS_YR4_RT': str, 'NOT1STGEN_DEATH_YR4_RT': str, 'NOT1STGEN_COMP_ORIG_YR4_RT': str, 'NOT1STGEN_COMP_4YR_TRANS_YR4_RT': str, 'NOT1STGEN_COMP_2YR_TRANS_YR4_RT': str, 'NOT1STGEN_WDRAW_ORIG_YR4_RT': str, 'NOT1STGEN_WDRAW_4YR_TRANS_YR4_RT': str, 'NOT1STGEN_WDRAW_2YR_TRANS_YR4_RT': str, 'NOT1STGEN_ENRL_ORIG_YR4_RT': str, 'NOT1STGEN_ENRL_4YR_TRANS_YR4_RT': str, 'NOT1STGEN_ENRL_2YR_TRANS_YR4_RT': str, 'NOT1STGEN_UNKN_ORIG_YR4_RT': str, 'NOT1STGEN_UNKN_4YR_TRANS_YR4_RT': str, 'NOT1STGEN_UNKN_2YR_TRANS_YR4_RT': str, 'DEATH_YR6_RT': str, 'COMP_ORIG_YR6_RT': str, 'COMP_4YR_TRANS_YR6_RT': str, 'COMP_2YR_TRANS_YR6_RT': str, 'WDRAW_ORIG_YR6_RT': str, 'WDRAW_4YR_TRANS_YR6_RT': str, 'WDRAW_2YR_TRANS_YR6_RT': str, 'ENRL_ORIG_YR6_RT': str, 'ENRL_4YR_TRANS_YR6_RT': str, 'ENRL_2YR_TRANS_YR6_RT': str, 'UNKN_ORIG_YR6_RT': str, 'UNKN_4YR_TRANS_YR6_RT': str, 'UNKN_2YR_TRANS_YR6_RT': str, 'LO_INC_DEATH_YR6_RT': str, 'LO_INC_COMP_ORIG_YR6_RT': str, 'LO_INC_COMP_4YR_TRANS_YR6_RT': str, 'LO_INC_COMP_2YR_TRANS_YR6_RT': str, 'LO_INC_WDRAW_ORIG_YR6_RT': str, 'LO_INC_WDRAW_4YR_TRANS_YR6_RT': str, 'LO_INC_WDRAW_2YR_TRANS_YR6_RT': str, 'LO_INC_ENRL_ORIG_YR6_RT': str, 'LO_INC_ENRL_4YR_TRANS_YR6_RT': str, 'LO_INC_ENRL_2YR_TRANS_YR6_RT': str, 'LO_INC_UNKN_ORIG_YR6_RT': str, 'LO_INC_UNKN_4YR_TRANS_YR6_RT': str, 'LO_INC_UNKN_2YR_TRANS_YR6_RT': str, 'MD_INC_DEATH_YR6_RT': str, 'MD_INC_COMP_ORIG_YR6_RT': str, 'MD_INC_COMP_4YR_TRANS_YR6_RT': str, 'MD_INC_COMP_2YR_TRANS_YR6_RT': str, 'MD_INC_WDRAW_ORIG_YR6_RT': str, 'MD_INC_WDRAW_4YR_TRANS_YR6_RT': str, 'MD_INC_WDRAW_2YR_TRANS_YR6_RT': str, 'MD_INC_ENRL_ORIG_YR6_RT': str, 'MD_INC_ENRL_4YR_TRANS_YR6_RT': str, 'MD_INC_ENRL_2YR_TRANS_YR6_RT': str, 'MD_INC_UNKN_ORIG_YR6_RT': str, 'MD_INC_UNKN_4YR_TRANS_YR6_RT': str, 'MD_INC_UNKN_2YR_TRANS_YR6_RT': str, 'HI_INC_DEATH_YR6_RT': str, 'HI_INC_COMP_ORIG_YR6_RT': str, 'HI_INC_COMP_4YR_TRANS_YR6_RT': str, 'HI_INC_COMP_2YR_TRANS_YR6_RT': str, 'HI_INC_WDRAW_ORIG_YR6_RT': str, 'HI_INC_WDRAW_4YR_TRANS_YR6_RT': str, 'HI_INC_WDRAW_2YR_TRANS_YR6_RT': str, 'HI_INC_ENRL_ORIG_YR6_RT': str, 'HI_INC_ENRL_4YR_TRANS_YR6_RT': str, 'HI_INC_ENRL_2YR_TRANS_YR6_RT': str, 'HI_INC_UNKN_ORIG_YR6_RT': str, 'HI_INC_UNKN_4YR_TRANS_YR6_RT': str, 'HI_INC_UNKN_2YR_TRANS_YR6_RT': str, 'DEP_DEATH_YR6_RT': str, 'DEP_COMP_ORIG_YR6_RT': str, 'DEP_COMP_4YR_TRANS_YR6_RT': str, 'DEP_COMP_2YR_TRANS_YR6_RT': str, 'DEP_WDRAW_ORIG_YR6_RT': str, 'DEP_WDRAW_4YR_TRANS_YR6_RT': str, 'DEP_WDRAW_2YR_TRANS_YR6_RT': str, 'DEP_ENRL_ORIG_YR6_RT': str, 'DEP_ENRL_4YR_TRANS_YR6_RT': str, 'DEP_ENRL_2YR_TRANS_YR6_RT': str, 'DEP_UNKN_ORIG_YR6_RT': str, 'DEP_UNKN_4YR_TRANS_YR6_RT': str, 'DEP_UNKN_2YR_TRANS_YR6_RT': str, 'IND_DEATH_YR6_RT': str, 'IND_COMP_ORIG_YR6_RT': str, 'IND_COMP_4YR_TRANS_YR6_RT': str, 'IND_COMP_2YR_TRANS_YR6_RT': str, 'IND_WDRAW_ORIG_YR6_RT': str, 'IND_WDRAW_4YR_TRANS_YR6_RT': str, 'IND_WDRAW_2YR_TRANS_YR6_RT': str, 'IND_ENRL_ORIG_YR6_RT': str, 'IND_ENRL_4YR_TRANS_YR6_RT': str, 'IND_ENRL_2YR_TRANS_YR6_RT': str, 'IND_UNKN_ORIG_YR6_RT': str, 'IND_UNKN_4YR_TRANS_YR6_RT': str, 'IND_UNKN_2YR_TRANS_YR6_RT': str, 'FEMALE_DEATH_YR6_RT': str, 'FEMALE_COMP_ORIG_YR6_RT': str, 'FEMALE_COMP_4YR_TRANS_YR6_RT': str, 'FEMALE_COMP_2YR_TRANS_YR6_RT': str, 'FEMALE_WDRAW_ORIG_YR6_RT': str, 'FEMALE_WDRAW_4YR_TRANS_YR6_RT': str, 'FEMALE_WDRAW_2YR_TRANS_YR6_RT': str, 'FEMALE_ENRL_ORIG_YR6_RT': str, 'FEMALE_ENRL_4YR_TRANS_YR6_RT': str, 'FEMALE_ENRL_2YR_TRANS_YR6_RT': str, 'FEMALE_UNKN_ORIG_YR6_RT': str, 'FEMALE_UNKN_4YR_TRANS_YR6_RT': str, 'FEMALE_UNKN_2YR_TRANS_YR6_RT': str, 'MALE_DEATH_YR6_RT': str, 'MALE_COMP_ORIG_YR6_RT': str, 'MALE_COMP_4YR_TRANS_YR6_RT': str, 'MALE_COMP_2YR_TRANS_YR6_RT': str, 'MALE_WDRAW_ORIG_YR6_RT': str, 'MALE_WDRAW_4YR_TRANS_YR6_RT': str, 'MALE_WDRAW_2YR_TRANS_YR6_RT': str, 'MALE_ENRL_ORIG_YR6_RT': str, 'MALE_ENRL_4YR_TRANS_YR6_RT': str, 'MALE_ENRL_2YR_TRANS_YR6_RT': str, 'MALE_UNKN_ORIG_YR6_RT': str, 'MALE_UNKN_4YR_TRANS_YR6_RT': str, 'MALE_UNKN_2YR_TRANS_YR6_RT': str, 'PELL_DEATH_YR6_RT': str, 'PELL_COMP_ORIG_YR6_RT': str, 'PELL_COMP_4YR_TRANS_YR6_RT': str, 'PELL_COMP_2YR_TRANS_YR6_RT': str, 'PELL_WDRAW_ORIG_YR6_RT': str, 'PELL_WDRAW_4YR_TRANS_YR6_RT': str, 'PELL_WDRAW_2YR_TRANS_YR6_RT': str, 'PELL_ENRL_ORIG_YR6_RT': str, 'PELL_ENRL_4YR_TRANS_YR6_RT': str, 'PELL_ENRL_2YR_TRANS_YR6_RT': str, 'PELL_UNKN_ORIG_YR6_RT': str, 'PELL_UNKN_4YR_TRANS_YR6_RT': str, 'PELL_UNKN_2YR_TRANS_YR6_RT': str, 'NOPELL_DEATH_YR6_RT': str, 'NOPELL_COMP_ORIG_YR6_RT': str, 'NOPELL_COMP_4YR_TRANS_YR6_RT': str, 'NOPELL_COMP_2YR_TRANS_YR6_RT': str, 'NOPELL_WDRAW_ORIG_YR6_RT': str, 'NOPELL_WDRAW_4YR_TRANS_YR6_RT': str, 'NOPELL_WDRAW_2YR_TRANS_YR6_RT': str, 'NOPELL_ENRL_ORIG_YR6_RT': str, 'NOPELL_ENRL_4YR_TRANS_YR6_RT': str, 'NOPELL_ENRL_2YR_TRANS_YR6_RT': str, 'NOPELL_UNKN_ORIG_YR6_RT': str, 'NOPELL_UNKN_4YR_TRANS_YR6_RT': str, 'NOPELL_UNKN_2YR_TRANS_YR6_RT': str, 'FIRSTGEN_DEATH_YR6_RT': str, 'FIRSTGEN_COMP_ORIG_YR6_RT': str, 'FIRSTGEN_COMP_4YR_TRANS_YR6_RT': str, 'FIRSTGEN_COMP_2YR_TRANS_YR6_RT': str, 'FIRSTGEN_WDRAW_ORIG_YR6_RT': str, 'FIRSTGEN_WDRAW_4YR_TRANS_YR6_RT': str, 'FIRSTGEN_WDRAW_2YR_TRANS_YR6_RT': str, 'FIRSTGEN_ENRL_ORIG_YR6_RT': str, 'FIRSTGEN_ENRL_4YR_TRANS_YR6_RT': str, 'FIRSTGEN_ENRL_2YR_TRANS_YR6_RT': str, 'FIRSTGEN_UNKN_ORIG_YR6_RT': str, 'FIRSTGEN_UNKN_4YR_TRANS_YR6_RT': str, 'FIRSTGEN_UNKN_2YR_TRANS_YR6_RT': str, 'NOT1STGEN_DEATH_YR6_RT': str, 'NOT1STGEN_COMP_ORIG_YR6_RT': str, 'NOT1STGEN_COMP_4YR_TRANS_YR6_RT': str, 'NOT1STGEN_COMP_2YR_TRANS_YR6_RT': str, 'NOT1STGEN_WDRAW_ORIG_YR6_RT': str, 'NOT1STGEN_WDRAW_4YR_TRANS_YR6_RT': str, 'NOT1STGEN_WDRAW_2YR_TRANS_YR6_RT': str, 'NOT1STGEN_ENRL_ORIG_YR6_RT': str, 'NOT1STGEN_ENRL_4YR_TRANS_YR6_RT': str, 'NOT1STGEN_ENRL_2YR_TRANS_YR6_RT': str, 'NOT1STGEN_UNKN_ORIG_YR6_RT': str, 'NOT1STGEN_UNKN_4YR_TRANS_YR6_RT': str, 'NOT1STGEN_UNKN_2YR_TRANS_YR6_RT': str, 'RPY_1YR_RT': str, 'COMPL_RPY_1YR_RT': str, 'NONCOM_RPY_1YR_RT': str, 'LO_INC_RPY_1YR_RT': str, 'MD_INC_RPY_1YR_RT': str, 'HI_INC_RPY_1YR_RT': str, 'DEP_RPY_1YR_RT': str, 'IND_RPY_1YR_RT': str, 'PELL_RPY_1YR_RT': str, 'NOPELL_RPY_1YR_RT': str, 'FEMALE_RPY_1YR_RT': str, 'MALE_RPY_1YR_RT': str, 'FIRSTGEN_RPY_1YR_RT': str, 'NOTFIRSTGEN_RPY_1YR_RT': str, 'RPY_3YR_RT': str, 'COMPL_RPY_3YR_RT': str, 'NONCOM_RPY_3YR_RT': str, 'LO_INC_RPY_3YR_RT': str, 'MD_INC_RPY_3YR_RT': str, 'HI_INC_RPY_3YR_RT': str, 'DEP_RPY_3YR_RT': str, 'IND_RPY_3YR_RT': str, 'PELL_RPY_3YR_RT': str, 'NOPELL_RPY_3YR_RT': str, 'FEMALE_RPY_3YR_RT': str, 'MALE_RPY_3YR_RT': str, 'FIRSTGEN_RPY_3YR_RT': str, 'NOTFIRSTGEN_RPY_3YR_RT': str, 'RPY_5YR_RT': str, 'COMPL_RPY_5YR_RT': str, 'NONCOM_RPY_5YR_RT': str, 'LO_INC_RPY_5YR_RT': str, 'MD_INC_RPY_5YR_RT': str, 'HI_INC_RPY_5YR_RT': str, 'DEP_RPY_5YR_RT': str, 'IND_RPY_5YR_RT': str, 'PELL_RPY_5YR_RT': str, 'NOPELL_RPY_5YR_RT': str, 'FEMALE_RPY_5YR_RT': str, 'MALE_RPY_5YR_RT': str, 'FIRSTGEN_RPY_5YR_RT': str, 'NOTFIRSTGEN_RPY_5YR_RT': str, 'RPY_7YR_RT': str, 'COMPL_RPY_7YR_RT': str, 'NONCOM_RPY_7YR_RT': str, 'LO_INC_RPY_7YR_RT': str, 'MD_INC_RPY_7YR_RT': str, 'HI_INC_RPY_7YR_RT': str, 'DEP_RPY_7YR_RT': str, 'IND_RPY_7YR_RT': str, 'PELL_RPY_7YR_RT': str, 'NOPELL_RPY_7YR_RT': str, 'FEMALE_RPY_7YR_RT': str, 'MALE_RPY_7YR_RT': str, 'FIRSTGEN_RPY_7YR_RT': str, 'NOTFIRSTGEN_RPY_7YR_RT': str, 'INC_PCT_LO': str, 'DEP_STAT_PCT_IND': str, 'DEP_INC_PCT_LO': str, 'IND_INC_PCT_LO': str, 'PAR_ED_PCT_1STGEN': str, 'INC_PCT_M1': str, 'INC_PCT_M2': str, 'INC_PCT_H1': str, 'INC_PCT_H2': str, 'DEP_INC_PCT_M1': str, 'DEP_INC_PCT_M2': str, 'DEP_INC_PCT_H1': str, 'DEP_INC_PCT_H2': str, 'IND_INC_PCT_M1': str, 'IND_INC_PCT_M2': str, 'IND_INC_PCT_H1': str, 'IND_INC_PCT_H2': str, 'PAR_ED_PCT_MS': str, 'PAR_ED_PCT_HS': str, 'PAR_ED_PCT_PS': str,
                                'DEP_INC_AVG': float, 'IND_INC_AVG': float, 'OVERALL_YR2_N': 'Int64', 'LO_INC_YR2_N': 'Int64', 'MD_INC_YR2_N': 'Int64', 'HI_INC_YR2_N': 'Int64', 'DEP_YR2_N': 'Int64', 'IND_YR2_N': 'Int64', 'FEMALE_YR2_N': 'Int64', 'MALE_YR2_N': 'Int64', 'PELL_YR2_N': 'Int64', 'NOPELL_YR2_N': 'Int64', 'LOAN_YR2_N': 'Int64', 'NOLOAN_YR2_N': 'Int64', 'FIRSTGEN_YR2_N': 'Int64', 'NOT1STGEN_YR2_N': 'Int64', 'OVERALL_YR3_N': 'Int64', 'LO_INC_YR3_N': 'Int64', 'MD_INC_YR3_N': 'Int64', 'HI_INC_YR3_N': 'Int64', 'DEP_YR3_N': 'Int64', 'IND_YR3_N': 'Int64', 'FEMALE_YR3_N': 'Int64', 'MALE_YR3_N': 'Int64', 'PELL_YR3_N': 'Int64', 'NOPELL_YR3_N': 'Int64', 'LOAN_YR3_N': 'Int64', 'NOLOAN_YR3_N': 'Int64', 'FIRSTGEN_YR3_N': 'Int64', 'NOT1STGEN_YR3_N': 'Int64', 'OVERALL_YR4_N': 'Int64', 'LO_INC_YR4_N': 'Int64', 'MD_INC_YR4_N': 'Int64', 'HI_INC_YR4_N': 'Int64', 'DEP_YR4_N': 'Int64', 'IND_YR4_N': 'Int64', 'FEMALE_YR4_N': 'Int64', 'MALE_YR4_N': 'Int64', 'PELL_YR4_N': 'Int64', 'NOPELL_YR4_N': 'Int64', 'LOAN_YR4_N': 'Int64', 'NOLOAN_YR4_N': 'Int64', 'FIRSTGEN_YR4_N': 'Int64', 'NOT1STGEN_YR4_N': 'Int64', 'OVERALL_YR6_N': 'Int64', 'LO_INC_YR6_N': 'Int64', 'MD_INC_YR6_N': 'Int64', 'HI_INC_YR6_N': 'Int64', 'DEP_YR6_N': 'Int64', 'IND_YR6_N': 'Int64', 'FEMALE_YR6_N': 'Int64', 'MALE_YR6_N': 'Int64', 'PELL_YR6_N': 'Int64', 'NOPELL_YR6_N': 'Int64', 'LOAN_YR6_N': 'Int64', 'NOLOAN_YR6_N': 'Int64', 'FIRSTGEN_YR6_N': 'Int64', 'NOT1STGEN_YR6_N': 'Int64',
                                'DEBT_MDN': float, 'GRAD_DEBT_MDN': float, 'WDRAW_DEBT_MDN': float, 'LO_INC_DEBT_MDN': float, 'MD_INC_DEBT_MDN': float, 'HI_INC_DEBT_MDN': float, 'DEP_DEBT_MDN': float, 'IND_DEBT_MDN': float, 'PELL_DEBT_MDN': float, 'NOPELL_DEBT_MDN': float, 'FEMALE_DEBT_MDN': float, 'MALE_DEBT_MDN': float, 'FIRSTGEN_DEBT_MDN': float, 'NOTFIRSTGEN_DEBT_MDN': float,
                                'DEBT_N': 'Int64', 'GRAD_DEBT_N': 'Int64', 'WDRAW_DEBT_N': 'Int64', 'LO_INC_DEBT_N': 'Int64', 'MD_INC_DEBT_N': 'Int64', 'HI_INC_DEBT_N': 'Int64', 'DEP_DEBT_N': 'Int64', 'IND_DEBT_N': 'Int64', 'PELL_DEBT_N': 'Int64', 'NOPELL_DEBT_N': 'Int64', 'FEMALE_DEBT_N': 'Int64', 'MALE_DEBT_N': 'Int64', 'FIRSTGEN_DEBT_N': 'Int64', 'NOTFIRSTGEN_DEBT_N': 'Int64', 'GRAD_DEBT_MDN10YR': float, 'CUML_DEBT_N': float, 'CUML_DEBT_P90': float, 'CUML_DEBT_P75': float, 'CUML_DEBT_P25': float, 'CUML_DEBT_P10': float, 'INC_N': 'Int64', 'DEP_INC_N': 'Int64', 'IND_INC_N': 'Int64', 'DEP_STAT_N': 'Int64', 'PAR_ED_N': 'Int64', 'APPL_SCH_N': 'Int64',
                                'REPAY_DT_MDN': str, 'SEPAR_DT_MDN': str, 'REPAY_DT_N': 'Int64', 'SEPAR_DT_N': 'Int64', 'RPY_1YR_N': 'Int64', 'COMPL_RPY_1YR_N': 'Int64', 'NONCOM_RPY_1YR_N': 'Int64', 'LO_INC_RPY_1YR_N': 'Int64', 'MD_INC_RPY_1YR_N': 'Int64', 'HI_INC_RPY_1YR_N': 'Int64', 'DEP_RPY_1YR_N': 'Int64', 'IND_RPY_1YR_N': 'Int64', 'PELL_RPY_1YR_N': 'Int64', 'NOPELL_RPY_1YR_N': 'Int64', 'FEMALE_RPY_1YR_N': 'Int64', 'MALE_RPY_1YR_N': 'Int64', 'FIRSTGEN_RPY_1YR_N': 'Int64', 'NOTFIRSTGEN_RPY_1YR_N': 'Int64', 'RPY_3YR_N': 'Int64', 'COMPL_RPY_3YR_N': 'Int64', 'NONCOM_RPY_3YR_N': 'Int64', 'LO_INC_RPY_3YR_N': 'Int64', 'MD_INC_RPY_3YR_N': 'Int64', 'HI_INC_RPY_3YR_N': 'Int64', 'DEP_RPY_3YR_N': 'Int64', 'IND_RPY_3YR_N': 'Int64', 'PELL_RPY_3YR_N': 'Int64', 'NOPELL_RPY_3YR_N': 'Int64', 'FEMALE_RPY_3YR_N': 'Int64', 'MALE_RPY_3YR_N': 'Int64', 'FIRSTGEN_RPY_3YR_N': 'Int64', 'NOTFIRSTGEN_RPY_3YR_N': 'Int64', 'RPY_5YR_N': 'Int64', 'COMPL_RPY_5YR_N': 'Int64', 'NONCOM_RPY_5YR_N': 'Int64', 'LO_INC_RPY_5YR_N': 'Int64', 'MD_INC_RPY_5YR_N': 'Int64', 'HI_INC_RPY_5YR_N': 'Int64', 'DEP_RPY_5YR_N': 'Int64', 'IND_RPY_5YR_N': 'Int64', 'PELL_RPY_5YR_N': 'Int64', 'NOPELL_RPY_5YR_N': 'Int64', 'FEMALE_RPY_5YR_N': 'Int64', 'MALE_RPY_5YR_N': 'Int64', 'FIRSTGEN_RPY_5YR_N': 'Int64', 'NOTFIRSTGEN_RPY_5YR_N': 'Int64', 'COUNT_ED': 'Int64',
                                'LOAN_EVER': float, 'PELL_EVER': float, 'AGE_ENTRY': float, 'AGEGE24': float, 'FEMALE': float, 'MARRIED': float, 'DEPENDENT': float, 'VETERAN': float, 'FIRST_GEN': float,
                                'FAMINC': float, 'MD_FAMINC': float, 'FAMINC_IND': float, 'PCT_WHITE': float, 'PCT_BLACK': float, 'PCT_ASIAN': float, 'PCT_HISPANIC': float, 'PCT_BA': float, 'PCT_GRAD_PROF': float, 'PCT_BORN_US': float, 'MEDIAN_HH_INC': float, 'POVERTY_RATE': float, 'UNEMP_RATE': float,
                                'COUNT_NWNE_P6': 'Int64', 'COUNT_WNE_P6': 'Int64', 'MN_EARN_WNE_P6': 'Int64', 'MD_EARN_WNE_P6': 'Int64', 'PCT10_EARN_WNE_P6': 'Int64', 'PCT25_EARN_WNE_P6': 'Int64', 'PCT75_EARN_WNE_P6': 'Int64', 'PCT90_EARN_WNE_P6': 'Int64', 'SD_EARN_WNE_P6': 'Int64', 'COUNT_WNE_INC1_P6': 'Int64', 'COUNT_WNE_INC2_P6': 'Int64', 'COUNT_WNE_INC3_P6': 'Int64', 'COUNT_WNE_INDEP0_INC1_P6': 'Int64', 'COUNT_WNE_INDEP0_P6': 'Int64', 'COUNT_WNE_INDEP1_P6': 'Int64', 'COUNT_WNE_MALE0_P6': 'Int64', 'COUNT_WNE_MALE1_P6': 'Int64',
                                'GT_25K_P6': float, 'MN_EARN_WNE_INC1_P6': float, 'MN_EARN_WNE_INC2_P6': float, 'MN_EARN_WNE_INC3_P6': float, 'MN_EARN_WNE_INDEP0_INC1_P6': float, 'MN_EARN_WNE_INDEP0_P6': float, 'MN_EARN_WNE_INDEP1_P6': float, 'MN_EARN_WNE_MALE0_P6': float, 'MN_EARN_WNE_MALE1_P6': float, 'DEBT_MDN_SUPP': float, 'GRAD_DEBT_MDN_SUPP': float, 'GRAD_DEBT_MDN10YR_SUPP': float, 'C150_L4_POOLED_SUPP': float, 'C150_4_POOLED_SUPP': float, 'C200_L4_POOLED_SUPP': float, 'C200_4_POOLED_SUPP': float,
                                'ALIAS': str, 'C100_4': float, 'D100_4': 'Int64', 'C100_L4': float, 'D100_L4': 'Int64', 'TRANS_4': float, 'DTRANS_4': 'Int64', 'TRANS_L4': float, 'ICLEVEL': 'Int64',
                                'UGDS_MEN': float, 'UGDS_WOMEN': float, 'CDR3_DENOM': 'Int64', 'CDR2_DENOM': 'Int64', 'T4APPROVALDATE': str, 'OPENADMP': 'Int64', 'UGNONDS': 'Int64', 'GRADS': 'Int64', 'ACCREDCODE': str, 'RET_FT4_POOLED': str,
                                'RET_FTL4_POOLED': float, 'RET_PT4_POOLED': float, 'RET_PTL4_POOLED': float, 'POOLYRSRET_FT': 'Int64', 'POOLYRSRET_PT': 'Int64', 'RET_FT4_POOLED_SUPP': float, 'RET_FTL4_POOLED_SUPP': float, 'RET_PT4_POOLED_SUPP': float, 'RET_PTL4_POOLED_SUPP': float, 'TRANS_4_POOLED': float, 'TRANS_L4_POOLED': float, 'DTRANS_4_POOLED': 'Int64', 'DTRANS_L4_POOLED': 'Int64',
                                'TRANS_4_POOLED_SUPP': float, 'TRANS_L4_POOLED_SUPP': float, 'C100_4_POOLED': float, 'C100_L4_POOLED': float, 'D100_4_POOLED': 'Int64', 'D100_L4_POOLED': 'Int64', 'POOLYRS100': 'Int64',
                                'C100_4_POOLED_SUPP': float, 'C100_L4_POOLED_SUPP': float, 'C150_4_PELL': float, 'D150_4_PELL': 'Int64', 'C150_L4_PELL': float, 'D150_L4_PELL': 'Int64', 'C150_4_LOANNOPELL': float, 'D150_4_LOANNOPELL': 'Int64', 'C150_L4_LOANNOPELL': float, 'D150_L4_LOANNOPELL': 'Int64', 'C150_4_NOLOANNOPELL': float, 'D150_4_NOLOANNOPELL': 'Int64', 'C150_L4_NOLOANNOPELL': float, 'D150_L4_NOLOANNOPELL': 'Int64',
                                'GT_28K_P6': float, 'OMACHT6_FTFT_POOLED': 'Int64', 'SCHTYPE': 'Int64', 'OPEFLAG': 'Int64', 'PRGMOFR': 'Int64',
                                'CIPCODE1': str, 'CIPTITLE1': str, 'CIPTFBS1': 'Int64', 'CIPTFBSANNUAL1': 'Int64', 'MTHCMP1': 'Int64', 'FTFTPCTPELL': float, 'FTFTPCTFLOAN': float, 'UG12MN': 'Int64', 'G12MN': 'Int64', 'POOLYRS_FTFTAIDPCT': 'Int64', 'FTFTPCTPELL_POOLED_SUPP': float, 'FTFTPCTFLOAN_POOLED_SUPP': float,
                                'POOLYRS_PLUSPCT': 'Int64', 'PLUS_DEBT_INST_N': 'Int64', 'PLUS_DEBT_INST_MD': 'Int64', 'PLUS_DEBT_ALL_N': 'Int64', 'PLUS_DEBT_ALL_MD': 'Int64', 'PLUS_DEBT_INST_COMP_N': 'Int64', 'PLUS_DEBT_INST_COMP_MD': 'Int64',
                                'PLUS_DEBT_INST_COMP_MDPAY10': float, 'PLUS_DEBT_INST_COMP_MD_SUPP': 'Int64', 'PLUS_DEBT_INST_COMP_MDPAY10_SUPP': float, 'PLUS_DEBT_ALL_COMP_N': 'Int64', 'PLUS_DEBT_ALL_COMP_MD': 'Int64', 'PLUS_DEBT_ALL_COMP_MDPAY10': float, 'PLUS_DEBT_ALL_COMP_MD_SUPP': 'Int64', 'PLUS_DEBT_ALL_COMP_MDPAY10_SUPP': float, 'PLUS_DEBT_INST_NOCOMP_N': 'Int64',
                                'PLUS_DEBT_INST_NOCOMP_MD': 'Int64', 'PLUS_DEBT_ALL_NOCOMP_N': 'Int64', 'PLUS_DEBT_ALL_NOCOMP_MD': 'Int64', 'PLUS_DEBT_INST_MALE_N': 'Int64', 'PLUS_DEBT_INST_MALE_MD': 'Int64', 'PLUS_DEBT_ALL_MALE_N': 'Int64', 'PLUS_DEBT_ALL_MALE_MD': 'Int64', 'PLUS_DEBT_INST_NOMALE_N': 'Int64', 'PLUS_DEBT_INST_NOMALE_MD': 'Int64', 'PLUS_DEBT_ALL_NOMALE_N': 'Int64', 'PLUS_DEBT_ALL_NOMALE_MD': 'Int64', 'PLUS_DEBT_INST_PELL_N': 'Int64', 'PLUS_DEBT_INST_PELL_MD': 'Int64', 'PLUS_DEBT_ALL_PELL_N': 'Int64', 'PLUS_DEBT_ALL_PELL_MD': 'Int64', 'PLUS_DEBT_INST_NOPELL_N': 'Int64', 'PLUS_DEBT_INST_NOPELL_MD': 'Int64', 'PLUS_DEBT_ALL_NOPELL_N': 'Int64', 'PLUS_DEBT_ALL_NOPELL_MD': 'Int64', 'COUNT_NWNE_3YR': 'Int64', 'COUNT_WNE_3YR': 'Int64', 'CNTOVER150_3YR': 'Int64', 'BBRR1_FED_UG_N': 'Int64',
                                'BBRR1_FED_UG_DFLT': float, 'BBRR1_FED_UG_DLNQ': float, 'BBRR1_FED_UG_FBR': float, 'BBRR1_FED_UG_DFR': float, 'BBRR1_FED_UG_NOPROG': float, 'BBRR1_FED_UG_MAKEPROG': float, 'BBRR1_FED_UG_PAIDINFULL': float, 'BBRR1_FED_UG_DISCHARGE': float, 'BBRR1_FED_UGCOMP_N': 'Int64', 'BBRR1_FED_UGCOMP_DFLT': float, 'BBRR1_FED_UGCOMP_DLNQ': float, 'BBRR1_FED_UGCOMP_FBR': float, 'BBRR1_FED_UGCOMP_DFR': float, 'BBRR1_FED_UGCOMP_NOPROG': float, 'BBRR1_FED_UGCOMP_MAKEPROG': float, 'BBRR1_FED_UGCOMP_PAIDINFULL': float, 'BBRR1_FED_UGCOMP_DISCHARGE': float, 'BBRR1_FED_UGNOCOMP_N': 'Int64', 'BBRR1_FED_UGNOCOMP_DFLT': float, 'BBRR1_FED_UGNOCOMP_DLNQ': float, 'BBRR1_FED_UGNOCOMP_FBR': float, 'BBRR1_FED_UGNOCOMP_DFR': float, 'BBRR1_FED_UGNOCOMP_NOPROG': float, 'BBRR1_FED_UGNOCOMP_MAKEPROG': float, 'BBRR1_FED_UGNOCOMP_PAIDINFULL': float, 'BBRR1_FED_UGNOCOMP_DISCHARGE': float, 'BBRR1_FED_UGUNK_N': 'Int64', 'BBRR1_FED_UGUNK_DFLT': float, 'BBRR1_FED_UGUNK_DLNQ': float, 'BBRR1_FED_UGUNK_FBR': float, 'BBRR1_FED_UGUNK_DFR': float, 'BBRR1_FED_UGUNK_NOPROG': float, 'BBRR1_FED_UGUNK_MAKEPROG': float, 'BBRR1_FED_UGUNK_PAIDINFULL': float, 'BBRR1_FED_UGUNK_DISCHARGE': float, 'BBRR1_FED_GR_N': 'Int64', 'BBRR1_FED_GR_DFLT': float, 'BBRR1_FED_GR_DLNQ': float, 'BBRR1_FED_GR_FBR': float, 'BBRR1_FED_GR_DFR': float, 'BBRR1_FED_GR_NOPROG': float, 'BBRR1_FED_GR_MAKEPROG': float, 'BBRR1_FED_GR_PAIDINFULL': float, 'BBRR1_FED_GR_DISCHARGE': float, 'BBRR1_FED_GRCOMP_N': 'Int64', 'BBRR1_FED_GRCOMP_DFLT': float, 'BBRR1_FED_GRCOMP_DLNQ': float, 'BBRR1_FED_GRCOMP_FBR': float, 'BBRR1_FED_GRCOMP_DFR': float, 'BBRR1_FED_GRCOMP_NOPROG': float, 'BBRR1_FED_GRCOMP_MAKEPROG': float, 'BBRR1_FED_GRCOMP_PAIDINFULL': float, 'BBRR1_FED_GRCOMP_DISCHARGE': float, 'BBRR1_FED_GRNOCOMP_N': 'Int64', 'BBRR1_FED_GRNOCOMP_DFLT': float, 'BBRR1_FED_GRNOCOMP_DLNQ': float, 'BBRR1_FED_GRNOCOMP_FBR': float, 'BBRR1_FED_GRNOCOMP_DFR': float, 'BBRR1_FED_GRNOCOMP_NOPROG': float, 'BBRR1_FED_GRNOCOMP_MAKEPROG': float, 'BBRR1_FED_GRNOCOMP_PAIDINFULL': float, 'BBRR1_FED_GRNOCOMP_DISCHARGE': float,
                                'LPSTAFFORD_CNT': 'Int64', 'LPSTAFFORD_AMT': 'Int64', 'LPPPLUS_CNT': 'Int64', 'LPPPLUS_AMT': 'Int64', 'LPGPLUS_CNT': 'Int64', 'LPGPLUS_AMT': 'Int64', 'FEDSCHCD': str
                                }
                          )

    # Truncate 9 digits ZIP code to 5 digits
    temp_df['ZIP'] = temp_df['ZIP'].str.slice(0, 5)

    # create an indicator column named "ACAD_YR" to identify where rows originate from
    temp_df['ACAD_YR'] = re.findall(r'\d+_\d+', filename)[0]

    # shift column 'ACAD_YR' to first position
    first_column = temp_df.pop('ACAD_YR')
    temp_df.insert(0, 'ACAD_YR', first_column)

    # append all temp_df into one list
    institution_level_list.append(temp_df)

# Concat 23 data frames into one data frame "institution_level_data"
institution_level_data = pd.concat(institution_level_list, axis=0, ignore_index=True)

# Split the "institution_level_data" into 10 data frames because the number of columns exceed Redshift limit 1600 columns
# Columns will be split based on the "dev-category" in the data dictionary
institution_data_dictionary= pd.read_excel(path_to_data_dictionary, sheet_name= 'institution_data_dictionary', engine= 'openpyxl')

# Forward fill to prevent error below since the data dictionary has special structure format
# ValueError: Cannot mask with non-boolean array containing NA / NaN values
institution_data_dictionary['VARIABLE NAME']= institution_data_dictionary['VARIABLE NAME'].fillna(method= 'ffill')

# Replace 4 mis-spelled "VARIABLE NAME" to prevent error below
# KeyError: "['D150_4_AIANOld', 'D150_L4_AIANOld', 'D150_4_HISPOld', 'D150_L4_HISPOld'] not in index"
institution_data_dictionary['VARIABLE NAME']= institution_data_dictionary['VARIABLE NAME'].str.upper()

# Keep only VARIABLE NAME that appear in the columns_to_read_list in the data dictionary (without this NAs error will pop up)
institution_data_dictionary= institution_data_dictionary[institution_data_dictionary['VARIABLE NAME'].isin(columns_to_read_list)]

# Group "VARIABLE NAME" by "dev-category", keep only unique "VARIABLE NAME"
variable_in_each_category= institution_data_dictionary.groupby('dev-category')['VARIABLE NAME'].unique()

# Split the "institution_level_data" into 10 data frames based on 10 "dev-category"
for category in range(len(variable_in_each_category)):
    subset_data= institution_level_data[variable_in_each_category[category]]

    # Keep the "ACAD_YR" and "UNITID" columns from the original data set for each of the subset data
    subset_data['ACAD_YR']= institution_level_data.loc[:, 'ACAD_YR']
    subset_data['UNITID']= institution_level_data.loc[:, 'UNITID']

    # Move these two columns to the first and second position for JOINING purpose
    first_column= subset_data.pop('ACAD_YR')
    second_column= subset_data.pop('UNITID')
    subset_data.insert(0, 'ACAD_YR', first_column)
    subset_data.insert(1, 'UNITID', second_column)

    # Create a variable to store category name
    category_name= variable_in_each_category.reset_index()['dev-category'][category]

    # Un-comment 2 lines below if you want to see what is in each subset_data
    #print(category_name)
    #print(subset_data)

    # Write to 10 csv files
    subset_data.to_csv(f'{output_path}/institution_level_data_{category_name}.csv', index=False, header=True)



## Import all files in output_path ("Cleaned Data Files" folder) to AWS S3
s3_bucket= "sample_bucket" # change the bucket name
profile_name= "sample_user" # change the profile name

# Create a function to upload all files in a directory to a S3 bucket
def upload_files_to_s3(path):
    boto_sess = boto3.Session(profile_name= profile_name)
    s3 = boto_sess.resource('s3')
    bucket = s3.Bucket(s3_bucket)

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path) + 1:], Body=data)

upload_files_to_s3(f'{output_path}')



## Check how much time it took to run this script
end= time.time() # set an end point to measure the elapsed time it took to run script
time_to_run= time.gmtime(end- start) # time to run the script in seconds
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run)) # 4.5 mins
