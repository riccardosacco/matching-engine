import json
import time
import multiprocessing
import botocore
from boto3 import client as boto3_client

#config = botocore.config.Config(connect_timeout=20, read_timeout=60, retries={'max_attempts': 1})
#config=botocore.client.Config(max_pool_connections=50)
config=botocore.config.Config(max_pool_connections=50)
lambda_client = boto3_client('lambda',config=config)
#lambda_client = boto3_client('lambda')
def runProcess(reqItem):
    start = time.time()
    #ts = reqItem["genre"]
    p_req = lambda_client.invoke(FunctionName="programmeMatchFunction-test-ds",
                                      InvocationType='RequestResponse',#RequestResponse #Event
                                      Payload=json.dumps(reqItem))
    #time.sleep(ts)
    print("Single thread time:"+reqItem["title"], time.time() - start)
    return p_req

def start_process():
    print('Starting', multiprocessing.current_process().name)

def unpack(l_req):
    unpack_res = []
    print("Running threaded max_workers=20 timeout=8")
    threaded_start = time.time()
    builtin_outputs = map(runProcess, l_req)
    print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
        maxtasksperchild=2,
    )
    pool_outputs = pool.map(runProcess, l_req)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print('Pool    :', pool_outputs)

    """ with concurrent.futures.ThreadPoolExecutor(max_workers=20, thread_name_prefix = 'Thread') as executor:
        futures_unpack = {executor.submit(runThread, item): item for item in l_req}        
        try:
            for future in concurrent.futures.as_completed(futures_unpack,timeout=8):
                try:
                    item = futures_unpack[future]
                    l_res = future.result()
                    data = json.loads(l_res['Payload'].read().decode())
                    try: 
                      #if not data['errorMessage']:
                        unpack_res.append(data['body'])
                      #else:
                        #print('Error:'+ data['errorMessage'])                        
                    except Exception as ex:
                        print('Exception: %s' % (ex))
                        print(data)
                except concurrent.futures.TimeoutError as tex:
                    print('TimeoutError')
                    raise tex
                except Exception as e:
                    print('Eccezione: %s' % (e))
               
        except concurrent.futures.TimeoutError as te:
            print('timeout error: %s' % (te))
        except Exception as exc:
            print('generated an exception: %s' % (exc))
        else:
            print('ok') """

    print('fine')
    ##print('fine',*unpack_res)
    print("Overall thread pool time:", time.time() - threaded_start)
    return unpack_res
