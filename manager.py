import os
import operator

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from health_company_data_api import application, db
from health_company_data_api.models import *


# Obtém a configuração a ser usada na aplicação, de acordo com o ambiente.
application.config.from_object('health_company_data_api.configurations.config.' +
                               os.environ['STAGE'].capitalize() + 'Config')

migrate = Migrate(application, db)
manager = Manager(application)

if os.environ['STAGE'].capitalize() in ['Local', 'Test']:
    manager.add_command('db', MigrateCommand)


@manager.command
def drop_db():
    if os.environ['STAGE'].capitalize() == 'Local':
        db.drop_all()
        db.engine.execute('DROP TABLE alembic_version;')


@manager.command
def routes():
    """
        Exibe as rotas da API.
    """
    rules = []
    for rule in application.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
        print(route)


if __name__ == '__main__':
    manager.run()
