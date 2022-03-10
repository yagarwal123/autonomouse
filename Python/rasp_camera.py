import paramiko
from scp import SCPClient
import zmq
import config

port = 5555
ip_address = "131.111.180.78"

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
    if config.RASPBERRY:
        print('start rpi host via ssh')
        print('ip address:' + ip_address)
        str = func_ssh(ip_address, "pi", "automouse",
                        'python "/home/pi/code/RPiCameraPlugin/Python/scripts/rpi_host.py" plugin', 0)

def start_record(rec_path):
    if config.RASPBERRY:
        print('starting recording')

        # now = datetime.now()
        # rec_path = now.strftime("%Y%m%d_%H%M%S")

        func_start(ip_address, port, rec_path)

def close_record():
    if config.RASPBERRY:
        print('closing recording')
        func_close(ip_address, port)
        print('3')

def stop_record():
    if config.RASPBERRY:
        print('stopping recording')
        func_stop(ip_address, port)

def getVideofile(test_id):
    if config.RASPBERRY:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("131.111.180.78", username="pi", password="automouse", timeout=3)
        # SCPCLient takes a paramiko transport as its only argument
        scp = SCPClient(ssh.get_transport())
        #scp.put('test.txt', 'test2.txt')
        scp.get(f'~/code/RPiCameraPlugin/Python/scripts/RPiCameraVideos/{test_id}_experiment_1_recording_1', recursive=True,local_path=test_id)
        scp.close()
        ssh.close()