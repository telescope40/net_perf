#Louis DeVictoria
#Python Script to load the dictionary file and jinja2 template to create a configuration

from jinja2 import Environment, FileSystemLoader , StrictUndefined
#Local Directory
file_loader = FileSystemLoader('../Notes')
#Load Environment
env = Environment(loader=file_loader)

#There is two templates for now , we comment out based if we need a spine of leaf config output
### Rack Template
template = env.get_template('filename.j2')
from Fileops_Scripts.nat import data
#Dictionary that contains Variables to populate the template files

def render_cfg():
    #Opens the host device dictionary and pulls the values
    #hostname = (data['device']['hostname'])
    #This will take the hostfile file variables and run through the jinja2 file and output a yaml file
    device_config = template.render(data, undefined=StrictUndefined)
    # Create the device config yaml file
    #device_file = hostname+"yml"


    with open(device_cfg_file, 'w+') as devicecfg:
        devicecfg.write(device_config)
        devicecfg.close()

    #Print the output
    print(device_config)


if __name__ == "__main__":
    render_cfg()
