import fb
from time import sleep
import beanstalkc

if __name__ == "__main__":
    sleep(0.05)
    process = True
    c = beanstalkc.Connection(host='localhost', port=11300)

    cmds = {}
    cmds['update_user_profile'] = fb.process_user_profile
    cmds['update_user_photos'] = fb.process_user_photos
    cmds['update_user_friends'] = fb.process_user_friends

    while process:
        print "sleeping for 50 ms"

        sleep(0.05)

        job = c.reserve()
        command = job.body
        print "received command : " + command

        cmd, user_id = command.split()
        
        if cmd == 'exit':
            break
        else:
            cmds[cmd](user_id)
            job.delete()


    c.close()
