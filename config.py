import yaml
import pprint 
import os
import itertools

def parameter_grid(parameter_dict):
    '''return a tuple: list of parameter names, parameter combinations'''
    values = parameter_dict.values()
    grid = [x for x in itertools.product(*values)]
    return list(parameter_dict.keys()), grid

def outdir(func):
    def wrapped(self, *args, **kwargs):
        odir = self.data['task']['output_dir']
        if not os.path.isdir(odir): 
            os.makedirs(odir)
        oldcwd = os.getcwd()
        os.chdir(odir)
        func(self, *args, **kwargs)
        os.chdir(oldcwd)
    return wrapped

class JobManager(object): 
    
    def __init__(self, fname): 
        self.fname = fname 
        with open(fname) as ifile: 
            self.data = yaml.load(ifile, Loader=yaml.Loader)
        self._decode()
        self._create_jobs()

    def _decode(self): 
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

    @outdir
    def set_output_dir(self):
        for jobname in self.data['jobs'].keys():
            os.mkdir(jobname)

    @outdir
    def write(self):
        with open('config.yaml', 'w') as ofile:
            ofile.write(yaml.dump(
                self.data
            ))

    @outdir 
    def write_run_scripts(self):
        for jobname, pars in self.data['jobs'].items():
            runscript = '''
{preamble}
{script} {pars}
'''.format(
    preamble = self.data['task']['preamble'],
    script = self.data['task']['script'],
    pars = ' '.join(str(par) for par in pars)
    )
            fname = '/'.join([jobname, 'run.sh'])
            with open(fname, 'w') as ofile:
                ofile.write(runscript)

    @outdir
    def write_job_scripts(self):
        runscript=self.data['task']['job_script']
        for jobname, pars in self.data['jobs'].items():
            fname = '/'.join([jobname, 'job.sh'])
            with open(fname, 'w') as ofile:
                ofile.write(runscript)

    @outdir
    def submit(self):
        subcmd = self.data['task']['sub_cmd']
        for jobname, pars in self.data['jobs'].items():
            cwd = os.getcwd()
            os.chdir(jobname)
            os.system('{} {}'.format(subcmd, 'job.sh'))
            os.chdir(cwd)

    def __str__(self):
        return pprint.pformat(self.data) 
        
