import unittest 
import pprint
import shutil
import tempfile
import os
import time
import re

from submit import * 
from config import JobManager, parameter_grid



class TestJobManager(unittest.TestCase): 

    def setUp(self):
        self.jobmng = JobManager('test.yaml')
        self.tempdir = tempfile.mkdtemp()
        self.jobmng.data['task']['output_dir'] = self.tempdir

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_decode(self):
        self.assertEqual(self.jobmng.script, 'hello_world.py')
        print(self.jobmng)

    def test_grid(self):
        names, grid = parameter_grid(self.jobmng.data['parameters'])
        self.assertListEqual(
            grid, 
            [(20, 1, 8), (20, 5, 8), (30, 1, 8), (30, 5, 8), (40, 1, 8), (40, 5, 8)]
        )
        self.assertListEqual(
            names,
            ['batch_size','epochs','n_neurons_dense']
        )
        self.assertDictEqual(
            self.jobmng.data['jobs'], 
            {'batch_size20__epochs1__n_neurons_dense8': (20, 1, 8),
             'batch_size20__epochs5__n_neurons_dense8': (20, 5, 8),
             'batch_size30__epochs1__n_neurons_dense8': (30, 1, 8),
             'batch_size30__epochs5__n_neurons_dense8': (30, 5, 8),
             'batch_size40__epochs1__n_neurons_dense8': (40, 1, 8),
             'batch_size40__epochs5__n_neurons_dense8': (40, 5, 8)}
        )

    def test_output_dir(self):
        self.jobmng.set_output_dir()
        self.assertSetEqual( set(os.listdir(self.tempdir)), 
                             set(self.jobmng.data['jobs'].keys())
        )
        self.jobmng.write()
        self.assertTrue(os.path.isfile(self.tempdir+'/config.yaml'))

    def test_run_scripts(self):
        self.jobmng.set_output_dir()
        self.jobmng.write_run_scripts()
        cwd = os.getcwd()
        os.chdir(self.tempdir)
        for jobname in self.jobmng.data['jobs'].keys():
            os.listdir(jobname)
            fname = '/'.join([jobname, 'run.sh'])
            self.assertTrue(os.path.isfile(fname))
        os.chdir(cwd)

class TestSubmit(unittest.TestCase): 
    
    def test_submit(self):
        jobmng = JobManager('test_simple.yaml')
        tempdir = tempfile.mkdtemp()
        jobmng.data['task']['output_dir'] = tempdir
        jobmng.set_output_dir()
        jobmng.write_run_scripts()        
        jobmng.write_job_scripts()
        jobmng.submit()
        time.sleep(0.5)
        pattern = re.compile('\d+')
        cwd = os.getcwd()
        os.chdir(tempdir)
        for jobname, jobpars in jobmng.data['jobs'].items():
            os.listdir(jobname)
            fname = '/'.join([jobname, 'nohup.out'])
            self.assertTrue(os.path.isfile(fname))
            with open(fname) as ifile:
                lines = ifile.readlines()
                self.assertTrue(len(lines)==1)
                matches = re.findall(pattern, lines[0])
                self.assertTrue(len(matches)==3)
                pars = [int(m) for m in matches]
                self.assertListEqual(pars, list(jobpars))
        os.chdir(cwd)
        

if __name__ == '__main__':
    unittest.main()
