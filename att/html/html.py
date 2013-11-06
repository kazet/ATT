import os
import shutil
from jinja2 import Environment, FileSystemLoader

def GetHTMLPath():
  return os.path.dirname(os.path.abspath(__file__))

def GetJinja2Env():
  template_path = os.path.join(GetHTMLPath(), 'templates')
  loader = FileSystemLoader(template_path)
  return Environment(loader=loader, trim_blocks=True)

def RenderTemplate(
    template_name,
    template_data,
    output_filename):
  rendered = GetJinja2Env() \
      .get_template(template_name) \
      .render(template_data) \
      .encode('utf-8')
  output = open(output_filename, 'w')
  output.write(rendered)
  output.close()

def CopyDependencies(
    dependencies,
    output_folder):
  for filename in dependencies:
    dst_path = os.path.join(output_folder, filename)
    src_path = os.path.join(GetHTMLPath(), 'dependencies', filename)
    if os.path.exists(dst_path):
      os.remove(dst_path)
    shutil.copyfile(src_path, dst_path) 
