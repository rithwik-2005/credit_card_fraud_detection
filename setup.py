from setuptools import find_packages, setup


def get_requirements(file_path: str):
    """
    Returns list of requirements from requirements.txt
    """
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")

    return requirements


setup(
    name="credit_card_fraud_detection",
    version="0.0.1",
    author="Vasa Rithwik",
    author_email="rithwikvasa@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=get_requirements("requirements.txt"),
)