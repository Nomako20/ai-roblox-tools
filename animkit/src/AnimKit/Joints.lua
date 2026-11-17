-- Joints: rig joint table, friendly aliases and human plausible limits.
-- Angles are ANATOMICAL degrees, side aware:
--   flex   : main bend. arm/leg: + = swing forward/up. elbow: + = bend. knee: + = bend.
--            ankle: + = toes up. wrist: + = palm side bend. spine/neck/root: + = bend forward / nod down.
--   abduct : sideways. limbs: + = away from the body. spine/neck/root: + = tilt to the character's right.
--   twist  : around the bone. limbs: + = rotate outward. spine/neck/root: + = turn to the character's right.
-- sx/sy/sz convert anatomical -> raw parent-part axes (x = flex, y = twist, z = abduct).
-- order "limb": twist, then abduct, then flex. order "spine": flex, then tilt, then turn.

local Joints = {}

local function def(parent, sx, sy, sz, order, flex, abduct, twist, maxPos)
	return {
		parent = parent, sx = sx, sy = sy, sz = sz, order = order,
		limits = { flex = flex, abduct = abduct, twist = twist },
		maxPos = maxPos or 0.25,
	}
end

local R15 = {
	LowerTorso = def("HumanoidRootPart", -1, -1, -1, "spine", { -180, 180 }, { -90, 90 }, { -180, 180 }, 4),
	UpperTorso = def("LowerTorso", -1, -1, -1, "spine", { -35, 75 }, { -35, 35 }, { -60, 60 }),
	Head = def("UpperTorso", -1, -1, -1, "spine", { -55, 60 }, { -40, 40 }, { -80, 80 }),
	LeftUpperArm = def("UpperTorso", 1, 1, -1, "limb", { -70, 185 }, { -30, 185 }, { -95, 95 }),
	RightUpperArm = def("UpperTorso", 1, -1, 1, "limb", { -70, 185 }, { -30, 185 }, { -95, 95 }),
	LeftLowerArm = def("LeftUpperArm", 1, 1, -1, "limb", { -5, 150 }, { -10, 10 }, { -90, 90 }),
	RightLowerArm = def("RightUpperArm", 1, -1, 1, "limb", { -5, 150 }, { -10, 10 }, { -90, 90 }),
	LeftHand = def("LeftLowerArm", 1, 1, -1, "limb", { -75, 80 }, { -30, 30 }, { -30, 30 }),
	RightHand = def("RightLowerArm", 1, -1, 1, "limb", { -75, 80 }, { -30, 30 }, { -30, 30 }),
	LeftUpperLeg = def("LowerTorso", 1, 1, -1, "limb", { -40, 125 }, { -25, 75 }, { -45, 45 }),
	RightUpperLeg = def("LowerTorso", 1, -1, 1, "limb", { -40, 125 }, { -25, 75 }, { -45, 45 }),
	LeftLowerLeg = def("LeftUpperLeg", -1, 1, -1, "limb", { -5, 150 }, { -10, 10 }, { -20, 20 }),
	RightLowerLeg = def("RightUpperLeg", -1, -1, 1, "limb", { -5, 150 }, { -10, 10 }, { -20, 20 }),
	LeftFoot = def("LeftLowerLeg", 1, 1, -1, "limb", { -55, 35 }, { -25, 25 }, { -25, 25 }),
	RightFoot = def("RightLowerLeg", 1, -1, 1, "limb", { -55, 35 }, { -25, 25 }, { -25, 25 }),
}

-- R15 canonical name -> R6 part name (nil = joint does not exist on R6)
local R15_TO_R6 = {
	LowerTorso = "Torso", Head = "Head",
	LeftUpperArm = "Left Arm", RightUpperArm = "Right Arm",
	LeftUpperLeg = "Left Leg", RightUpperLeg = "Right Leg",
}

local R6 = {}
for r15Name, r6Name in pairs(R15_TO_R6) do
	local src = R15[r15Name]
	local copy = table.clone(src)
	copy.limits = table.clone(src.limits)
	copy.parent = (r6Name == "Torso") and "HumanoidRootPart" or "Torso"
	R6[r6Name] = copy
end

Joints.R15 = R15
Joints.R6 = R6
Joints.R15_TO_R6 = R15_TO_R6

-- Friendly aliases -> R15 canonical name. Keys are normalized (lowercase, no spaces/_/-).
local ALIASES = {
	root = "LowerTorso", hips = "LowerTorso", pelvis = "LowerTorso", lowertorso = "LowerTorso",
	waist = "UpperTorso", spine = "UpperTorso", chest = "UpperTorso", torso = "UpperTorso", uppertorso = "UpperTorso",
	neck = "Head", head = "Head",
}
for _, side in ipairs({ "Left", "Right" }) do
	local s, l = side, string.lower(side)
	local short = string.sub(l, 1, 1)
	local function add(names, target)
		for _, n in ipairs(names) do
			ALIASES[l .. n] = s .. target
			ALIASES[short .. n] = s .. target
		end
	end
	add({ "shoulder", "upperarm", "arm" }, "UpperArm")
	add({ "elbow", "lowerarm", "forearm" }, "LowerArm")
	add({ "wrist", "hand" }, "Hand")
	add({ "hip", "upperleg", "thigh", "leg" }, "UpperLeg")
	add({ "knee", "lowerleg", "shin" }, "LowerLeg")
	add({ "ankle", "foot" }, "Foot")
end

function Joints.normalizeKey(name)
	return (string.gsub(string.lower(tostring(name)), "[%s_%-%.]", ""))
end

function Joints.table(rigType)
	return rigType == "R6" and R6 or R15
end

-- Resolve a user joint name to the rig part name.
-- Returns partName or nil, plus a status: "ok" | "absent" (valid name, joint missing on this rig) | "unknown"
function Joints.resolve(name, rigType)
	local tbl = Joints.table(rigType)
	local key = Joints.normalizeKey(name)
	for partName in pairs(tbl) do
		if Joints.normalizeKey(partName) == key then
			return partName, "ok"
		end
	end
	local canonical = ALIASES[key]
	if not canonical then
		return nil, "unknown"
	end
	if rigType == "R6" then
		local r6 = R15_TO_R6[canonical]
		if r6 then
			return r6, "ok"
		end
		return nil, "absent"
	end
	return canonical, "ok"
end

-- Closest known names, for "did you mean" messages.
function Joints.suggest(name, rigType)
	local key = Joints.normalizeKey(name)
	local out = {}
	local pool = {}
	for k in pairs(ALIASES) do table.insert(pool, k) end
	for k in pairs(Joints.table(rigType)) do table.insert(pool, k) end
	for _, cand in ipairs(pool) do
		local c = Joints.normalizeKey(cand)
		if #key >= 3 and (string.find(c, key, 1, true) or string.find(key, c, 1, true)) then
			table.insert(out, cand)
		end
	end
	table.sort(out)
	return out
end

function Joints.isCenter(partName)
	return not (string.find(partName, "Left", 1, true) or string.find(partName, "Right", 1, true))
end

function Joints.mirrorName(partName)
	if string.find(partName, "Left", 1, true) then
		return (string.gsub(partName, "Left", "Right"))
	elseif string.find(partName, "Right", 1, true) then
		return (string.gsub(partName, "Right", "Left"))
	end
	return partName
end

-- Rest C0 rotations of the stock rigs (used when no real rig is given). R15 stock C0s have no rotation.
local function rot(...) return CFrame.new(0, 0, 0, ...) end
Joints.STANDARD_C0ROT = {
	R15 = {},
	R6 = {
		Torso = rot(-1, 0, 0, 0, 0, 1, 0, 1, 0),
		Head = rot(-1, 0, 0, 0, 0, 1, 0, 1, 0),
		["Right Arm"] = rot(0, 0, 1, 0, 1, 0, -1, 0, 0),
		["Left Arm"] = rot(0, 0, -1, 0, 1, 0, 1, 0, 0),
		["Right Leg"] = rot(0, 0, 1, 0, 1, 0, -1, 0, 0),
		["Left Leg"] = rot(0, 0, -1, 0, 1, 0, 1, 0, 0),
	},
}

return Joints
