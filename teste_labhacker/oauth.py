from social_core.backends.github import GithubOAuth2


class CustomGithubOAuth2(GithubOAuth2):
    name = "custom-github"
    def get_scope(self):
        scope = super(CustomGithubOAuth2, self).get_scope()     
        scope = scope + ['public_repo', 'user']
        return scope