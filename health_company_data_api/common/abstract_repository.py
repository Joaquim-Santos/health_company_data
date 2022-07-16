import importlib
import inspect

from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

from health_company_data_api import db
from health_company_data_api.common.exceptions import IntegrityException, EntityNotFound, GenericException


class AbstractRepository(ABC):
    """
        Classe abstrata para criar repositórios.
    """

    @property
    @abstractmethod
    def model_module(self):
        """
            tring para o caminho do módulo de modelo.
        """
        pass

    @property
    @abstractmethod
    def model_class(self):
        """
            tring para o nome da classe do modelo.
        """
        pass

    def _get_model(self):
        """
            Método para retornar uma instância do módulo do modelo.

            Returns
            ----------
            Object
                Uma instância do modelo especificado no atributo 'model_class'.
        """
        model_class = getattr(importlib.import_module(self.model_module), self.model_class)
        return model_class()

    def get_model_columns(self):
        """
            Método para retornar a lista de colunas do modelo do repositório.

            Returns
            ----------
            list
                Lista de string com as colunas do modelo do repositório.
        """
        model_class = getattr(importlib.import_module(self.model_module), self.model_class)
        return [m.key for m in model_class().__table__.columns]

    @staticmethod
    def commit():
        return db.session.commit()

    @staticmethod
    def rollback():
        return db.session.rollback()

    def flush_and_commit(self, new_model=None, commit_at_the_end=True):
        try:
            if new_model is not None:
                db.session.add(new_model)
            db.session.flush()
        except IntegrityError as exception1:
            db.session.rollback()
            raise IntegrityException(f'Erro de integridade ao tentar criar ou atualizar a entidade '
                                     f'{self._get_model().__tablename__}',
                                     payload={'integrity_error': str(exception1)})
        except Exception as exception2:
            db.session.rollback()
            raise GenericException(f'Comportamento inesperado ao tentar criar ou atualizar a entidade '
                                   f'{self._get_model().__tablename__}',
                                   payload={'generic_error': str(exception2)})
        if commit_at_the_end:
            db.session.commit()

    def find(self, id_=None, filters=None):
        """
            Método genérico para encontrar a primeira entidade do modelo do repositório pelo id ou filtros.

            Parameters
            ----------
            id_: int
                Id da entidade refernte à sua chave primária.

            filters
               Filtros do SQLAlchemy para a entidade a ser encontrada.

            Returns
            ----------
            Object
                Primeira entidade do modelo do repositório encontrada com oid.

            Raises
            ----------
            EntityNotFound
                Se não encontrou nenhuma entidade.
        """
        if filters is not None:
            model = self._get_model().query.filter(filters).first()
        else:
            primary_key = inspect(self._get_model().__class__).primary_key[0]
            model = self._get_model().query.filter(primary_key == id_).first()

        if not model:
            raise EntityNotFound(f"Entidade {self._get_model().__tablename__} não encontrada.")

        return model.to_json()

    def find_many(self, filters):
        """
            Método genérico para encontrar as entidades do modelo com base nos filtros.

            Parameters
            ----------
            filters
               Filtros do SQLAlchemy para a entidade a ser encontrada.

            Returns
            ----------
            Object
                Primeira entidade do modelo do repositório encontrada com oid.

            Raises
            ----------
            EntityNotFound
                Se não encontrou nenhuma entidade.
        """
        models = self._get_model().query.filter(filters).all()

        return [model.to_json() for model in models]

    def all(self):
        """
            Método genérico para recuperar todas as entidades do modelo do repositório.

            Returns
            ----------
            Object
                Todas as entidades existentes do modelo do repositório.
        """
        return [item.to_json() for item in self._get_model().query.all()]

    def create(self, attributes, commit_at_the_end=True):
        """
            Método genérico para persistir uma entidade do modelo do repositório.

            Parameters
            ----------
            attributes: dict
                Valores da entidade a ser persistida.

            commit_at_the_end: boolean
                Flag para executar automaticamente o db.session.commit() após inserir o modelo e nenhum erro ocorre.

            Returns
            ----------
            Object
                Entidade depois de persistida.

            IntegrityException
                Se um erro de integridade é identificado durante a criação.
        """
        new_model = self._get_model()

        for key, value in attributes.items():
            if key in self.get_model_columns():
                setattr(new_model, key, value)

        self.flush_and_commit(new_model, commit_at_the_end)
        return new_model.to_json()

    def create_many(self, entities, commit_at_the_end=True):
        """
            Método genérico para persistir uma entidade do modelo do repositório.

            Parameters
            ----------
            entities: list
                Lista de entidades a serem persistidas.

            commit_at_the_end: boolean
                Flag para executar automaticamente o db.session.commit() após inserir as entidades e nenhum erro ocorre.

            Returns
            ----------
            List
                Todas as entidades que foram persistidas.

            IntegrityException
                Se um erro de integridade é identificado durante a criação de alguma entidade.
        """
        new_entities = []
        for entity in entities:
            new_entities.append(
                self.create(entity, commit_at_the_end=False)
            )

        if commit_at_the_end:
            db.session.commit()

        return new_entities

    def update(self, id_, attributes, commit_at_the_end=True, filters=None):
        """
            Método genérico para atualizar uma entidade do modelo do repositório.

            Parameters
            ----------
            id_: int
                Identificador da entidade que precisa ser atualizada.

            attributes: dict
                Valores da entidade que serão atualizados.

            commit_at_the_end: boolean
                Flag para executar automaticamente o db.session.commit() após inserir o modelo e nenhum erro ocorre.

            filters
               Filtros do SQLAlchemy para a entidade que precisa ser atualizada.

            Returns
            ----------
            Object
                Entidade depois de atualizada.

            Raises
            ----------
            EntityNotFound
                Se não encontrou nenhuma entidade.

            IntegrityException
                Se um erro de integridade é identificado durante a criação.
        """
        if filters is not None:
            model = self._get_model().query.filter(filters).first()
        else:
            primary_key = inspect(self._get_model().__class__).primary_key[0]
            model = self._get_model().query.filter((primary_key == id_)).first()

        if not model:
            raise EntityNotFound(f"Entidade {self._get_model().__tablename__} a ser atualizada não encontrada.")

        for key, value in attributes.items():
            if key in model.to_dict().keys():
                setattr(model, key, value)

        self.flush_and_commit(commit_at_the_end=commit_at_the_end)
        return model.to_json()

    def delete(self, id_, commit_at_the_end=True):
        """
           Método genérico para deletar uma entidade do modelo do repositório.

           Parameters
           ----------
           id_: int
               Identificador da entidade que precisa ser deletada.

           commit_at_the_end: boolean
               Flag para executar automaticamente o db.session.commit() após inserir o modelo e nenhum erro ocorr

           Returns
           ----------
           Object
               Objeto com uma mensagem de sucesso após a entidade ser deletada.

           Raises
           ----------
           EntityNotFound
               Se não encontrou nenhuma entidade.
       """
        primary_key = inspect(self._get_model().__class__).primary_key[0]
        model = self._get_model().query.filter(primary_key == id_).first()

        if not model:
            raise EntityNotFound(f"Entidade {self._get_model().__tablename__} a ser apagada não encontrada.")

        db.session.delete(model)

        if commit_at_the_end:
            db.session.commit()

        return {'mensagem': 'Entidade removida com sucesso!'}

    def delete_by_filter(self, filters, commit_at_the_end=True):
        """
           Método genérico para deletar uma entidade do modelo do repositório, com base em um filtro.

           Parameters
           ----------
           filters
               Filtros do SQLAlchemy para as entidades a serem removidas.

           commit_at_the_end: boolean
               Flag para executar automaticamente o db.session.commit() após inserir o modelo e nenhum erro ocorre.

           Returns
           ----------
           Object
               Objeto com uma mensagem de sucesso após as entidades serem deletadas.

       """
        db.session.query(self._get_model().__class__) \
            .filter(filters).delete()

        if commit_at_the_end:
            db.session.commit()

        return {'mensagem': 'Entidades removidas com sucesso!'}
