from github import Github

def get_repos(login):
    """ Returns repositories of user as list of dict """
    g = Github()
    try:
        repos = g.get_user(login).get_repos()
    except Exception:
        return {}
    repos = [repo for repo in repos if repo.fork == False]

    returned_dicts = []
    for repo in repos:
        returned_dicts.append( dict([(key[1:],val) for key,val in repo.__dict__.items()]) )

    return returned_dicts


def get_user(login):
    """ Returns info about github user as dict """
    g = Github()
    try:
        user = g.get_user(login)
    except Exception:
        return {}

    return dict([(key[1:],val) for key,val in user.__dict__.items()
                               if type(val).__name__!='instance' or val.__class__.__name__!='_NotSetType'])