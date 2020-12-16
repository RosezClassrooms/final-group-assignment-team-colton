import random
from abc import ABC, abstractmethod
#assigns an estimated time to completion for each instance
class Assignment:
    MIN_TIME = 2
    MAX_TIME = 15
    PRCNT = 100

    def __init__(self):
        self.total_time = random.randint(Assignment.MIN_TIME, Assignment.MAX_TIME)
        self.time_to_completion = self.total_time

    def is_complete(self):
        return self.time_to_completion == 0

    def get_ttc(self):
        return self.time_to_completion

    def assn_complete(self):
        return self.is_complete

    def percentage_complete(self):
        return (1- (self.time_to_completion/self.total_time)) * Assignment.PRCNT

    def do_work(self, hours):
        if self.time_to_completion - hours > 0:
            self.time_to_completion =- hours
        else:
            self.time_to_completion = 0

    def __str__(self):
        return f"Time Remaining : {self.time_to_completion} hours out of {self.total_time} \n {self.percentage_complete():.2f}% complete"


#Template Pattern
class Activity(ABC):

    # This is the template method
    def activity(self, time):
        self.time = time
        self.effect = {}
        self.set_effect()
        self.get_effect()
        self.get_time()

    def get_effect(self):
        return self.effect

    def get_time(self):
        return self.time

    @abstractmethod
    def set_effect(self):
        pass


class SimpleActivity(Activity):
    def set_effect(self):
        self.effect = {'anxiety': 0, 'efficiency': 0, 'health': 0}


class TaxingActivity(Activity):
    def set_effect(self):
        self.effect = {'anxiety': 1, 'efficiency': -1, 'health': -1}


class RejuvenatingActivity(Activity):
    def set_effect(self):
        self.effect = {'anxiety': -1, 'efficiency': 1, 'health': 1}


class Health:
    MAX = 10
    AVG = 7.5
    SCALE = 10

    def __init__(self):
        self.nutrition = random.randint(self.AVG * self.SCALE, self.MAX * self.SCALE)
        self.rest = random.randint(self.AVG * self.SCALE, self.MAX * self.SCALE)
        self.anxiety = random.randint(self.AVG * self.SCALE, self.MAX * self.SCALE)
        self.efficiency = random.randint(self.AVG * self.SCALE, self.MAX * self.SCALE)
        self.health = random.randint(self.AVG * self.SCALE, self.MAX * self.SCALE)

    def get_nutrition(self):
        return self.nutrition

    def get_rest(self):
        return self.rest

    def get_anxiety(self):
        return self.anxiety

    def get_efficiency(self):
        return self.efficiency

    def get_self(self):
        return self.health

    def update_nutrition(self, amount):
        self.nutrition += (amount * self.SCALE)

    def update_rest(self, amount):
        self.rest += (amount * self.SCALE)

    def update_anxiety(self, amount):
        self.anxiety += (amount * self.SCALE)

    def update_efficiency(self, amount):
        self.efficiency += (amount * self.SCALE)

    def update_health(self, amount):
        self.health += (amount * self.SCALE)



class Schedule:
    def __init__(self):
        self.activities = [[], [], [], [], [], [], []]

    def add_activity(self, day, activity, duration, effect):
        if effect == 'taxing':
            ta = TaxingActivity()
            ta.activity(duration)
            self.activities[day].append(ta)
        elif effect == 'rejuvenating':
            ra = RejuvenatingActivity()
            ra.activity(duration)
            self.activities[day].append(ra)
        else:
            sa = SimpleActivity()
            sa.activity(duration)
            self.activities[day].append(sa)

    def remove_activity(self, day, activity):
        self.activities[day][activity] = 0

    def get_activities(self):
        return self.activities

    def duration_activities(self, day):
        sum = 0
        for a in self.activities[day]:
            sum += a.get_time()
        return sum


class Student:

    def __init__(self):
        self.assn_ttc = []
        self.assignments = []
        self.schedule = Schedule()
        self.health = Health()
        self.free_time = [0,0,0,0,0,0,0]
        #self.strategy = Strategy()

    def print_student(self):
        print ("Assignments: {}".format(self.assignments))
        print ("Assignments time to completion: {}".format(self.assn_ttc))
        print ("Schedule: {}".format(self.schedule))
        print ("Health: {}".format(self.health))
        print ("Strategy: {}".format((self.strategy)))

    def adjust_levels(self):
        if isinstance(self.strategy, Optimistic):
            self.health.update_anxiety(-3)
            self.health.update_rest(-2)
            self.health.update_health(-3)
            self.health.update_efficiency(3)
        elif isinstance(self.strategy, Procrastinator):
            self.health.update_nutrition(2)
            self.health.update_rest(3)
            self.health.update_efficiency(-2)
            self.health.update_anxiety(1)
        else:
            self.health.update_anxiety(-4)
            self.health.update_efficiency(4)

    def add_assignments(self, num):
        while num > 0:
            assn = Assignment()
            self.assignments.append(assn)
            self.assn_ttc.append(assn.get_ttc())
            num -= 1

    def check_and_remove_assignments(self):
        for assn in self.assignments:
            if assn.assn_complete():
                self.assignments.remove(assn)

    def total_assn_time(self):
        sum = 0
        for assn in self.assignments:
            sum += assn.get_ttc()
        return sum

    #takes in raw schedule in form: [[day, activity, duration, effect]]
    def add_schedule(self, raw_sc):
        for a in raw_sc:
            print (a)
            self.schedule.add_activity(a[0], a[1], a[2], a[3])


    def update_ttc(self):
        for assn in self.assignments:
            self.assn_ttc[self.assignments.index(assn)] = assn.get_ttc()



    def calc_free_time(self):
        for day in self.free_time:
            self.free_time[day] = 24 - self.schedule.duration_activities(day)

    def total_free_time(self):
        return sum(self.free_time)

    def shortest_assn(self):
        return min(self.assn_ttc)

    def choose_strategy(self,day):
        if (self.free_time[day] >= self.shortest_assn()) and (self.health.get_efficiency() >= 50) and (self.health.get_anxiety() <= 50):
            self.strategy = Optimistic(self, day)
            self.strategy.work_on_assignment()
            self.adjust_levels()
        elif (self.health.get_anxiety() > 50) and (self.health.get_efficiency() < 50) and (self.health.get_self() < 50 or self.health.get_nutrition() < 50 or self.health.get_rest() < 50):
            self.strategy = Procrastinator(self, day)
            self.strategy.work_on_assignment()
            self.adjust_levels()
        else:
            self.strategy = Orderly(self, day)
            self.strategy.work_on_assignment()
            self.adjust_levels()

    def perform_activities(self, day):
        for activity in self.schedule.get_activities()[day]:
            self.health.update_anxiety(activity.get_effect()['anxiety'])
            self.health.update_efficiency(activity.get_effect()['efficiency'])
            self.health.update_health(activity.get_effect()['self'])


class Strategy(ABC):

    def __init__(self, student, day):
        self.student = student
        self.day = day

    @abstractmethod
    def work_on_assignment(self):
        pass

class Optimistic(Strategy):

    def work_on_assignment(self):
        print ("Using Optimistic Strategy")
        for day in self.student.schedule:
            for assn in self.student.assignments:
                assn.do_work(self.student.assignment_time[day])
                self.student.update_ttc()
            self.student.perform_activities(day)



class Procrastinator(Strategy):

    def work_on_assignment(self):
        print ("Using Procrastinator Strategy")
        for day in self.student.schedule:
            for assn in self.student.assignments:
                assn.do_work(4)
                self.student.update_ttc()
            self.student.perform_activities(day)


class Orderly(Strategy):
    def work_on_assignment(self):
        print ("Using Orderly Strategy")
        if (self.student.total_assn_time() < self.student.total_free_time()):
            for assn in self.student.assignments:
                assn.do_work(assn.get_ttc())
                self.student.update_ttc()
            for day in self.student.schedule:
                self.student.perform_activity(day)





def main():

    student = Student()
    student.add_assignments(3)

    raw_sc = [
              [0, 'sleep', 8, 'rejuvenating'], [1, 'sleep', 8, 'rejuvenating'], [2, 'sleep', 8, 'rejuvenating'], [3, 'sleep', 8, 'rejuvenating'], [4, 'sleep', 8, 'rejuvenating'], [5, 'sleep', 8, 'rejuvenating'], [6, 'sleep', 8, 'rejuvenating'],
              [0, 'work', 3, 'taxing'], [2, 'work', 3, 'taxing'], [4, 'work', 3, 'taxing'], [6, 'work', 3, 'taxing'],
              [0, 'eat', 2, 'rejuvenating'], [1, 'eat', 2, 'rejuvenating'], [2, 'eat', 2, 'rejuvenating'], [3, 'eat', 2, 'rejuvenating'], [4, 'eat', 2, 'rejuvenating'], [5, 'eat', 2, 'rejuvenating'], [6, 'eat', 2, 'rejuvenating'],
              [0, 'exercise', 1, 'neither'], [1, 'exercise', 1, 'neither'], [2, 'exercise', 1, 'neither'], [3, 'exercise', 1, 'neither'], [4, 'exercise', 1, 'neither'],
              [0, 'commute', 2, 'taxing'], [1, 'commute', 2, 'taxing'], [2, 'commute', 2, 'taxing'], [3, 'commute', 2, 'taxing'], [4, 'commute', 2, 'taxing']
              ]
    student.add_schedule(raw_sc)

    day = 0
    while day <= 6:
        student.choose_strategy(day)
        student.print_student()
        day += 1


if __name__ == "__main__":
    main()