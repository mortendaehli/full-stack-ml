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

### Run with Docker Compose

Make sure .env is populated, then run docker-compose:

```bash
docker-compose up
```

### "Code" of conduct
We apply the following philosophies:
- Pre-commit with black, flake8, isort and prettier to ensure uniform style throughout the project
- Pre-commit with bandit to uncover security issues within the code
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Semantic versioning](https://semver.org/)

### Todo:
- Add .snyk for dependency scanning
- Create explicitly separate network for backend network vs. Traefik
- Ensure docker containers are running as non-root -> bitnami containers or manual handling
- Use KeyVault or similar for secrets handling instead of environmental variables
- Set up test db.


### Long term todo:
- Change to Oauth (Authorization flow)[https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow] or other flow depending on needs.
- Use Azure (AD as basis for RBAC)[https://docs.microsoft.com/en-us/azure/active-directory/develop/custom-rbac-for-developers]

### Features:
- RBAC
- Use OpenAPI spec for frontend
- Axio for API handling
- Implement machine learning for logged in users
