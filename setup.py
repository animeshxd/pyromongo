from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    readme = f.read()
with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

setup(
    name="pyromongo",
    version="0.0.3",
    description="Mongo Session Storage for pyrogram",
    long_description=readme,
    long_description_content_type="text/markdown",
    
    packages=["pyromongo"],

    url="https://github.com/animeshxd/pyromongo",
    author="Animesh Murmu",
    author_email="am2646374@gmail.com",

    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
    ],

    keywords="async mongo session storage pyrogram",
    python_requires=">=3.7.0",
    install_requires=requires,

)
