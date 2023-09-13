import hashlib
import json
import os

import llm
from loguru import logger as logging


class LLMDriver:
    def __init__(self, name, api_key=None, cache_path=None, model_params=None):
        self.model_name = name
        self.model = llm.get_model(name)
        self.model.key = api_key
        self.cache_path = cache_path
        self.model_params = {
            "characteristics": {},
            "heuristic": {},
            "apply_heuristic": {}
        } if model_params is None else model_params

        if self.cache_path is not None and not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path, exist_ok=True)

    def make_cache_key(self, identifier):
        ident = identifier.copy()
        ident.append(self.model_name)
        key_hash = hashlib.md5(str(ident).encode()).hexdigest()

        return key_hash

    def get_cached(self, identifier):
        if self.cache_path is None:
            return None
        hash_key = self.make_cache_key(identifier)
        cache_path = os.path.join(self.cache_path, hash_key)
        if not os.path.exists(cache_path):
            return None
        with open(cache_path) as f:
            return json.load(f)

    def set_cache(self, identifier, data):
        if self.cache_path is None:
            return
        hash_key = self.make_cache_key(identifier)
        cache_path = os.path.join(self.cache_path, hash_key)
        with open(cache_path, 'w') as f:
            json.dump(data, f)

    def ask(self, prompt, is_json=True, variation=0, prevent_cache=False, **kwargs):
        identifier = [prompt, is_json, variation, kwargs]

        if not prevent_cache:
            cached = self.get_cached(identifier)
            if cached is not None:
                return cached

        logging.info(f'Calling API: {prompt} ({self.model_name}, {kwargs})')

        answer = self.model.prompt(prompt, **kwargs).text()

        logging.info(f'Answer: {answer}')

        if is_json:
            try:
                answer = json.loads(answer)
            except Exception:
                logging.error(f"Could not parse JSON in prompt {prompt}. \n Answer: {answer}", )
                answer = None

        if answer is not None:
            self.set_cache(identifier, answer)

        return answer
