import itertools
from typing import Callable 

from montecarlo4fms.aafm.models.feature_model import FeatureModel, Feature
from montecarlo4fms.aafm.models.fm_configuration import FMConfiguration
from montecarlo4fms.aafm.utils import fm_utils

from bdd_metamodel.models import BDDModel


class VariationPointAnalysis:

    def __init__(self, feature_model: FeatureModel, bdd_model: BDDModel):
        self.feature_model = feature_model
        self.bdd_model = bdd_model
        
    def get_variation_points(self) -> list[Feature]:
        return [f for f in self.feature_model.get_features() if len(self.get_variants(f)) > 0]

    def get_variants(self, vp: Feature) -> list[Feature]:
        optional_features = []
        for r in vp.get_relations():
            if r.is_optional():
                optional_features.extend(r.children)
            elif r.is_alternative():
                return r.children
            elif r.is_or():
                return r.children
        return optional_features
        
    def get_variants_combinations(self, vp: Feature) -> list[list[Feature]]:
        variants = self.get_variants(vp)
        if len(variants) == 0:
            return []

        if fm_utils.is_alternative_group(vp):
            return [[v] for v in variants]
        elif fm_utils.is_or_group(vp):
            return self._get_combinations(variants, initial_k=1)
        else:
            return self._get_combinations(variants, initial_k=0)

    def _get_combinations(self, variants: list[Feature], initial_k: int=1) -> list[list[Feature]]:
        combinations = []
        for k in range(initial_k, len(variants)+1, 1):
            for v in itertools.combinations(variants, k):
                combinations.append(list(v))
        return combinations

    # def get_configurations(self, vp: Feature, filter_test: Callable=None) -> list[FMConfiguration]:
    #     configurations = self.bdd_model.get_configurations([vp])
    #     if filter is None:
    #         return configurations
    #     else:
    #         return list(filter(filter_test, configurations))

    
    #def get_uniform_random_sample(self, configurations: list[FMConfiguration], size: int)