from flask import Flask, request
from git import Repo

import json
import sys
import os, os.path

github_user = 'so-rose'
TOKEN = 'siueyrhg87w35ht8jmwfy7h5g'

app = Flask(__name__)

@app.route('/',methods=['POST'])
def foo():
	data = request.get_json()

	print("New commit by: {}".format(data['commits'][0]['author']['name']), file=sys.stderr)
	print("Header: ", request.headers)
	
	if request.headers['X-Gitlab-Token'] == TOKEN :
		proj_name = data['project']['name']
		github_link = 'git@github.com/{0}/{1}.git'.format(github_user, proj_name)
		gitlab_link = data['project']['git_http_url']
		repo_path = "/opt/git-repos/{}".format(proj_name)
		
		#Initialize & prepare repo object.
		if os.path.isdir(repo_path) :
			repo = Repo(repo_path)
			github = repo.remotes.github
			gitlab = repo.remotes.origin
		else :
			repo = Repo.clone_from(gitlab_link, repo_path)
			github = repo.create_remote('github', github_link)
			gitlab = repo.remotes.origin
		
		#Get remotes, pull and push.
		for branch in repo.branches :
			repo.git.checkout(branch)
			gitlab.pull()
			github.push()
			
		print(github.fetch())
		
		return "OK"
	else :
		return 403

if __name__ == '__main__':
	app.run(port=7080)
