from setuptools import setup, find_packages


setup(
    name='olxer',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        main=main:main
    ''',
)
# setup(
#     name='olxer',
#     version='0.1',
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         'Click',
#     ],
#     entry_points='''
#         [console_scripts]
#         olxer=olxer.olxer
#     ''',
# )