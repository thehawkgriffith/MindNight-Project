import random
import numpy as np
from time import sleep
import os

class Agent:

    def __init__(self, id):
        '''
        id: Player id
        '''
        self.id = id
        self.role = "Agent"


    def action(self):
        print("{}'s action:".format(self.id))
        action = input("Secure(s): ")
        return 'secure'

    def propose(self, num):
        print("{}'s proposal.".format(self.id))
        choice = input("Propose(p) or Skip(s):")
        if choice == "p":
            print("Enter choice of node team of {} people.".format(num))
            members = []
            for i in range(num):
                print("Choice ", i + 1, ":")
                members += [int(input())]
            return members, False
        return None, True

    def return_choice(self, members):
        print(self.id, "choose your action: Accept(1) or Reject(0)")
        choice = int(input())
        return choice


class Hacker:

    def __init__(self, id):
        '''
        id: Player id
        '''
        self.id = id
        self.role = "Hacker"

    def action(self):
        print("{}'s action:".format(self.id))
        action = input("Secure(s) or Hack(h): ")
        if action == 's':
            return 'secure'
        return 'hack'

    def propose(self, num):
        print("{}'s proposal.".format(self.id))
        choice = input("Propose(p) or Skip(s):")
        if choice == "p":
            print("Enter choice of node team of {} people.".format(num))
            members = []
            for i in range(num):
                print("Choice ", i+1, ":")
                members += [int(input())]
            return members, False
        return None, True

    def return_choice(self, members):
        print(self.id, "choose your action: Accept(1) or Reject(0)")
        choice = int(input())
        return choice

class Node:

    def __init__(self, id, mem):
        '''
        id: Node number/id
        mem: Required number of members to go on this node
        '''
        self.req_members = mem
        self.id = id
        self._secured = None

    def mission(self, members, seq):
        '''
        members: List of member objects
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
        random.shuffle(self.players)
        self.sequence = self.players

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

    def proposal(self, members, player):
        print("The following members have been proposed by {}.".format(player.id))
        choices = []
        for member in members:
            print(">", self.sequence[member].id)
        count_acc = 0
        for user in self.sequence:
            choices += [user.return_choice(members)]
        count_acc = choices.count(1)
        if count_acc <= 3:
            print("The proposal failed!")
            print("The following players accepted it:")
            for i in range(6):
                if choices[i] == 1:
                    print(">", self.sequence[i].id)
            sleep(3)
            return False
        print("The proposal succeeded!")
        print("The following players rejected it:")
        for i in range(6):
            if choices[i] == 0:
                print(">", self.sequence[i].id)
        return True

    def start_node(self, node):
        rejected_props = 0
        print("Night {} has begun.".format(node.id))
        sleep(2)
        while True:
            if rejected_props == 5:
                print("Hackers win!")
                self.reset()
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
                self.last += 1
                if self.last > 5:
                    self.last = self.last % 5
                continue
            accepted = self.proposal(members, self.sequence[self.last])
            self.last += 1
            if self.last > 5:
                self.last = self.last % 5
            if accepted:
                secured, hack_num = node.mission(members, self.sequence)
                break
            else:
                rejected_props += 1
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
            condition = self.start_node(node)
            if condition:
                self.display()
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
                break
            if hacked_nodes >= 3:
                print("Hackers won!")
                break
        self.display()
        self.reset()

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


def main():
    env = Environment()
    env.flow()

main()