-- Presets: named poses in anatomical degrees (see Joints.lua for sign meaning).
-- Right side variants are authored; use `mirror = true` in a keyframe for the left side.
-- root.pos is in studs relative to HumanoidRootPart (y < 0 = crouch lower).

local P = {}

P.neutral = {}

P.tpose = {
	left_shoulder = { abduct = 90 }, right_shoulder = { abduct = 90 },
}

P.idle = {
	waist = { flex = 2 },
	neck = { flex = 3 },
	left_shoulder = { abduct = 6, flex = 3 }, right_shoulder = { abduct = 6, flex = 3 },
	left_elbow = { flex = 10 }, right_elbow = { flex = 10 },
	left_knee = { flex = 4 }, right_knee = { flex = 4 },
	left_hip = { flex = 2 }, right_hip = { flex = 2 },
}

P.idle_inhale = {
	root = { pos = { 0, 0.04, 0 } },
	waist = { flex = -2 },
	neck = { flex = 1 },
	left_shoulder = { abduct = 9, flex = 2 }, right_shoulder = { abduct = 9, flex = 2 },
	left_elbow = { flex = 12 }, right_elbow = { flex = 12 },
	left_knee = { flex = 2 }, right_knee = { flex = 2 },
}

-- Run: right foot strikes ahead, left arm forward. Mirror for the other side.
P.run_contact = {
	root = { flex = 10, twist = -6, pos = { 0, -0.15, 0 } },
	waist = { flex = 5, twist = 12 },
	neck = { flex = -8, twist = -6 },
	right_hip = { flex = 40 }, right_knee = { flex = 15 }, right_ankle = { flex = 10 },
	left_hip = { flex = -25 }, left_knee = { flex = 50 }, left_ankle = { flex = -20 },
	left_shoulder = { flex = 45, abduct = 8 }, left_elbow = { flex = 80 },
	right_shoulder = { flex = -40, abduct = 8 }, right_elbow = { flex = 55 },
}

-- Run: right leg under the body carrying weight, left knee driving forward and high.
P.run_passing = {
	root = { flex = 10, pos = { 0, 0.12, 0 } },
	waist = { flex = 5 },
	neck = { flex = -8 },
	right_hip = { flex = -5 }, right_knee = { flex = 25 }, right_ankle = { flex = -10 },
	left_hip = { flex = 55 }, left_knee = { flex = 105 }, left_ankle = { flex = 5 },
	left_shoulder = { flex = 10, abduct = 8 }, left_elbow = { flex = 85 },
	right_shoulder = { flex = -5, abduct = 8 }, right_elbow = { flex = 85 },
}

-- Right hand punch.
P.fight_stance = {
	root = { twist = 15, pos = { 0, -0.2, 0 } },
	waist = { twist = 5, flex = 8 },
	neck = { twist = -15, flex = 5 },
	left_hip = { flex = 20, abduct = 8 }, left_knee = { flex = 25 },
	right_hip = { flex = -10, abduct = 8 }, right_knee = { flex = 25 },
	left_shoulder = { flex = 55, abduct = 10 }, left_elbow = { flex = 120 },
	right_shoulder = { flex = 40, abduct = 15 }, right_elbow = { flex = 130 },
}

P.punch_windup = {
	root = { twist = 25, pos = { 0, -0.25, 0 } },
	waist = { twist = 20, flex = 6 },
	neck = { twist = -35, flex = 5 },
	left_hip = { flex = 22, abduct = 8 }, left_knee = { flex = 30 },
	right_hip = { flex = -12, abduct = 8 }, right_knee = { flex = 30 },
	left_shoulder = { flex = 55, abduct = 10 }, left_elbow = { flex = 115 },
	right_shoulder = { flex = 15, abduct = 25 }, right_elbow = { flex = 140 },
}

P.punch_hit = {
	root = { twist = -10, pos = { 0, -0.2, -0.15 } },
	waist = { twist = -25, flex = 12 },
	neck = { twist = 30, flex = 0 },
	left_hip = { flex = 25, abduct = 8 }, left_knee = { flex = 30 },
	right_hip = { flex = -18, abduct = 8 }, right_knee = { flex = 15 },
	left_shoulder = { flex = 40, abduct = 10 }, left_elbow = { flex = 125 },
	right_shoulder = { flex = 90, abduct = 5 }, right_elbow = { flex = 5 }, right_wrist = { flex = 0 },
}

P.jump_crouch = {
	root = { flex = 15, pos = { 0, -0.7, 0 } },
	waist = { flex = 20 },
	neck = { flex = -25 },
	left_hip = { flex = 75 }, right_hip = { flex = 75 },
	left_knee = { flex = 95 }, right_knee = { flex = 95 },
	left_ankle = { flex = 35 }, right_ankle = { flex = 35 },
	left_shoulder = { flex = -45, abduct = 10 }, right_shoulder = { flex = -45, abduct = 10 },
	left_elbow = { flex = 20 }, right_elbow = { flex = 20 },
}

P.jump_air = {
	root = { flex = -5, pos = { 0, 0.3, 0 } },
	waist = { flex = -10 },
	neck = { flex = -10 },
	left_hip = { flex = 30 }, right_hip = { flex = 20 },
	left_knee = { flex = 55 }, right_knee = { flex = 35 },
	left_ankle = { flex = -30 }, right_ankle = { flex = -30 },
	left_shoulder = { flex = 150, abduct = 20 }, right_shoulder = { flex = 150, abduct = 20 },
	left_elbow = { flex = 20 }, right_elbow = { flex = 20 },
}

P.jump_land = {
	root = { flex = 12, pos = { 0, -0.5, 0 } },
	waist = { flex = 18 },
	neck = { flex = -15 },
	left_hip = { flex = 60 }, right_hip = { flex = 60 },
	left_knee = { flex = 80 }, right_knee = { flex = 80 },
	left_ankle = { flex = 30 }, right_ankle = { flex = 30 },
	left_shoulder = { flex = 35, abduct = 30 }, right_shoulder = { flex = 35, abduct = 30 },
	left_elbow = { flex = 35 }, right_elbow = { flex = 35 },
}

-- Right hand wave: upper arm out to the side, rotated outward so the forearm points up.
-- Swing the hand by changing right_elbow.flex (70 = hand tilts out, 110 = hand tilts over the head).
P.wave = {
	waist = { abduct = -4 },
	neck = { abduct = 6, flex = -3 },
	right_shoulder = { abduct = 95, twist = 90, flex = 10 }, right_elbow = { flex = 90 },
	left_shoulder = { abduct = 6 }, left_elbow = { flex = 10 },
}
P.wave_out = { right_shoulder = { abduct = 95, twist = 90, flex = 10 }, right_elbow = { flex = 70 },
	waist = { abduct = -4 }, neck = { abduct = 6, flex = -3 }, left_shoulder = { abduct = 6 }, left_elbow = { flex = 10 } }
P.wave_in = { right_shoulder = { abduct = 95, twist = 90, flex = 10 }, right_elbow = { flex = 115 },
	waist = { abduct = -4 }, neck = { abduct = 6, flex = -3 }, left_shoulder = { abduct = 6 }, left_elbow = { flex = 10 } }

P.sit = {
	left_hip = { flex = 90, abduct = 5 }, right_hip = { flex = 90, abduct = 5 },
	left_knee = { flex = 90 }, right_knee = { flex = 90 },
	left_shoulder = { flex = 25, abduct = 5 }, right_shoulder = { flex = 25, abduct = 5 },
	left_elbow = { flex = 50 }, right_elbow = { flex = 50 },
	waist = { flex = 3 },
}

P.victory = {
	root = { pos = { 0, 0.1, 0 } },
	waist = { flex = -10 },
	neck = { flex = -20 },
	left_shoulder = { abduct = 150, flex = 15 }, right_shoulder = { abduct = 150, flex = 15 },
	left_elbow = { flex = 15 }, right_elbow = { flex = 15 },
	left_wrist = { flex = 20 }, right_wrist = { flex = 20 },
	left_hip = { abduct = 6 }, right_hip = { abduct = 6 },
}

-- Two handed weapon raised high over the head (right hand leads).
P.overhead_raise = {
	root = { flex = -5, pos = { 0, 0.05, 0.1 } },
	waist = { flex = -18 },
	neck = { flex = -15 },
	left_shoulder = { flex = 170, abduct = -10 }, right_shoulder = { flex = 170, abduct = -10 },
	left_elbow = { flex = 60 }, right_elbow = { flex = 60 },
	left_wrist = { flex = -30 }, right_wrist = { flex = -30 },
	left_hip = { flex = 15 }, right_hip = { flex = -10 },
	left_knee = { flex = 10 }, right_knee = { flex = 10 },
}

P.overhead_slam = {
	root = { flex = 25, pos = { 0, -0.6, -0.2 } },
	waist = { flex = 45 },
	neck = { flex = -30 },
	left_shoulder = { flex = 60, abduct = -10 }, right_shoulder = { flex = 60, abduct = -10 },
	left_elbow = { flex = 5 }, right_elbow = { flex = 5 },
	left_wrist = { flex = 20 }, right_wrist = { flex = 20 },
	left_hip = { flex = 70 }, right_hip = { flex = 10 },
	left_knee = { flex = 85 }, right_knee = { flex = 55 },
	left_ankle = { flex = 35 }, right_ankle = { flex = 0 },
}

return P
