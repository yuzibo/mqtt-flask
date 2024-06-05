import time, os
from paho.mqtt import client as mqtt_client
from flask import Flask, json
# Flask
app = Flask(__name__)
app.config.from_pyfile("config.py")

# config
poweron_time = app.config['POWERON_TIME']
poweroff_time = app.config['POWEROFF_TIME']
reset_time = app.config['RESET_TIME']
client_id =app.config['CLIENT_ID']
machine_sn =app.config['MACHINE_SN']
username =app.config['USERNAME']
password = app.config['PASSWORD']
broker = app.config['BROKER']
port = app.config['PORT']
topic = app.config['TOPIC']

# device json
devicelistfilename = os.path.join(app.static_folder, 'data', 'devicelist.json')
with open(devicelistfilename) as json_file:
    devicelistjson = json.load(json_file)


# main
@app.route("/")
def index():
    return "<p>MQTT WSGI Webapp!</p>"

@app.route("/<string:action>/<int:id>")
def board_action(action,id):
    client = connect_mqtt()
    client.loop_start()
    result=publish(client,action,id)
    client.disconnect()
    return f"{result}"

@app.route('/help')
def help():
    help_info = "这是一个远程重启设备的网站服务\n命令：\ncurl http://服务器IP/help           获取帮助信息\ncurl http://服务器IP/reset/设备ID   重启\ncurl http://服务器IP/devicelist     获取设备列表\n"
    return f"{help_info}"


@app.route('/devicelist')
def devicelist():
    devicelistdata=''
    for i,o in devicelistjson.items():
        devicelistdata += '设备:%s  ID:%s \n' % (i,o)
    return f"{devicelistdata}"




# mqtt client 
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username,password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,action,board_id):
    msg_count = 0
    while True:
        time.sleep(1)
        if action == 'reset': 
            action_time = reset_time
        elif action == 'poweroff':
            action_time = poweroff_time
        elif action == 'poweron':
            action_time = poweron_time
        else:
            return f"Error action !!!"

        msg='{"id":"%s","sn":"%s","params": [{"p":"COM_ALL","k":"mb","v":{"opr":"openone","io":%s,"time":%s,"addr":254}}]}'%(client_id,machine_sn,board_id,action_time)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            return f'设备ID: %s 已处理' % board_id
        else:
            return f"Failed to send message to topic {topic}"

def disconnect_mqtt():
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")
    client.on_disconnect = on_disconnect


