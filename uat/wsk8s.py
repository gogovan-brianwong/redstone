import websocket
import ssl
from subprocess import check_output


def on_message(ws, message):
    print('message received ..')
    print(message)


def on_error(ws, error):
    print ('error happened .. ')
    print (error)


def on_close(ws):
    print ("### closed ###")


def on_open(ws):

    print ('Opening Websocket connection to the server ... ')
    # This session_key I got, need to be passed over websocket header isntad
    # of ws.send.
    #ws.send(session_key)
token = "c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe"
# token = check_output(["oc", "whoami", "-t"])
pod = "redis-redis-2579253076-x81v7"
# exec_command = "/bin/sh".replace(" ", "+")
exec_command = '/bin/bash'

url = "wss://k8s-master-elb.allbright.local:443/api/v1/namespaces/kube-system/pods/%s/exec?command=%s&stderr=true&stdin=true&stdout=true&tty=true" % (pod, exec_command)
header = "Authorization: Bearer " + token



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                header = [header]
                                )
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

#    ws.on_message = on_message
#    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})