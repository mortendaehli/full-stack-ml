# full-stack-ml

Demo full stack machine learning

## Developer note

### Local prerequisites

- _Linux, MacOS or Windows with WSL 2_:
- _Python >=3.9_: [Python Docs](https://www.python.org/about/gettingstarted/)
- _Node_: [Node Docs](https://nodejs.org/en/docs/guides/getting-started-guide/)
- _Pip_: [Pip Docs](https://pip.pypa.io/en/stable/getting-started/)
- _Git_: [Git Docs](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- _pre-commit_: [Pre-commit Docs](https://pre-commit.com/)
- _Poetry_: [Poetry Docs](https://python-poetry.org/docs/)
- _Docker and Docker Compose_:
  - [Docker Engine Docs](https://docs.docker.com/engine/)
  - [Docker Compose Docs](https://docs.docker.com/compose/)
- _Snyk_: [Snyk](https://snyk.io/) (Requires license)

Add libraries and projects as source root:
- projects/backend
- libraries/imagenet
- etc.

### "Code" of conduct
We apply the following philosophies:
- Pre-commit with black, flake8, isort and prettier to ensure uniform style throughout the project
- Pre-commit with bandit to uncover security issues within the code
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Semantic versioning](https://semver.org/)

### Todo:
- Change to Oauth Implicit or Authorization flow depending on our needs
- Resolve / investigate node security warnings(!)
- Add .snyk for dependency scanning
- Create separate network for backend -> We do not want to expose all services
- Ensure no environmental variables are used for production. -> KeyVault