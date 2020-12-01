import json
import time
from multiprocessing import Pipe, Process
import multiprocessing
import botocore
from boto3 import client as boto3_client

#config = botocore.config.Config(connect_timeout=20, read_timeout=60, retries={'max_attempts': 1})
#config=botocore.client.Config(max_pool_connections=50)
config=botocore.config.Config(max_pool_connections=50)
lambda_client = boto3_client('lambda',config=config)
#lambda_client = boto3_client('lambda')
def runProcess(reqItem,conn):
    start = time.time()
    #ts = reqItem["genre"]
    p_req = lambda_client.invoke(FunctionName="programmeMatchFunction-test-ds",
                                      InvocationType='RequestResponse',#RequestResponse #Event
                                      Payload=json.dumps(reqItem))
    #time.sleep(ts)
    print("Single thread time:"+reqItem["title"], time.time() - start)
    data = json.loads(p_req['Payload'].read().decode())
    conn.send([data])
    #conn.close()
    #return p_req


def unpack(l_req):
    unpack_res = []
    threaded_start = time.time()

    """  # create a list to keep all processes
    processes = []
    
    # create a list to keep connections
    parent_connections = []
    
    
    plimit = multiprocessing.cpu_count()
    print(plimit)
    for data in l_req:   #This loop can be parallelized
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        
        process = Process(target=runProcess, args=(data, child_conn,))
        processes.append(process)
        
    # start all processes
    for process in processes:
        process.start()
        
    # make sure that all processes have finished
    for process in processes:
        process.join()
        
    for parent_connection in parent_connections:
        data = parent_connection.recv()[0]
        #ans += parent_connection.recv()[0]
        
        try: 
                      #if not data['errorMessage']:
            unpack_res.append(data['body'])
                      #else:
                        #print('Error:'+ data['errorMessage'])                        
        except Exception as ex:
            print('Exception: %s' % (ex))
            print(data) """


    plimit = multiprocessing.cpu_count()

    # Setup management variables
    parent_conns = []
    pcount = 0
    i = 0

    for data in l_req:
        # Create the pipe for parent-child process communication
        parent_conn, child_conn = multiprocessing.Pipe()
        # create the process, pass data to be operated on and connection
        process = Process(target=runProcess, args=(data, child_conn,))
        parent_conns.append(parent_conn)
        process.start()
        pcount += 1
        if pcount == plimit: # There is not currently room for another process
            # Wait until there are results in the Pipes
            finishedConns = multiprocessing.connection.wait(parent_conns)
            # Collect the results and remove the connection as processing
            # the connection again will lead to errors
            for conn in finishedConns:
                
                data = conn.recv()[0]
                try: 
                      #if not data['errorMessage']:
                    unpack_res.append(data['body'])
                      #else:
                        #print('Error:'+ data['errorMessage'])                        
                except Exception as ex:
                    print('Exception: %s' % (ex))
                    print(data) 
                
                parent_conns.remove(conn)
                # Decrement pcount so we can add a new process
                pcount -= 1

    # Ensure all remaining active processes have their results collected
    for conn in parent_conns:
        data = conn.recv()[0]
        try: 
                      #if not data['errorMessage']:
            unpack_res.append(data['body'])
                      #else:
                        #print('Error:'+ data['errorMessage'])                        
        except Exception as ex:
            print('Exception: %s' % (ex))
            print(data) 
        conn.close()

    # Process results as needed 

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
