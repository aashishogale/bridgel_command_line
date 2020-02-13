import click
from github import Github
from github import InputGitTreeElement
import os
import requests
import json
from git import Repo
import jwt
from os import path
import uuid            




@click.command()
@click.option('--get_question', default=None)
@click.option('--enter_solution', default=None)
def add_to_git(get_question, enter_solution):

    if get_question: 
        if path.exists(".bltools"):
            with open(".bltools", "r+") as f:
                token =  f.read()
                user_dict = jwt.decode(token, "secret", algorithms=['HS256'])
                if not user_dict.get("mac_id") == hex(uuid.getnode()):
                    exit()
        else:
            username = click.prompt('Please enter username', type=str)
            password = click.prompt('Please enter a password', type=str, hide_input=True)
            user_dict = {"username": username, "password":password}
            with open(".bltools", "w+") as f:
                encoded_jwt = jwt.encode({'username': username, "password":password, "mac_id":hex(uuid.getnode()) 
}, "secret", algorithm='HS256')
                f.write(encoded_jwt.decode("utf-8"))
        result = requests.post('http://127.0.0.1:8000/getAuthorization', data = json.dumps(user_dict))
        result = json.loads(result.content)     
        filepath = os.path
        collaborator = Github(user_dict.get("username"), user_dict.get("password"))
        collaborator_user = collaborator.get_user()       
        if not result.get("token"):
            exit()
        g = Github(result.get("token"))
        user = g.get_user()
        try:
            repo = user.create_repo(user_dict.get("username")+"_"+get_question)
        except Exception as e:
            pass
        try:
            repo.create_file("README.md", "readme", "readme", branch="master")
            repo.create_file("{}.py".format(get_question), get_question, get_question, branch="master")
            repo.add_to_collaborators(user_dict.get("username"), permission="push")
        except Exception as e:
            pass
        try:
            repo = Repo.clone_from("https://github.com/aashishogale/{}.git".format(user_dict.get("username")+"_"+get_question),"/home/anurag/Documents/{}".format(user_dict.get("username")+"_"+get_question), branch='master')
        except Exception as e:
            pass
    if enter_solution:      
        username = click.prompt('Please enter username', type=str)
        password = click.prompt('Please enter a password', type=str, hide_input=True)
        result = requests.post('http://127.0.0.1:8000/getAuthorization', data = json.dumps({'username': username, "password":password}))
        result = json.loads(result.content)
        if not result.get("token"):
            exit()
        repo = Repo("/home/admin2/Documents/{}".format(username+"_"+enter_solution))
        print (repo.working_dir)
        new_file_path = os.path.join(repo.working_tree_dir, "{}.py".format(enter_solution))
        repo.index.add([new_file_path])
        repo.index.commit("final_commit")
        repo.remotes.origin.push()
        g = Github(result.get("token"))
        user = g.get_user()
        try:
            repo = user.get_repo(username+"_"+enter_solution)
            sb = repo.get_branch("master")
            repo.create_git_ref(ref='refs/heads/Final-Release', sha=sb.commit.sha)

            sha = repo.get_branch("Final-Release").commit.sha
            tag = repo.create_git_tag(tag="v-1.0", message="tag message", object=sha, type="commit") 
            ref = "refs/tags/"+ tag.tag
            repo.create_git_ref(ref, tag.sha)
        except Exception as e:
            pass
        result = requests.post('http://127.0.0.1:8000/saveTagLink', data = json.dumps({'username': username, "repository_name":enter_solution}))


        




    


 






     

        



        

    









   
        

        

        


   
    

        # repo.create_file(os.path.abspath(add[1].strip("/")), "init commit", "added")         
        # print(os.path.abspath(add)) 






    
    

