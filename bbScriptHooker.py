from __future__ import print_function
import frida
import sys
import atexit
def cleanup():
    global script
    script.unload()

session = frida.attach("BBCPEX.exe")
script = session.create_script("""
Interceptor.detachAll()
Interceptor.attach(ptr("%s"), function(args) {
        var cmd = Memory.readUInt(args[0]);
        var message = "";
        if(cmd == 0)
            message = Memory.readCString(args[0].add(4));
        //if(cmd < 3 && cmd != 2)
        if(this.context.ecx.toInt32() == 0x1FBF200C)
            send([args[0].toInt32(),this.context.ecx.toInt32(),Memory.readUInt(args[0]),message]);
});
""" % 0x4D4870)

def on_message(message, data):
    #print(message)
    print("{1:X} {0:X} {2} >> {3}".format(*message["payload"]))
script.on('message', on_message)
script.load()
sys.stdin.read()