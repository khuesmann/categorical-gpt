# CategoricalGPT

When analyzing heterogeneous data comprising numerical and categorical attributes, it is common to treat the different data types separately or transform the categorical attributes to numerical ones. The transformation has the advantage of facilitating an integrated multi-variate analysis of all attributes. We propose a novel technique for transforming categorical data into interpretable numerical feature vectors using Large Language Models (LLMs). The LLMs are used to identify the categorical attributes' main characteristics and assign numerical values to these characteristics, thus generating a multi-dimensional feature vector. The transformation can be computed fully automatically, but due to the interpretability of the characteristics, it can also be adjusted intuitively by an end user. We provide a respective interactive tool that aims to validate and possibly improve the AI-generated outputs.
Having transformed a categorical attribute, we propose novel methods for ordering and color-coding the categories based on the similarities of the feature vectors.
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

This guide gives you an introduction on how to use CategoricalGPT to perform an automatic (unsupervised) data transformation.

## Define a LLM Driver
This package utilizes the [llm](https://pypi.org/project/llm/) module to interact with different LLMs.
You can define the model parameters for each step of the pipeline. Look up the [llm](https://pypi.org/project/llm/) documentation for more information on how to install new models and which parameters each model can use.

Additionally, you can define a cache path. Prompts to the given LLM can be cached to avoid unnecessary API calls.
```python
from categorical_gpt import LLMDriver

llm_driver = LLMDriver(
    'gpt-3.5-turbo',
    api_key='sk-123456789abc',
    cache_path='path/to/optional/cache',
    model_params={
        "characteristics": {
            "n": 1,
            "temperature": 0.9,
            "top_p": 1
        },
        "heuristic": {
            "n": 1,
            "temperature": 0.7,
            "top_p": 1
        },
        "apply_heuristic": {
            "n": 1,
            "temperature": 0.01,
            "top_p": 0.1
        }
    }
)
```

## Run the transformation
```python
from categorical_gpt import CategoricalGPT

# First define a LLM driver.
llm_driver = ...

# Initialize the CategoricalGPT object with the driver, category name and category options
category_name = 'Car Brand'
category_options = ['Mercedes', 'Ferrari', 'Nissan', 'Kia', 'Ford', 'BMW', 'Bugatti']
cgpt = CategoricalGPT(llm_driver=llm_driver, category_name=category_name, options=category_options)

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
from categorical_gpt import CategoricalGPT

llm_driver = ...

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

In order to supervise the transformatin process, we offer a graphical user interface that can be run via a webserver (Flask). 
See the [Flask](https://flask.palletsprojects.com/en/2.3.x/) documentation for more information.

```python
from categorical_gpt import start_gui

llm_driver = ...

# See Flask documentation for all available parameters
start_gui(llm_driver, debug=True, threaded=True, host="0.0.0.0", port=5001)
```

This will start up the webserver, that can be visited via http://localhost:5001/ . Full guide for the GUI can be found here.
