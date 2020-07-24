import shutil
import tempfile

class WorkDirectory:
    def __init__(self, prefix="workdir"):
        self.prefix = prefix
        self.init_work_dir()
    
    def init_work_dir(self):
        self.work_dir = tempfile.mkdtemp(prefix=self.prefix)

    def get_work_dir(self):
        return  self.work_dir

    def clean(self):
        shutil.rmtree(self.work_dir)