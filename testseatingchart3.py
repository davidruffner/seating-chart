import seatingchart as sc 
import random
import numpy as np
import matplotlib.pyplot as plt
import copy

guests = ["Antonette",  
          "Cinda",  
          "Nathan",  
          "Deidra", 
          "Merna",  
          "Renata",  
          "Londa",  
          "Lila",  
          "Kathryne",  
          "Lieselotte",  
          "Teofila",  
          "Hubert",  
          "Isadora",  
          "Elina",  
          "Enola",  
          "Emile",  
          "Brendan",  
          "Kit",  
          "Deetta",  
          "Jade"
          ]

guestlist = sc.GuestList()
for i,g in enumerate(guests):
    gobj = sc.Guest()
    gobj.set_name(g)
    
    gn=guests.pop(i)
    friends = random.sample(guests,10)
    guests.insert(i,gn)

    gobj.set_friendnames(friends)

    guestlist.insert_guest(gobj)

nguests = len(guests)
seatsper = 5

chart = sc.SeatingChart(guestlist,nguests/seatsper,seatsper)
chart0=copy.deepcopy(chart)
print ''
print "Guests to be seated and their friends"

org = sc.Organizer(guestlist,chart)
org0 = sc.Organizer(guestlist,chart0)
#Seat everyone
org.seatguests()



print "The final seating chart"
chart.print_seatingchart()
chart.print_chart()

print "now do Metropolis algorithim to increase friendships"
org1 = copy.deepcopy(org)
org2 = copy.deepcopy(org)
org3 = copy.deepcopy(org)

nsteps = 1000
steps = np.arange(nsteps)
friendsT1 = np.zeros(nsteps)
friendsT2 = np.zeros(nsteps)
friendsT3 = np.zeros(nsteps)
for i in steps:
    friendsT1[i] = org1.metropolisstep(0.01)
    friendsT2[i] = org2.metropolisstep(.1)
    friendsT3[i] = org3.metropolisstep(1)

#Now compare to what happens if i just seat people with friends
org0.sc.print_chart()
org0.seatguestsfriends()
count=org0.friendcount()
print "Number of friends with seating with friends method"
print count
print "friends T1,T2,T3"
print [friendsT1[-1],friendsT2[-1],friendsT3[-1]]
plt.plot(steps, friendsT1,label='T1')
plt.plot(steps, friendsT2,label='T2')
plt.plot(steps, friendsT3,label='T3')
plt.legend( loc='upper left')
plt.xlabel="step"
plt.ylabel="friendships"

plt.show()


