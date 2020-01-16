from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template

import serial

from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee import constants
from utils.zigbee_classes.clusters.attribute import Attribute
#from forms import AddGroupForm, RemoveGroupForm

comport='/dev/ttyACM0'

app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
    # Start commissioning.
    # cli_instance.bdb.start()
    #response = [(1234, 10)]
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None
        
    with open("nodes.txt") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(content)    
    
    devices = []
    for i in range(0, len(content)):
        parts = content[i].split('|')
        attr = Attribute(cluster=0x6, id=0,type=0)
        state = 0
        try:
            state = cli_instance.zcl.readattr(eui64=int(parts[0], 16), attr=attr, ep=int(parts[1])).value        
        except:
            print("couldn't get state")
        
        devices.append((parts[0], parts[1], state))
    
    with open("switches.txt") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(content)    
    
    groups = []
    for i in range(0, len(content)):
        parts = content[i].split('|')
        groups.append((parts[0], parts[1]))
    
    print(devices)
    cli_instance.close_cli()
    
    return render_template('index.html', nodes=devices, groups=groups, grouplen=len(groups), nodelen=len(devices))
    
@app.route('/control_device')
def control_device():
    dev = request.args.get('device')
    ep = request.args.get('endpoint')
    state = request.args.get('state')
    
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None

    print("CLI device created, trying to connect ...")
    if (state == "on"):
        cli_instance.zcl.generic(eui64=int(dev, 16), ep=int(ep), cluster=constants.ON_OFF_CLUSTER, profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=constants.ON_OFF_ON_CMD, payload=[])
    else:
        cli_instance.zcl.generic(eui64=int(dev, 16), ep=int(ep), cluster=constants.ON_OFF_CLUSTER, profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=constants.ON_OFF_OFF_CMD, payload=[])
    print("set device " + request.args.get('device') + " to " + request.args.get('state'))
    cli_instance.close_cli()
    #return '<a href="/index"><button type="button" class="btn btn-primary">Back to devices</button></a>'
    return redirect(url_for('index'))
    
@app.route('/info')
def info():
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None
        
    dev = request.args.get('device')
    ep = request.args.get('endpoint')
    state = 'on'
    try:
        state = cli_instance.zcl.readattr(eui64=int(parts[0], 16), attr=attr, ep=int(parts[1])).value        
    except:
        print("couldn't get state")
        
    #cli_instance.zcl.generic(eui64=int(dev, 16), ep=int(ep), cluster=int("0x4", 16), profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=int("0x1", 16), payload=[ (  0x3333, 0x21)])    
            
    with open("switches.txt") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(content)    
    
    groups = []
    for i in range(0, len(content)):
        parts = content[i].split('|')
        addr = int(parts[0], 16)
        addrstr = str('{:x}'.format(addr + 1))
            #SwitchFile.write())
        groups.append((addrstr, parts[1]))

    state = 0
     
    #add_group_form = AddGroupForm
    #remove_group_form = RemoveGroupForm
    cli_instance.close_cli()
    return render_template('info.html', device=dev, endpoint=ep,state=state, groups=groups, len=len(groups)) # add_group_form=add_group_form, remove_group_form=remove_group_form)
    #return "nice"
    
    
@app.route('/group_control')
def group_control():
    dev = request.args.get('device')
    ep = request.args.get('endpoint')
    group = request.args.get('group')
    add = request.args.get('action')
    
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None
        
    if (add == 'add'):
        cli_instance.zcl.generic(eui64=int(dev, 16), ep=int(ep), cluster=0x4, profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=0x0, payload=[(int(group, 16), constants.UINT16_TYPE)])
    else:
        cli_instance.zcl.generic(eui64=int(dev, 16), ep=int(ep), cluster=0x4, profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=0x3, payload=[(int(group, 16), constants.UINT16_TYPE)])
    
    cli_instance.close_cli()
    
    return redirect(url_for('info') + '?device=' + dev + '&endpoint=' + ep)
    
@app.route('/kick')
def kick():
    dev = request.args.get('device')
    
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None
        
    print(dev) 
    cli_instance.zdo.leave(short_addr=int(dev, 16))    
    
    
    with open("nodes.txt") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(content)    
    
    devices = []
    for i in range(0, len(content)):
        parts = content[i].split('|')
        attr = Attribute(cluster=0x6, id=0,type=0)
        state = 0
        try:
            state = cli_instance.zcl.readattr(eui64=int(parts[0], 16), attr=attr, ep=int(parts[1])).value        
        except:
            print("couldn't get state")
        if (parts[0] != dev):
            devices.append((parts[0], parts[1], state))
    
    with open("switches.txt") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(content)    
    
    groups = []
    for i in range(0, len(content)):
        parts = content[i].split('|')
        if (parts[0] != dev):
            devices.append((parts[0], parts[1]))
        
    BulbFile=open('nodes.txt','w')
    SwitchFile=open('switches.txt','w')

    for element in devices:
        if (str(element[1]) == '10'):
            BulbFile.write(str(element[0]))
            BulbFile.write('|')
            BulbFile.write(str(element[1]))
            BulbFile.write('\n')
        else:
            #addr = int(element[0], 16)
            
            #SwitchFile.write(str('{:x}'.format(addr + 1)))
            SwitchFile.write(str(element[0]))
            SwitchFile.write('|')
            SwitchFile.write(str(element[1]))
            SwitchFile.write('\n')
    BulbFile.close()
    SwitchFile.close()    
        
    cli_instance.close_cli()
    
    return redirect(url_for('index'))    
    
    
@app.route('/refresh')
def refresh():
    # a = int("BAF1", 16)
    # hexx = str('{:x}'.format(a+ 1))
    # print(hexx)

    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None

    #print("CLI device created, trying to connect ...")

    #devices = [(4211, 10)]
    # devices = cli_instance.zdo.match_desc([6], [], 80.0, 0xFFFd, 0xFFFd, 0x0104)
    devices = cli_instance.zdo.match_desc([0], [], 80.0, 0xFFFd, 0xFFFd, 0x0104)
    print(devices)
    BulbFile=open('nodes.txt','w')
    SwitchFile=open('switches.txt','w')

    for element in devices:
        if (str(element[1]) == '10'):
            BulbFile.write(str(element[0]))
            BulbFile.write('|')
            BulbFile.write(str(element[1]))
            BulbFile.write('\n')
        else:
            #addr = int(element[0], 16)
            
            #SwitchFile.write(str('{:x}'.format(addr + 1)))
            SwitchFile.write(str(element[0]))
            SwitchFile.write('|')
            SwitchFile.write(str(element[1]))
            SwitchFile.write('\n')
    BulbFile.close()
    SwitchFile.close()

    cli_instance.close_cli()
    return redirect(url_for('index'))
    #return '<a href="/index"><button type="button" class="btn btn-primary">Back to devices</button></a>'
   
@app.route('/start_commisioning')   
def start_commisioning():
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #   cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None
        
    # Start commissioning.
    cli_instance.bdb.start()
    
    return redirect(url_for('index')) 
    
@app.route('/start_network')   
def start_network():
    try:
        cli_instance = ZbCliDevice({'com_port': comport})
        cli_instance.bdb.channel = [20] # channel must be dictionary
        cli_instance.bdb.role = 'zc' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None
        
    # Start commissioning.
    cli_instance.bdb.start()
    
    return redirect(url_for('index'))