from setuptools import setup, find_packages
setup(
    name='django-create-project',
    author='David Ziegler',
    author_email='david.ziegler@gmail.com',
    version='0.1.0',
    url='http://github.com/dziegler/',
    packages=find_packages(),
    package_data = {'': ['files/*.*'],},
    description='a better way to create django projects',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points = {
        'console_scripts':[
            'create_project = create_project.create:main'
        ]
    }
)
