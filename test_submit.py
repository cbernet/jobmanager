import unittest 
import pprint
import shutil
import tempfile
import os

from submit import * 
from config import JobManager, parameter_grid



class TestJobManager(unittest.TestCase): 
    
    def test_decode(self):
        jobmng = JobManager('test.yaml')
        self.assertEqual(jobmng.script, 'hello_world.py')
        print(jobmng)

    def test_grid(self):
        jobmng = JobManager('test.yaml')
        names, grid = parameter_grid(jobmng.data['parameters'])
        self.assertListEqual(
            grid, 
            [(20, 1, 8), (20, 5, 8), (30, 1, 8), (30, 5, 8), (40, 1, 8), (40, 5, 8)]
        )
        self.assertListEqual(
            names,
            ['batch_size','epochs','n_neurons_dense']
        )
        self.assertDictEqual(
            jobmng.data['jobs'], 
            {'batch_size20__epochs1__n_neurons_dense8': (20, 1, 8),
             'batch_size20__epochs5__n_neurons_dense8': (20, 5, 8),
             'batch_size30__epochs1__n_neurons_dense8': (30, 1, 8),
             'batch_size30__epochs5__n_neurons_dense8': (30, 5, 8),
             'batch_size40__epochs1__n_neurons_dense8': (40, 1, 8),
             'batch_size40__epochs5__n_neurons_dense8': (40, 5, 8)}
        )

    def test_output_dir(self):
        jobmng = JobManager('test.yaml')
        tempdir = tempfile.mkdtemp()
        jobmng.data['task']['output_dir'] = tempdir
        jobmng.set_output_dir()
        self.assertSetEqual( set(os.listdir(tempdir)), 
                             set(jobmng.data['jobs'].keys())
        )
        jobmng.write()
        self.assertTrue(os.path.isfile(tempdir+'/config.yaml'))
        shutil.rmtree(tempdir)

class TestSubmit(unittest.TestCase): 
    
    def test_1(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
