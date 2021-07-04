import subprocess
import os
import time

start= time.time() # set a start point to measure the elapsed time it take to run script

input_path= r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\Cleaned Data Files'
for subdir, dirs, files in os.walk(input_path):
    for file in files:
        subprocess.run(f'csvsql -i postgresql {file}', cwd= input_path)

end= time.time() # set an end point to measure the elapsed time it took to run script
time_to_run= time.gmtime(end- start) # time to run the script in seconds
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run)) # 35 mins
