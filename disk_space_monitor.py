import shutil
import smtplib
from email.mime.text import MIMEText
import platform
import win32api # need to install package: pypiwin32

### FOLLOW STEP 1 THROUGH STEP 3 BEFORE EXECUTE THE SCRIPT

# STEP 1: Change the path you want to check the disk space. For example: "C:\\Users\\znguyen"
path = ""
        # if a path is provided, the disk_space_monitor() function will only check disk space for that path
        # if no path is provided, the disk_space_monitor() function will check all available drives in server

# STEP 2: Set the alert threshold (decimal): if percent_space_available < alert_threshold, alert email will be sent
alert_threshold= 0.25

# STEP 3: Set up the senders and receivers for your email alert
send_from_email= "sample_email@abc.com"
send_to_email= "sample_email_2@abc.com"

# STEP 4: Run the script and check the result
# Define function to monitor disk space and send alert email
def disk_space_monitor():
    # Define function to re-format the output of disk usage (convert bytes to Gb)
    def formatSize(bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            return "Error"
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%.2f Gb" % (G)
            else:
                return "%.2f Mb" % (M)
        else:
            return "%.2f kb" % (kb)

    # Define function to send email alert when percent_space_available < threshold
    def report_via_email():
        '''
        In case you are getting error like this:
        raise SMTPAuthenticationError(code, resp)
        smtplib.SMTPAuthenticationError: (534, b'5.7.14
        Go to this link below and select Turn On
        https://www.google.com/settings/security/lesssecureapps
        '''
        if path:
            msg = MIMEText("Warning! Server: " + '"{}"'.format(server_name) + " path " + '"{}"'.format(path) +
                           " is running out of disk space. Only " + percent_space_available +
                           " (" + free_space + ")" + " space left." + " Please check")
            msg["Subject"] = server_name + " | " + path + " | " + percent_space_available \
                             + " (" + free_space + ")" + " space left"
            msg["From"] = send_from_email
            msg["To"] = send_to_email
            with smtplib.SMTP("smtp-relay.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.sendmail(send_from_email, send_to_email, msg.as_string())
        else:
            msg = MIMEText("Warning! Server: " + '"{}"'.format(server_name) + " path " + '"{}"'.format(i) +
                           " is running out of disk space. Only " + percent_space_available +
                           " (" + free_space + ")" + " space left." + " Please check")
            msg["Subject"] = server_name + " | " + i + " | " + percent_space_available\
                             + " (" + free_space + ")" + " space left"
            msg["From"] = send_from_email
            msg["To"] = send_to_email
            with smtplib.SMTP("smtp-relay.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.sendmail(send_from_email, send_to_email, msg.as_string())

    # Show server name (computer name)
    server_name = platform.node()
    print("Server: ", server_name)

    # Show all available drives
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    print("List of all disk drives in this server: ", drives)
    print("\n")

    # Main part of the outer disk_space_monitor function
    if path: # if a path is provided above, this function only check disk space for that path
             # if no path is provided above, this function will check all available drives in server
        stat = shutil.disk_usage(path)
        print("Disk", '"{}"'.format(path), "statistics in bytes:", stat)
        free_space = formatSize(stat[2])
        percent_space_available = "{0:.0%}".format((stat[2] / stat[0]))
        percent_space_used = "{0:.0%}".format(1 - (stat[2] / stat[0]))
        if stat[2] / stat[0] < alert_threshold:
            print("Free space left:", percent_space_available, "(", free_space, ")")
            print("Warning!!! You has used up to", percent_space_used, "of your disk space")
            print("Low disk space warning sent via email")
            report_via_email()
        else:
            print("Free space left:", percent_space_available, "(", free_space, ")")
    else:
        for i in drives:
            stat= shutil.disk_usage(i)
            print("Disk", '"{}"'.format(i), "statistics in bytes:", stat)
            free_space = formatSize(stat[2])
            percent_space_available= "{0:.0%}".format((stat[2]/ stat[0]))
            percent_space_used= "{0:.0%}".format(1-(stat[2]/ stat[0]))
            if stat[2] / stat[0] < alert_threshold:
                print("Free space left:", percent_space_available, "(", free_space, ")")
                print("Warning!!! You has used up to", percent_space_used, "of your disk space")
                print("Low disk space warning sent via email")
                print("\n")
                report_via_email()
            else:
                print("Free space left:", percent_space_available, "(", free_space, ")")
                print("\n")

disk_space_monitor()
