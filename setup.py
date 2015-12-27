from distutils.core import setup

py_modules = [
    'pymongo',
    'Flask'
]
setup(
        name='Cafe-Order-System',
        license='MIT',
        author='Prokuma',
        author_email='root@prokuma.kr',
        version='1.0',
        description='Robot Cafe Order System',
        py_modules=py_modules,
      )