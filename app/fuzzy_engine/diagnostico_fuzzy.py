# fuzzy_engine/diagnostico_fuzzy.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class DiagnosticoFuzzy:
    """
    Motor fuzzy com suporte a múltiplas 'doenças'. Cada doença tem
    seu conjunto de regras. Retorna também quais regras foram acionadas.
    """

    def __init__(self):
        # Universos
        self.febre = ctrl.Antecedent(np.arange(35, 41.1, 0.1), 'febre')
        self.tosse = ctrl.Antecedent(np.arange(0, 11, 1), 'tosse')
        self.saturacao = ctrl.Antecedent(np.arange(70, 101, 1), 'saturacao')
        self.risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

        # Pertinências (reutilizáveis)
        self._criar_pertinencias()

        # Regras por doença
        self.rulesets = {
            'Respiratória': self._rules_respiratoria(),
            'Viral': self._rules_viral(),
            'Bacteriana': self._rules_bacteriana()
        }

        # ControlSystems cache
        self.ctrls = {k: ctrl.ControlSystem(v) for k, v in self.rulesets.items()}

    def _criar_pertinencias(self):
        # febre
        self.febre['normal']   = fuzz.gaussmf(self.febre.universe, 36.5, 0.3)
        self.febre['moderada'] = fuzz.gaussmf(self.febre.universe, 38.0, 0.4)
        self.febre['alta']     = fuzz.trimf(self.febre.universe, [38.5, 40, 41])

        # tosse
        self.tosse['leve']     = fuzz.trimf(self.tosse.universe, [0, 0, 4])
        self.tosse['moderada'] = fuzz.trimf(self.tosse.universe, [2, 5, 8])
        self.tosse['forte']    = fuzz.trimf(self.tosse.universe, [6, 10, 10])

        # saturacao
        self.saturacao['boa']     = fuzz.trimf(self.saturacao.universe, [94, 100, 100])
        self.saturacao['moderada'] = fuzz.trimf(self.saturacao.universe, [88, 94, 98])
        self.saturacao['baixa']   = fuzz.trimf(self.saturacao.universe, [70, 70, 90])

        # risco
        self.risco['baixo']  = fuzz.trimf(self.risco.universe, [0, 0, 50])
        self.risco['medio']  = fuzz.trapmf(self.risco.universe, [30, 50, 70, 90])
        self.risco['alto']   = fuzz.trimf(self.risco.universe, [70, 100, 100])

    # --- Rules for each disease (examples) ---
    def _rules_respiratoria(self):
        r1 = ctrl.Rule(self.febre['alta'] & self.tosse['forte'] & self.saturacao['baixa'], self.risco['alto'])
        r2 = ctrl.Rule(self.febre['moderada'] & self.tosse['moderada'], self.risco['medio'])
        r3 = ctrl.Rule(self.tosse['leve'] & self.saturacao['boa'], self.risco['baixo'])
        r4 = ctrl.Rule(self.saturacao['baixa'] & self.tosse['forte'], self.risco['alto'])
        r5 = ctrl.Rule(self.febre['alta'] & self.saturacao['moderada'], self.risco['medio'])
        r6 = ctrl.Rule(self.febre['normal'] & self.tosse['leve'], self.risco['baixo'])
        return [r1, r2, r3, r4, r5, r6]

    def _rules_viral(self):
        # Exemplo: viral tem febre alta mas tosse moderada
        r1 = ctrl.Rule(self.febre['alta'] & self.tosse['moderada'], self.risco['alto'])
        r2 = ctrl.Rule(self.febre['moderada'] & self.tosse['moderada'], self.risco['medio'])
        r3 = ctrl.Rule(self.febre['normal'] & self.tosse['leve'], self.risco['baixo'])
        r4 = ctrl.Rule(self.saturacao['baixa'] & self.febre['alta'], self.risco['alto'])
        return [r1, r2, r3, r4]

    def _rules_bacteriana(self):
        # Exemplo: bacteriana tende a dar risco alto quando febre alta mesmo sem saturação baixa
        r1 = ctrl.Rule(self.febre['alta'] & (self.tosse['moderada'] | self.tosse['forte']), self.risco['alto'])
        r2 = ctrl.Rule(self.febre['moderada'] & self.tosse['forte'], self.risco['medio'])
        r3 = ctrl.Rule(self.tosse['leve'] & self.saturacao['boa'], self.risco['baixo'])
        r4 = ctrl.Rule(self.febre['alta'] & self.saturacao['baixa'], self.risco['alto'])
        return [r1, r2, r3, r4]

    def calcular_risco(self, disease, febre_val, tosse_val, saturacao_val):
        """
        Retorna (risco_val, fired_rules_indices, simulation object)
        fired_rules_indices: lista de índices das regras que tiveram ativação > 0
        """
        if disease not in self.ctrls:
            raise ValueError("Doença desconhecida")

        csim = ctrl.ControlSystemSimulation(self.ctrls[disease])

        csim.input['febre'] = febre_val
        csim.input['tosse'] = tosse_val
        csim.input['saturacao'] = saturacao_val

        csim.compute()
        risco = csim.output['risco']

        # Determinar regras ativadas: percorrer regras do sistema
        fired = []
        rules = self.rulesets[disease]
        # Para pegar a ativação, precisamos recomputar manualmente as antecedências:
        # skfuzzy não expõe diretamente os graus cada regra após compute() de forma trivial,
        # mas podemos avaliar a antecedência fuzzy usando as funções de pertinência.
        # Iremos aproximar: avaliar MIN/OR conforme cada regra criada e checar se > 0
        for idx, r in enumerate(rules):
            # r.antecedent é uma skfuzzy AntecedentLabel (complex). Para simplicidade,
            # usaremos uma heurística: se as condições textuais estiverem presentes nas labels,
            # testamos os graus:
            try:
                # cada termo antecedent pode ser composto por expr; skfuzzy fornece uma string em r.__repr__.
                # Heurística: verificar presença de labels e calcular grau mínimo (AND) / máximo (OR)
                # Vamos buscar r.antecedent.A que representa um expression tree; para compatibilidade e robustez,
                # calcular manualmente as combinações mais simples (AND das partes).
                antecedent = r.antecedent
                # skfuzzy uses fuzzy expressions; evaluate via .inputs? Fallback:
                # We'll approximate by checking textual labels in repr:
                rep = repr(antecedent)
                # For each known label, compute membership degree and then approximate rule degree
                degrees = []
                # febre labels:
                if "febre" in rep:
                    # check which label name appears
                    for label in ['alta', 'moderada', 'normal']:
                        if f"febre.{label}" in rep:
                            degrees.append(self.febre[label].membership_function(self.febre.universe, febre_val) if hasattr(self.febre[label],'membership_function') else fuzz.interp_membership(self.febre.universe, self.febre[label].mf, febre_val))
                if "tosse" in rep:
                    for label in ['forte','moderada','leve']:
                        if f"tosse.{label}" in rep:
                            degrees.append(self.tosse[label].membership_function(self.tosse.universe, tosse_val) if hasattr(self.tosse[label],'membership_function') else fuzz.interp_membership(self.tosse.universe, self.tosse[label].mf, tosse_val))
                if "saturacao" in rep:
                    for label in ['baixa','moderada','boa']:
                        if f"saturacao.{label}" in rep:
                            degrees.append(self.saturacao[label].membership_function(self.saturacao.universe, saturacao_val) if hasattr(self.saturacao[label],'membership_function') else fuzz.interp_membership(self.saturacao.universe, self.saturacao[label].mf, saturacao_val))
                # fallback: if degrees empty, set 0
                rule_degree = 0.0
                if degrees:
                    # if rule used AND, approx as min; if OR present, max. We're conservative and use min.
                    rule_degree = min(degrees)
                if rule_degree > 0.0:
                    fired.append((idx, float(rule_degree)))
            except Exception:
                continue

        return risco, fired, csim
