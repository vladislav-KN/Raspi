import git
repo = git.Repo("<the file directory of your local gihub repo>")
repo.remotes.origin.pull()