# Solving State Explosion with A Petri-Nets and Vectors

Event driven programming has a problem formally modeling events
https://en.wikipedia.org/wiki/Event-driven_programming#Criticism

#### The Problem

https://barrgroup.com/Embedded-Systems/How-To/State-Machines-Event-Driven-Systems

```
Due to the phenomenon known as "state explosion," the complexity of a traditional FSM tends to grow much faster
than the complexity of the reactive system it describes. This happens because the traditional state machine formalism
inflicts repetitions.
```

### Bitwrap Solution

#### Some Computer Science:

What is a bitwrap machine?

It's a specialized form of:
https://en.wikipedia.org/wiki/Matrix_clock

It has elements in common with:
https://en.wikipedia.org/wiki/Counter_machine

Each machine schema is represented as the "Vector Form" of a Petri-Net
https://en.wikipedia.org/wiki/Petri_net

### Vector Form

given a simple 3-place Petri-Net

#TODO add diagram

#### State-Vectors

A 3-place Petri-Net - inital state

```
[1,0,0]
```

we execute the 'YAY' instruction
```
 [ 1,0,0]
+[-1,1,0]
 --------
 [ 0,1,0]
```

once this transition happens this graph cannot execute 'YAY' again.


NOTE: Due to the properties of Petri-Nets
the valid range of scalar values is constrained to natural numbers. (integers >=0)

```
 [ 0,1,0]
+[-1,1,0]
 --------
 [-1,1,0] <= invalid state
```

Using this machine as a programing model -
we can easily validate the output of our instruction by testing for any negative scalar values.

#### Playable Tic-Tac-Toe Demo

See A 21-place Petri-Net in action:

https://bitwrap.github.io/#octothorpe

By using state-vectors designed to model the tic-tac-toe board, we can effectively model
a game of tic-tac-to as a deterministic state machine without suffering from 'State Explosion'


