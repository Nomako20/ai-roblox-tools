-- AnimKit: declarative character animation for Roblox. Made by Nomako20 with Claude.
-- Describe WHAT the pose is (spec); AnimKit handles joints, hierarchy, CFrames and limits.
--
--   local AnimKit = require(game.ServerStorage.AnimKit)
--   local res = AnimKit.create(spec, workspace.MyRig)   -- validate + build + save
--   print(res.text)

local Joints = require(script.Joints)
local Presets = require(script.Presets)
local Rig = require(script.Rig)
local Validator = require(script.Validator)
local Builder = require(script.Builder)
local Preview = require(script.Preview)

local AnimKit = {}
AnimKit.VERSION = "1.0.0"
AnimKit.Examples = require(script.Examples)
AnimKit.Presets = Presets

local function rigInfoOf(rig)
	if rig == nil then return nil end
	if type(rig) == "table" and rig.motors then return rig end
	local info, err = Rig.inspect(rig)
	if not info then error("AnimKit: " .. err, 3) end
	return info
end

-- Validate only. Returns result { ok, errors, warnings, clamped, anim, text }.
function AnimKit.validate(spec, rig)
	local res = Validator.validate(spec, rigInfoOf(rig))
	res.text = Validator.format(res)
	return res
end

-- Validate + build. Returns KeyframeSequence (or nil) and the result.
function AnimKit.build(spec, rig)
	local info = rigInfoOf(rig)
	local res = Validator.validate(spec, info)
	if res.ok then
		res.sequence = Builder.build(res.anim, info or Rig.standard(res.anim.rigType))
		local problems = Builder.check(res.sequence, info or Rig.standard(res.anim.rigType))
		for _, p in ipairs(problems) do
			table.insert(res.errors, "builder: " .. p)
		end
		res.ok = #problems == 0
	end
	res.text = Validator.format(res)
	return res.ok and res.sequence or nil, res
end

-- Save a built sequence under rig.AnimSaves (or ServerStorage.AnimSaves when rig is nil).
function AnimKit.save(sequence, rig)
	local model = type(rig) == "table" and rig.model or rig
	return Builder.save(sequence, model)
end

-- Validate + build + save in one call. Returns result (result.saved = the KeyframeSequence).
function AnimKit.create(spec, rig)
	local seq, res = AnimKit.build(spec, rig)
	if seq then
		local saved, container = AnimKit.save(seq, rig)
		res.saved = saved
		res.text ..= ("\nSaved: %s"):format(saved:GetFullName())
		res.container = container
	end
	return res
end

-- Play on a rig (Edit or Play mode). `what` = spec or KeyframeSequence. Returns handle with :Stop().
function AnimKit.preview(rig, what, opts)
	local info = rigInfoOf(rig)
	local seq = what
	if typeof(what) ~= "Instance" then
		local res
		seq, res = AnimKit.build(what, info)
		if not seq then error("AnimKit: spec invalid\n" .. res.text, 2) end
	end
	return Preview.play(info, seq, opts)
end

-- Freeze the rig at time t of a spec (for screenshots). AnimKit.resetPose(rig) undoes it.
function AnimKit.poseAt(rig, spec, t)
	local info = rigInfoOf(rig)
	local res = Validator.validate(spec, info)
	if not res.ok then error("AnimKit: spec invalid\n" .. Validator.format(res), 2) end
	Preview.poseAt(info, res.anim, t)
	return res
end

function AnimKit.stop(rig)
	local model = type(rig) == "table" and rig.model or rig
	Preview.stop(model)
end

function AnimKit.resetPose(rig)
	Preview.reset(rigInfoOf(rig))
end

-- Introspection helpers for agents.
function AnimKit.presetNames()
	local t = {}
	for k in pairs(Presets) do table.insert(t, k) end
	table.sort(t)
	return t
end

function AnimKit.jointInfo(rigType)
	local lines = {}
	for name, def in pairs(Joints.table(rigType or "R15")) do
		local l = def.limits
		table.insert(lines, ("%s (parent %s) flex %d..%d abduct %d..%d twist %d..%d"):format(
			name, def.parent, l.flex[1], l.flex[2], l.abduct[1], l.abduct[2], l.twist[1], l.twist[2]))
	end
	table.sort(lines)
	return table.concat(lines, "\n")
end

AnimKit.inspectRig = Rig.inspect

return AnimKit
