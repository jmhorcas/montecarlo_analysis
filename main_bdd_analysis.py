import math 
import random
import statistics

from montecarlo4fms.aafm.fileformats.featureide_parser import FeatureIDEParser
from montecarlo4fms.aafm.fileformats.cnf_reader import CNFReader

from bdd_metamodel.models import BDDModel, VariationPointAnalysis

from evaluation.jhipster import jhipster


PIZZAS_FM = '(Pizza) && (!Normal || Size) && (!Big || Size) && (!Size || Big || Normal) && (!Normal || !Big) && (!Topping || Pizza) && (!Size || Pizza) && (!Dough || Pizza) && (!CheesyCrust || Pizza) && (!Pizza || Topping) && (!Pizza || Size) && (!Pizza || Dough) && (!Salami || Topping) && (!Ham || Topping) && (!Mozzarella || Topping) && (!Topping || Mozzarella || Salami || Ham) && (!Neapolitan || Dough) && (!Sicilian || Dough) && (!Dough || Neapolitan || Sicilian) && (!Sicilian || !Neapolitan) && (!CheesyCrust || Big)'
AAFMFRAMEWORK_EXCERPT_FM = '(AAFMFramework) && (!Packages || AAFMFramework) && (!Solvers || AAFMFramework) && (!System || AAFMFramework) && (!AAFMFramework || System) && (!Linux || System) && (!Win || System) && (!System || Linux || Win) && (!Win || !Linux) && (!python-sat || Packages) && (!pycosat || Packages) && (!pyPicosat || Packages) && (!pyglucose || Packages) && (!Packages || pycosat || python-sat || pyglucose || pyPicosat) && (!MiniSAT || Solvers) && (!PicoSAT || Solvers) && (!Glucose || Solvers) && (!Solvers || MiniSAT || PicoSAT || Glucose) && (!PicoSAT || pycosat || pyPicosat) && (!Glucose || python-sat || pyglucose) && (!MiniSAT || python-sat) && (!Win || !pyPicosat)'
AAFMFRAMEWORK_FM = '(AAFMFramework) && (!python-sat || APISolvers) && (!pycosat || APISolvers) && (!pylgl || APISolvers) && (!pyPicosat || APISolvers) && (!pyglucose || APISolvers) && (!pycryptosat || APISolvers) && (!satyrn || APISolvers) && (!satispy || APISolvers) && (!umo || APISolvers) && (!pydepqbf || APISolvers) && (!APISolvers || satyrn || pycryptosat || satispy || pyglucose || pylgl || pycosat || umo || python-sat || pydepqbf || pyPicosat) && (!pipdeptree || pip) && (!Utils || Packages) && (!ParserTechnology || Packages) && (!DepMng || Packages) && (!APISolvers || Packages) && (!Packages || DepMng) && (!MiniSAT || Solvers) && (!PicoSAT || Solvers) && (!Glucose || Solvers) && (!Lingeling || Solvers) && (!Solvers || Glucose || Lingeling || PicoSAT || MiniSAT) && (!Operations || AutomatedReasoning) && (!Solvers || AutomatedReasoning) && (!AutomatedReasoning || Solvers) && (!ValidModel || Operations) && (!ValidConfiguration || Operations) && (!ValidProduct || Operations) && (!AllProducts || Operations) && (!DeadFeatures || Operations) && (!CoreFeatures || Operations) && (!ErrorDetection || Operations) && (!ErrorDiagnosis || Operations) && (!Operations || ErrorDiagnosis || ErrorDetection || ValidConfiguration || ValidModel || DeadFeatures || ValidProduct || AllProducts || CoreFeatures) && (!Packages || AAFMFramework) && (!Metamodels || AAFMFramework) && (!AutomatedReasoning || AAFMFramework) && (!Interoperability || AAFMFramework) && (!System || AAFMFramework) && (!AAFMFramework || Metamodels) && (!AAFMFramework || System) && (!pip || DepMng) && (!setuptools || DepMng) && (!wheel || DepMng) && (!pkg-resources || DepMng) && (!DepMng || pip) && (!DepMng || setuptools) && (!FeatureIDE || Interoperability) && (!SPLOT || Interoperability) && (!UVL || Interoperability) && (!Interoperability || SPLOT || FeatureIDE || UVL) && (!Linux || System) && (!Win || System) && (!System || Linux || Win) && (!Win || !Linux) && (!antlr4-python3-runtime || ParserTechnology) && (!SimpleParse || ParserTechnology) && (!lark-parser || ParserTechnology) && (!ParserTechnology || antlr4-python3-runtime || lark-parser || SimpleParse) && (!ebnf || lark-parser) && (!FeatureModel || Metamodels) && (!CNFModel || Metamodels) && (!DecisionModel || Metamodels) && (!six || Utils) && (!pybind11 || Utils) && (!Utils || six || pybind11) && (!MiniSAT || satispy || umo || python-sat) && (!Lingeling || satispy || pylgl || python-sat) && (!PicoSAT || pycosat || pyPicosat) && (!Glucose || python-sat || pyglucose) && (pybind11 || !satyrn) && (pybind11 || !pyglucose) && (!python-sat || six) && (!Win || !umo) && (!Win || !pyPicosat) && (!CNFModel || AutomatedReasoning) && (!AutomatedReasoning || CNFModel) && (!Linux || !pip || pkg-resources) && (!UVL || ParserTechnology)'
JHIPSTER = '(JHipster) && (!HazelCast || Hibernate2ndLvlCache) && (!EhCache || Hibernate2ndLvlCache) && (!Hibernate2ndLvlCache || EhCache || HazelCast) && (!HazelCast || !EhCache) && (!MicroserviceApplication || Server) && (!UaaServer || Server) && (!Server || MicroserviceApplication || UaaServer) && (!UaaServer || !MicroserviceApplication) && (!Gradle || BackEnd) && (!Maven || BackEnd) && (!BackEnd || Maven || Gradle) && (!Gradle || !Maven) && (!Generator || JHipster) && (!Authentication || JHipster) && (!SocialLogin || JHipster) && (!Database || JHipster) && (!SpringWebSockets || JHipster) && (!Libsass || JHipster) && (!ClusteredSession || JHipster) && (!BackEnd || JHipster) && (!InternationalizationSupport || JHipster) && (!Docker || JHipster) && (!TestingFrameworks || JHipster) && (!JHipster || Generator) && (!JHipster || Authentication) && (!JHipster || BackEnd) && (!JHipster || TestingFrameworks) && (!MySQL || Production) && (!MariaDB || Production) && (!PostgreSQL || Production) && (!Production || PostgreSQL || MySQL || MariaDB) && (!MariaDB || !MySQL) && (!MySQL || !PostgreSQL) && (!MariaDB || !PostgreSQL) && (!SQL || Database) && (!Cassandra || Database) && (!MongoDB || Database) && (!Database || Cassandra || SQL || MongoDB) && (!SQL || !Cassandra) && (!MongoDB || !SQL) && (!MongoDB || !Cassandra) && (!H2 || Development) && (!PostgreSQLDev || Development) && (!MariaDBDev || Development) && (!MySql || Development) && (!Development || MySql || H2 || PostgreSQLDev || MariaDBDev) && (!PostgreSQLDev || !H2) && (!MariaDBDev || !H2) && (!H2 || !MySql) && (!MariaDBDev || !PostgreSQLDev) && (!PostgreSQLDev || !MySql) && (!MariaDBDev || !MySql) && (!DiskBased || H2) && (!InMemory || H2) && (!H2 || InMemory || DiskBased) && (!DiskBased || !InMemory) && (!Hibernate2ndLvlCache || SQL) && (!Development || SQL) && (!Production || SQL) && (!ElasticSearch || SQL) && (!SQL || Development) && (!SQL || Production) && (!HTTPSession || Authentication) && (!OAuth2 || Authentication) && (!Uaa || Authentication) && (!JWT || Authentication) && (!Authentication || OAuth2 || JWT || HTTPSession || Uaa) && (!HTTPSession || !OAuth2) && (!Uaa || !HTTPSession) && (!HTTPSession || !JWT) && (!Uaa || !OAuth2) && (!JWT || !OAuth2) && (!Uaa || !JWT) && (!Protractor || TestingFrameworks) && (!Gatling || TestingFrameworks) && (!Cucumber || TestingFrameworks) && (!TestingFrameworks || Gatling) && (!TestingFrameworks || Cucumber) && (!MicroserviceGateway || Application) && (!Monolithic || Application) && (!Application || MicroserviceGateway || Monolithic) && (!Monolithic || !MicroserviceGateway) && (!Server || Generator) && (!Application || Generator) && (!Generator || Server || Application) && (!Application || !Server) && (!OAuth2 || SocialLogin || MicroserviceApplication || SQL || MongoDB) && (!SocialLogin || HTTPSession || JWT) && (!SocialLogin || SQL || MongoDB) && (!SocialLogin || Monolithic) && (!UaaServer || Uaa) && (OAuth2 || SocialLogin || MicroserviceApplication || SQL || MongoDB || Cassandra) && (!Server || !Protractor) && (Server || Protractor) && (!MySQL || H2 || MySql) && (JWT || Uaa || !MicroserviceApplication) && (JWT || Uaa || !MicroserviceGateway) && (!Monolithic || JWT || HTTPSession || OAuth2) && (!MariaDB || H2 || MariaDBDev) && (!PostgreSQL || H2 || PostgreSQLDev) && (Application || !SpringWebSockets) && (Application || !ClusteredSession) && (!Libsass || Application)'

N_MC_SIMULATIONS = 100
PERCENTAGE_SIMULATIONS = 0.01
RUNS = 30
DIGIT_PRECISION = 4

def main():
    fide_parser = FeatureIDEParser(jhipster.FM_FILE, no_read_constraints=True)
    fm = fide_parser.transform()

    # Read the feature model as CNF model with complex constraints
    cnf_reader = CNFReader(jhipster.CNF_FILE)
    cnf_model = cnf_reader.transform()

    # Read the jHipster configurations
    jhipster_configurations = jhipster.read_jHipster_feature_model_configurations()


    bdd = BDDModel(feature_model=fm, cnf_formula=JHIPSTER)
    
    print(f"Variables: {bdd.variables}")
    print(f"#Variables: {len(bdd.variables)}")
    print(f"#Configurations: {bdd.get_number_of_configurations()}")
    
    vp_analysis = VariationPointAnalysis(fm, bdd)
    vps = vp_analysis.get_variation_points()
    print(f"#Variation points: {len(vps)}")

    # for vp in vps:
    #     print(f"VP: {vp}")
    #     combinations = vp_analysis.get_variants_combinations(vp)
    #     print(f" |->#{len(combinations)}")
    
    with open("jhipster_analysis.csv", 'w+') as file:
        file.write("Variation points, Variation point, Configurations, Defective configs., Real prob. defect. configs., Simulations, Median defect. configs., Mean defect. configs., Std defect. configs., Prob. defect. configs., Combinations, Variant combination, NofFeatures, Configs. combi., Ratio, Defect. configs. combi., Prob. defect. configs. combi., Simulations, Runs, Median defect. configs., Mean defect. configs., Std defect. configs., Prob. defect. configs.\n")

        for vp in vps:
            # Real probabilities of each variation point
            vp_configurations = bdd.get_configurations(selected_features=[vp])
            vp_defective_configs = [c for c in vp_configurations if jhipster_configurations[c]]
            vp_probability_defective_configs = round(len(vp_defective_configs) / len(vp_configurations), DIGIT_PRECISION)


            # Monte Carlo simulations for the variation point
            vp_simulations = math.ceil(len(vp_configurations) * PERCENTAGE_SIMULATIONS)
            runs = RUNS
            vp_defective_configs_in_sample_per_runs = []
            for r in range(runs):
                vp_sample_configurations = random.sample(vp_configurations, vp_simulations)
                vp_defective_configs_in_sample = [c for c in vp_sample_configurations if jhipster_configurations[c]]
                vp_defective_configs_in_sample_per_runs.append(len(vp_defective_configs_in_sample))

            vp_median_defective_configs_in_sample = round(statistics.median(vp_defective_configs_in_sample_per_runs), DIGIT_PRECISION)
            vp_mean_defective_configs_in_sample = round(statistics.mean(vp_defective_configs_in_sample_per_runs), DIGIT_PRECISION)
            vp_std_defective_configs_in_sample = round(statistics.stdev(vp_defective_configs_in_sample_per_runs), DIGIT_PRECISION)
            vp_sample_median_probability_defective_configs = round(vp_median_defective_configs_in_sample / vp_simulations, DIGIT_PRECISION)

            combinations = vp_analysis.get_variants_combinations(vp)
            variants = vp_analysis.get_variants(vp)
            combinations = variants  # only for optional features analysis 
            optional_choice = [True, False]
            for combi in combinations:
                # Real probabilities of each variant combination
                #selected_features = list(set(combi).union({vp}))
                #deselected_features = list(set(variants) - set(combi))

                # only for optional features analysis 
                original_combi = combi
                for choice in optional_choice:
                    if choice:    
                        combi = [original_combi]  
                        selected_features = combi + [vp]  
                        deselected_features = []
                    else:
                        combi = []  
                        selected_features = [vp]  
                        deselected_features = [original_combi]
                        

                    combi_configurations = bdd.get_configurations(selected_features=selected_features, deselected_features=deselected_features)
                    combi_configurations_ratio = round(len(combi_configurations) / len(vp_configurations), DIGIT_PRECISION)
                    if len(combi_configurations) > 0:
                        combi_defective_configs = [c for c in combi_configurations if jhipster_configurations[c]]
                        combi_probability_defective_configs = round(len(combi_defective_configs) / len(combi_configurations), DIGIT_PRECISION)

                        # Monte Carlo simulations
                        simulations = math.ceil(len(combi_configurations) * PERCENTAGE_SIMULATIONS)
                        # if simulations > len(combi_configurations):
                        #     simulations = len(combi_configurations)
                        runs = RUNS
                        defective_configs_in_sample_per_runs = []
                        for r in range(runs):
                            sample_configurations = random.sample(combi_configurations, simulations)
                            defective_configs_in_sample = [c for c in sample_configurations if jhipster_configurations[c]]
                            defective_configs_in_sample_per_runs.append(len(defective_configs_in_sample))
                        
                        median_defective_configs_in_sample = round(statistics.median(defective_configs_in_sample_per_runs), DIGIT_PRECISION)
                        mean_defective_configs_in_sample = round(statistics.mean(defective_configs_in_sample_per_runs), DIGIT_PRECISION)
                        std_defective_configs_in_sample = round(statistics.stdev(defective_configs_in_sample_per_runs), DIGIT_PRECISION)
                        sample_median_probability_defective_configs = round(median_defective_configs_in_sample / simulations, DIGIT_PRECISION)

                        file.write(f'{len(vps)}, {vp.name}, {len(vp_configurations)}, {len(vp_defective_configs)}, {vp_probability_defective_configs}, ' \
                                    + f'{vp_simulations}, {vp_median_defective_configs_in_sample}, {vp_mean_defective_configs_in_sample}, {vp_std_defective_configs_in_sample}, {vp_sample_median_probability_defective_configs}, ' \
                                    + f'{len(combinations)}, "{[str(f) for f in combi]}", {len(combi)}, {len(combi_configurations)}, {combi_configurations_ratio}, {len(combi_defective_configs)}, {combi_probability_defective_configs}, ' \
                                    + f'{simulations}, {runs}, {median_defective_configs_in_sample}, {mean_defective_configs_in_sample}, {std_defective_configs_in_sample}, {sample_median_probability_defective_configs}\n')
                    else:
                        file.write(f'{len(vps)}, {vp.name}, {len(vp_configurations)}, {len(vp_defective_configs)}, {vp_probability_defective_configs}, ' \
                                + f'{vp_simulations}, {vp_median_defective_configs_in_sample}, {vp_mean_defective_configs_in_sample}, {vp_std_defective_configs_in_sample}, {vp_sample_median_probability_defective_configs}, ' \
                                + f'{len(combinations)}, "{[str(f) for f in combi]}", {len(combi)}, {len(combi_configurations)}, {combi_configurations_ratio}, {0}, {0}, ' \
                                + f'{"-"}, {"-"}, {"-"}, {"-"}, {"-"}, {"-"}\n')

    # for v in bdd.variables:
    #     print(f"#Configs {v}: {bdd.get_number_of_configurations([v])} ({round(bdd.get_number_of_configurations([v]) / bdd.get_number_of_configurations(), 2)})")
    #     print(f"#RealConfigs {v}: {len([c for c in configurations if v in c])}")

def calculate_montecarlo_approximation():
    fide_parser = FeatureIDEParser(jhipster.FM_FILE, no_read_constraints=True)
    fm = fide_parser.transform()

    # Read the feature model as CNF model with complex constraints
    cnf_reader = CNFReader(jhipster.CNF_FILE)
    cnf_model = cnf_reader.transform()

    # Read the jHipster configurations
    jhipster_configurations = jhipster.read_jHipster_feature_model_configurations()

    bdd = BDDModel(feature_model=fm, cnf_formula=JHIPSTER)
    nof_configurations = bdd.get_number_of_configurations()
    all_configurations = bdd.get_configurations()
    all_defective_configs = [c for c in all_configurations if jhipster_configurations[c]]
    all_prob_defect_configs = round(len(all_defective_configs) / len(all_configurations), DIGIT_PRECISION)

    print(f"Variables: {bdd.variables}")
    print(f"#Variables: {len(bdd.variables)}")
    print(f"#Configurations: {len(all_configurations)}")
    
    with open("jhipster_mc_approximation.csv", 'w+') as file:
        file.write("Runs, Total configs., Total Defective configs., Real Prob. Defect. configs., Percentage, Simulations, Median defect. configs., Mean defect. configs., Std defect. configs., Prob. defect. configs., Error\n")

        percentages = [x/1000 for x in range(1, 101, 1)]
        simulations_list = [1] + [x for x in range(10, 5001, 10)]
        #for percentage_sim in percentages:    
        print("Simulation: ", end='', flush=True)
        for simulations in simulations_list:
            runs = RUNS
            #simulations = math.ceil(len(all_configurations) * percentage_sim)
            percentage_sim = round(simulations/len(all_configurations), DIGIT_PRECISION)
            print(f"{simulations} ", end='', flush=True)

            defective_configs_in_sample_per_runs = []
            for r in range(runs):
                sample_configurations = random.sample(all_configurations, simulations)
                defective_configs_in_sample = [c for c in sample_configurations if jhipster_configurations[c]]
                defective_configs_in_sample_per_runs.append(len(defective_configs_in_sample))
                            
            median_defective_configs_in_sample = round(statistics.median(defective_configs_in_sample_per_runs), DIGIT_PRECISION)
            mean_defective_configs_in_sample = round(statistics.mean(defective_configs_in_sample_per_runs), DIGIT_PRECISION)
            std_defective_configs_in_sample = round(statistics.stdev(defective_configs_in_sample_per_runs), DIGIT_PRECISION)
            sample_median_probability_defective_configs = round(median_defective_configs_in_sample / simulations, DIGIT_PRECISION)

            error = round(abs(sample_median_probability_defective_configs - all_prob_defect_configs), DIGIT_PRECISION)
            file.write(f'{runs}, {len(all_configurations)}, {len(all_defective_configs)}, {all_prob_defect_configs}, {percentage_sim}, {simulations}, ' \
                                + f'{median_defective_configs_in_sample}, {mean_defective_configs_in_sample}, {std_defective_configs_in_sample}, {sample_median_probability_defective_configs}, {error}\n')


if __name__ == "__main__":
    main()
    #calculate_montecarlo_approximation()