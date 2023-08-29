import os.path
import pickle
import json
import hashlib
import time
import requests
from loguru import logger as logging

from .llm_driver import LLMDriver


class OpenAIDriver(LLMDriver):
    def __init__(self, api_key, cache_path=None):
        self.api_key = api_key
        self.cache_path = cache_path
        if cache_path is not None and not os.path.exists(cache_path):
            os.mkdir(cache_path)

    def cached(self, filename, result=None, prevent_cache=False):
        if self.cache_path is None:
            return result

        cache_path = os.path.join(self.cache_path, filename + '.pkl')
        if result is None and os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        else:
            if result is not None:
                with open(cache_path, 'wb') as f:
                    pickle.dump(result, f)
            return result

    def ask(self, prompt, is_json=True, variation=0, temperature=0.7, prevent_cache=False, model="gpt-3.5-turbo", n=1, top_p=1):

        key = f"{model} + {prompt} + {str(temperature)} + {json.dumps(is_json)}" + f"{n}" + f"{variation}" + f"{top_p}"
        key_hash = hashlib.md5(key.encode()).hexdigest()

        if self.cache_path is not None and not prevent_cache:
            answer = self.cached(key_hash)

            if answer is not None and not prevent_cache:
                return answer

        answer = self.get_answer(prompt, is_json, model=model, temperature=temperature, n=n, top_p=top_p)
        if self.cache_path is not None and answer is not None and answer != 'n/a':
            logging.info(f'Adding to cache: {answer}')
            self.cached(key_hash, result=answer, prevent_cache=True)

        if answer != 'n/a' and answer is not None:
            return answer
        else:
            logging.error(f"No answer found for prompt {prompt}")
            return None

    def get_answer(self, prompt, is_json=True, is_retry=False, **kwargs):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }
        data = {
            "model": kwargs['model'],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs['temperature'],
            "n": kwargs['n'],
            "top_p": kwargs['top_p']
        }

        try:
            logging.info(f'Calling API (temp={kwargs["temperature"]}, top_p={kwargs["top_p"]}, model={kwargs["model"]}) for prompt: "{prompt}"')
            response = requests.post(url, headers=headers, json=data).json()

            if "error" in response:
                logging.error("POST ERROR: " + response["error"]["message"])
                return None

            answer_data = response["choices"][0]

            if answer_data["finish_reason"] != "stop":
                logging.error(f"Finish reason was not 'stop'. Retrying prompt {prompt}")
                return None

            answer = answer_data["message"]["content"]

            logging.info(f'Answer: "{answer}"')

            if is_json:
                try:
                    answer = json.loads(answer)
                except Exception:
                    logging.warning(f"Could not parse JSON in prompt {prompt}. Answer: {answer}", )
                    return 'n/a'

            return answer
        except Exception as e:
            logging.error(e)
            if not is_retry:
                time.sleep(5)
                return self.get_answer(prompt=prompt, is_json=is_json, is_retry=True, **kwargs)
            return None
