import seatingchart as sc 

aly = sc.Guest()
aly.set_name("aly")
aly.set_friendnames(list([]))

bob = sc.Guest()
bob.set_name("bob")
bob.set_friendnames(list(["cat"]))

cat = sc.Guest()
cat.set_name("cat")
cat.set_friendnames(list(["bob","aly"]))



guestlist = sc.GuestList()
guestlist.insert_guest(bob)
guestlist.insert_guest(aly)
guestlist.insert_guest(cat)

print "Guests:"
guestlist.print_list()
print ""
# randguest = guestlist.pick_rand()
# name = randguest.get_name() 
# print "the lucky guest is " + name


print "guests to be seated"
guestlist.print_listtoseat()

chart = sc.SeatingChart(1,3)
print "The seating chart"
chart.print_chart()

print "guests to be seated"
guestlist.print_listtoseat()

randguest = guestlist.pick_rand()
randguestname = randguest.get_name()
print randguestname+" will be seated"
chart.seat_guest(randguest)
friend = guestlist.pick_friend_of(randguest)
if not (friend is None):
    friendname = friend.get_name()
    print randguest.get_name()+"'s friend " + \
        friendname+" will be seated also"
    chart.seat_guest(friend)
print "The final seating chart"
chart.print_seatingchart()

