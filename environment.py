import random
import numpy as np
from time import sleep
import os


class Agent:

    def __init__(self, id):
        '''
        Parameters:
        id: Player id/name

        Description:
        Initializes the agent object.
        '''
        self.id = id
        self.role = "Agent"
        self.skip = True


    def action(self):
        '''
        Parameters:
        None

        Description:
        Takes node action from user.
        '''
        print("{}'s action:".format(self.id))
        action = input("Secure(s): ")
        return 'secure'

    def rl_action(self):
        '''
        Parameters:
        None

        Description:
        Takes node action from RL Agent.
        No other option for an agent so always secures.
        '''
        print("{}'s action:".format(self.id))
        print(self.id, "chose to secure.")
        return 'secure'

    def propose(self, num):
        '''
        Parameters:
        num: Number of people in a team
        required for the node.

        Description:
        Takes in a team proposal by a user.
        Users can either propose or skip.
        '''
        print("{}'s proposal.".format(self.id))
        choice = input("Propose(p) or Skip(s):")
        if choice == "s" and self.skip:
            self.skip = False
            return None, True
        else:
            print("Enter choice of node team of {} people.".format(num))
            members = []
            for i in range(num):
                print("Choice ", i + 1, ":")
                members += [int(input())]
            return members, False

    def rlpropose(self, team):
        '''
        Parameters:
        team: The team decided by the RL Agent.

        Description:
        Takes in a team proposal by an RL Agent.
        The Agent can either propose or skip.
        '''
        # team = [6, 6, 6, 6] means skip
        if team == [6, 6, 6, 6]:
            print("{} chose to skip.")
            return None, True
        else:
            return team, False

    def return_choice(self):
        '''
        Parameters:
        members: Members of the team proposed for the node.

        Description:
        Takes in a choice by a user for the proposed team.
        Users can either accept or reject.
        '''
        print(self.id, "choose your action: Accept(1) or Reject(0)")
        choice = int(input())
        return choice

    def rl_return_choice(self, action):
        '''
        Parameters:
        action: Choice towards the team proposed for the node
        by the RL Agent.

        Description:
        Takes in a choice by the RL Agent for the proposed team.
        Agent can either accept or reject.
        '''
        if action == 1:
            print(self.id, "chose to accept.")
        else:
            print(self.id, "chose to reject.")
        return action


class Hacker:

    def __init__(self, id):
        '''
        Parameters:
        id: Player id/name

        Description:
        Initializes the agent object.
        '''
        self.id = id
        self.role = "Hacker"
        self.skip = True

    def action(self):
        '''
        Parameters:
        None

        Description:
        Takes node action from user.
        '''
        print("{}'s action:".format(self.id))
        action = input("Secure(s) or Hack(h): ")
        if action == 's':
            return 'secure'
        return 'hack'

    def rl_action(self, action):
        '''
        Parameters:
        action: Node action chosen by RL Agent.

        Description:
        Takes node action from RL Agent.
        RL Agent can either secure or hack.
        '''
        print("{}'s action:".format(self.id))
        if action == 0:
            print(self.id, "chose to secure.")
            return 'secure'
        print(self.id, "chose to hack.")
        return 'hack'

    def propose(self, num):
        '''
        Parameters:
        num: Number of people in a team
        required for the node.

        Description:
        Takes in a team proposal by a user.
        Users can either propose or skip.
        '''
        print("{}'s proposal.".format(self.id))
        choice = input("Propose(p) or Skip(s):")
        if choice == "s" and self.skip:
            self.skip = False
            return None, True
        else:
            print("Enter choice of node team of {} people.".format(num))
            members = []
            for i in range(num):
                print("Choice ", i + 1, ":")
                members += [int(input())]
            return members, False

    def rl_propose(self, team):
        '''
        Parameters:
        team: The team decided by the RL Agent.

        Description:
        Takes in a team proposal by an RL Agent.
        The Agent can either propose or skip.
        '''
        if team == [6, 6, 6, 6]:
            print("{} chose to skip.")
            return None, True
        else:
            return team, False

    def return_choice(self):
        '''
        Parameters:
        members: Members of the team proposed for the node.

        Description:
        Takes in a choice by a user for the proposed team.
        Users can either accept or reject.
        '''
        print(self.id, "choose your action: Accept(1) or Reject(0)")
        choice = int(input())
        return choice

    def rl_return_choice(self, action):
        '''
        Parameters:
        action: Choice towards the team proposed for the node
        by the RL Agent.

        Description:
        Takes in a choice by the RL Agent for the proposed team.
        Agent can either accept or reject.
        '''
        if action == 1:
            print(self.id, "chose to accept.")
        else:
            print(self.id, "chose to reject.")
        return action


class Node:

    def __init__(self, id, mem):
        '''
        Parameters:
        id: Node number/id.
        mem: Required number of members to go on this node.

        Description:
        Initializes a node object.
        '''
        self.req_members = mem
        self.id = id
        self._secured = None

    def mission(self, members, seq):
        '''
        Parameters:
        members: Node team that is going on this node.
        seq: Sequence of players in the game.

        Description:
        Carries out the node mission taking in the node team
        and returns whether node was hacked or secured along
        with the number of hackers detected if hacked.
        '''
        assert len(members) == self.req_members
        choices = [seq[mem].action() for mem in members]
        if 'hack' in choices:
            self._secured = False
            return False, choices.count('hack')
        self._secured = True
        return True, 0


class Environment:

    def __init__(self):
        self.last = 0
        names = ['Liam', 'Noah', 'William', 'James', 'Logan', 'Benjamin', 'Mason', 'Elijah', 'Oliver', 'Jacob', 'Emma',
                 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Evelyn', 'Abigail']
        pattern = [2, 3, 4, 3, 4]
        self.nodes = []
        for i in range(5):
            self.nodes.append(Node(i+1, pattern[i]))
        name_idx = np.random.choice(names, 6, False)
        self.players = [
            Agent(name_idx[0]),
            Agent(name_idx[1]),
            Agent(name_idx[2]),
            Agent(name_idx[3]),
            Hacker(name_idx[4]),
            Hacker(name_idx[5])
        ]
        self.sequence = self.players
        random.shuffle(self.sequence)
        self.history = np.zeros([5, 10, 14])
        self.row = 0
        self.agent_reward = 0
        self.hacker_reward = 0

    def reset(self):
        self.last = 0
        names = ['Liam', 'Noah', 'William', 'James', 'Logan', 'Benjamin', 'Mason', 'Elijah', 'Oliver', 'Jacob', 'Emma',
                 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Evelyn', 'Abigail']
        pattern = [2, 3, 4, 3, 4]
        self.nodes = []
        for i in range(5):
            self.nodes.append(Node(i + 1, pattern[i]))
        name_idx = np.random.choice(names, 6, False)
        self.players = [
            Agent(name_idx[0]),
            Agent(name_idx[1]),
            Agent(name_idx[2]),
            Agent(name_idx[3]),
            Hacker(name_idx[4]),
            Hacker(name_idx[5])
        ]
        random.shuffle(self.players)
        self.sequence = self.players
        self.history = np.zeros([5, 10, 14])
        self.row = 0
        self.agent_reward = 0
        self.hacker_reward = 0

    def proposal(self, members, player):
        print("The following members have been proposed by {}.".format(player.id))
        choices = []
        for member in members:
            print(">", self.sequence[member].id)
        for user in self.sequence:
            choices += [user.return_choice(members)]
        count_acc = choices.count(1)
        accepts = [0, 0, 0, 0, 0, 0]
        if count_acc <= 3:
            print("The proposal failed!")
            print("The following players accepted it:")
            for i in range(6):
                if choices[i] == 1:
                    print(">", self.sequence[i].id)
                    accepts[i] = 1
            sleep(3)
            return False, accepts
        print("The proposal succeeded!")
        print("The following players rejected it:")
        accepts = [1, 1, 1, 1, 1, 1]
        for i in range(6):
            if choices[i] == 0:
                print(">", self.sequence[i].id)
                accepts[i] = 0
        return True, accepts

    def start_node(self, node):
        self.row = 0
        rejected_props = 0
        print("Night {} has begun.".format(node.id))
        sleep(2)
        hack_num = 0
        while True:
            if rejected_props == 5:
                print("Hackers win!")
                return True
            os.system("clear")
            print("Players:")
            print("#    Name")
            print("------------")
            print("Rejected Proposals: ", rejected_props)
            i = 0
            for player1 in self.sequence:
                print(i, "   ", player1.id)
                i += 1
            members, skip = self.sequence[self.last].propose(node.req_members)
            if skip:
                self.add_history([6,6,6,6], self.last, [0,0,0,0,0,0], node, 0)
                self.row += 1
                self.last += 1
                if self.last > 5:
                    self.last = self.last % 5
                continue
            team = [6, 6, 6, 6]
            for i in range(node.req_members):
                team[i] = members[i]
            accepted, accepts = self.proposal(members, self.sequence[self.last])
            if accepted:
                secured, hack_num = node.mission(members, self.sequence)
                self.add_history(team, self.last, accepts, node, hack_num)
                break
            else:
                rejected_props += 1
                self.add_history(team, self.last, accepts, node, hack_num)
            self.row += 1
            self.last += 1
            if self.last > 5:
                self.last = self.last % 5
            os.system("clear")
        if secured:
            print("The node was secured!")
            print("No hackers detected.")
            sleep(3)
        else:
            print("The node was hacked!")
            print(hack_num, "hackers detected.")
            sleep(3)
        os.system("clear")

    def flow(self):
        self.render()
        for node in self.nodes:
            self.reset_skips()
            condition = self.start_node(node)
            if condition:
                self.display()
                self.agent_reward = -100
                self.hacker_reward = 100
                return
            self.render()
            sec_nodes = 0
            hacked_nodes = 0
            for node_temp in self.nodes:
                if node_temp._secured:
                    sec_nodes += 1
                elif node_temp._secured == False:
                    hacked_nodes += 1
            if sec_nodes >= 3:
                print("Agents won!")
                self.agent_reward = 100
                self.hacker_reward = -100
                break
            if hacked_nodes >= 3:
                print("Hackers won!")
                self.agent_reward = -100
                self.hacker_reward = 100
                break
        self.display()

    def reset_skips(self):
        for player in self.sequence:
            player.skip = True

    def render(self):
        i = 0
        print("--------------MINDNIGHT-----------------")
        print("----------------------------------------")
        print("Players:")
        print("#    Name")
        print("------------")
        for player in self.sequence:
            print(i, "   ", player.id)
            i += 1
        print("Nodes:")
        print("#   Secured")
        print("-----------")
        for node in self.nodes:
            if node._secured:
                temp = "Secured"
            elif node._secured == False:
                temp = "Hacked"
            else:
                temp = "N/A"
            print(node.id, "  ", temp)
        print("---------------------------------------")
        sleep(4)
        os.system("clear")

    def display(self):
        i = 0
        print("--------------MINDNIGHT-----------------")
        print("---------------RESULTS------------------")
        print("Players:")
        print("#    Name       Role")
        print("--------------------")
        for player in self.sequence:
            print(i, "   ", player.id, "   ", player.role)
            i += 1
        print("---------------------------------------")
        sleep(4)

    def add_history(self, team, proposer, accepts, node, hackers_det):
        if node._secured == False:
            hacked = 2
        elif node._secured:
            hacked = 1
        else:
            hacked = 0
        temp = []
        temp.extend(team)
        temp.extend(accepts)
        temp.extend([proposer])
        temp.extend([0])
        temp.extend([hacked])
        temp.extend([hackers_det])
        self.history[node.id-1][self.row] = np.array(temp)

    def state(self, player=0):
        current_state = self.history
        for node in range(5):
            for row in range(10):
                current_state[node][row][11] = player
        return current_state