import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem

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
    sample_messages = [
        ("spBv1.0/topic1/subtopic1", "payload1"),
        ("spBv1.0/topic1/subtopic2", "payload2"),
        ("spBv1.0/topic7/subtopica/subc", "payload3"),
    ]

    app = QApplication(sys.argv)
    ex = MQTTTreeDisplay()

    for topic, payload in sample_messages:
        add_to_tree(topic, payload)

    sys.exit(app.exec_())
