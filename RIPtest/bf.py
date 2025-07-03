import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *

bf = Session(host="localhost")
bf.set_network('ChainGadget')
SNAPSHOT_DIR = '.'
bf.init_snapshot(SNAPSHOT_DIR, name='snapshot-1', overwrite=True)
print(bf.q.interfaceProperties().answer().frame())
bf.q.interfaceProperties().answer().frame().to_csv('results.csv', index=False)