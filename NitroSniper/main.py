import websocket, json, threading, time, datetime, re, tls_client
from Modules.spoof import Spoof
from Modules.logging import Logging
from Modules.init import Init
from Modules.general import General

class Sniper:
    def __init__(self, token, apiver, delay) -> None:
        self.token = token
        self.pattern = r'https:\/\/discord\.gift\/[a-zA-Z0-9]{16,24}'
        self.session = tls_client.Session()
        self.start   = 0
        self.apiver  = apiver
        self.delay   = delay
        self.spoof   = Spoof()
        self.logging = Logging()
        self.headers = {}


    def detect(self, content):
        self.start = time.time()
        match = re.search(self.pattern, content)
        if match:
            time.sleep(self.delay)
            threading.Thread(target=self.redeem, args=(match.group(0),)).start()

    def redeem(self, code):
        codeid = code.split("/")[-1]
        api = f"https://discord.com/api/v{self.apiver}/entitlements/gift-codes/{codeid}/redeem"
        r = self.session.post(api, headers=self.headers)
        if r.status_code == 200:
            self.logging.Success(f"Redeemed {code} in {round(time.time() - self.start, 2)} seconds")
        else:
            self.logging.Error(f"Failed to redeem {code} in {round(time.time() - self.start, 2)} seconds")
        self.start = 0

    def init(self):
        self.headers = self.spoof.headers(self.token)

class Websocket:
    def __init__(self) -> None:
        self.websocket_endpoint = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.heartbeat_interval = 0
        self.token              = ""
        self.apiver             = ""
        self.username           = ""
        self.delay              = 0
        self.sniper             = None
        self.logging            = Logging()
        self.general            = General()
        self.ws                 = websocket.WebSocketApp(
            self.websocket_endpoint,
            on_message=self.ws_on_message,
            on_close=self.ws_on_close,
            on_open=self.ws_on_open
        )

    def ws_payload(self):
        return json.dumps({
            "op" : 1,
            "d"  : "null"
        })
    
    def ws_identify_payload(self):
        return json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513,
                "properties": {
                    "$os": "windows",
                    "$browser": "Discord",
                    "$device": "pc"
                }
            }
        })
    
    def ws_heartbeat(self):
        while True:
            self.ws.send(self.ws_payload())
            time.sleep(self.heartbeat_interval / 1000)

    def ws_on_message(self, ws, message):
        if message:
            data = json.loads(message)
            if data.get("op", "") == 10:
                self.heartbeat_interval = data["d"]["heartbeat_interval"] 
                threading.Thread(target=self.ws_heartbeat).start()
                self.ws.send(self.ws_identify_payload())
            elif data['t'] == "MESSAGE_CREATE":
                contetnt = data['d']['content']
                self.sniper.detect(contetnt)

    def ws_on_error(self, ws, error):
        self.logging.Error(error)

    def ws_on_close(self, ws):
        self.logging.Error("disconnected")

    def ws_on_open(self, ws):
        self.logging.Success(f"Connected to the Discord V{self.apiver} gateway as {self.username}")

    def run(self):
        self.ws.run_forever()

    def load_config(self):
        with open("Assets/Config.json", "r") as f:
            config = json.load(f)
            self.token  = config["Token"]
            self.apiver = config["ApiVersion"]
            self.delay  = config["Delay"]
    
    def init(self):
        self.general.ascii_art()
        self.load_config()
        check = self.general.token_check(self.token)
        if check != False:
            self.username = check 
        self.sniper = Sniper(self.token, self.apiver, self.delay)
        self.sniper.init()
        self.run()

if __name__ == "__main__":
    Init().config()
    socket = Websocket()
    socket.init()