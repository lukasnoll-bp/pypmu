import json
import random
import threading

from synchrophasor.frame import ConfigFrame2
from synchrophasor.pmu import Pmu


"""
randomPMU will listen on ip:port for incoming connections.
After request to start sending measurements - random
values for phasors will be sent.
"""
lock = threading.Lock()

if __name__ == "__main__":
    with open("./config/config.json") as f:
        config = json.load(f)

    pmu = Pmu(ip=config["pmu"]["host"], port=config["pmu"]["port"])
    pmu.logger.setLevel("DEBUG")

    cfg = ConfigFrame2(config["pmu"]["id"],  # PMU_ID
                       1000000,  # TIME_BASE
                       1,  # Number of PMUs included in data frame
                       config["pmu"]["name"],  # Station name
                       config["pmu"]["id"],  # Data-stream ID(s)
                       (True, True, True, True),  # Data format - POLAR; PH - REAL; AN - REAL; FREQ - REAL;
                       6,  # Number of phasors
                       0,  # Number of analog values
                       0,  # Number of digital status words
                       ["VA", "VB", "VC", "IA", "IB", "IC"],  # Channel Names
                       [(0, "v"), (0, "v"),(0, "v"), (0, "v"), (0, "v"), (0, "v")],  # Conversion factor for phasor channels - (float representation, not important)
                       [],  # Conversion factor for analog channels
                       [],  # Mask words for digital status words
                       50,  # Nominal frequency
                       1,  # Configuration change count
                       30)  # Rate of phasor data transmission)

    pmu.set_configuration(cfg)
    pmu.set_header("Hello")
    pmu.run()

    while True:
        if pmu.clients:
            pmu.send_data(phasors=[(random.uniform(config["phasors"]["A"]["V"][0], config["phasors"]["A"]["V"][1]), random.uniform(-0.1, 0.3)),
                                   (random.uniform(config["phasors"]["B"]["V"][0], config["phasors"]["B"]["V"][1]), random.uniform(1.9, 2.2)),
                                   (random.uniform(config["phasors"]["C"]["V"][0], config["phasors"]["C"]["V"][1]), random.uniform(3.0, 3.14)),
                                   (random.uniform(config["phasors"]["A"]["I"][0], config["phasors"]["A"]["I"][1]), random.uniform(-0.1, 0.3)),
                                   (random.uniform(config["phasors"]["B"]["I"][0], config["phasors"]["B"]["I"][1]),random.uniform(-0.1, 0.3)),
                                   (random.uniform(config["phasors"]["C"]["I"][0], config["phasors"]["C"]["I"][1]),random.uniform(-0.1, 0.3))
                                   ],
                           freq=random.uniform(config["phasors"]["frequency"][0], config["phasors"]["frequency"][1]),
                          dfreq=random.uniform(config["phasors"]["frequency-deviation"][0], config["phasors"]["frequency-deviation"][1]))

    pmu.join()
