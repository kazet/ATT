import os
import yaml

class BaseFactory(object):
  @classmethod
  def Register(cls, makeable_class):
    cls.CLASSES[makeable_class.__name__] = makeable_class
    return makeable_class

  @classmethod
  def Make(cls, config):
    if not config['class'] in cls.CLASSES:
      raise Exception("[%s] no such class: `%s'\n" % (
                      cls.__class__.__name__,
                      config.get('class', '')))
    else:
      child_cls = cls.CLASSES[config['class']]
      return child_cls(config)


  @classmethod
  def MakeFromFile(cls, file_name):
    try:
      config = yaml.load(open(file_name))
    except Exception, e:
      raise Exception("[%s] unable to load YAML config from %s: %s\n" % (
                      cls.__class__.__name__,
                      file_name,
                      e))
    config['runtime'] = {'config_dir': os.path.dirname(file_name)}
    return cls.Make(config)
