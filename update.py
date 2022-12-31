import git
repo = git.Repo("https://github.com/vladisloveK/Raspi")
repo.remotes.origin.pull()