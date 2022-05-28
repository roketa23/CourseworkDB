from datetime import datetime
from subprocess import Popen
import yadisk

token = 'AQAAAAAQEPmeAAftsWqwSQxi7kZTvYFSuCscuDU'
y = yadisk.YaDisk(token=token)


def run():
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    y.upload(r'C:\Program Files\backup\backup_here.backup', f'/BackupBD/{date}.backup')
    y.upload(r'C:\Program Files\backup\backup_here.log', f'/BackupBD/{date}.log')


run()