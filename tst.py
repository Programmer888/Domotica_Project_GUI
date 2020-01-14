#the cli wrapper was installed using : pip install zb-cli-wrapper
# 





import serial

from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee import constants



def main():
    try:
        cli_instance = ZbCliDevice({'com_port': 'COM4'})
        #cli_instance.bdb.channel = [16] # channel must be dictionary
        #cli_instance.bdb.role = 'zr' # set coordinator role
    except serial.serialutil.SerialException:
        print('Can not create CLI device')
        cli_instance.close_cli()
        return None

    print("CLI device created, trying to connect ...")
    
    # # Start commissioning.
    #cli_instance.bdb.start()
    
    cmd = ""
    while cmd != "exit" :
        cmd = input("> ")
        cmdparts = cmd.split( )
        if (cmdparts[0] == "show" or cmdparts[0] == "sh"):
            if (cmdparts == "devices"[1] or cmdparts[1] == "dev"):
                #zdo match_desc 0xfffd 0xfffd 0x0104 1 0 0
                response = cli_instance.zdo.match_desc([], [], 80.0, 0xFFFd, 0xFFFd, 0x0104)
                print(response)
            
        elif (cmdparts[0] == "set"):
            if (cmdparts[1] == "device" or cmdparts[1] == "dev"):
                if(cmdparts[2] == "on"):
                    cli_instance.zcl.generic(eui64=int(cmdparts[3], 16), ep=int(cmdparts[4]), cluster=constants.ON_OFF_CLUSTER, profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=constants.ON_OFF_ON_CMD, payload=[]) 
                elif (cmdparts[2] == "off"):
                    cli_instance.zcl.generic(eui64=int(cmdparts[3], 16), ep=int(cmdparts[4]), cluster=constants.ON_OFF_CLUSTER, profile=constants.DEFAULT_ZIGBEE_PROFILE_ID, cmd_id=constants.ON_OFF_OFF_CMD, payload=[])  
        
        # if (cmd == "show devices" or cmd == "sh dev"):
            # #zdo match_desc 0xfffd 0xfffd 0x0104 1 0 0
            # response = cli_instance.zdo.match_desc([], [], 80.0, 0xFFFd, 0xFFFd, 0x0104)
            # print(response)
        # elif (cmd == "short"):
            # print("kort")
        # elif (cmd == "set device to 
        
        #else if(cmd == "long")
        
    
    
    # cli_instance.close_cli()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()