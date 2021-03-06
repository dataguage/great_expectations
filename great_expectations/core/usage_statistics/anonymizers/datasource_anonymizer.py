from great_expectations.core.usage_statistics.anonymizers.anonymizer import Anonymizer
from great_expectations.datasource import Datasource, PandasDatasource, SqlAlchemyDatasource, SparkDFDatasource


class DatasourceAnonymizer(Anonymizer):
    def __init__(self, salt=None):
        super(DatasourceAnonymizer, self).__init__(salt=salt)

        # ordered bottom up in terms of inheritance order
        self._ge_classes = [
            PandasDatasource,
            SqlAlchemyDatasource,
            SparkDFDatasource,
            Datasource
        ]

    def anonymize_datasource_info(self, name, config):
        anonymized_info_dict = dict()
        anonymized_info_dict["anonymized_name"] = self.anonymize(name)

        self.anonymize_object_info(
            anonymized_info_dict=anonymized_info_dict,
            ge_classes=self._ge_classes,
            object_config=config
        )

        if anonymized_info_dict.get("parent_class") == "SqlAlchemyDatasource":
            sqlalchemy_dialect = config["engine"]
            anonymized_info_dict["sqlalchemy_dialect"] = sqlalchemy_dialect

        return anonymized_info_dict
