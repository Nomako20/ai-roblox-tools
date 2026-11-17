-- Examples: ready specs (also used as tests). AnimKit.Examples.punch etc.

local E = {}

E.idle_breathe = {
	name = "AnimKit_IdleBreathe", rig = "R15", length = 3, looped = true, priority = "Idle",
	keyframes = {
		{ time = 0, pose = "idle" },
		{ time = 1.5, pose = "idle_inhale" },
		-- closing keyframe at t=3 is added automatically because looped = true
	},
}

E.run = {
	name = "AnimKit_Run", rig = "R15", length = 0.6, looped = true, priority = "Movement",
	easing = "Linear",
	keyframes = {
		{ time = 0, pose = "run_contact" },
		{ time = 0.15, pose = "run_passing" },
		{ time = 0.3, pose = "run_contact", mirror = true },
		{ time = 0.45, pose = "run_passing", mirror = true },
	},
}

E.punch = {
	name = "AnimKit_Punch", rig = "R15", length = 0.7, looped = false, priority = "Action",
	keyframes = {
		{ time = 0, pose = "fight_stance" },
		{ time = 0.15, pose = "punch_windup", easing = "Linear" }, -- fast straight drive into the hit
		{ time = 0.23, pose = "punch_hit" },
		{ time = 0.32, pose = "punch_hit", joints = { right_shoulder = { flex = 95 } } }, -- follow through
		{ time = 0.7, pose = "fight_stance" },
	},
}

E.wave = {
	name = "AnimKit_Wave", rig = "R15", length = 2.1, looped = false, priority = "Action",
	keyframes = {
		{ time = 0, pose = "idle" },
		{ time = 0.35, pose = "wave" },
		{ time = 0.6, pose = "wave_out" },
		{ time = 0.85, pose = "wave_in" },
		{ time = 1.1, pose = "wave_out" },
		{ time = 1.35, pose = "wave_in" },
		{ time = 1.6, pose = "wave" },
		{ time = 2.1, pose = "idle" },
	},
}

E.jump = {
	name = "AnimKit_Jump", rig = "R15", length = 1.1, looped = false, priority = "Action",
	keyframes = {
		{ time = 0, pose = "idle" },
		{ time = 0.2, pose = "jump_crouch", easing = "Linear" },
		{ time = 0.32, pose = "jump_air", easing = { "CubicV2", "InOut" } },
		{ time = 0.62, blend = { "jump_air", "jump_land", 0.4 } },
		{ time = 0.75, pose = "jump_land" },
		{ time = 1.1, pose = "idle" },
	},
}

E.sword_slam = {
	name = "AnimKit_SwordSlam", rig = "R15", length = 1.4, looped = false, priority = "Action",
	keyframes = {
		{ time = 0, pose = "idle" },
		{ time = 0.4, pose = "overhead_raise" },                                     -- anticipation (slow)
		{ time = 0.5, pose = "overhead_raise", add = { waist = { flex = -5 } }, easing = "Linear" }, -- hang
		{ time = 0.58, pose = "overhead_slam" },                                     -- action (fast)
		{ time = 0.66, pose = "overhead_slam", add = { root = { pos = { 0, -0.1, 0 } }, waist = { flex = 5 } } }, -- impact
		{ time = 1.05, blend = { "overhead_slam", "idle", 0.5 } },                    -- follow through
		{ time = 1.4, pose = "idle" },                                               -- settle
	},
}

return E
