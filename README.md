## Streamlit App

This repo contains the code for running a Streamlit App in 2 environments:

1. `dev`: A development environment running locally on docker
2. `prd`: A production environment running on AWS ECS

## Setup Workspace

1. Clone the git repo

> from the `streamlit-app` dir:

2. Create + activate a virtual env:

```sh
python3 -m venv aienv
source aienv/bin/activate
```

3. Install `phidata`:

```sh
pip install phidata
```

4. Setup workspace:

```sh
phi ws setup
```

5. Copy `workspace/example_secrets` to `workspace/secrets`:

```sh
cp -r workspace/example_secrets workspace/secrets
```

6. Optional: Create `.env` file:

```sh
cp example.env .env
```

## Run Streamlit App locally

1. Install [docker desktop](https://www.docker.com/products/docker-desktop)

2. Set OpenAI Key

Set the `OPENAI_API_KEY` environment variable using

```sh
export OPENAI_API_KEY=sk-***
```

**OR** set in the `.env` file

3. Start the workspace using:

```sh
phi ws up
```

Open [localhost:8501](http://localhost:8501) to view the Streamlit App.

4. Stop the workspace using:

```sh
phi ws down
```

## Next Steps:

- [Run the Streamlit App on AWS](https://docs.phidata.com/templates/streamlit-app#run-on-aws)
- [Update the dev application](https://docs.phidata.com/day-2/dev-app)
- [Update the production application](https://docs.phidata.com/day-2/production-app)
- [Add python dependencies](https://docs.phidata.com/day-2/python-libraries)
- [Format & validate your code](https://docs.phidata.com/day-2/format-and-validate)
- [Secret management](https://docs.phidata.com/day-2/secrets)
- [CI/CD](https://docs.phidata.com/day-2/ci-cd)
- [Add database tables](https://docs.phidata.com/day-2/database-tables)
- [Read the LLM App guide](https://docs.phidata.com/templates/llm-app)
