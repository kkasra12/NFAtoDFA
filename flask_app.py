from flask import Flask,render_template,request
from dfa import state,dfa
from utils import nfaTodfa,dfa_minimization
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("getData.html")

@app.route("/toDfa")
def todfa():
    states_json = eval(request.values['states'])
    states = {}
    for s in states_json:
        isInitial,isFinal=False,False
        if s.get("isInitial"):
            isInitial=True
        if s.get("isFinal"):
            isFinal=True
        states.update({s['id']:state(s['label'],isFinal=isFinal,isInitial=isInitial)})
    transitions_json = eval(request.values['transitions'])
    for t in transitions_json:
        states[t['from']].connect(states[t['to']],t['label'])
    machine=dfa()
    for s in states.values():
        machine.add_state(s)

    dfa_machine,state_map = nfaTodfa(machine)
    minize_rule = dfa_minimization(dfa_machine)

    states_json = []
    transitions_json = []
    transition_id = 0
    for s in dfa_machine.states:
        new_state = {"id":s.name,"label":s.name}
        if s.isFinal:
            new_state.update({"isFinal":1})
        if s.isInitial:
            new_state.update({"isInitial":1})
        states_json.append(new_state)
        tmp = s.get_neighbours()
        for t in tmp:
            for next_s in tmp[t]:
                new_edge = {"id":str(transition_id),"from":s.name,"to":next_s,"label":str(t),"arrows":"to"}
                if t == "":
                    new_edge.update({"epsilon":1})
                else:
                    new_edge.update({"epsilon":0})
                transitions_json.append(new_edge)
                transition_id+=1
    print([[j.name for j in i] for i in minize_rule])
    return render_template("show_dfa.html",states_json=states_json,transitions_json=transitions_json,
                            state_map="<br>".join([i+":["+",".join([j.name for j in state_map[i]])+"]" for i in state_map]),
                            minimze_rule = str([[j.name for j in i] for i in minize_rule]))

if __name__=="__main__":
    app.run(debug=True)
