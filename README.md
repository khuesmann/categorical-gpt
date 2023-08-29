# CategoricalGPT

This package is an implementation of the paper "Large Language Models for Categorical Data Transformation".

Due to the lack of an inherent mathematical structure, categorical data are limited or difficult to analyze with conventional techniques. To address this challenge, this paper introduces a novel technique for transforming categorical data into interpretable numerical feature vectors using Large Language Models.

Our approach identifies common characteristics across category options and assigns numerical values to them, creating a multi-dimensional representation that can be readily processed using traditional methods.

# Installation

Install via PIP

```bash
pip install categorical-gpt
```

or install from source

```bash
pip install -e .
```

# Getting Started

## Quick start

This guide gives you an introduction on how to use CategoricalGPT to perform an automatic (unsupervised) data transformation.

```python
from categorical_gpt import OpenAIDriver
from categorical_gpt import CategoricalGPT

# First define a LLM driver.
# This package offers the OpenAI Driver, but you can define your own drivers for different LLMs
llm_driver = OpenAIDriver(cache_path='.cache', api_key='sk-ABC123')

# Initialize the CategoricalGPT object with the driver, category name and category options
cgpt = CategoricalGPT(llm_driver=llm_driver, category_name='Car Brand', options=['Mercedes', 'Ferrari', 'Nissan', 'Kia', 'Ford', 'BMW', 'Bugatti'])

# Perform the full transfromation in one go. You can assign the model parameters for each step of the pipeline.
feature_vectors = cgpt.transform(
    characteristic_model_params={
        "n": 1,
        "temperature": 0.7,
        "top_p": 1
    },
    heuristic_model_params={
        "n": 1,
        "temperature": 0.7,
        "top_p": 1
    },
    apply_heuristic_model_params={
        "n": 1,
        "temperature": 0.01,
        "top_p": 0.1
    }
)
```

## More granular transformation

The above approach shows a single function-call to perform the transformation. You can also use it more granular as follows:

```python
from categorical_gpt import OpenAIDriver
from categorical_gpt import CategoricalGPT

# First define a LLM driver.
# This package offers the OpenAI Driver, but you can define your own drivers for different LLMs
llm_driver = OpenAIDriver(cache_path='.cache', api_key='sk-ABC123')

# Initialize the CategoricalGPT object with the driver, category name and category options
cgpt = CategoricalGPT(llm_driver=llm_driver, category_name='Car Brand', options=['Mercedes', 'Ferrari', 'Nissan', 'Kia', 'Ford', 'BMW', 'Bugatti'])

# Load the characteristics and the frequencies (relative), given the number n of calls to the API
characteristics, characteristic_frequencies = cgpt.get_characteristics(n=1, temperature=0.7, top_p=1, model="gpt-3.5-turbo", prevent_cache=False)

# For each characteristic, we are going to load the heuristic and the value assignments.
for characteristic in characteristics:

    # Load the heuristic for the given characteristic and also get information about the (relative) frequencies depending on the number n of calls to the API
    heuristic, heuristic_frequencies = cgpt.get_heuristic(characteristic=characteristic, n=1, temperature=0.7, top_p=1, model="gpt-3.5-turbo", prevent_cache=False)

    # Given the heuristic and characteristic, load the value assignments for all category options.
    # If n > 1, we return the mean value of all calls to the API. The statistics consists of (value_stds, value_max_diffs).
    value_assignments, value_assignment_statistics = cgpt.apply_heuristic(characteristic=characteristic, heuristic=heuristic)

# After loading all required data, we can create the feature vector
feature_vectors = cgpt.make_feature_vector()
```

## Visualization applications for the transformed data

Given a set of transformed `feature_vectors`, we can apply some approaches that are useful for visualization.

### Embedding

We can perform a Multidimensional Scaling (MDS) embedding on the given feature vectors. Possible distance metrics are `['euclidean', 'cosine', 'pearson']`. Possible normalization strategies are `['minmax', 'meanstd', 'custom']`. For the option `custom`, you have define it like this: `custom:min_val,max_val`, where `min_val` and `max_val` are the numerical values for the normalization.

```python
from categorical_gpt import CategoricalGPT, make_mds_embedding

cgpt = CategoricalGPT(...)

# Make sure that you have a fully loaded cgpt instance with the feature vectors built.
mds, mds_eigen, distance_matrix = make_mds_embedding(cgpt, distance_metric='euclidean', n_dim=3, tolist=False, normalization='minmax')
```

### Color-map

The color-map functionality assigns colors to each category option. The colors are assinged such that similar options share a similar color.

```python
from categorical_gpt import CategoricalGPT, color_coding

cgpt = CategoricalGPT(...)

# Make sure that you have a fully loaded cgpt instance with the feature vectors built.
color_mapping = color_coding(cgpt)
```

### Ordering

We can order the category options, so that category options that are similar are ordered close to each other. We provide multiple methods on how to create ordering: `['mds', 'tsp', 'tsp+mds', 'umap', 'lexicographic']`

```python
from categorical_gpt import CategoricalGPT, ordered_options

cgpt = CategoricalGPT(...)

# Make sure that you have a fully loaded cgpt instance with the feature vectors built.
ordered_options = ordered_options(cgpt, ordering_method='tsp+mds', embedding_distance_metric='euclidean')
```

## Fine-tuning GUI

In order to supervise the transformatin process, we offer a graphical user interface that can be run via a webserver (Flask). In order to use the build-in OpenAI Driver, you have to specify the environment variables `OPENAI_API_KEY=sk-you-key` and `CACHE_PATH=path-to-the-cache` when launching the respective python script.

```python
from categorical_gpt import api

# See Flask documentation for all available parameters
api.run(debug=False, threaded=True, host="0.0.0.0", port=5001)
```

This will start up the webserver, that can be visited via http://localhost:5001/ . Full guide for the GUI can be found here.

Right now, we have mapped two models, `gpt-3.5-turbo` and `gpt-4` to the OpenAI-Driver. If you want to use another model in the GUI, just do the following:

```python
from categorical_gpt import api, driver_mappings

driver_mappings['ANY_OTHER_MODEL_NAME'] = ModelDriverClass(...)
api.run(debug=False, threaded=True, host="0.0.0.0", port=5001)
```
