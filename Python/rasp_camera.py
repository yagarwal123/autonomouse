import paramiko
import zmq

port = 5555
ip_addresses = ["131.111.180.78"]

def func_ssh(address, usr, pwd, command, pseudoterminal):
    try:
        print("ssh " + usr + "@" + address + ", running : " +
              command)
        client = paramiko.SSHClient()
        client.load_system_host_keys()  # this loads any local ssh keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(address, username=usr, password=pwd, timeout=3)
        _, ss_stdout, ss_stderr = client.exec_command(command, get_pty=pseudoterminal)
        print(ss_stdout)
        print(ss_stderr)
        # r_out, r_err = ss_stdout.readlines(), ss_stderr.read() program gets stuck here if not commented
        # print(r_err)
        # if len(r_err) > 5:
        #    print(r_err)
        # else:
        #    print(r_out)
        client.close()
    except IOError:
        print(".. host " + address + " is not up")
        # return "host not up", "host not up"
        return "host not up"

def func_start(address, port, rec_path):
    url = "tcp://%s:%d" % (address, port)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(url)

    msg = 'Start'
    msg += ' Experiment={}'.format(1)
    msg += ' Recording={}'.format(1)
    msg += ' Path={}'.format(rec_path)
    socket.send_string(msg, flags=0, encoding='utf-8')
    str = socket.recv()
    return str

def func_close(address, port):  # address='172.29.37.78'; port = 5555
    # address=131.111.180.48
    url = "tcp://%s:%d" % (address, port)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(url)

    msg = 'Close'
    # socket.RCVTIMEO = 5000  # in milliseconds
    # socket.send_string(msg, flags=0, encoding='utf-8')

    # poller = zmq.Poller()
    # poller.register(socket, zmq.POLLIN)

    # try:
    #  socket.send_string(msg, flags=zmq.NOBLOCK, encoding='utf-8')
    #  #str = socket.recv(zmq.NOBLOCK)
    #  #socks = poller.poll(1000)
    #  socks = dict(poller.poll(1000))
    #  if socks:
    #    if socks.get(socket) == zmq.POLLIN:
    #     print("got message %s",socket.recv(zmq.NOBLOCK))
    #  else:
    #    print("error: message timeout")
    # except zmq.ZMQError as e:
    #  print('Close Error: %s', e)

    print('1')
    try:
        socket.send_string(msg, flags=zmq.NOBLOCK, encoding='utf-8')
        print('Close Send Success')
    except zmq.ZMQError as e:
        print('Close Send Error: %s', e)

    # https://stackoverflow.com/questions/7538988/zeromq-how-to-prevent-infinite-wait
    # https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/multisocket/zmqpoller.html

    print('2')

def func_stop(address, port):
    url = "tcp://%s:%d" % (address, port)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(url)

    msg = 'Stop'
    try:
        socket.send_string(msg, flags=zmq.NOBLOCK, encoding='utf-8')
        str = socket.recv(zmq.NOBLOCK)
        print(str)
    except zmq.ZMQError as e:
        print('Close Error: %s', e)



def start_rpi_host():
    print('start rpi host via ssh')
    for i in range(0, len(ip_addresses)):
        print('ip address:' + ip_addresses[i])
        str = func_ssh(ip_addresses[i], "pi", "automouse",
                        'python "/home/pi/code/RPiCameraPlugin/Python/scripts/rpi_host.py" plugin', 0)

def start_record(rec_path):
    print('starting recording')

    # now = datetime.now()
    # rec_path = now.strftime("%Y%m%d_%H%M%S")

    for i in range(0, len(ip_addresses)):
        func_start(ip_addresses[i], port, rec_path)

def close_record():
    print('closing recording')
    for i in range(0, len(ip_addresses)):
        func_close(ip_addresses[i], port)
        print('3')

def stop_record():
    print('stopping recording')
    for i in range(0, len(ip_addresses)):
        func_stop(ip_addresses[i], port)