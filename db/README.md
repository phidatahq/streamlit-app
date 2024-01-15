## Running database migrations

Steps to migrate the database using alembic:

1. Add/update SqlAlchemy tables in the `db/tables` directory.
2. Import the SqlAlchemy class in the `db/tables/__init__.py` file.
3. Create a database revision using: `alembic -c db/alembic.ini revision --autogenerate -m "Revision Name"`
4. Migrate database using: `alembic -c db/alembic.ini upgrade head`

> Note: Set Env Var `MIGRATE_DB = True` to run the database migration in the entrypoint script at container startup.

Checkout the docs on [adding database tables](https://docs.phidata.com/day-2/database-tables).

## Creat a database revision using alembic

Run the alembic command to create a database migration in the dev container:

```bash
docker exec -it streamlit-app-dev alembic -c db/alembic.ini revision --autogenerate -m "Initialize DB"
```

## Migrate development database

Run the alembic command to migrate the dev database:

```bash
docker exec -it streamlit-app-dev alembic -c db/alembic.ini upgrade head
```

## Migrate production database

1. Recommended: Set Env Var `MIGRATE_DB = True` which runs `alembic -c db/alembic.ini upgrade head` from the entrypoint script at container startup.
2. **OR** you can SSH into the production container to run the migration manually

```bash
ECS_CLUSTER=streamlit-app-prd-cluster
TASK_ARN=$(aws ecs list-tasks --cluster streamlit-app-prd-cluster --query "taskArns[0]" --output text)
CONTAINER_NAME=streamlit-app-prd

aws ecs execute-command --cluster $ECS_CLUSTER \
    --task $TASK_ARN \
    --container $CONTAINER_NAME \
    --interactive \
    --command "alembic -c db/alembic.ini upgrade head"
```

---

## How to create the migrations directory

> This has already been run and is described here for completeness

```bash
docker exec -it streamlit-app-dev zsh

cd db
alembic init migrations
```

- After running the above commands, the `db/migrations` directory should be created.
- Update `alembic.ini`
  - set `script_location = db/migrations`
  - uncomment `black` hook in `[post_write_hooks]`
- Update `migrations/env.py` file following [this link](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
