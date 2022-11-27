# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    
    # For agent to cross bridge, it should move towards the reward at either end (so discount should be high) and there should be less chance of moving in perpendicular directions (low or no noise)
    answerDiscount = 0.9

    # answerNoise = 0 should also work
    answerNoise = 0.01
    return answerDiscount, answerNoise

def question3a():

    # For agent to prefer closer exit, discount should be low
    answerDiscount = 0.1

    # For agent to actively go to closer exit (risking cliff), noise should be very low (otherwise the agent will take actions to actively avoid cliff)
    answerNoise = 0

    # For agent to prefer risky but short path, living reward should be negative
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():

    # For agent to prefer closer exit, discount should be low
    answerDiscount = 0.1

    # For agent to avoid cliff, there should be some noise so that agent actively avoids taking actions that might lead to cliff
    answerNoise = 0.1

    # For agent to prefer closer exit, living reward should be negative
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():

    # For agent to prefer further exit, discount should be low
    answerDiscount = 0.9

    # For agent to exhibit risky behaviour, noise should be very low
    answerNoise = 0

    # For agent to prefer an exit, living reward should be negative
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():

    # For agent to prefer further exit, discount should be low
    answerDiscount = 0.9

    # For agent to avoid cliff, there should be some noise so that agent actively avoids taking actions that might lead to cliff
    answerNoise = 0.2

    # For agent to prefer an exit, living reward should be negative
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.1
    answerNoise = 0.2

    # For agent to avoid any exit (cliff or otherwise), living reward should be significantly higher
    answerLivingReward = 10
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    # return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'
    return 'NOT POSSIBLE' # The agent is not able to find optimal policy to cross the bridge in 50 iterations

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
