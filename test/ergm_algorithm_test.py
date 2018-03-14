from study.algorithm.ERGM_algorithm import *
from multiprocessing import Pool

# Default value
filename = "../asset/ergm_sample_data.CSV"
target = "Travel_time"

ERGM(filename, target)

# pool = Pool(processes=4)
# pool.map(ERGM, filename=filename, target=target)
# pool.close()
# pool.join()




