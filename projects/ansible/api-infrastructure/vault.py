import json

import requests
import os
import subprocess

VAULT_ADDRESS = os.getenv('VAULT_ADDR', 'http://localhost:8200')
VAULT_TOKEN = os.getenv('VAULT_TOKEN', 'root')


class VaultException(Exception):
    pass

def run(command: list):
    full_command = [
        'kubectl', 'exec', '-it', 'vault-0', '--', *command
    ]
    result = subprocess.run(full_command, capture_output=True, text=True)
    if result.returncode != 0:
        raise VaultException(f"Executing {full_command}:\n\n{result.stderr}")
    return result.stdout

def generate_rootca():
    return run('pki/root/generate/internal', data={"type":"pki"}, method='POST')

def main():
    print(generate_rootca())

if __name__ == '__main__':
    main()
