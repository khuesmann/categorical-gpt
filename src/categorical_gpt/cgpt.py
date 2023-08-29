import os
import numpy as np
import json
from loguru import logger as logging

DEFAULT_CHARACTERISTIC_PROMPT = "Given a dataset {dataset_name} with a categorical attribute '{category_name}' " \
                                "which has the following possible values: {options}. " \
                                "Identify features and characteristics for the category '{category_name}' to compare the given options. " \
                                "Ensure these characteristics can be represented as a continuous numerical value on a scale from 0 to 100. " \
                                "Be concise. Respond with a valid JSON array that follows the structure ['characteristic1', 'characteristic2', ...]"

DEFAULT_HEURISTIC_PROMPT = "Given a dataset {dataset_name} with a categorical attribute '{category_name}'. " \
                           "A given category option can be described using the characteristics '{characteristic}'. " \
                           "Provide a guiding principle for assigning a numerical value, ranging between 0 and 100, to the specified options. " \
                           "Start your response with 'To assign a numerical value ranging from 0 to 100 for the characteristic {characteristic}, ...' " \
                           "Be concise. Respond with an explanation for the heuristic only, no additional explanations. "

DEFAULT_APPLY_HEURISTIC_PROMPT = "Given a dataset {dataset_name} with a categorical attribute '{category_name}' " \
                                 "which has the following possible values: {options}. " \
                                 "A given option can be described using the characteristic '{characteristic}'. " \
                                 "Allocate a numeric value to each of the options using the heuristic: \n {heuristic} \n " \
                                 "Be concise. Make sure that the values are on a scale from 0 to 100. " \
                                 "Respond with a JSON array only, that follows this structure: \n" \
                                 '{{ "option_1": numerical_value_for_characteristic , ... list all options-number pairs }}'


class CategoricalGPT:
    def __init__(self, llm_driver, category_name, options, dataset_name="", characteristic_prompt=None, heuristic_prompt=None, apply_heuristic_prompt=None,
                 verbose=True):

        if not verbose:
            logging.remove()

        self.category_name = category_name
        self.options = sorted(list(set(options)))
        self.llm = llm_driver
        self.characteristics = []
        self.characteristic_certainties = {}
        self.heuristic_certainties = {}
        self.characteristic_value_stds = {}
        self.characteristic_value_max_diff = {}
        self.characteristic_values = {}
        self.heuristics = {}
        self.dataset_name = f"'{dataset_name}'" if dataset_name else ""
        self.feature_vectors = None
        self.characteristic_prompt = characteristic_prompt if characteristic_prompt is not None else DEFAULT_CHARACTERISTIC_PROMPT
        self.heuristic_prompt = heuristic_prompt if heuristic_prompt is not None else DEFAULT_HEURISTIC_PROMPT
        self.apply_heuristic_prompt = apply_heuristic_prompt if apply_heuristic_prompt is not None else DEFAULT_APPLY_HEURISTIC_PROMPT

    def set_options(self, options):
        self.options = options

    def get_characteristics(self, capitalized=True, append=False, n=1, **kwargs):
        all_characteristics = []
        for i in range(n):
            prompt = self.characteristic_prompt.format(dataset_name=self.dataset_name, category_name=self.category_name, options=json.dumps(self.options))
            characteristics = self.llm.ask(prompt, is_json=True, variation=i, **kwargs)

            if characteristics is not None:
                if capitalized:
                    all_characteristics = all_characteristics + [t.capitalize() for t in characteristics]
                else:
                    all_characteristics = all_characteristics + characteristics

        self.characteristic_certainties = {item: (all_characteristics.count(item) / n) for item in all_characteristics}

        if append:
            self.characteristics += list(set(sorted(self.characteristic_certainties, key=lambda x: self.characteristic_certainties[x])))
            self.characteristics = list(set(self.characteristics))
        else:
            self.characteristics = list(set(sorted(self.characteristic_certainties, key=lambda x: self.characteristic_certainties[x])))

        return self.characteristics, self.characteristic_certainties

    def get_heuristic(self, characteristic, n=1, **kwargs):
        heuristics = []

        for i in range(n):
            prompt = self.heuristic_prompt.format(dataset_name=self.dataset_name, category_name=self.category_name, characteristic=characteristic)
            heuristic = self.llm.ask(prompt, is_json=False, variation=i, **kwargs)

            if heuristic is not None:
                heuristics.append(heuristic)

        self.heuristic_certainties[characteristic] = {item: (heuristics.count(item) / n) for item in heuristics}
        self.heuristics[characteristic] = max(self.heuristic_certainties[characteristic], key=self.heuristic_certainties[characteristic].get)

        return self.heuristics[characteristic], self.heuristic_certainties[characteristic]

    def apply_heuristic(self, characteristic, heuristic, n=1, **kwargs):
        final_assignments = []
        for i in range(n):
            prompt = self.apply_heuristic_prompt.format(
                dataset_name=self.dataset_name, category_name=self.category_name, options=json.dumps(self.options), characteristic=characteristic,
                heuristic=heuristic
            )
            option_assignments = self.llm.ask(prompt, is_json=True, variation=i, **kwargs)

            if option_assignments is None:
                option_assignments = {}

            for option in self.options:
                if option not in option_assignments:
                    option_assignments[option] = -1
                    logging.warning(f"Option '{option}' failed to assign value (characteristic={characteristic}).")

            final_assignments.append(option_assignments)

        average_dict = {}
        std_dict = {}
        max_diff_dict = {}

        keys = final_assignments[0].keys()  # Assuming all dictionaries have the same keys

        for key in keys:
            values = [d[key] for d in final_assignments]
            average_dict[key] = sum(values) / len(values)
            std_dict[key] = np.std(values)
            max_diff_dict[key] = np.max(values) - np.min(values)

        self.characteristic_value_stds[characteristic] = std_dict
        self.characteristic_values[characteristic] = average_dict
        self.characteristic_value_max_diff[characteristic] = max_diff_dict

        return self.characteristic_values[characteristic], (self.characteristic_value_stds[characteristic], self.characteristic_value_max_diff[characteristic])

    def transform(self, characteristic_model_params={}, heuristic_model_params={}, apply_heuristic_model_params={}):
        characteristics, _ = self.get_characteristics(**characteristic_model_params)
        for characteristic in characteristics:
            heuristic, _ = self.get_heuristic(characteristic=characteristic, **heuristic_model_params)
            value_assignments, _ = self.apply_heuristic(characteristic=characteristic, heuristic=heuristic, **apply_heuristic_model_params)

        self.make_feature_vectors()

        return self.feature_vectors

    def make_feature_vectors(self, as_dict=False):
        option_features = {}

        for option in self.options:
            option_features[option] = {}
            for characteristic in self.characteristics:
                if characteristic not in self.characteristic_values:
                    continue
                v = self.characteristic_values[characteristic][option]
                if not isinstance(v, (int, float)) or v < 0:
                    logging.warning(f"Option '{option}' for characteristic '{characteristic}' failed to assign value.")
                    continue
                option_features[option][characteristic] = v
            if not as_dict:
                option_features[option] = list(option_features[option].values())

        self.feature_vectors = option_features

        return option_features

    def add_characteristic(self, characteristic):
        if characteristic not in self.characteristics:
            self.characteristics = self.characteristics + [characteristic]

    def structure(self):
        return {
            'characteristics': [{"name": c, "is_active": True} for c in self.characteristics],
            'characteristic_certainties': self.characteristic_certainties,
            'heuristics': self.heuristics,
            'heuristic_certainties': self.heuristic_certainties,
            'characteristic_values': self.characteristic_values,
            'characteristic_value_stds': self.characteristic_value_stds,
        }

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def save(self, path):
        with open(path, 'w') as f:
            f.write(
                json.dumps(
                    {
                        'characteristics': self.characteristics,
                        'characteristic_certainties': self.characteristic_certainties,
                        'heuristics': self.heuristics,
                        'heuristic_certainties': self.heuristic_certainties,
                        'characteristic_values': self.characteristic_values,
                        'characteristic_value_stds': self.characteristic_value_stds,
                    }
                )
            )

    def load(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                j = json.loads(f.read())
                for key, value in j.items():
                    setattr(self, key, value)
                self.make_feature_vectors()
                return True
        return False

    def update_from_structure(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                if key == 'characteristics':
                    value = [v['name'] for v in value if v['is_active'] is True]
                setattr(self, key, value)
        self.make_feature_vectors()
