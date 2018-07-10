import shutil
source = data.get('source')
destination = data.get('destination')

shutil.copyfile(source, destination)