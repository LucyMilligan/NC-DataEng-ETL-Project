from utils.transform_load_utils import get_table_name
import pytest

# import boto3
# from moto import mock_aws
# import os


class TestGetTableName:
    def test_get_table_name_returns_transformed_table_name(self):
        file_key = "2025/3/transformed-sales-2025-03-05 15:00:22.634136"
        expected = "sales"
        result = get_table_name(file_key)
        assert result == expected

    def test_get_table_name_returns_ingested_table_name(self):
        file_key = "2025/3/ingested-sales-2025-03-05 15:00:22.634136"
        expected = "sales"
        result = get_table_name(file_key)
        assert result == expected

    def test_get_table_name_returns_blank(self):
        with pytest.raises(UnboundLocalError):
            file_key = "test"
            get_table_name(file_key)
