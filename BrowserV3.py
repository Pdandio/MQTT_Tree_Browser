import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
import paho.mqtt.client as mqtt
import Payload_pb2 as Payload

class MQTTTreeDisplay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MQTT Messages Tree Display')
        self.setGeometry(100, 100, 600, 400)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabels(['MQTT Messages'])
        self.tree_widget.setGeometry(50, 50, 500, 300)
        self.setCentralWidget(self.tree_widget)

        self.show()

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = decode_sparkplug_b(msg.payload)
    add_to_tree(topic, json.dumps(payload, indent=4, default=str))

def decode_sparkplug_b(payload):
    decoded_payload = Payload.Payload()
    decoded_payload.ParseFromString(payload)
    return decoded_payload

def add_to_tree(topic, payload):
    topic_parts = topic.split('/')

    current_level = ex.tree_widget.invisibleRootItem()
    for part in topic_parts:
        found = False
        for i in range(current_level.childCount()):
            if current_level.child(i).text(0) == part:
                found = True
                current_level = current_level.child(i)
                break

        if not found:
            new_item = QTreeWidgetItem()
            new_item.setText(0, part)
            current_level.addChild(new_item)
            current_level = new_item

    payload_item = QTreeWidgetItem(current_level)
    payload_item.setText(0, payload)
    current_level.addChild(payload_item)

if __name__ == '__main__':
    # Set up MQTT client
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("xxx.xxx.xxx.xxx", 1883, 60)
    client.subscribe("#", 0)  # Use a wildcard to subscribe to all topics
    client.loop_start()

    app = QApplication(sys.argv)
    ex = MQTTTreeDisplay()
    sys.exit(app.exec_())
