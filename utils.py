from dfa import state,dfa

def nfaTodfa(nfa):
    if nfa.is_dfa():
        return
    states_map = {} #new_state_in_dfa:[states in nfa]
    states_mapR = {}
    que = [] #a que to find new states
    d=dfa()
    if len(nfa.get_initialStates()) != 1:
        raise "Initial state Error!!"
    new_state = state(create_new_name([i.name for i in d.states]))
    new_state.isInitial = True
    states_map.update({ new_state.name : nfa.get_initialStates() })
    states_mapR.update({tuple(id(i) for i in nfa.get_initialStates()): new_state})
    d.add_state(new_state)
    que.append(new_state)
    while 1.1+2.2!=3.3:
        #input()
        if len(que):
            current_state = que.pop(0)
        else:
            break
        #print(states_map)
        '''
        poping a state from que means:
            1.state has been added to dictionary and dfa
            2.state is not connected properly
        so this loop will try to find proper connections per aplphabet
        '''
        tmp = {}
        for t in sorted(nfa.get_alphabet()):
            if t=="":
                continue
            dest = []
        #    print("t: "+t+"\tcurstate: "+current_state.name+"\tstates_map: {"+str(",".join([i+"->"+",".join([j.name for j in states_map[i]]) for i in states_map] )))

            for s in states_map[current_state.name]:
                #for i in s.neighbours.get(t):
                for i in s.transition_function(t):
                    if not i in dest:
                        dest.append(i)
            if dest != []:
                dest.sort()
                dest_id = tuple(id(i) for i in dest)
        #        print("||".join([i.name for i in dest]))
        #        print(dest_id)
                if not dest in states_map.values():
        #            print("newstateadded")
                    new_state = state(create_new_name([i.name for i in d.states]))
                    for i in dest:
                        if i.isInitial:
                            #new_state.isInitial = True
                            pass
                        if i.isFinal:
                            new_state.isFinal = True
                        if new_state.isInitial and new_state.isFinal:
                            break
                    states_map.update({new_state.name : dest })
                    states_mapR.update({tuple(id(i) for i in dest): new_state})
                    d.add_state(new_state)
                    que.append(new_state)
                    current_state.connect(new_state,t)
                else:
        #            print("no need for new state")
                    current_state.connect(states_mapR[tuple(id(i) for i in dest)],t)
        #    print("-"*20+"\n")
        #    print("t: "+t+"\tcurstate: "+current_state.name+"\tstates_map: {"+str(",".join([i+"->"+",".join([j.name for j in states_map[i]]) for i in states_map] )))
        #    print(d)
    #ADD DEAD STATE
    alphabet = d.get_alphabet()
    dead_state = state("dead_state")
    is_dead_state_used = False
    for s in d.states:
        for a in alphabet:
            if not a in s.neighbours:
                s.connect(dead_state,a)
                is_dead_state_used = True
    if is_dead_state_used:
        d.add_state(dead_state)
        for i in alphabet:
            dead_state.connect(dead_state,i)

    #ADD INITIAL AND FINAL STATES
    '''for s in nfa.states:
        if s.isInitial:
            for i in '''
    return d,states_map

def dfa_minimization(m):
    print(m)
    l = [[],[]]
    states_num = {}
    for s in m.states:
        if s.isFinal:
            l[1].append(s)
            states_num.update({id(s):1})
        else:
            l[0].append(s)
            states_num.update({id(s):0})
    while "4:20":
        print([[j.name for j in i] for i in l])
        #print([[id(j) for j in i] for i in l])
        #print(states_num)
        to_be_add = []
        for i in l:
            new_set = []
            j=1
            while j < len(i):
                is_same = 1
                for a in m.get_alphabet():
                    print("---\n"+i[0].name+"\n"+i[j].name+"\n---")
                    if states_num[id(i[0].neighbours[a][0])] != states_num[id(i[j].neighbours[a][0])]:
                        is_same = 0
                        print("---\n"+i[0].name+"\n"+i[j].name+"\n---xxxxxxxxxxxxx")
                        break
                if not is_same:
                    tmp = i.pop(j)
                    new_set.append(tmp)
                    states_num[id(tmp)] = len(l)
                else:
                    j+=1
            to_be_add.append(new_set)
        is_added = 0
        for i in to_be_add:
            if i != []:
                l.append(i)
                is_added = 1
        if not is_added:
            break
    return l

def create_new_name(names):
    i=0
    while True:
        if "q"+str(i) in names:
            i=i+1
        else:
            return "q"+str(i)
    return "q0"

if __name__ == "__main__":
    '''a = state("a",isInitial=True)
    b = state("b")
    c = state("c")
    d = state("d")
    e = state("e",isFinal=True)
    m0 = dfa()
    for i in [a,b,c,d,e]:
        m0.add_state(i)
    for i in [a,b,c,d,e]:
        a.connect(i,'0')
    a.connect(d,'1')
    a.connect(e,'1')
    b.connect(c,'0')
    b.connect(e,'1')
    c.connect(b,'1')
    d.connect(e,'0')
'''
    a = state("a",isInitial=True)
    b = state("b")
    c = state("c",isFinal=True)
    d = state("d",isFinal=True)
    e = state("e",isFinal=True)
    f = state("f")
    m0 = dfa()
    for i in [a,b,c,d,e,f]:
        m0.add_state(i)
    a.connect(b,'0')
    a.connect(d,'1')
    b.connect(c,'1')
    b.connect(a,'0')
    c.connect(f,'1')
    c.connect(e,'0')
    d.connect(e,'0')
    d.connect(f,'1')
    f.connect(f,"0")
    f.connect(f,"1")
    e.connect(e,"0")
    e.connect(f,"1")

    #m1,sm = nfaTodfa(m0)
    print(m0)
    #print(m1)
    #print("\n".join([i+"->["+",".join([j.name for j in sm[i]])+"]" for i in sm]))
    dfa_minimization(m0)
    print("go to hell!!")
