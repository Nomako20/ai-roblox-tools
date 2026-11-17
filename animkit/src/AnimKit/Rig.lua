-- Rig: reads a character model's Motor6D tree (or stands in a stock R15/R6 layout).
-- info = { model, rigType, motors = { [part1Name] = { motor, parent = part0Name, c0rot } }, root = "HumanoidRootPart" }

local Joints = require(script.Parent.Joints)

local Rig = {}

local function rotOnly(cf)
	return cf - cf.Position
end

function Rig.detectType(model)
	local hum = model:FindFirstChildOfClass("Humanoid")
	if model:FindFirstChild("UpperTorso") or model:FindFirstChild("LowerTorso") then
		return "R15"
	end
	if model:FindFirstChild("Torso") then
		return "R6"
	end
	if hum then
		return hum.RigType == Enum.HumanoidRigType.R6 and "R6" or "R15"
	end
	return nil
end

-- Returns info or nil, error
function Rig.inspect(model)
	if typeof(model) ~= "Instance" or not model:IsA("Model") then
		return nil, "rig must be a Model (select the character model, not a part)"
	end
	local rigType = Rig.detectType(model)
	if not rigType then
		return nil, ("'%s' does not look like an R15 or R6 character"):format(model.Name)
	end
	local motors = {}
	for _, d in ipairs(model:GetDescendants()) do
		if d:IsA("Motor6D") and d.Part0 and d.Part1
			and d.Part0:IsDescendantOf(model) and d.Part1:IsDescendantOf(model) then
			motors[d.Part1.Name] = { motor = d, parent = d.Part0.Name, c0rot = rotOnly(d.C0) }
		end
	end
	if not model:FindFirstChild("HumanoidRootPart") then
		return nil, ("'%s' has no HumanoidRootPart"):format(model.Name)
	end
	local missing = {}
	for partName in pairs(Joints.table(rigType)) do
		if not motors[partName] then
			table.insert(missing, partName)
		end
	end
	return {
		model = model, rigType = rigType, motors = motors,
		root = "HumanoidRootPart", missing = missing,
	}
end

-- Stock layout without a real model (build only, no preview).
function Rig.standard(rigType)
	local motors = {}
	local c0 = Joints.STANDARD_C0ROT[rigType] or {}
	for partName, def in pairs(Joints.table(rigType)) do
		motors[partName] = { parent = def.parent, c0rot = c0[partName] }
	end
	return { rigType = rigType, motors = motors, root = "HumanoidRootPart", missing = {} }
end

-- Parts in parent-before-child order, starting under the root.
function Rig.ordered(info)
	local children = {}
	for part, m in pairs(info.motors) do
		children[m.parent] = children[m.parent] or {}
		table.insert(children[m.parent], part)
	end
	local out = {}
	local function walk(name, depth)
		if depth > 64 then return end
		local kids = children[name]
		if not kids then return end
		table.sort(kids)
		for _, k in ipairs(kids) do
			table.insert(out, k)
			walk(k, depth + 1)
		end
	end
	walk(info.root, 0)
	return out
end

-- Clear every Transform this tool may have written.
function Rig.resetPose(info)
	for _, m in pairs(info.motors) do
		if m.motor then
			m.motor.Transform = CFrame.identity
		end
	end
end

return Rig
