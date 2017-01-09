#!/usr/bin/env python3

from flask import Flask, request
from git import Repo

import json
import sys
import os, os.path

#For this to work, 

github_user = open('/opt/git-repos/github-user', 'r').readlines()[0].rstrip()

app = Flask(__name__)

@app.route('/',methods=['POST'])
def foo():
	data = request.get_json()

	print("New commit by: {}".format(data['commits'][0]['author']['name']), file=sys.stderr)
	print("Header: ", request.headers)
	
	proj_name = data['project']['name']
	TOKEN = open('/opt/git-repos/token_{}'.format(proj_name), 'r').readlines()[0].rstrip()
	
	if request.headers['X-Gitlab-Token'] == TOKEN :
		github_link = 'git@github.com:{0}/{1}.git'.format(github_user, proj_name)
		gitlab_link = data['project']['git_http_url']
		repo_path = "/opt/git-repos/{}".format(proj_name)
		
		#Initialize & prepare repo object.
		if os.path.isdir(repo_path) :
			repo = Repo(repo_path)
			github = repo.remotes.github
			gitlab = repo.remotes.origin
			repo.git.fetch()
		else :
			repo = Repo.clone_from(gitlab_link, repo_path)
			github = repo.create_remote('github', github_link)
			gitlab = repo.remotes.origin
			repo.git.fetch()
		
		#Get remotes, pull and push.
		for branch in repo.branches :
			print(branch)
			repo.git.checkout(branch)
			gitlab.pull()
			github.push()
					
		return "OK"
	else :
		return 403

if __name__ == '__main__':
	app.run(port=7080)
