from health_company_data_api.common.abstract_service import AbstractService


class TransactionsService(AbstractService):
    repository_module = "health_company_data_api.repositories.transactions"
    repository_class = "TransactionsRepository"

    def get_transactions(self, transactions_filters: dict) -> list:
        return self.get_repository().get_transactions(transactions_filters)
