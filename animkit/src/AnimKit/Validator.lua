-- Validator: checks a spec, resolves every keyframe to a clamped pose, and returns a report.
-- Never throws for bad input; read result.ok / result.errors / result.warnings / result.clamped.

local HttpService = game:GetService("HttpService")
local Joints = require(script.Parent.Joints)
local PoseMath = require(script.Parent.PoseMath)
local Resolve = require(script.Parent.Resolve)

local Validator = {}

local PRIORITIES = { Core = true, Idle = true, Movement = true, Action = true,
	Action2 = true, Action3 = true, Action4 = true }
local STYLES = { Linear = true, Constant = true, Elastic = true, Cubic = true, Bounce = true, CubicV2 = true }
local DIRS = { In = true, Out = true, InOut = true }

local function newReport()
	local r = { errors = {}, warnings = {}, clamped = {}, _seen = {} }
	function r:error(where, msg) table.insert(self.errors, where .. ": " .. msg) end
	function r:warn(msg) table.insert(self.warnings, msg) end
	function r:warnOnce(msg)
		if not self._seen[msg] then self._seen[msg] = true; table.insert(self.warnings, msg) end
	end
	return r
end

local function parseEasing(e, dirOverride, report, where)
	local style, dir = "CubicV2", "InOut"
	if type(e) == "string" then
		style = e
	elseif type(e) == "table" then
		style = e.style or e[1] or style
		dir = e.direction or e[2] or dir
	elseif e ~= nil then
		report:error(where, "easing must be a style name or {style, direction}")
	end
	dir = dirOverride or dir
	if not STYLES[style] then
		report:error(where, ("easing style '%s' invalid (Linear, Constant, Cubic, CubicV2, Elastic, Bounce)"):format(tostring(style)))
		style = "CubicV2"
	end
	if not DIRS[dir] then
		report:error(where, ("easing direction '%s' invalid (In, Out, InOut)"):format(tostring(dir)))
		dir = "InOut"
	end
	return style, dir
end

local function decode(spec, report)
	if type(spec) == "string" then
		local ok, res = pcall(HttpService.JSONDecode, HttpService, spec)
		if not ok then
			report:error("spec", "JSON parse failed: " .. tostring(res))
			return nil
		end
		return res
	end
	if type(spec) ~= "table" then
		report:error("spec", "spec must be a table or a JSON string")
		return nil
	end
	return spec
end

-- rigInfo is optional (from Rig.inspect). Returns result table.
function Validator.validate(specIn, rigInfo)
	local report = newReport()
	local spec = decode(specIn, report)
	local result = { ok = false, errors = report.errors, warnings = report.warnings, clamped = report.clamped }
	if not spec then return result end

	local rigType = spec.rig and string.upper(tostring(spec.rig)) or nil
	if rigType and rigType ~= "R15" and rigType ~= "R6" then
		report:error("rig", "must be \"R15\" or \"R6\"")
		rigType = nil
	end
	if rigInfo and rigType and rigInfo.rigType ~= rigType then
		report:error("rig", ("spec is %s but the rig '%s' is %s"):format(rigType, rigInfo.model and rigInfo.model.Name or "?", rigInfo.rigType))
	end
	rigType = rigType or (rigInfo and rigInfo.rigType) or "R15"
	if not spec.rig then report:warn("rig not set, using " .. rigType) end

	local length = spec.length
	if type(length) ~= "number" or length <= 0 or length > 120 then
		report:error("length", "must be a number of seconds between 0 and 120")
		length = 1
	end
	local fps = spec.fps or 60
	if type(fps) ~= "number" or fps < 1 or fps > 240 then
		report:error("fps", "must be between 1 and 240"); fps = 60
	end
	local priority = spec.priority or "Action"
	if not PRIORITIES[priority] then
		report:error("priority", "must be Core, Idle, Movement, Action, Action2, Action3 or Action4"); priority = "Action"
	end
	if spec.looped ~= nil and type(spec.looped) ~= "boolean" then
		report:error("looped", "must be true or false")
	end
	local looped = spec.looped == true

	local kfs = spec.keyframes
	if type(kfs) ~= "table" or #kfs == 0 then
		report:error("keyframes", "need at least one keyframe")
		return result
	end

	local ctx = { spec = spec, rigType = rigType, report = report }
	local defs = Joints.table(rigType)
	local out, lastTime = {}, -1
	for i, kf in ipairs(kfs) do
		local where = ("keyframe %d"):format(i)
		if type(kf) ~= "table" then
			report:error(where, "must be a table"); continue
		end
		local t = kf.time
		if type(t) ~= "number" then
			report:error(where, "time missing (seconds)"); continue
		end
		local snapped = math.floor(t * fps + 0.5) / fps
		if math.abs(snapped - t) > 1e-4 then
			report:warn(("%s: time %g snapped to frame %g"):format(where, t, snapped))
		end
		t = snapped
		where = ("keyframe %d (t=%g)"):format(i, t)
		if t < 0 or t > length + 1e-6 then
			report:error(where, ("time outside 0..length (%g)"):format(length))
		end
		if t <= lastTime then
			report:error(where, "times must be strictly increasing (sort keyframes, no duplicates)")
		end
		lastTime = math.max(lastTime, t)
		local style, dir = parseEasing(kf.easing or spec.easing, kf.direction, report, where)
		local pose = Resolve.keyframe(kf, ctx, where)
		for part, v in pairs(pose) do
			local notes = PoseMath.clamp(v, defs[part])
			for _, n in ipairs(notes) do
				table.insert(report.clamped, ("t=%g %s: %s"):format(t, part, n))
			end
			if rigInfo and not rigInfo.motors[part] then
				report:warnOnce(("rig has no Motor6D driving '%s', that joint will not move"):format(part))
			end
		end
		table.insert(out, { time = t, style = style, direction = dir, pose = pose })
	end

	if #out > 0 and out[1].time > 0 then
		report:warn("first keyframe is not at time 0; the rig holds neutral until then")
	end
	if looped and #out > 0 and spec.autoClose ~= false and out[#out].time < length - 1e-6 then
		local first = out[1]
		table.insert(out, { time = length, style = first.style, direction = first.direction, pose = PoseMath.copy(first.pose) })
		report:warn(("looped: added closing keyframe at t=%g copying keyframe 1 (set autoClose=false to skip)"):format(length))
	end

	result.ok = #report.errors == 0
	result.anim = {
		name = tostring(spec.name or "AnimKitAnimation"), rigType = rigType, length = length,
		fps = fps, looped = looped, priority = priority, keyframes = out,
	}
	return result
end

function Validator.format(result)
	local lines = { result.ok and "OK" or ("FAILED with " .. #result.errors .. " error(s)") }
	for _, e in ipairs(result.errors) do table.insert(lines, "ERROR  " .. e) end
	for _, w in ipairs(result.warnings) do table.insert(lines, "WARN   " .. w) end
	for _, c in ipairs(result.clamped) do table.insert(lines, "CLAMP  " .. c) end
	if result.anim then
		local a = result.anim
		table.insert(lines, ("%s  %s  %gs  %d keyframes  looped=%s  priority=%s"):format(
			a.name, a.rigType, a.length, #a.keyframes, tostring(a.looped), a.priority))
	end
	return table.concat(lines, "\n")
end

return Validator
