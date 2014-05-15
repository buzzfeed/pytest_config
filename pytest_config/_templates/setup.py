try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

setup(name='{project_name}')
