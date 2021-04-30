from famapy.core.transformations import ModelToModel

from famapy.metamodels.pysat_metamodel.models.pysat_model import PySATModel

from bdd_metamodel.models import BDDModel


class PySATToBDD(ModelToModel):
    """Incomplete!!!"""


    @staticmethod
    def get_source_extension() -> str:
        return 'pysat'

    @staticmethod
    def get_destination_extension() -> str:
        return 'bdd'

    def __init__(self, source_model: PySATModel):
        self.source_model = source_model
        self.destination_model = BDDModel()

    def transform(self) -> BDDModel:
        self.destination_model.built(self.source_model.cnf)
        