import base64
import logging
import kopf
import tempfile
import paramiko
import os
import git

def read_secret(secret_name, secret_key):
    # Simulated function to read a secret from Kubernetes
    secret_data = {
        'ssh-private-key': 'base64_private_key_here'
    }
    
    try:
        encoded_key = secret_data[secret_key]
        
        # Add padding if necessary
        missing_padding = len(encoded_key) % 4
        if missing_padding:
            encoded_key += '=' * (4 - missing_padding)
        
        try:
            decoded_key = base64.b64decode(encoded_key)
        except base64.binascii.Error as e:
            raise kopf.PermanentError(f"Failed to decode base64 key: {e}")
        
        logging.info(f"Successfully decoded the secret key '{secret_key}' from '{secret_name}'")
        
        # Add debug log to print the decoded key
        logging.debug(f"Decoded key: {decoded_key}")
        
        return decoded_key
    except KeyError:
        raise kopf.PermanentError(f"Secret key '{secret_key}' not found in secret '{secret_name}'")
    except Exception as e:
        raise kopf.PermanentError(f"An error occurred while decoding the secret: {e}")

# Example variables
repo_url = 'git@ssh.dev.azure.com:v3/CloudSpotpl/IaC/test'
branch_name = 'main'
commit_message = 'Initial commit'
code_to_add = 'print(", World!")'

try:
    ssh_key = read_secret('ssh-key-secret', 'ssh-private-key')
except Exception as e:
    logging.error(f"Failed to read SSH key from secret: {e}")
    raise kopf.PermanentError(f"Failed to read SSH key from secret: {e}")

try:
    with tempfile.TemporaryDirectory() as clone_path:

        ssh_key_obj = paramiko.RSAKey(data=ssh_key)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect('ssh.dev.azure.com', username='git', pkey=ssh_key_obj)

        # Set up the GIT_SSH_COMMAND to use paramiko
        os.environ['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no'

        if not repo_url:
            raise ValueError("The repository URL is not set or is invalid.")

        try:

            repo = git.Repo.clone_from(repo_url, clone_path, branch=branch_name)
            logging.info(f"Repository cloned from {repo_url} to {clone_path}")
        except git.exc.GitCommandError as e:
            logging.error(f"Git command failed: {e}")
except Exception as e:
    raise kopf.PermanentError(f"An error occurred: {e}")
