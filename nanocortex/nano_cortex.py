import time
import paho.mqtt.client as mqtt

from memory.in_memory import InMemoryManager


class NanoCortex:
    def __init__(self, broker_configs, 
                 topics=[],
                 update_duration=1,
                 verbose=True,
                 memory_manager=None):
        # Initialize MQTT client
        self.broker_configs = broker_configs
        self.name = self.broker_configs.get("CLIENT_NAME", "client")
        self.topics = topics
        self.update_duration = update_duration
        self.verbose = verbose
        
        self.client = mqtt.Client(self.name)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Memory
        self.memory_manager = memory_manager or InMemoryManager()
        
        # Connect to broker MQTT
        self.client.connect(self.broker_configs["HOST"], self.broker_configs["PORT"], self.broker_configs["KEEPALIVE"])
        self.client.loop_start()
        
        # Initialize state machine
        self.current_state = 'INITIALIZING'
        
    def print(self, message):
        if self.verbose:
            print(message)

    def on_connect(self, client, userdata, flags, rc):
        self.print("Connected with result code "+str(rc))
        # Assinando o tópico para receber mensagens dos sensores
        for topic in self.topics:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        self.print(f"Message received: {msg.payload}")
        self.memory_manager.store_short_term(msg.payload)
        self.decide_transition()

    def decide_transition(self):
        # Implementação simples da lógica de decisão para a transição de estados
        if self.current_state == 'INITIALIZING':
            self.current_state = 'RUNNING'
        elif self.current_state == 'RUNNING':
            # Alguma lógica para decidir a próxima ação
            pass
        # Registra o evento
        self.log_event(self.current_state)

    def perform_action(self):
        pass
        
    def log_event(self, state):
        self.memory_manager.store_long_term('event_history', state)

    def run(self):
        try:
            while True:
                frame_start_time = time.time()
                try:
                    self.perform_action()
                except:
                    self.print("[Error] performing action")
                frame_end_time = time.time()
                elapsed_time = frame_end_time - frame_start_time
                time_to_sleep = self.update_duration - elapsed_time
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)

        except KeyboardInterrupt:
            self.client.loop_stop()
            self.client.disconnect()
            self.print("Disconnected from MQTT broker")