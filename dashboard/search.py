from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request
from github import Github, GithubException, RateLimitExceededException

from dashboard.forms import SearchForm
from dashboard.repository import Repository

bp = Blueprint('search', __name__, url_prefix='/search', template_folder='templates', static_folder='static')


@bp.route('/', methods=['GET', 'POST'])
def search():
    s_form = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(s_form)
    return render_template('index.html', form=s_form)

@bp.route('/results')
def search_results(search):
    search_string = search.data['search']
    sort_type = search.data['select'].lower()
    flash(sort_type)
    repos = search_orgs(search_string, sort_type=sort_type)
    if repos:
        return render_template('index.html', form=search, repos=repos)
    return redirect('/search')

def search_orgs(org, sort_type='stars'):
    git = app.config['_GIT']
    try:
        org = git.get_organization(org)
        found_repos = org.get_repos()
        # TODO: caching.
        repos = [Repository(name=repo.name,
                            stargazers_count=repo.stargazers_count,
                            forks_count=repo.forks_count,
                            contributors_count=repo.get_contributors().totalCount)
                            for repo in found_repos]
        # Sort everyting asc/desc.
        # TODO: sort both ways.
        if sort_type == 'stars':
            repos.sort(key=lambda x: x.stargazers_count, reverse=True)
        elif sort_type == 'contributors':
            repos.sort(key=lambda x: x.contributors_count, reverse=True)
        elif sort_type == 'forks':
            repos.sort(key=lambda x: x.forks_count, reverse=True)
        return repos
    except GithubException as e:
        if isinstance(e, RateLimitExceededException):
            return render_template('rate-limit.html')
        return render_template('error.html')
