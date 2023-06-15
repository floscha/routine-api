from importlib import metadata

__version__ = metadata.version(__package__)

del metadata  # avoid polluting the results of dir(__package__)
