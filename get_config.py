import yaml
with open("config.yaml") as f:
    config = yaml.load(f.read())

__all__ = (config,)