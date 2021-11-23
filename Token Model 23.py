import numpy as np
# import matplotlib.pyplot as plt
import random2 as random

# Note: The the counting of tokens seems to be wrong, someone gained 3 tokens but only -2 from the rest of the group

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

    # token exchange
    tokenLimit = 2 # the maxiumum number of tokens a user is able to have
    buyPrice = 3
    sellPrice = 2
    buyers = np.zeros((2,1))
    sellers = np.zeros((2,1))
    transaction = 0 # count of num of transactions

    # Food circle
    profit = 0
    # boolean
    seated = False  # Default
    cooking = False  # Default

    def __init__(self, name):
        self.name = name
        # hunger
        self.chef = round(int(np.random.normal(User.chef_mean, User.chef_sd, 1)))  # set hunger on a scale of 1-10
        self.tokens = 2
        self.happiness = 0
        self.bought = False
        self.money = 0
        self.buys = 0
        self.sells = 0

        User.allhappy.append(self.happiness)
        User.objs.append(self)  # this adds this instance to the class list of all the instances


# SEATING(): This goes through each cook and assigs them a table of guests

    def seating(self,order):
        table = []
        # Selecting cooks
        if self.cooking == True:    # The following only happens with cooks
            # go through all the objects
            for i in order:
                obj = all_usr[i]
                # while there are empty seats
                if len(table) < User.seats_num:
                    # print('vars(obj):',vars(obj))
                    # If the guest has not been seated anywhere else
                    if obj.seated == False and obj.tokens > 0: # All cooks have seated set to True
                        table.append(obj)   # list of guests at the table
                        # print(l=en(table),table)
                        obj.seated = True   # the guest is at a table
                    else:
                        pass
                else:
                    pass
            # Setting object variables for this cook
            self.guest_num = len(table)  # tally up number of guests
            self.table_pcent = 100 * self.guest_num / User.seats_num
            self.spare_seats = self.seats_num - self.guest_num
        else:
            pass



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

    def happy(self,i):
        if self.cooking == True:
            if self.table_pcent > 70:
                self.happiness += 1 # You had enough guests
            elif self.guest_num == 0:
                self.happiness -= 2 # no guests
            else:
                self.happiness -= 1 # not enough guests
        # if you had enough tokens
        elif self.tokens > 1:
            if self.seated == False and self.will == True:
                self.happiness -= 2 # you weren't seated
            elif self.will == True:
                self.happiness += 1 # seated

        User.allhappy[i] = self.happiness # Storing happiness for global analysis

    def token(self):
        if self.cooking == True:
            self.tokens += self.guest_num # Cook gets a token for each guest
        elif self.seated == True:
            self.tokens -= 1 # Loose 1 token

# CHEF_TODAY() gives the user their chef rating for the day
    @classmethod
    def chef_today(cls):
        for obj in cls.objs:
            obj.chef_today = np.random.normal(obj.chef, cls.sd,1)  # Hunger today varies  with a standard deviation from the instances particular hunger


# STATUS() This prints the active satus of all users
    @classmethod
    def status(cls,state = True):
        for obj in cls.objs:
            print('#',obj.name,' cooking', obj.cooking,' seated', obj.seated,' tokens', obj.tokens,' will',obj.will,' happy', obj.happiness)

# HAPPY_INFO() Gets some statistics on the happpiness of people
    @staticmethod
    def happy_info(printt=False):
        happy = np.array(User.allhappy)
        User.happyMean = np.mean(happy, axis=0)
        User.happyStd = np.std(happy, axis=0)
        if printt == 'print':
            print('mean', User.happyMean, 'std', User.happyStd)

# DISPLAY() this prints of everything at the end, all the stats and data are shown here
    @classmethod
    def display(cls,DATA = False,HAPPY=False):
        if DATA == True:
            print('Data: [meals cooked, portions missed, spare seats]', User.data,people*days,'total')
            print('Sales: transactions',User.transaction,' profit',User.profit)
        if HAPPY == True:
            for obj in cls.objs:
                print('Name = ', obj.name, ' Happiness = ', obj.happiness,' Chef level = ', obj.chef) # Happy

    @classmethod
    def reset(cls):
        cls.buyers = np.zeros((2,1))
        cls.sellers = np.zeros((2,1))
        for obj in cls.objs:
            obj.seated = False
            obj.guest_num = 0
            obj.spare_seats = 0
            obj.cooking = False
            obj.bought = False


    @classmethod
    def willingness(cls,obj,state='On'):
        if state == 'On':
            meanDiff = obj.happiness - cls.happyMean
            if meanDiff < 2*cls.happyStd and meanDiff > 2: # If the user is less happy than the mean by 2 standard deviations
                obj.will = False
            else:
                obj.will = True
        else:
            obj.will = True
        return obj.will


# DECISION() chooses how the user is feeling about cooking a meal, this determines if they are a chef: Calls WILLINGNESS
    @classmethod
    def decision(cls):
        for obj in cls.objs:
            # Calls willingness: this is the mechanism where angry users stop using the system
                if cls.willingness(obj,'On') == True: # Turn the mechanism 'On' or 'Off' by adjusting the argument
                    # If cooking or guest
                    if obj.chef_today >= User.threshold and obj.tokens < cls.tokenLimit:  # Comparing hunger_today to the threshold hunger ( will they want to cook for multiple people )
                        obj.cooking = True
                        obj.seated = True
                    elif obj.tokens == 0 and obj.chef_today >= User.low_threshold:
                        obj.cooking = True
                        obj.seated = True
                    else:
                        obj.cooking = False
                else:
                    obj.cooking = False # If the user is no longer willing then they will not cook any longer

    @classmethod
    def sell_buy_desire(cls):
        # for token limit
        if cls.tokenLimitState == True:
            for obj in cls.objs:
                if obj.tokens > cls.tokenLimit:  # 1 token is the maximum allowable token size
                    obj.sellDesire = True
                    token4sale = obj.tokens - cls.tokenLimit
                elif obj.tokens == 0 and obj.chef_today <= User.threshold:
                    obj.buyDesire = True



    @classmethod
    def sell_buy_list(cls):
        obShuffle = list(cls.objs)  #
        random.shuffle(obShuffle)  # Shuffling the list of users

        # First section creates the seller and buyer lists
        for obj in obShuffle:
            # Sellers
            if obj.tokens > cls.tokenLimit:  # 1 token is the maximum allowable token size
                spare = obj.tokens - cls.tokenLimit
                print('spare', spare)
                cls.sellers = np.append(cls.sellers, [[obj.name], [spare]], 1)
            # Buyers
            if obj.tokens == 0 and obj.chef_today <= User.threshold:
                cls.buyers = np.append(cls.buyers, [[obj.name], [1]], 1)  # here the buyers only want 1 token each
        # Remove first column of zeros
        cls.sellers = np.delete(cls.sellers, 0, 1)
        cls.buyers = np.delete(cls.buyers, 0, 1)

        print('sellers', cls.sellers)
        print('buyers', cls.buyers)



    @classmethod
    def exchange(cls,status = 'On'):
    # if the exchange system is in use
        if status == 'On':
        # Go through the lists and perform the sales
            for i in range(len(cls.sellers[0,:])): # i is in [1,2,3,4]
                seller = int(cls.sellers[0,i])-1 # position of seller in objs
                tokenNum = int(cls.sellers[1,i]) # how many tokens are they selling
            # Go through buyers
                for j in range(len(cls.buyers[0,:])):
                    buyer = int(cls.buyers[0,j])-1 # position of buyer in objs
                    tokenReq = int(cls.buyers[1,j])
                # Buyer hasn't finished buying yet
                    if cls.objs[buyer].bought == False:
                    # if the amount being sold is >= than how much the buyer is asking for
                        if tokenNum >= tokenReq:
                            # Use selling function
                            cls.make_sale(buyer, seller, tokenReq)
                            # Buyer has finished buying
                            cls.objs[buyer].bought = True # the buyer token requirement has been met

                    # if there are less being sold by the seller than the buyer wants
                        elif tokenNum < tokenReq:
                            if cls.objs[buyer].bought == False:
                                # Use selling function
                                cls.make_sale(buyer,seller,tokenNum)
                                # remove the bought tokens from the buyers list
                                cls.buyers[1, j] -= tokenNum


# MAKE_SALE() completes an exchange of tokens and collects data
    @classmethod
    def make_sale(cls,buyer,seller,tokenNum): # buyer and seller is the 'name' of the instance in question
        # Settling money and tokens
        cls.objs[buyer].tokens += tokenNum
        cls.objs[seller].tokens -= tokenNum
        cls.objs[seller].money += cls.sellPrice
        cls.objs[buyer].money -= cls.buyPrice
        # Data collection
        cls.transaction += tokenNum
        cls.objs[buyer].buys += tokenNum
        cls.objs[seller].sells += tokenNum
        cls.profit += (cls.buyPrice - cls.sellPrice)

people = 10 # how many users to simulate
days = 10
names = list(range(1, people + 1))  # list [1,2,3...] of all the users for the experiment
all_usr = {name: User(name=name) for name in names}  # using a dictionary to store & create the objects

tick = 0

while tick < days:

    print('\n')

    User.chef_today()
    User.happy_info('print')  # Data about all happiness. (False) if you want to print the result
    User.exchange('On')  # ('Off' if no exchange) It performs all the token exchanges
    User.decision() # Calculates the chef levels

# Seating the guests, first they are randomised and then seated
    order = list(range(1, len(User.objs) + 1))
    random.shuffle(order)  # Random order of names
    for i in order:
        all_usr[i].seating(order)

    print(vars(all_usr[1]))
# Counting / totaling after the day
    for i in range(1,len(all_usr)+1):
        all_usr[i].happy(i-1)  # gathering the happiness
        all_usr[i].count() # data gathering
        all_usr[i].token() # balancing tokens

    # Printing the satus of user
    User.status(True) # set False to not print

    User.display()
    User.reset()

    tick += 1

User.display(True,True) # (DATA,HAPPY) shows results