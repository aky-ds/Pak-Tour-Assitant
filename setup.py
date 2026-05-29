from setuptools import setup,find_packages


def get_requires(file_path:str):
    requires=[]
    with open(file_path) as f:
        requires=f.readlines()
        requires=[require.replace('\n','') for require in requires]
        if '-e .' in requires:
            requires.remove('-e .')
    return requires

setup(
    
    name='Pak Travel Assistant',
    version=0.1,
    author='Ayazulhaq Yousafzai',
    author_email='www.ayazkhan.com.21@gmail.com',
    description='Multi Agentic Pak Travel Assistant',
    install_requires=get_requires('requirements_dev.txt'),
    packages=find_packages()
    
)