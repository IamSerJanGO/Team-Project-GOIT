from setuptools import setup, find_namespace_packages

setup(
    name="BotDan",
    version="0.0.0",
    description="Botdan - reincarnation of a suffering person. In the past, he was a boy who\
          was abandoned by a girl because he forgot her name.\
          After this no one knew his fate. In the new life he decided to change.",
    url="https://github.com/IamSerJanGO/Team-Project-GOIT",
    author="Crutch Team: Team leader - Sergey Serov, Scrum master - Zeyneb Khalil, Team soul - Bogdan Sikan,\
          Team brain - Olga Tsyban, Team heart - Maria Khorunzha",
    license="MIT",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["botya = crutching_botdan.main:main"]},
)
