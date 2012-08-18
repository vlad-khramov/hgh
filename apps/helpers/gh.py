from github import Github

def get_repos(login):
    """returns repositories of user as list of dict"""
    g = Github()
    try:
        repos = g.get_user(login).get_repos()
    except Exception:
        return []
    repos = [repo for repo in repos if repo.fork == False]

    returned_dicts = []
    for repo in repos:
        returned_dicts.append( dict([(key[1:],val) for key,val in repo.__dict__.items()]) )

    return returned_dicts