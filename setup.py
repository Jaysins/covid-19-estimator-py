from setuptools import setup, find_packages

setup(name="covid19-estimator-py", packages=find_packages(),
      install_requires=["falcon==2.0.0", "marshmallow==3.5.1", "six==1.14.0", "python-dateutil==2.8.1",
                        "dicttoxml==1.7.4", "redis==3.4.1"])
