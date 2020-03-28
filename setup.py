from setuptools import find_packages, setup


setup(
    name='sl-cicd',
    verion='0.1.0',
    packages=find_packages('src', exclude=['test', 'venv']),
    package_dir={'': 'src'},
    install_requires=[
        'boto3==1.9.252'
    ]
)