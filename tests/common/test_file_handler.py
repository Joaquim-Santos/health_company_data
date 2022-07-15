import pytest
import os

from health_company_data_api.common.file_handler import get_log_files, load_file
from health_company_data_api.common.exceptions import EntityNotFound


class TestFileHandler:

    def test_get_log_files_with_one_file(self):
        expected_data = ['health_company_data_api.log']

        assert expected_data == get_log_files(os.environ.get("LOGS_FOLDER"))

    def test_load_file_with_retrieved_content(self):
        content = load_file(os.environ.get("LOGS_FOLDER"), 'health_company_data_api.log')
        assert isinstance(content, str)

    def test_load_file_with_file_not_found(self):
        with pytest.raises(EntityNotFound, match='Arquivo health_company_data_api.txt não encontrado.'):
            load_file(os.environ.get("LOGS_FOLDER"), 'health_company_data_api.txt')
