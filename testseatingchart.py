import seatingchart
aly = seatingchart.Guest()
aly.set_name("aly")
aly.set_number(1)

bob = seatingchart.Guest()
bob.set_name("bob")
bob.set_number(2)


guestlist = seatingchart.GuestList()
guestlist.insert_guest(bob)
guestlist.insert_guest(aly)

guestlist.print_list()

randguest = guestlist.pick_rand()
name = randguest.get_name()
print "the lucky guest is " + name

print "guests to be seated"
guestlist.print_listtoseat()
