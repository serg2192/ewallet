import multiprocessing


bind = '0.0.0.0:8080'
backlog = 2048
workers = 2*multiprocessing.cpu_count() + 1
threads = 1
worker_class = 'aiohttp.GunicornWebWorker'
reload = True
# reload_engine = 'inotify'
print_config = True
reuse_port = False
