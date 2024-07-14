# -*- coding: utf-8 -*-
import argparse
import os

from github import Github

TMP_DIR = "tmp/pip_pkgs"
DIR = "pip_pkgs"


def get_me(user):
    return user.get_user().login


def is_me(issue, me):
    return issue.user.login == me


def login(token):
    return Github(token)


def get_repo(user: Github, repo: str):
    return user.get_repo(repo)


def download_pip_pkgs(issue):
    pkg = issue.title.strip()
    os.system(f'pip install {pkg}')
    tmp_dir = os.path.realpath(TMP_DIR)
    os.system(f'mkdir {tmp_dir}')
    target_dir = os.path.realpath(DIR)
    os.system(f'echo {pkg} > {tmp_dir}_tmp2/')
    os.system(f'pip wheel {pkg} -w {tmp_dir}')
    os.system(f'echo "{pkg} ============" > {os.path.join(target_dir, "pkg-list.txt")}')
    os.system(f'ls -lh {tmp_dir} >> {os.path.join(target_dir, "pkg-list.txt")}')
    os.system(f'mv {tmp_dir}/* {target_dir}')


def main(token, repo_name, issue_number):
    user = login(token)
    me = get_me(user)
    repo = get_repo(user, repo_name)
    issue = repo.get_issue(int(issue_number))
    print('issue.title=', issue.title)
    print('issue.html_url=', issue.html_url)
    print('issue.body=', issue.body)
    if issue.comments:
        for c in issue.get_comments():
            if is_me(c, me):
                print('comment.body=', c.body)
    download_pip_pkgs(issue)
    # todo rm
    files = os.listdir('.')
    for f in files:
        print('list dir f=', f)
    print('download ok!')


if __name__ == "__main__":
    if not os.path.exists(DIR):
        os.mkdir(DIR)
        print(f'dir is {os.path.realpath(DIR)}')
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument("--issue_number", help="issue_number")
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
