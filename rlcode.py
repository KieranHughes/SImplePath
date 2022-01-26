import matlab.engine
import subprocess
from subprocess import Popen, DEVNULL, STDOUT
import time
from tensorforce import Agent, Environment
from mininet.net import Mininet
from mininet.clean import cleanup
import os
import statistics
from network import Network
from mininet.cli import CLI
import random


allNodes = ["h2", "h3", "h4", "h5"]
defaultFwRules = [['00:00:00:00:00:01','00:00:00:00:00:04']]
global net, attack, attackType, alerts, attackLocation, attackVersion, path, attackOrder, path1_status, path2_status, path3_status #environment


class alert:
    def __init__(self, alert_id, source, destination, dst_prt):
        self.alert_id = alert_id
        self.source = source
        self.destination = destination
        self.dst_prt = dst_prt


class state:
    def __init__(self, nodesDown,  attLocation, path1_status, path2_status, path3_status): # pressure, composition, flow, production, steps, attType, droppedPackets, reactorPressure, productQuality):
        self.nodesDown = nodesDown
        self.attLocation = attLocation
        self.path1_status = path1_status
        self.path2_status = path2_status
        self.path3_status = path3_status


class attackSim:

    global stage, attackVersion, path1stat, path2stat, path3stat


    def step(self):

        global stage, attackLocation, path, path1stat, path2stat, path3stat

        if attackVersion == 1:

            print("Path selected: " + str(path))

            if path == 1:
                if attackLocation == 1:
                    if net.canReach('h1', 'h2'):
                        attackLocation = 2
                        print("Host 2 reached")
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path1stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 2:
                    if net.canReach('h2','h3'):
                        print('Host 3 reached')
                        attackLocation = 3
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path1stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 3:
                    if net.canReach('h3', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path1stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                else:
                    if net.canReach('h3', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path1stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation


            elif path == 2:
                if attackLocation == 1:
                    if net.canReach('h1', 'h2'):
                        attackLocation = 2
                        print("Host 2 reached")
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path2stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 2:
                    if net.canReach('h2','h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path2stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                else:
                    if net.canReach('h2', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path2stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation
            elif path == 3:
                if attackLocation == 1:
                    if net.canReach('h1', 'h3'):
                        attackLocation = 3
                        print("Host 3 reached")
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path3stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 3:
                    if net.canReach('h3','h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path3stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                else:
                    if net.canReach('h3', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        path3stat = 0
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

            elif path == 4:
                if attackLocation == 1:
                    if net.canReach('h1', 'h3'):
                        attackLocation = 3
                        print("Host 3 reached")
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 3:
                    if net.canReach('h3','h2'):
                        print('Host 2 reached')
                        attackLocation = 2
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 2:
                    if net.canReach('h2', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                else:
                    if net.canReach('h2', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation
            elif path == 5:
                if attackLocation == 1:
                    if net.canReach('h1', 'h5'):
                        attackLocation = 5
                        print("Host 5 reached")
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 5:
                    if net.canReach('h5','h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                else:
                    if net.canReach('h5', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

            elif path == 6:
                if attackLocation == 1:
                    if net.canReach('h1', 'h5'):
                        attackLocation = 5
                        print("Host 5 reached")
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 5:
                    if net.canReach('h5','h3'):
                        print('Host 3 reached')
                        attackLocation = 3
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation

                elif attackLocation == 3:
                    if net.canReach('h3', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation
                else:
                    if net.canReach('h3', 'h4'):
                        print('Host 4 reached')
                        attackLocation = 4
                        return attackLocation
                    else:
                        attackOrder.remove(path)
                        if len(attackOrder) > 0:
                            path = attackOrder[0]
                        attackLocation = 1
                        return attackLocation



class networkEnvironment(Environment):

    def __init__(self):
        super().__init__()

    def states(self):
        return dict(type='float', shape=(5,), min_value=0.0, max_value=1.0)

    def actions(self):
        return dict(type='int', num_values=14)


    def reset(self):

        global net

        net.stopNetwork()
        subprocess.call("sudo mn -c", shell=True)

        # resetting firewall
        self.resetFirewall()

        net = Network()
        net.createNet()
        net.startNetwork()

        current_state = self.getState()
        states = float(current_state.nodesDown), float(current_state.attLocation), float(current_state.path1_status), float(current_state.path2_status), float(current_state.path3_status) #float(current_state.attType), , float(current_state.droppedPackets), float(current_state.reactorPressure), float(current_state.productQuality)

        # starting attack


        return states

    def execute(self, actions):
        # return the state
        global attackType, attackLocation, critAlerts
        #try:
        self.applyAction(actions)
        #except:
        #    print("error!")
        time.sleep(0.05)
        current_state = self.getState()
        attackLocation = attack.step()
        states = float(current_state.nodesDown), float(current_state.attLocation), float(current_state.path1_status), float(current_state.path2_status), float(current_state.path3_status) #float(current_state.attType), , float(current_state.droppedPackets), float(current_state.reactorPressure), float(current_state.productQuality)
        # return the Reward
        reward = self.getReward(current_state)
        # check if the episode is finshed
        terminal = self.isTerminal(current_state)
        return states, terminal, reward

    def isTerminal(self, state):
            if len(attackOrder) < 1:
                return True
            else:
                return False



    def getState(self):

        nodesDown = 0

        for i in allNodes:
            if net.checkAlive(i) != "up":
                nodesDown = nodesDown + 1

        currentState = state(nodesDown/5, attackLocation/5, path1stat, path2stat, path3stat) #attackType , packetsDropped, pressure, quality
        return currentState

    def getReward(self, state):

        reward = 0

        if state.attLocation == 0.20:
            reward += 73
        elif state.attLocation == 0.40:
            reward -= 3
        elif state.attLocation == 0.60:
            reward -= 3
        elif state.attLocation == 0.80:
            reward -= 3
        elif state.attLocation == 1:
            reward -= 10

        return reward

    def shutdown_host(self, host):
        host.stop()

    def block_node(self, addr):
        global pOpen
        # append new rule
        blockRules = ",['" + addr + "' ,'00:00:00:00:00:01'], ['" + addr + "' ,'00:00:00:00:00:02'], ['" + addr + "' ,'00:00:00:00:00:03'], ['" + addr + "' ,'00:00:00:00:00:04'], ['" + addr + "' ,'00:00:00:00:00:05'], ['" + addr + "','00:00:00:00:00:06'], ['" + addr + "', '00:00:00:00:00:07'], ['" + addr + "','00:00:00:00:00:08']]"
        with open('/home/kieran/pox/pox/misc/firewall.py', 'r') as file:
            data = file.readlines()
            file.close()
        data[5] = data[5][0:-2] + blockRules + '\n'
        with open('/home/kieran/pox/pox/misc/firewall.py', 'w') as file:
            file.writelines(data)
            file.close()
        os.system("fuser -k 6633/tcp")
        subprocess.Popen(["./pox.py", "openflow.of_01", "forwarding.l2_learning", "misc.firewall"], cwd="/home/kieran/pox", stdout=DEVNULL, stderr=STDOUT, close_fds=True)
        time.sleep(0.3)


    def resetFirewall(self):
        global pOpen
        with open('/home/kieran/pox/pox/misc/firewall_forRestore.py', 'r') as file:
            data = file.readlines()
            file.close()
        with open('/home/kieran/pox/pox/misc/firewall.py', 'w') as file:
            file.writelines(data)
            file.close()
        os.system("fuser -k 6633/tcp")
        subprocess.Popen(["./pox.py", "openflow.of_01", "forwarding.l2_learning", "misc.firewall"], cwd="/home/kieran/pox", stdout=DEVNULL, stderr=STDOUT, close_fds=True)
        time.sleep(0.3)


    def applyAction(self, action):

        switcher = {

            0: lambda: net.shutdown_host("h2"), # CorpNetworkMachineA
            1: lambda: net.shutdown_host("h3"), # CorpNetworkMachineB
            2: lambda: net.shutdown_host("h5"), # EngineeringStation
            3: lambda: net.startHost("h2"), # CorpNetworkMachineA
            4: lambda: net.startHost("h3"), # CorpNetworkMachineB
            5: lambda: net.startHost("h4"), # EngineeringStation
            6: lambda: net.startHost("h5"), # EngineeringStation
            7: lambda: net.disableNodeInterface("h2", "h2-eth0"), # CorpNetworkMachineA
            8: lambda: net.disableNodeInterface("h3", "h3-eth0"), # CorpNetworkMachineB
            9: lambda: net.disableNodeInterface("h5", "h5-eth0"), # EngineeringStation
            10: lambda: net.enableNodeInterface("h2", "h2-eth0"), # CorpNetworkMachineA
            11: lambda: net.enableNodeInterface("h3", "h3-eth0"), # CorpNetworkMachineB
            12: lambda: net.enableNodeInterface("h5", "h5-eth0"), # EngineeringStation
            13: lambda: print("No action taken")}

        return switcher.get(action, lambda: "invalid")()


environment = Environment.create(environment=networkEnvironment, max_episode_timesteps=9)
#rlAgent = Agent.create(agent='ppo', environment=environment, batch_size=10, learning_rate=1e-3, update_frequency=10, saver=dict(directory='normalisedState', frequency=3, max_checkpoints=1000))
#rlAgent = Agent.create(agent='ppo', environment=environment, batch_size=32, saver=dict(directory='threeNodes', frequency=3, max_checkpoints=1000))
rlAgent = Agent.load(directory='threeNodes', format='checkpoint', environment=environment)
actionsTaken = []
net = Network()
net.createNet()
net.startNetwork()
attackVersion = 1
for _ in range(1):
    totalReward = 0
    attack = attackSim()
    attackLocation = 1
    stage = 0
    path1stat = 1
    path2stat = 1
    path3stat = 1
    path4stat = 1
    states = environment.reset()
    attackOrder = [1,2,3,4]
    random.shuffle(attackOrder)
    terminal = False
    #terminal = environment.isTerminal(states)
    print('Attack order:' + str(attackOrder))
    path = attackOrder[0]
    attackLocation = 1

    while not terminal:
        actions = rlAgent.act(states=states)
        actionsTaken.append(str(actions))
#        print('action taken: ' + str(actions))
        states, terminal, reward = environment.execute(actions)

        rlAgent.observe(terminal=terminal, reward=reward)
        totalReward = totalReward + reward
    print(totalReward)
    if attackVersion == 1:
        f = open("/home/kieran/Desktop/CPS_IRS/results/attackScenario1/rewardGained.txt", "a")
        f.write(str(totalReward) + "\n")
        f.close()
        f = open("/home/kieran/Desktop/CPS_IRS/results/attackScenario1/actionsTaken.txt", "a")
        for i in actionsTaken:
            f.write(str(i) + "\n")
        f.close()
        actionsTaken.clear()
    elif attackVersion == 2:
        f = open("/home/kieran/Desktop/CPS_IRS/results/attackScenario2/rewardGained_scenario2.txt", "a")
        f.write(str(totalReward) + "\n")
        f.close()
        f = open("/home/kieran/Desktop/CPS_IRS/results/attackScenario2/actionsTaken_scenario2.txt", "a")
        for i in actionsTaken:
            f.write(str(i) + "\n")
        f.close()
        actionsTaken.clear()


for _ in range(20):
    attackVersion == 1
    print('Attack version:' + str(attackVersion))
    sum_rewards = 0.0
    attack = attackSim()
    attackLocation = 1
    path1stat = 1
    path2stat = 1
    path3stat = 1
    path4stat = 1
    states = environment.reset()
    attackOrder = [5,6]
    random.shuffle(attackOrder)
    #terminal = environment.isTerminal(states)
    print('Attack order:' + str(attackOrder))
    path = attackOrder[0]
    attackLocation = 1
    terminal = False
    internals = rlAgent.initial_internals()

    while not terminal:

        actions, internals = rlAgent.act(states=states, internals=internals, independent=True, deterministic=True)
        actionsTaken.append(str(actions))
        states, terminal, reward = environment.execute(actions)
        sum_rewards += reward

        print('Action: ' + str(actions))
    print(sum_rewards)

# Close agent and environment

rlAgent.close()
environment.close()
