# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        allstates = self.mdp.getStates()
        for i in range(self.iterations):         
            temp_values = util.Counter()
            for state in allstates:
                max_val = -10000
                allactions = self.mdp.getPossibleActions(state)
                for action in allactions:
                    q_value = self.computeQValueFromValues(state, action)
                    if q_value > max_val:
                        max_val = q_value
                        temp_values[state] = max_val
            self.values = temp_values
        #return self.values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0

        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
          qValue += prob * (self.mdp.getReward(state,action,nextState) + self.discount*self.getValue(nextState))

        return qValue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        maxQvalue = float("-inf")
        qValue = 0

        actions = self.mdp.getPossibleActions(state)
        if not actions:
          return None
        qValue = 0
        for a in actions:
          qValue = self.getQValue(state,a);
          if qValue >= maxQvalue:
            bestAction = a
            maxQvalue = qValue

        return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return True

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        num_states = len(states)
        for i in range(self.iterations):
          while i >= num_states:
              i = i - num_states
          state = states[i]              
          if not self.mdp.isTerminal(state):
            values = []
            for action in self.mdp.getPossibleActions(state):
              q_value = self.computeQValueFromValues(state, action)
              values.append(q_value)
            self.values[state] = max(values)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        pred = util.Counter()
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for newState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        if newState in pred:
                            pred[newState].append(state)
                        else:
                            pred[newState] = [state]
                        
        priorityQ = util.PriorityQueue()                
        for state in self.mdp.getStates():
          if not self.mdp.isTerminal(state):
            values = []
            for action in self.mdp.getPossibleActions(state):
              QV = self.computeQValueFromValues(state, action)
              values.append(QV)
            difference = abs(max(values) - self.values[state])
            priorityQ.update(state, - difference)

        for i in range(self.iterations):
          if not priorityQ.isEmpty():

              temp_state = priorityQ.pop()
              if not self.mdp.isTerminal(temp_state):
                values = []
                for action in self.mdp.getPossibleActions(temp_state):
                    QV = self.computeQValueFromValues(temp_state, action)
                    values.append(QV)
                self.values[temp_state] = max(values)

          for i in pred[temp_state]:
            if not self.mdp.isTerminal(i):
              values = []
              for action in self.mdp.getPossibleActions(i):
                q_value = self.computeQValueFromValues(i, action)
                values.append(q_value)
              difference = (max(values) - self.values[i])
              if difference >= 0:
                  exit
              else:
                  difference = -1 * difference
              if difference > self.theta:
                priorityQ.update(i, -difference)        
                            

