import click
from github import Github
import os
import requests
import json
from git import Repo
import jwt
from os import path
import uuid


def process_get_question(get_question):
    if path.exists(".bltools"):
        user_dict = get_user_from_file()
        if not user_dict:
            return dict()
    else:
        username = click.prompt('Please enter username', type=str)
        password = click.prompt('Please enter a password', type=str, hide_input=True)
        user_dict = {"username": username, "password": password}
        add_token_to_file(user_dict)
    result = requests.post('http://127.0.0.1:8000/getAuthorization', data=json.dumps(user_dict))
    result = json.loads(result.content)
    if not result.get("token"):
        exit()
    g = Github(result.get("token"))
    user = g.get_user()
    try:
        repo = user.create_repo(user_dict.get("username") + "_" + get_question[0])
    except Exception as e:
        pass
    try:
        repo.create_file("README.md", "readme", "readme", branch="master")
        repo.create_file("{}.py".format(get_question[0]), get_question[0], get_question[0], branch="master")
        repo.add_to_collaborators(user_dict.get("username"), permission="push")
    except Exception as e:
        pass
    try:
        Repo.clone_from("https://github.com/{}/{}.git".format(result.get("owner"),
                                                              user_dict.get("username") + "_" + get_question[0]),
                        "{}/{}".format(get_question[1], user_dict.get("username") + "_" + get_question[0]),
                        branch='master')

    except Exception as e:
        pass
    return 1


def get_user_from_file():
    with open(".bltools", "r+") as f:
        token = f.read()
        user_dict = jwt.decode(token, "secret", algorithms=['HS256'])
        if not user_dict.get("mac_id") == hex(uuid.getnode()):
            return 0
        return user_dict


def add_token_to_file(user_dict):
    with open(".bltools", "w+") as f:
        encoded_jwt = jwt.encode(
            {'username': user_dict.get("username"), "password": user_dict.get("password"), "mac_id": hex(uuid.getnode())
             }, "secret", algorithm='HS256')
        f.write(encoded_jwt.decode("utf-8"))
    return 1


def process_enter_solution(enter_solution):
    user_dict = get_user_from_file()
    result = requests.post('http://127.0.0.1:8000/getAuthorization', data=json.dumps(user_dict))
    result = json.loads(result.content)
    if not result.get("token"):
        exit()
    repo = Repo("/".join(enter_solution.split("/")[:-1]))
    new_file_path = os.path.join(repo.working_tree_dir, "{}".format(enter_solution))
    repo.index.add([new_file_path])
    repo.index.commit("final_commit")
    repo.remotes.origin.push()
    g = Github(result.get("token"))
    user = g.get_user()
    try:
        repo = user.get_repo(enter_solution.split("/")[-2])
        sb = repo.get_branch("master")
        repo.create_git_ref(ref='refs/heads/Final-Release', sha=sb.commit.sha)
        sha = repo.get_branch("Final-Release").commit.sha
        tag = repo.create_git_tag(tag="v-1.0", message="tag message", object=sha, type="commit")
        ref = "refs/tags/" + tag.tag
        repo.create_git_ref(ref, tag.sha)
    except Exception as e:
        pass
    result = requests.post('http://127.0.0.1:8000/saveTagLink', data=json.dumps(
        {'username': user_dict.get("username"), "repository_name": enter_solution.split("/")[-1]}))
