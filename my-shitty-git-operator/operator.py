import os
import kopf
import logging
import requests
from github import Github


GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = "" #update with your repo name


g = Github(GITHUB_TOKEN)

try:
    repo = g.get_repo(GITHUB_REPO)
except Exception as e:
    logging.error(f"Error accessing the repository: {e}")
    raise

@kopf.on.create('myresources.mygroup.example.com')
def create_fn(spec, **kwargs):
    # Extract information from the custom resource spec
    branch_name = spec.get('branch', 'default-branch')
    file_path = spec.get('file_path', 'default_file.txt')
    file_content = spec.get('file_content', 'default content')
    pr_title = spec.get('pr_title', 'Default PR Title')
    pr_body = spec.get('pr_body', 'Default PR Body')
    
   
    logging.info(f"Branch: {branch_name}, File Path: {file_path}, PR Title: {pr_title}")
    
    
    create_branch(branch_name)
    
    
    commit_file(branch_name, file_path, file_content)
    
    
    create_pull_request(branch_name, pr_title, pr_body)

def create_branch(branch_name):
    
    main_branch_ref = repo.get_git_ref('heads/main')
    
    repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=main_branch_ref.object.sha)
    logging.info(f"Branch {branch_name} created successfully.")

def commit_file(branch_name, file_path, file_content):
    try:
        
        contents = repo.get_contents(file_path, ref=branch_name)
        repo.update_file(contents.path, f"Update {file_path}", file_content, contents.sha, branch=branch_name)
        logging.info(f"File {file_path} updated successfully.")
    except Exception as e:
        repo.create_file(file_path, f"Create {file_path}", file_content, branch=branch_name)
        logging.info(f"File {file_path} created successfully.")

def create_pull_request(branch_name, pr_title, pr_body):
    pr = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base='main')
    logging.info(f"Pull request {pr_title} created successfully with number {pr.number}.")
