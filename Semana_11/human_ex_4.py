"""Exercise # 4 - week 11"""

class Arm:
    def __init__(self, side, upper_arm, forearm, hand, fingers):
        self.side = side
        self.upper_arm = upper_arm
        self.forearm = forearm
        self.hand = hand
        self.fingers = fingers

class Leg:
    def __init__(self, side, thigh, calf, foot, toes):
        self.side = side  
        self.thigh = thigh
        self.calf = calf
        self.foot = foot
        self.toes = toes

class Head:
    def __init__(self, eyes, mouth, nose, ears, head_hair,facial_hair):
        self.eyes = eyes
        self.mouth = mouth
        self.nose = nose
        self.ears = ears
        self.head_hair = head_hair
        self.facial_hair = facial_hair

class Torso:
    def __init__(self, left_arm, right_arm):
        self.left_arm = left_arm
        self.right_arm = right_arm

class LowerBody:
    def __init__(self, left_leg, right_leg):
        self.left_leg = left_leg
        self.right_leg = right_leg

class Human:
    def __init__(self, head, torso, lower_body,skin_color):
        self.head = head
        self.torso = torso
        self.lower_body = lower_body
        self.skin_color