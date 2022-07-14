from datetime import datetime, timedelta


class Utils:
    """
        Classe que fornece métodos genéricos úteis.
    """

    @staticmethod
    def get_timestamp_number_from_some_day_before_now(days: int):
        """
            Método para obter o valor numérico de timestamp de um determinado dia anterior ao dia atual.

            Parameters
            ----------
            days: int
                Quantidade de dias para subtrair da data atual.

            Returns
            ----------
            int
                Timestamp do dia obtido.
        """
        target_day = (datetime.today() - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
        return int(datetime.timestamp(target_day))

    @staticmethod
    def convert_timestamp_number_to_datetime(timestamp: int):
        """
            Método para converter o valor de timestamp numérico de uma data para o dia correspondente,
            no formato de objeto datetime.

            Parameters
            ----------
            timestamp: int
                Valor em timestamp a ser convertido.

            Returns
            ----------
            datetime
                Objeto datetime correspondente ao timestamp informado.
        """
        return datetime.fromtimestamp(timestamp).replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_datetime_from_some_day_before_now(days: int):
        """
            Método para obter a data de um determinado dia anterior ao dia atual.

            Parameters
            ----------
            days: int
                Quantidade de dias para subtrair da data atual.

            Returns
            ----------
            datetime
                Data do dia obtido.
        """
        return (datetime.today() - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
