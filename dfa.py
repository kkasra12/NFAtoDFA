class  state:
    def __init__(self, name, isFinal=False, isInitial=False):
        self.name = name
        self.isFinal = isFinal
        self.isInitial = isInitial
        self.neighbours = {} # {trans:[state(s)]}
    def connect(self, next_state, trans):
        if type(next_state)!=type(self) or type(trans)!=type(""):
            raise "type error!!"
        if trans in self.neighbours:
            if next_state in self.neighbours[trans]:
                return
            print("# WARNING: duplicated transition!! ")
            self.neighbours[trans].append(next_state)
        else:
            self.neighbours.update({trans:[next_state]})
        return True
    def get_neighbours(self):
        return {i:[j.name for j in self.neighbours[i]] for i in self.neighbours}
    def all_nextStates(self):
        tmp=[]
        for i in self.neighbours.values():
            for j in i:
                if not j in tmp:
                    tmp.append(j)
        return tmp
    def transition_function(self,symbol):
        epsilon_transitions = [self]
        tmp = 0
        while tmp < len(epsilon_transitions):
            to_be_add = []
            for i in range(tmp,len(epsilon_transitions)):
                if epsilon_transitions[i].neighbours.get(""):
                    to_be_add+=epsilon_transitions[i].neighbours[""]
            tmp=len(epsilon_transitions)
            for i in to_be_add:
                if i not in epsilon_transitions:
                    epsilon_transitions.append(i)
        i=0
        ans = []
        while i < len(epsilon_transitions):
            tmp = epsilon_transitions[i].neighbours.get(symbol)
            if tmp:
                ans += tmp
            i+=1
        tmp = 0
        while tmp < len(ans):
            to_be_add = []
            for i in range(tmp,len(ans)):
                if ans[i].neighbours.get(""):
                    to_be_add+=ans[i].neighbours[""]
            tmp=len(ans)

            for i in to_be_add:
                if i not in ans:
                    ans.append(i)
        return ans

    def __str__(self):
        ans = str(self.name) + "->" + str(self.get_neighbours())
        if self.isFinal:
            ans += " (Final)"
        if self.isInitial:
            ans += " (Initial)"
        return ans
    def __lt__(self,other):
        if type(other) != type(self):
            raise "type error!!"
        return self.name < other.name
    def __eq__(self,other):
        return type(other)==type(self) and other.name==self.name and self.isFinal==other.isFinal and self.isInitial==other.isInitial
class dfa:
    def __init__(self):
        self.states = [] #list of state classes
    def add_trans_byname(self, start_state, end_state, transition):
        for i in self.states:
            if i.name == start_state:
                for j in self.states:
                    if j.name == end_state:
                        i.connect(j,transition)
                        return True
        return False
    def find_count(self, state_name):
        '''find the number of state in the states list'''
        return [i.name for i in self.states].find(state_name)
    def add_state_byname(self, state_name):
        if state_name in [i.name for i in self.states]:
            raise "duplicated state name\n\tstates_list:\t"+str(self.states)+"\n\tnew state name\t" + state_name
        self.states.append(state(state_name))
        return True
    def add_state(self,state_toadd):
        if state_toadd not in self.states:
            self.states.append(state_toadd)
    def add_final_state(self,state_name):
        for i in self.states:
            if i.name == state_name:
                i.isFinal = True
                return True
        raise "no state with given name founded!!! :("
    def add_initial_state(self, state_name):
        for i in self.states:
            if i.name == state_name:
                i.isInitial = True
                return True
        raise "state not founded!!!"
    @property
    def number_of_states(self):
        for i in range(len(self.states)):
            if type(self.states[i])!=type(state("")):
                self.states.pop(i)
        return len(self.states)
    def is_dfa(self):
        for i in self.states:
            #check duplicated or epsilon transitions
            for j in i.neighbours:
                if j=='' or len(i.neighbours[j])>1:
                    return False
            #check if state stisfies all alphabets
            for j in self.get_alphabet():
                if j not in i.neighbours.keys():
                    return False
        return True
    def __str__(self):
        return "states: " + "-".join([i.name for i in self.states]) + "\n\t" + "\n\t".join([str(i) for i in self.states]) + "\n" + "-"*20

    def get_initialStates(self):
        return [i for i in self.states if i.isInitial]
    def get_finalStates(self):
        return [i for i in self.states if i.isFinal]
    def get_alphabet(self):
        alphabet = []
        for i in self.states:
            for j in i.neighbours:
                if j not in alphabet:
                    alphabet.append(j)
        return alphabet
    def find_unreachable(self,delete_unreachables=False):
        visited_states = [*self.get_initialStates()]
        tmp = 0 # renderd states
        while 2+2==5-1: #after this loop reachable states are stored in visited_states
            visited_states_len = len(visited_states)
            for i in range(tmp,visited_states_len):
                next_states = visited_states[i].all_nextStates()
                for j in next_states:
                    if j not in visited_states:
                        visited_states.append(j)
            if visited_states_len == len(visited_states):
                break
            tmp = visited_states_len
        if delete_unreachables:
            i=0
            deleted_states = []
            while i < len(self.states):
                if self.states[i] not in visited_states:
                    deleted_states.append(self.states.pop(i))
                else:
                    i=i+1
            return deleted_states
        elif not delete_unreachables:
            return [i for i in self.states if i not in visited_states]
        else:
            raise "unvalid arguments!!"

if __name__ == "__main__":
    '''q0 = state("q0",isInitial=True)
    q1 = state("q1")
    print(q0<q1)
    q2 = state("q2",isFinal=True)
    q3 = state("q3")
    q4 = state("q4")
    print(q0)
    print(q1)
    d = dfa()
    from show_dfa import draw_dfa
    #draw_dfa(d)
    for i in [q0,q1,q2,q3,q4]:
        d.add_state(i)
    q0.connect(q1,'a')
    q0.connect(q0,'a')
    q0.connect(q0,'b')
    q1.connect(q2,'b')
    q3.connect(q4,'v')
    print(d)

    print("final states:\t"+str([i.name for i in d.get_finalStates()]) + "\ninitial states:\t" + str([i.name for i in d.get_initialStates()]))

    print("q0's next states for all transitions:" + str([j.name for j in q0.all_nextStates()]))
    print("d's alphabet:"+ str(d.get_alphabet()))
    print("unreachables:" + str([i.name for i in d.find_unreachable(delete_unreachables=True)]))
    print(d)
    print("d's alphabet:"+ str(d.get_alphabet()))
    print("if d is dfa:" + str(d.is_dfa()))'''
    ################################################
q0 = state("q0")
q1 = state("q1")
q2 = state("q2")
q3 = state("q3")
q4 = state("q4")
q0.connect(q0,"")
q0.connect(q1,"")
q1.connect(q2,"0")
q2.connect(q3,"")
q2.connect(q4,"")
print([i.name for i in q0.transition_function("0")])
