from config import JobManager

if __name__ == '__main__':
    import sys
    jobmng = JobManager(sys.argv[1])
    jobmng.set_output_dir()
    jobmng.write()
    jobmng.write_run_scripts()
    jobmng.write_job_scripts()
    jobmng.submit()
