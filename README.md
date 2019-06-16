# Github Dashboard


## Usage

1. Create a [github auth token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) and give it repo permissions.

2. Save the above token `export GITHUB_TOKEN=[token]`

3. Download dependencies `python setup.py install` (this project uses Python 3.7.3)

4. Set necessary flask app variable `export FLASK_APP=dashboard`

4. Run the Flask server `flask run` and navigate to [localhost:5000/](localhost:5000/)

## Design

This project uses Flask in the backend with minimal bootstrap CSS and HTML.

Rather than make raw requests to the Github API myself I opted to use the open source
wrapper [PyGithub](https://github.com/PyGithub/PyGithub). This was interesting decision
that I think I would not make again if I were to start over fresh.

While PyGithub made making the requests much simpler and handles all the JSON parsing
for me it also requires either a username/password combination or a token for API
requests.

This is a hassle for users since they may not have a github account, and it's an
unnessary step since you can make unauthenticated requests to the endpoints.

On the backend the way my filters work is a little less than desirable. I didn't have
a good idea of what I wanted the dashboard to look like so I started coding as simply
as I could which I think led to some problems that then became to hard to back out of.
Namely the form submission to search made it so that each filter requires a new fetch
of the same data rather than just a reorganized sort. Adding a cache would definitely
make this easier to deal with.

Cosmetically this is not the best looking dashboard and if I wish I had more time to 
add a few more features (in no particular order):

- Better error pages
- Ability to sort in either asc/desc order
- Dynamic refresh when selecting a new filter
- More color
- Less ugly buttons/layout
