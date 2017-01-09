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
	proj_name = data['project']['name']
	
	print('\n\n {}: Latest commit authored by {}'.format(proj_name, data['commits'][0]['author']['name']))
	
	TOKEN = open('/opt/git-repos/token_{}'.format(proj_name), 'r').readlines()[0].rstrip()
	
	if request.headers['X-Gitlab-Token'] == TOKEN :
		github_link = 'git@github.com:{0}/{1}.git'.format(github_user, proj_name)
		gitlab_link = data['project']['git_http_url']
		repo_path = "/opt/git-repos/{}".format(proj_name)
		
		#Initialize & prepare repo object.
		if os.path.isdir(repo_path) :
			repo = Repo(repo_path)
			github = repo.remotes.github
			gitlab = repo.remotes.gitlab
		else :
			repo = Repo.init(repo_path)
			gitlab = repo.create_remote('gitlab', gitlab_link)
			github = repo.create_remote('github', github_link)
		
		fetchData = gitlab.fetch()
		
		#Get remotes, pull and push.
		for branch in [str(data.ref).split('/')[1] for data in fetchData if 'gitlab' in str(data)] :
			print('Checkout, pull, and push branch: {}'.format(branch))
			repo.git.checkout(branch)
			gitlab.pull()
			github.push()
					
		return "OK"
	else :
		return 403

if __name__ == '__main__':
	app.run(port=7080)
