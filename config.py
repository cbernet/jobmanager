import yaml
import pprint 
import os
import itertools

def parameter_grid(parameter_dict):
    '''return a tuple: list of parameter names, parameter combinations'''
    values = parameter_dict.values()
    grid = [x for x in itertools.product(*values)]
    return list(parameter_dict.keys()), grid


class JobManager(object): 
    
    def __init__(self, fname): 
        self.fname = fname 
        with open(fname) as ifile: 
            self.data = yaml.load(ifile, Loader=yaml.Loader)
        self._decode()
        self._create_jobs()

    def _decode(self): 
        # self.outdir = self.data['task']['output_dir']
        self.script = os.path.basename(self.data['task']['script'])
        parnames, grid = parameter_grid(self.data['parameters'])
        self.data['info'] = {
            'script':self.script,
            'par_names':parnames,
            'par_values':grid
        }

    def _create_jobs(self):
        job_infos = self.data['info']
        script = job_infos['script']
        par_names = job_infos['par_names']
        values = job_infos['par_values']
        jobs = dict()
        for vals in values:
            namefields = []
            for val,name in zip(vals, par_names):
                namefields.append('{}{}'.format(name,val))
            jobs['__'.join(namefields)] = vals
        self.data['jobs'] = jobs

    def set_output_dir(self):
        odir = self.data['task']['output_dir']
        if not os.path.isdir(odir): 
            os.makedirs(odir)
        oldcwd = os.getcwd()
        os.chdir(odir)
        for jobname in self.data['jobs'].keys():
            os.mkdir(jobname)
        os.chdir(oldcwd)

    def write(self):
        odir = self.data['task']['output_dir']
        if not os.path.isdir(odir): 
            os.makedirs(odir)
        oldcwd = os.getcwd()     
        os.chdir(odir)
        with open('config.yaml', 'w') as ofile:
            ofile.write(yaml.dump(
                self.data
            ))
        os.chdir(oldcwd)

    def __str__(self):
        return pprint.pformat(self.data) 
        
