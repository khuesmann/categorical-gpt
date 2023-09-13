import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_static_files(path, prefix='src/categorical_gpt/'):
    res = []
    for root, dirs, files in os.walk(path):
        for file in files:
            res.append(os.path.join(root, file).replace(prefix, ''))
    return res

setuptools.setup(
    name="categorical-gpt",
    version="0.1.9",
    author="Karim Huesmann",
    author_email="karimhuesmann@gmail.com",
    description="Transformation of categorical data to numerical feature vectors with Large Language Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khuesmann/categorical-gpt",
    project_urls={
        "Homepage": "https://github.com/khuesmann/categorical-gpt",
        "Bug Tracker": "https://github.com/khuesmann/categorical-gpt/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_dir={"categorical_gpt": "src/categorical_gpt"},
    package_data={
        'categorical_gpt': get_static_files('src/categorical_gpt/gui/.output/public', 'src/categorical_gpt/'),
    },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["scikit-learn", "scikit-image", "numpy", "flask", "flask-cors", "networkx", "umap-learn", "loguru", "requests"],
)
