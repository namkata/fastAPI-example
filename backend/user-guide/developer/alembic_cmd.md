# https://alembic.sqlalchemy.org/en/latest/tutorial.html

*  alembic init alembic
*  alembic list_templates

Create a Migration Script:
* alembic revision -m "create account table"

Running our First Migration:
* alembic upgrade head

Partial Revision Identifiers:
* alembic upgrade ae1

Relative Migration Identifiers:
* alembic upgrade +2
* alembic downgrade -1
* alembic upgrade ae10+2

Getting Information:
* alembic current
* alembic history --verbose

Downgrading:
*  alembic downgrade base

Auto generating migrations
* alembic revision --autogenerate -m "Added account table"