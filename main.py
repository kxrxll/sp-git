from git import Repo
import threading

# Change to path variable to your backup folder
path = "destination"
repo_url = "git@github.com:{user}/{remote repo}.git"
sec = 3600


def run_on_time(func, sec, path, repo_url):
    # Function for repeating
    def func_wrapper():
        run_on_time(func, sec, path, repo_url)
        func(path, repo_url)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def git_check(path):
    #  Git check and update function
    try:
        repo = Repo.init(path)
    except:
        repo = Repo(path)
    # Add all files in the folder
    repo.git.add('.')
    # Auto commit
    repo.index.commit("Auto commit from backup system")


def push_remote(path, repo_url):
    try:
        repo = Repo.init(path)
    except:
        repo = Repo(path)
    try:
        remote = repo.create_remote('main', repo_url)
    except:
        pass
    remote.push(refspec='{}:{}'.format('main', 'main'))


def remote_commit(path, repo_url):
    git_check(path)
    push_remote(path, repo_url)


run_on_time(remote_commit, sec, path, repo_url)
