import time
import paho.mqtt.client as paho
import ssl

# define callbacks
def on_message(client, userdata, message):
    pass

def on_log(client, userdata, level, buf):
    # print("log: ", buf)
    pass

def on_connect(client, userdata, flags, rc):
    # print("publishing")
    pass

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))

ca_certs = "/etc/mosquitto/ssl/all-ca.crt"
certfile = "/etc/mosquitto/ssl/client.crt"
keyfile = "/etc/mosquitto/ssl/client.key"
cert_reqs = ssl.CERT_REQUIRED
tls_version = ssl.PROTOCOL_TLSv1_2

def mqtt_connect(host, port, MQTT_HOST, client_id, user_name, password, keepalive, topic, **kwargs):
    print(kwargs)
    if "clean_session" not in kwargs:
        clean_session = kwargs['clean_session'] #create flag in class
    else:
        clean_session = False #create flag in class

    client = paho.Client(client_id=client_id, clean_session=clean_session)

    if "connected_flag" in kwargs:
        client.connected_flag = kwargs['connected_flag'] #create flag in class
    else:
        client.connected_flag = False

    if "bad_connection_flag" in kwargs:
        client.bad_connection_flag = kwargs['bad_connection_flag']
    else:
        client.bad_connection_flag = False

    if "on_message" in kwargs:
        client.on_message = kwargs['on_message']
    else:
        client.on_message = on_message

    if "on_log" in kwargs:
        client.on_log = kwargs['on_log']
    else:
        client.on_log = on_log

    if "on_connect" in kwargs:
        client.on_connect = kwargs['on_connect']
    else:
        client.on_connect = on_connect

    if "on_subscribe" in kwargs:
        client.on_subscribe = kwargs['on_subscribe']
    else:
        client.on_subscribe = on_subscribe
    print("connecting to broker")

    client.username_pw_set (user_name, password)
    client.tls_set(ca_certs=ca_certs, certfile=certfile, keyfile=keyfile, cert_reqs=cert_reqs, tls_version=tls_version)
    client.tls_insecure_set(True)
    # client.enable_logger(logger=MQTT_LOG_DEBUG)
    client.will_set(topic,"mmwave subscription",1,retain=False)
    client.connect(host, port , keepalive)
    # ksjung will set
    # client.will
    client.subscribe(topic, 1)

    client.loop_start()
    return client

set_num = 0
set_message = ""
def mqtt_publish(client, topic, message, qos=1, retain=False, set_max=20):
    if set_max <= 1:
        client.will_set(topic,"set_max less than 1, willset",1,retain=False)
        client.publish(topic, message, qos, retain)
    else:
        global set_num, set_message, test_num
        set_message += message
        if set_num == set_max:
            client.will_set(topic,"set_max willset",1,retain=False)
            client.publish(topic, set_message, qos, retain)
            set_message = ""
            set_num = 0
        else:
            set_message += "|"
            set_num += 1

def mqtt_disconnect(client):
    client.loop_stop()
    client.disconnect()
