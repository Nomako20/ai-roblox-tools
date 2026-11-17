-- Builder: validated anim -> KeyframeSequence with Poses nested like the Motor6D tree,
-- and saving into the rig's AnimSaves (ServerStorage.AnimSaves when there is no rig).

local ServerStorage = game:GetService("ServerStorage")
local Joints = require(script.Parent.Joints)
local PoseMath = require(script.Parent.PoseMath)
local Rig = require(script.Parent.Rig)

local Builder = {}

-- Pose.CFrame for every driven part of one keyframe: { [part] = CFrame }
function Builder.transforms(kf, rigInfo)
	local defs = Joints.table(rigInfo.rigType)
	local out = {}
	for part, m in pairs(rigInfo.motors) do
		local v, def = kf.pose[part], defs[part]
		if v and def then
			out[part] = PoseMath.toTransform(PoseMath.localCFrame(v, def), m.c0rot)
		else
			out[part] = CFrame.identity
		end
	end
	return out
end

local function makePose(name, cf, kf)
	local p = Instance.new("Pose")
	p.Name = name
	p.CFrame = cf
	p.Weight = 1
	p.EasingStyle = Enum.PoseEasingStyle[kf.style]
	p.EasingDirection = Enum.PoseEasingDirection[kf.direction]
	return p
end

-- anim: result.anim from Validator. rigInfo: Rig.inspect(model) or Rig.standard(type).
function Builder.build(anim, rigInfo)
	rigInfo = rigInfo or Rig.standard(anim.rigType)
	local seq = Instance.new("KeyframeSequence")
	seq.Name = anim.name
	seq.Loop = anim.looped
	seq.Priority = Enum.AnimationPriority[anim.priority]
	seq:SetAttribute("AnimKit", true)
	seq:SetAttribute("AnimKitLength", anim.length)

	local order = Rig.ordered(rigInfo)
	for i, kf in ipairs(anim.keyframes) do
		local key = Instance.new("Keyframe")
		key.Name = ("KF%02d"):format(i)
		key.Time = kf.time
		local cfs = Builder.transforms(kf, rigInfo)
		local poses = {}
		local rootPose = makePose(rigInfo.root, CFrame.identity, kf)
		rootPose.Parent = key
		poses[rigInfo.root] = rootPose
		for _, part in ipairs(order) do
			local parentPose = poses[rigInfo.motors[part].parent]
			if parentPose then
				local p = makePose(part, cfs[part], kf)
				p.Parent = parentPose
				poses[part] = p
			end
		end
		key.Parent = seq
	end
	return seq
end

local function uniqueName(container, base)
	local name, n = base, 1
	while true do
		local existing = container:FindFirstChild(name)
		if not existing or existing:GetAttribute("AnimKit") == true then
			return name, existing
		end
		n += 1
		name = ("%s_%d"):format(base, n)
	end
end

-- Saves seq. Replaces only an older AnimKit-made sequence of the same name, never someone else's.
-- Returns the saved KeyframeSequence and the container it went into.
function Builder.save(seq, model)
	local container
	if typeof(model) == "Instance" then
		container = model:FindFirstChild("AnimSaves")
		if not container then
			container = Instance.new("ObjectValue")
			container.Name = "AnimSaves"
			container.Parent = model
		end
	else
		container = ServerStorage:FindFirstChild("AnimSaves")
		if not container then
			container = Instance.new("Folder")
			container.Name = "AnimSaves"
			container.Parent = ServerStorage
		end
	end
	local name, old = uniqueName(container, seq.Name)
	if old then old:Destroy() end
	seq.Name = name
	seq.Parent = container
	return seq, container
end

-- Structural self check of a built sequence; returns list of problems (empty = fine).
function Builder.check(seq, rigInfo)
	local problems = {}
	local expected = 1 + #Rig.ordered(rigInfo)
	for _, key in ipairs(seq:GetKeyframes()) do
		local count = 0
		for _, d in ipairs(key:GetDescendants()) do
			if d:IsA("Pose") then
				count += 1
				local parent = d.Parent
				local m = rigInfo.motors[d.Name]
				if m and (not parent:IsA("Pose") or parent.Name ~= m.parent) then
					table.insert(problems, ("%s: pose %s is under %s, expected %s"):format(key.Name, d.Name, parent.Name, m.parent))
				end
			end
		end
		if count ~= expected then
			table.insert(problems, ("%s: %d poses, expected %d"):format(key.Name, count, expected))
		end
	end
	return problems
end

return Builder
