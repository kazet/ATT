"""See `Subclassing conventions' in the documentation."""

import os
import yaml

class BaseFactory(object):
  """A base class for all factories. After registering the classes or
  providing them in the CLASSES variable in the child factory class,
  you will be able to create objects from configuration dictionaries
  or Yaml configuration files.

  Configuration dictionary should contain a class field, containing the
  newly created object class and will be passed to the newly created
  class constructor.

  --- Runtime information ---
  Currently, the one runtime setting is the configuration path.
  If you are creating a class from a yaml file, its path will be passed
  in the config directory (see MakeFromFile documentation), so that
  you will be able to provide relative paths in the config files.
  """
  CLASSES = {}

  @classmethod
  def Register(cls, makeable_class):
    """Register a new class. After Register(), you will be able to
    create an object using ChildFactoryClass.Make(config_dict).

    You may use it as a decorator (@FactoryClass.Register).
    """
    cls.CLASSES[makeable_class.__name__] = makeable_class
    return makeable_class

  @classmethod
  def Make(cls, config):
    """Create an object from a configuration dict."""
    if not config['class'] in cls.CLASSES:
      raise Exception("[%s] no such class: `%s'\n" % (
                      cls.__class__.__name__,
                      config.get('class', '')))
    else:
      child_cls = cls.CLASSES[config['class']]
      return child_cls(config)


  @classmethod
  def MakeFromFile(cls, file_name):
    """Create an object from a configuration file."""
    try:
      config = yaml.load(open(file_name))
    except Exception, exception:
      raise Exception("[%s] unable to load YAML config from %s: %s\n" % (
                      cls.__class__.__name__,
                      file_name,
                      exception))
    config['runtime'] = {'config_dir': os.path.dirname(file_name)}
    return cls.Make(config)
