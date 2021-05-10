import random

from montecarlo4fms.aafm.models.feature_model import FeatureModel, Feature
from montecarlo4fms.aafm.models.fm_configuration import FMConfiguration

try:
    from dd.cudd import BDD
except ImportError:
    from dd.autoref import BDD


class BDDModel:
    """
    A Binary Decision Diagram (BDD) representation of the feature model given as a CNF formula.

    It relies on the dd module: https://pypi.org/project/dd/
    """

    AND = '&'
    OR = '|'
    NOT = '!'

    def __init__(self, feature_model: FeatureModel, cnf_formula: str):
        self.feature_model = feature_model
        self.cnf = cnf_formula.replace('-', '')
        self.variables = self._extract_variables(self.cnf)
        self.bdd = BDD()  # Instantiate a manager
        self.declare_variables(self.variables)  # Declare variables
        self.expression = self.bdd.add_expr(self.cnf)

    def _extract_variables(self, cnf_formula: str) -> list[str]:
        variables = set()
        for v in cnf_formula.split():
            if BDDModel.AND not in v and BDDModel.OR not in v:
                var = v.strip().replace('(', '').replace(')', '').replace(BDDModel.NOT, '')
                variables.add(var)
        return list(variables)

    def declare_variables(self, variables: list[str]):
        for v in variables:
            self.bdd.declare(v)

    def serialize(self, filepath: str, filetype: str='png'):
        self.bdd.dump(filename=filepath, roots=[self.expression], filetype=filetype)

    def get_number_of_configurations(self, selected_features: list[Feature]=None, deselected_features: list[Feature]=None) -> int:
        if not selected_features:
            expr = self.cnf
        else:
            expr = f' {BDDModel.AND} '.join([f.name for f in selected_features])
        if deselected_features:
            expr += f' {BDDModel.AND} ' +  f' {BDDModel.AND} !'.join([f.name for f in deselected_features])

        expr += f' {BDDModel.AND} ' + '{x}'.format(x=self.expression)
        u = self.bdd.add_expr(expr)
        return self.bdd.count(u, nvars=len(self.variables))
    
    def get_configurations(self, selected_features: list[Feature]=None, deselected_features: list[Feature]=None) -> list[FMConfiguration]:
        if not selected_features:
            expr = self.cnf
        else:
            expr = f' {BDDModel.AND} '.join([f.name for f in selected_features])
        if deselected_features:
            expr += f' {BDDModel.AND} ' +  f' {BDDModel.AND} '.join(['!' + f.name for f in deselected_features])

        expr += f' {BDDModel.AND} ' + '{x}'.format(x=self.expression)
        u = self.bdd.add_expr(expr)
        configs = []
        for c in self.bdd.pick_iter(u, care_vars=self.variables):
            elements = {self.feature_model.get_feature_by_name(f): True for f in c.keys() if c[f]}
            configs.append(FMConfiguration(elements))
        return configs

    # def get_uniform_random_sample(self, size: int) -> list[list[str]]:
    #     """This generates all configurations."""
    #     configs = self.get_configurations()
    #     if size > len(configs):
    #         size = len(configs)
    #     return random.sample(configs, size)

    # def get_random_configuration(self) -> list[str]:
    #     """This follows the Knut algorithm, but needs to be optimized"""
    #     solutions = self.bdd.count(self.expression, nvars=len(self.variables))
    #     expr = ""
    #     variables = list(self.variables)
    #     while solutions > 1:
    #         feature = random.choice(variables)
    #         variables.remove(feature)
    #         possible_expr = expr + f' {BDDModel.AND} '.join([feature]) + f' {BDDModel.AND} '
    #         formula = possible_expr + '{x}'.format(x=self.expression)
    #         u = self.bdd.add_expr(formula)
    #         solutions = self.bdd.count(u, nvars=len(self.variables))
    #         if solutions <= 0:
    #             possible_expr = expr + f' {BDDModel.AND} '.join(['!' + feature]) + f' {BDDModel.AND} '
    #             formula = possible_expr + '{x}'.format(x=self.expression)
    #             u = self.bdd.add_expr(formula)
    #             solutions = self.bdd.count(u, nvars=len(self.variables))
    #         expr = possible_expr
    #     config = self.bdd.pick(u)
    #     return sorted([f for f in config.keys() if config[f]])
        
    # def get_sample_of_configurations(self, size: int) -> list[list[str]]:
    #     """
    #     Bad implementation, we need to: 
    #     The original algorithm by Knuth is specified on BDDs very efficiently, as the probabilities required for all the possible SAT solutions are computed just once with a single BDD traversal, 
    #     and then reused every time a solution is generated.
    #     """

    #     nof_configs = self.get_number_of_configurations()
    #     if size > nof_configs:
    #         size = nof_configs

    #     sample = list()
    #     while len(sample) < size:
    #         config = self.get_random_configuration()
    #         if config not in sample:
    #             sample.append(config)
    #     return sample

