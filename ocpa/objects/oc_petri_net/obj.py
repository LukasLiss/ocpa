from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Any


class ObjectCentricPetriNet(object):
    class Place(object):
        def __init__(self, name, object_type, out_arcs=None, in_arcs=None, initial=False, final=False):
            self.__name = name
            self.__object_type = object_type
            self.__initial = initial
            self.__final = final
            self.__in_arcs = in_arcs if in_arcs != None else set()
            if out_arcs != None:
                self.__out_arcs = out_arcs
            else:
                self.__out_arcs = set()

        def __set_name(self, name):
            self.__name = name

        def __get_name(self):
            return self.__name

        def __get_object_type(self):
            return self.__object_type

        def __get_initial(self):
            return self.__initial

        def __get_final(self):
            return self.__final

        def __get_out_arcs(self):
            return self.__out_arcs

        def __set_out_arcs(self, out_arcs):
            self.__out_arcs = out_arcs

        def __get_in_arcs(self):
            return self.__in_arcs

        def __set_in_arcs(self, in_arcs):
            self.__in_arcs = in_arcs

        @property
        def preset(self):
            return set([in_arc.source for in_arc in self.__in_arcs])

        @property
        def postset(self):
            return set([out_arc.target for out_arc in self.__out_arcs])

        def __repr__(self):
            return str(self.name)

        def __eq__(self, other):
            # keep the ID for now in places
            return id(self) == id(other)

        def __hash__(self):
            # keep the ID for now in places
            return id(self)

        def __deepcopy__(self, memodict={}):
            if id(self) in memodict:
                return memodict[id(self)]
            new_place = ObjectCentricPetriNet.Place(
                self.name, properties=self.properties)
            memodict[id(self)] = new_place
            for arc in self.in_arcs:
                new_arc = deepcopy(arc, memo=memodict)
                new_place.in_arcs.add(new_arc)
            for arc in self.out_arcs:
                new_arc = deepcopy(arc, memo=memodict)
                new_place.out_arcs.add(new_arc)
            return new_place

        object_type = property(__get_object_type)
        initial = property(__get_initial)
        final = property(__get_final)
        out_arcs = property(__get_out_arcs, __set_out_arcs)
        in_arcs = property(__get_in_arcs, __set_in_arcs)
        name = property(__get_name, __set_name)

    class Transition(object):
        def __init__(self, name, label=None, in_arcs=None, out_arcs=None, properties=None, silent=False):
            self.__name = name
            self.__label = None if label is None else label
            self.__in_arcs = set() if in_arcs is None else in_arcs
            self.__out_arcs = set() if out_arcs is None else out_arcs
            self.__silent = silent
            self.__properties = dict() if properties is None else properties

        def __set_name(self, name):
            self.__name = name

        def __get_name(self):
            return self.__name

        def __set_label(self, label):
            self.__label = label

        def __get_label(self):
            return self.__label

        def __get_out_arcs(self):
            return self.__out_arcs

        def __get_in_arcs(self):
            return self.__in_arcs

        def __set_properties(self, properties):
            self.__properties = properties

        def __get_properties(self):
            return self.__properties

        def __get_silent(self):
            return self.__silent

        def __set_silent(self, silent):
            self.__silent = silent

        @property
        def preset(self):
            return set([in_arc.source for in_arc in self.__in_arcs])

        @property
        def preset_object_type(self):
            return set([in_arc.source.object_type for in_arc in self.__in_arcs])

        @property
        def postset(self):
            return set([out_arc.target for out_arc in self.__out_arcs])

        @property
        def postset_object_type(self):
            return set([out_arc.target.object_type for out_arc in self.__out_arcs])

        def __repr__(self):
            if self.label is None:
                return str(self.name)
            else:
                return str(self.label)

        def __eq__(self, other):
            # keep the ID for now in transitions
            return id(self) == id(other)

        def __hash__(self):
            # keep the ID for now in transitions
            return id(self)

        def __deepcopy__(self, memodict={}):
            if id(self) in memodict:
                return memodict[id(self)]
            new_trans = ObjectCentricPetriNet.Transition(
                self.name, self.label, properties=self.properties)
            memodict[id(self)] = new_trans
            for arc in self.in_arcs:
                new_arc = deepcopy(arc, memo=memodict)
                new_trans.in_arcs.add(new_arc)
            for arc in self.out_arcs:
                new_arc = deepcopy(arc, memo=memodict)
                new_trans.out_arcs.add(new_arc)
            return new_trans

        name = property(__get_name, __set_name)
        label = property(__get_label, __set_label)
        in_arcs = property(__get_in_arcs)
        out_arcs = property(__get_out_arcs)
        properties = property(__get_properties, __set_properties)
        silent = property(__get_silent, __set_silent)

    class Arc(object):
        def __init__(self, source, target, variable=False, weight=1, properties=None):
            if type(source) is type(target):
                raise Exception('Petri nets are bipartite graphs!')
            self.__source = source
            self.__target = target
            self.__weight = weight
            self.__variable = variable
            self.__properties = dict() if properties is None else properties

        def __get_source(self):
            return self.__source

        def __set_source(self, source):
            self.__source = source

        def __set_weight(self, weight):
            self.__weight = weight

        def __get_weight(self):
            return self.__weight

        def __get_target(self):
            return self.__target

        def __set_target(self, target):
            self.__target = target

        def __get_variable(self):
            return self.__variable

        def __set_properties(self, properties):
            self.__properties = properties

        def __get_properties(self):
            return self.__properties

        def __repr__(self):
            if type(self.source) is ObjectCentricPetriNet.Transition:
                if self.source.label:
                    return "(t)" + str(self.source.label) + "->" + "(p)" + str(self.target.name)
                else:
                    return "(t)" + str(self.source.name) + "->" + "(p)" + str(self.target.name)
            if type(self.target) is ObjectCentricPetriNet.Transition:
                if self.target.label:
                    return "(p)" + str(self.source.name) + "->" + "(t)" + str(self.target.label)
                else:
                    return "(p)" + str(self.source.name) + "->" + "(t)" + str(self.target.name)

        def __hash__(self):
            return id(self)

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target

        def __deepcopy__(self, memodict={}):
            if id(self) in memodict:
                return memodict[id(self)]
            new_source = memodict[id(self.source)] if id(self.source) in memodict else deepcopy(self.source,
                                                                                                memo=memodict)
            new_target = memodict[id(self.target)] if id(self.target) in memodict else deepcopy(self.target,
                                                                                                memo=memodict)
            memodict[id(self.source)] = new_source
            memodict[id(self.target)] = new_target
            new_arc = ObjectCentricPetriNet.Arc(
                new_source, new_target, weight=self.weight, properties=self.properties)
            memodict[id(self)] = new_arc
            return new_arc

        source = property(__get_source, __set_source)
        target = property(__get_target, __set_target)
        variable = property(__get_variable)
        weight = property(__get_weight, __set_weight)
        properties = property(__get_properties, __set_properties)

    def __init__(self, name=None, places=None, transitions=None, arcs=None, properties=None, nets=None):
        self.__name = "" if name is None else name
        self.__places = places if places != None else set()
        self.__transitions = transitions if transitions != None else set()
        self.__arcs = arcs if arcs != None else set()
        self.__properties = dict() if properties is None else properties
        self.__nets = nets if nets is not None else dict()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def places(self):
        return self.__places

    @property
    def transitions(self):
        return self.__transitions

    @property
    def arcs(self):
        return self.__arcs

    @property
    def properties(self):
        return self.__properties

    @property
    def object_types(self):
        return list(set([pl.object_type for pl in self.__places]))

    @property
    def nets(self):
        return self.__nets

    def add_arc(self, arc):
        self.__arcs.add(arc)
        arc.source.out_arcs.add(arc)
        arc.target.in_arcs.add(arc)

    def remove_place(self, pl):
        self.__places.remove(pl)
        remove_arcs = set()
        for arc in self.arcs:
            if arc.source == pl:
                remove_arcs.add(arc)
            elif arc.target == pl:
                remove_arcs.add(arc)
        self.remove_arcs(remove_arcs)

    def remove_arc(self, arc):
        self.__arcs.remove(arc)
        arc.source.out_arcs.remove(arc)
        arc.target.in_arcs.remove(arc)

    def remove_arcs(self, arcs):
        for arc in arcs:
            self.remove_arc(arc)

    def add_arcs(self, arcs):
        for arc in arcs:
            self.add_arc(arc)

    def remove_transition(self, t):
        self.__transitions.remove(t)
        remove_arcs = set()
        for arc in self.arcs:
            if arc.source == t:
                remove_arcs.add(arc)
            elif arc.target == t:
                remove_arcs.add(arc)
        self.remove_arcs(remove_arcs)

    def find_arc(self, source, target):
        for arc in self.__arcs:
            if arc.source == source and arc.target == target:
                return arc
        return None

    def find_transition(self, name):
        for transition in self.__transitions:
            if transition.name == name:
                return transition
        return None


@dataclass
class Marking(object):
    _tokens: Set[Tuple[ObjectCentricPetriNet.Place, str]
                 ] = field(default_factory=set)

    @property
    def tokens(self) -> Set[Tuple[ObjectCentricPetriNet.Place, str]]:
        return self._tokens

    def add_token(self, pl, obj):
        temp_tokens = set([(pl, oi) for (pl, oi) in self._tokens if oi == obj])
        self._tokens -= temp_tokens
        self._tokens.add((pl, obj))


@dataclass
class Subprocess(object):
    _ocpn: ObjectCentricPetriNet
    _object_types: Set[str] = field(default_factory=set)
    _activities: Set[str] = field(
        default_factory=set)
    _transitions: Set[ObjectCentricPetriNet.Transition] = field(
        default_factory=set)
    _sound: Any = False

    @property
    def object_types(self) -> Set[str]:
        return self._object_types

    @property
    def transitions(self) -> Set[ObjectCentricPetriNet.Transition]:
        return self._transitions

    @property
    def sound(self):
        return self._sound

    def __post_init__(self):
        if self._object_types != None:
            self._object_types = self._object_types
        else:
            self._object_types = self._ocpn.object_type

        if self._activities != None:
            self._transitions = [self._ocpn.find_transition(
                act) for act in self._activities]

            in_tpl = {tr: [arc.source for arc in tr.in_arcs]
                      for tr in self._transitions}
            out_tpl = {tr: [arc.target for arc in tr.out_arcs]
                       for tr in self._transitions}
            tpl = {tr: in_tpl[tr]+out_tpl[tr] for tr in self._transitions}
            self._sound = True if all(any(
                True if p.object_type in self._object_types else False for p in tpl[tr]) for tr in self._transitions) else False
        else:
            in_tpl = {tr: [arc.source for arc in tr.in_arcs]
                      for tr in self._ocpn.transitions}
            out_tpl = {tr: [arc.target for arc in tr.out_arcs]
                       for tr in self._ocpn.transitions}
            tpl = {tr: in_tpl[tr]+out_tpl[tr] for tr in self._ocpn.transitions}
            self._transitions = list(set(
                [tr for tr in self._ocpn.transitions for p in tpl[tr] if p.object_type in self._object_types]))
            self._sound = True
