import numpy as np
# import matplotlib.pyplot as plt
import random2 as random

class User:
# Setting all the class variables
    seats_num = 3  # number of people that are cooked for
    sd = 2  # standard deviation of each persons daily hunger
    objs = []  # list of all the objects

    # Default variables
    allhappy = []

    # How the users huger is defined
    threshold = 7  # Above which the user wants to cook for multiple people
    low_threshold = 5 # Threshold for people with 0 tokens
    chef_sd = 1  # standard deviation for the hungers
    chef_mean = 5  # mean of all the hungers
    data = [0, 0, 0]  # [meals cooked,portions missed,spare seats]


    # boolean
    seated = False  # Default
    cooking = False  # Default

    def __init__(self, name):
        self.name = name
        # hunger
        self.chef = round(int(np.random.normal(User.chef_mean, User.chef_sd, 1)))  # set hunger on a scale of 1-10
        self.tokens = 1
        self.happiness = 0
        User.allhappy.append(self.happiness)
        User.objs.append(self)  # this adds this instance to the class list of all the instances


# SEATING(): This goes through each cook and assigs them a table of guests

    def seating(self,order):
        table = []
        # Selecting cooks
        if self.cooking == True:    # The following only happens with cooks
            # print('i am a cook')
            # print('len(table',len(table),'seats_num',User.seats_num)
            # go through all the objects




            for i in order:
                obj = all_usr[i]
                # while there are empty seats
                if len(table) < User.seats_num:
                    # print('vars(obj):',vars(obj))
                    # If the guest has not been seated anywhere else
                    if obj.seated == False and obj.tokens > 0: # All cooks have seated set to True
                        table.append(obj)   # list of guests at the table
                        # print(len(table),table)
                        obj.seated = True   # the guest is at a table
                    else:
                        pass
                else:
                    pass

        else:
            pass

        # Setting object variables for this cook
        self.guest_num = len(table)  # tally up number of guests
        self.table_pcent = 100 * self.guest_num / User.seats_num
        self.spare_seats = self.seats_num - self.guest_num

# HAPPY() generates the happiness based on if the user has been seated/ has had enough guests. I
# It also calls COUNT() is applied to each user and gathers all the data.
    def count(self):  # counting the data up
        if self.cooking == True:
            User.data[0] += 1  # number of cooks
            User.data[2] += self.spare_seats
        elif self.cooking == False and self.seated == False: # you are a guest who wasn't seated
            User.data[1] += 1 # portions missed
        else:
            pass


# Gets some statistics on the happpiness of people
    @staticmethod
    def happy_info():
        happy = np.array(User.allhappy)
        User.happyMean = np.mean(happy, axis=0)
        User.happyStd = np.std(happy, axis=0)

    def happy(self,i):
        if self.cooking == True:
            if self.table_pcent > 70:
                self.happiness += 1 # You had enough guests
            elif self.guest_num == 0:
                self.happiness -= 2 # no guests
            else:
                self.happiness -= 1  # not enough guests
        # if you had enough tokens
        elif self.tokens > 1:
            if self.seated == False:
                self.happiness -= 2 # you weren't seated
            else:
                self.happiness += 1 # seated

        User.allhappy[i] = self.happiness # Storing happiness for global analysis


    def token(self):
        if self.cooking == True:
            self.tokens += self.guest_num # Cook gets a token for each guest
        elif self.seated == True:
            self.tokens -= 1 # Loose 1 token


# DISPLAY() this prints of everything at the end, all the stats and data are shown here
    @classmethod
    def display(cls,DATA = False,HAPPY=False):
        if DATA == True:
            print('Data: [meals cooked, portions missed, spare seats]', User.data,people*days,'total')
        if HAPPY == True:
            for obj in cls.objs:
                print('Name = ', obj.name, ' Happiness = ', obj.happiness,' Chef level = ', obj.chef) # Happy


    @classmethod
    def reset(cls):
        for obj in cls.objs:
            obj.seated = False
            obj.guest_num = 0
            obj.spare_seats = 0

# DECISION() chooses how the user is feeling about cooking a meal, this determines if they are a chef
    @classmethod
    def decision(cls):
        for obj in cls.objs:
            # Assign willingness
            if abs(mean - obj.happiness)

            obj.chef_today = np.random.normal(obj.chef, cls.sd,1)  # Hunger today varies with a standard deviation from the instances particular hunger
            if obj.chef_today >= User.threshold:  # Comparing hunger_today to the threshold hunger ( will they want to cook for multiple people )
                obj.cooking = True
                obj.seated = True
            elif obj.tokens == 0 and obj.chef_today >= User.low_threshold:
                obj.cooking = True
                obj.seated = True
            else:
                obj.cooking = False
    # Creating the users

class fdCircle(User):
    pass

print(help(fdCircle))

people = 100 # how many users to simulate
days = 1000
names = list(range(1, people + 1))  # list [1,2,3...] of all the users for the experiment
all_usr = {name: User(name=name) for name in names}  # using a dictionary to store & create the objects

print(all_usr)
# Defining variables
tick = 0

while tick < days:
    # print('\n')

    User.decision() # Calculates the chef levels

    order = list(range(1, len(User.objs) + 1))
    random.shuffle(order)  # Random order of names
    for i in order:
        all_usr[i].seating(order)

# status of users
#     for i in all_usr:
#         print('#',all_usr[i].name,' cooking', all_usr[i].cooking,'    seated', all_usr[i].seated,'    tokens', all_usr[i].tokens,)


    for i in range(1,len(all_usr)):
        all_usr[i].happy(i)  # gathering the happiness
        all_usr[i].count() # data gathering

        all_usr[i].token() # balancing tokens

    User.happy_info() # Data about all happiness
    User.display()
    User.reset()

    tick += 1


User.display(True,True) # (DATA,HAPPY) shows results