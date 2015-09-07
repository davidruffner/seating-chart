import random
import numpy as np
import pandas
import matplotlib.pyplot as plt

"""
This simple program will try to sort out a seating chart from a list of
people and their inter-relationships.

Modifications:
 3/9/2014  written by David Ruffner
"""


class Guest(object):
    def __init__(self, name, friends=None):
        """
        Constructs a guest object

        Inputs
        -----
        :param name: string
        :keyword friends: list of strings
        """
        self.name = name
        if friends is None:
            self.friendnames = list()
        else:
            self.set_friendnames(friends)

    def set_name(self, newname):
        self.name = newname

    def set_friendnames(self, friendnames):
        self.friendnames = friendnames

    def get_name(self):
        return self.name

    def get_friendnames(self):
        return self.friendnames


class GuestList(object):
    def __init__(self, guestnames=None):
        """
        Makes a list of Guest objects and of guest names,
        and a dictionary relating the names to the objects

        Inputs
        -------
        :keyword guestnames: list of strings
        """
        if guestnames is None:
            self.guests = list()
        else:
            self.guests = [Guest(name) for name in guestnames]
        self.guestdict = {g.get_name(): g for g in self.guests}

    def fromExcel(self, excelfile):
        """
        Imports a guest list from an excel file.

        The file should have the guest names on the leftmost column and then
        friend names in adjacent columns

        Uses python pandas for the import. It also won't repeat names.

        :param excelfile:
        """
        peopledf = pandas.read_excel(excelfile)
        # Read in all the names
        allnames = set()
        for column in peopledf[1:]:
            for rownum in peopledf.index:
                name = peopledf.iloc[rownum][column]
                # print rownum, column, name
                if name is np.nan:
                    continue
                allnames.add(name)
        self.guests = [Guest(name) for name in allnames]
        self.guestdict = {g.get_name(): g for g in self.guests}

        # Find all the friends
        for rownum in peopledf.index:
            friends = [str(name) for name in peopledf.iloc[rownum].values if name is not np.nan]
            [self.guestdict[friend].set_friendnames(friends) for friend in friends]

    def insert_guest(self, guest):
        self.guests.append(guest)
        self.guestdict[guest.get_name()] = guest

    def print_list(self):
        for guest in self.guests:
            name = guest.get_name()
            print name

    def print_friendlist(self):
        for guest in self.guests:
            name = guest.get_name()
            friends = guest.get_friendnames()
            print name + ":" + ",".join(friends)


class SeatingChart(object):
    def __init__(self, guestlist, tables, seatper):
        """
        Object for keeping track of where guests will be sitting
        :param guestlist: list of guest objects
        :param tables: int number of tables
        :param seatper: int number of people per table
        """
        self.chart = [['' for x in xrange(seatper)] for y in xrange(tables)]
        self.seatdict = dict()
        self.open = [(y, x) for x in xrange(seatper) for y in xrange(tables)]
        self.seated = list()
        self.toseat = [g.get_name() for g in guestlist.guests]
        self.gl = guestlist

    def pick_rand(self):
        if len(self.toseat) == 0:
            return None
        randguestname = random.choice(self.toseat)
        return randguestname

    def pick_friend_of(self, guestname):
        guest = self.gl.guestdict[guestname]
        friendnames = list(guest.get_friendnames())
        if len(friendnames) == 0:
            return None  # It returns none if there are no friends of this
            # schmuck who need to be seated
        random.shuffle(friendnames)
        for f in friendnames:
            if self.toseat.count(f) == 0:
                pass
            else:
                return f
        print "The schmuck has no friends or they are already seated"
        return None

    def seat_guest(self, guestname):
        n = guestname
        if len(self.open) == 0:
            print "No more seats!"
            return
        seatindex = self.open.pop(random.randrange(len(self.open)))
        self.chart[seatindex[0]][seatindex[1]] = n

        # update the seatdict, and seated
        self.seated.append(n)
        self.seatdict[n] = seatindex
        self.toseat.remove(n)

    def seat_guest_here(self, guestname, index):
        # check if the seat is open
        if self.open.count(index) == 0:
            print "the seat is already filled!!"
            return None
        else:
            self.open.remove(index)
        self.chart[index[0]][index[1]] = guestname

        # update the seatdict, and seated
        self.seated.append(guestname)
        self.seatdict[guestname] = index
        self.toseat.remove(guestname)

    def seat_guestfriend(self, guestname, friendname):
        """
        Seats the friend of a guest at the guests table

        First need to find the table the guest is sitting at
        and then the open seats at that table

        Inputs
        -------
        :param guestname: string
        :param friendname: string
        :return:
        """
        index = self.seatdict[guestname]
        tablenum = index[0]
        openseats = [(x, y) for x, y in self.open if x == tablenum]
        if not (len(openseats) == 0):
            seatindex = openseats.pop(random.randrange(len(openseats)))
            self.chart[seatindex[0]][seatindex[1]] = friendname

            # update the seatdict, and seated
            self.open.remove(seatindex)
            self.seated.append(friendname)
            self.seatdict[friendname] = seatindex
            self.toseat.remove(friendname)
            return seatindex
        else:
            return None

    def pick_randremove(self):
        if len(self.seated) == 0:
            return None
        randguestname = random.choice(self.seated)
        index = self.seatdict[randguestname]
        # update lists and dictionaries

        self.chart[index[0]][index[1]] = ''
        self.seatdict.pop(randguestname, None)
        self.open.append(index)
        self.seated.remove(randguestname)
        self.toseat.append(randguestname)
        return [randguestname, index]

    def remove_guest_here(self, guestname, index):
        n = guestname
        self.chart[index[0]][index[1]] = ''
        self.seatdict.pop(n, None)
        self.open.append(index)
        self.seated.remove(n)
        self.toseat.append(n)
        return [n, index]

    def print_chart(self):
        print self.chart

    def print_seatingchart(self):
        for n in self.seated:
            index = self.seatdict[n]
            print (n, index)

    def to_excel(self, outfile='SeatingChart.xlsx'):
        chartdf = pandas.DataFrame(self.chart)
        chartdf.index = ["Table {0}".format(i) for i in chartdf.index]
        chartdf.to_excel(outfile)


class Organizer(object):
    def __init__(self, guestlist, seatingchart):
        self.gl = guestlist
        self.sc = seatingchart
        self.friendships = 0

    def seatguests(self):
        """
        This method seats all of the guests randomly
        :return:
        """
        print "Seating guests and their friends"
        nguests = len(self.gl.guests)
        for i in xrange(nguests):
            randguest = self.sc.pick_rand()
            if randguest is None:
                print "exit for loop"
                break
            else:
                self.sc.seat_guest(randguest)

    def seatguestsfriends(self):
        """
        This method seats all of the guests and tries to put the friends
        :return:
        """
        # at the same table
        print "Seating guests and their friends"
        nguests = len(self.gl.guests)
        for i in xrange(nguests):
            randguestname = self.sc.pick_rand()
            if randguestname is None:
                print "exit for loop"
                break
            rgn = randguestname
            self.sc.seat_guest(rgn)
            randguest = self.gl.guestdict[rgn]
            friends = randguest.get_friendnames()
            print "Seated " + rgn + ", seating friends also..."
            for f in friends:
                friend = self.sc.pick_friend_of(randguestname)
                if not (friend is None):
                    seatindex = self.sc.seat_guestfriend(rgn, friend)
                    if seatindex is None:
                        self.sc.seat_guest(friend)
                        print "There is no room at the table for the friend"

    def tablefriendcount(self, tablenum):
        count = 0
        names = self.sc.chart[tablenum]
        for i, n in enumerate(names):
            try:
                gobj = self.gl.guestdict[n]
            except KeyError:
                continue
            fns = gobj.get_friendnames()
            # Find the friends that are at the table by set intersection
            friendshere = list(set(fns).intersection(set(names)))
            count += len(friendshere) / 2.
        return count

    def friendcount(self):
        count = 0
        ntables = len(self.sc.chart)
        for i in xrange(ntables):
            count += self.tablefriendcount(i)
        return count

    def switch_rand(self):
        # Remove the two guests, saving their info and checking if possible
        info1 = self.sc.pick_randremove()
        if info1 is None:
            return None
        info2 = self.sc.pick_randremove()
        if info2 is None:
            return None
        # Switch their seats
        self.sc.seat_guest_here(info1[0], info2[1])
        self.sc.seat_guest_here(info2[0], info1[1])

    def metropolisstep(self, temp=0.1):
        """
        This method switches two friends and checks to see if it makes
        things better. If it doesn't it still makes the switch with some
        probability that is defined by the effective temperature in
        units of friendships

        Inputs
        ------
        :keyword temp: int, specifies how much random swiching will be done
        :return:
        """

        # First check the number of friends to get a baseline
        friendcount0 = self.friendcount()
        # Remove the two guests, saving their info and checking if possible
        info1 = self.sc.pick_randremove()
        if info1 is None:
            return None
        info2 = self.sc.pick_randremove()
        if info2 is None:
            return None
        # Switch their seats
        self.sc.seat_guest_here(info1[0], info2[1])
        self.sc.seat_guest_here(info2[0], info1[1])
        # First check the number of friends again to see if it improved
        friendcount1 = self.friendcount()

        if friendcount1 >= friendcount0:
            # If there are more friends than keep the switch!
            print "Made the switch"
            return friendcount1
        else:
            delfriends = friendcount1 - friendcount0
            expdelfriends = np.exp(delfriends / temp)
            rand = random.random()
            if rand >= expdelfriends:
                # if there are fewer friends then put it back
                print "better to keep the old way"
                self.sc.remove_guest_here(info1[0], info2[1])
                self.sc.remove_guest_here(info2[0], info1[1])
                self.sc.seat_guest_here(info1[0], info1[1])
                self.sc.seat_guest_here(info2[0], info2[1])
                return friendcount0
            else:
                print "it's temporarily worse but keep it"
                return friendcount1

def main(excelfilein,excelfileout):
    guestlist = GuestList()
    guestlist.fromExcel(excelfilein)
    guestlist.print_friendlist()


    nguests = len(guestlist.guests)
    print nguests
    seatsper = 8
    print nguests/seatsper

    chart = SeatingChart(guestlist, nguests/seatsper+1, seatsper)
    org = Organizer(guestlist, chart)
    # Seat everyone
    print "Seat guests with a friend"
    org.seatguestsfriends()
    print "now do Metropolis algorithim to increase friendships"
    count0 = org.friendcount()
    nsteps = 1000
    friendsT1 = np.zeros(nsteps)
    steps = np.arange(nsteps)
    for i in steps:
        print i
        friendsT1[i] = org.metropolisstep(temp=0.01)
    count1 = org.friendcount()
    print "Metropolis algorithm added {0} friends".format(count1-count0)
    print "export seating chart to an excel file"
    plt.plot(steps, friendsT1, label='T1')
    plt.xlabel = "step"
    plt.ylabel = "friendships"
    plt.show()
    org.sc.to_excel(excelfileout)


if __name__ == '__main__':
    import sys
    umesg = "python -m seatingchart.seatingchar excelfilein (excelfileout)"
    if len(sys.argv) > 1:
        # print 'nothing here'
        if len(sys.argv) > 2:
            excelfilein = sys.argv[1]
            excelfileout = sys.argv[2]
            main(excelfilein, excelfileout)
        else:
            excelfilein = sys.argv[1]
            excelfileout = excelfilein[:-5]+"out"+excelfilein[-5:]
            main(excelfilein, excelfileout)
    else:
        print umesg


