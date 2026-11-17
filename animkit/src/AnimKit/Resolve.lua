-- Resolve: turns keyframe pose descriptions (preset names, inline poses, mirror, blend,
-- joint overrides) into a pose keyed by real rig part names. Never throws; it reports.

local Joints = require(script.Parent.Joints)
local PoseMath = require(script.Parent.PoseMath)
local Presets = require(script.Parent.Presets)

local Resolve = {}

local function presetNames(spec)
	local names = {}
	for k in pairs(Presets) do table.insert(names, k) end
	for k in pairs(spec.presets or {}) do table.insert(names, k) end
	table.sort(names)
	return table.concat(names, ", ")
end

-- raw { jointName = value } -> pose { rigPart = value }
function Resolve.pose(raw, ctx, where, mode, into)
	local out = into or {}
	if type(raw) ~= "table" then
		ctx.report:error(where, "pose must be a table of joints, e.g. { right_elbow = { flex = 90 } }")
		return out
	end
	for name, value in pairs(raw) do
		local part, status = Joints.resolve(name, ctx.rigType)
		if status == "unknown" then
			local hint = Joints.suggest(name, ctx.rigType)
			ctx.report:error(where, ("unknown joint '%s'%s"):format(tostring(name),
				#hint > 0 and (" (did you mean: " .. table.concat(hint, ", ") .. ")") or ""))
		elseif status == "absent" then
			ctx.report:warnOnce(("joint '%s' does not exist on %s, ignored"):format(tostring(name), ctx.rigType))
		else
			local def = Joints.table(ctx.rigType)[part]
			local parsed, err = PoseMath.parseValue(value, def)
			if not parsed then
				ctx.report:error(where, ("%s: %s"):format(tostring(name), err))
			elseif mode == "override" then
				PoseMath.override(out, part, parsed, value)
			else
				PoseMath.add(out, part, parsed)
			end
		end
	end
	return out
end

local function base(ref, ctx, where, depth)
	if type(ref) == "table" then
		return Resolve.pose(ref, ctx, where, "add")
	end
	if type(ref) ~= "string" then
		ctx.report:error(where, "pose must be a preset name or a table")
		return {}
	end
	local custom = ctx.spec.presets and ctx.spec.presets[ref]
	if custom ~= nil then
		ctx.cache = ctx.cache or {}
		if ctx.cache[ref] then return PoseMath.copy(ctx.cache[ref]) end
		local p
		if type(custom) == "table" and (custom.base or custom.pose or custom.blend or custom.joints or custom.mirror) then
			p = Resolve.keyframe(custom, ctx, where .. " preset '" .. ref .. "'", depth + 1)
		else
			p = Resolve.pose(custom, ctx, where .. " preset '" .. ref .. "'", "add")
		end
		ctx.cache[ref] = p
		return PoseMath.copy(p)
	end
	local builtin = Presets[ref]
	if builtin == nil then
		ctx.report:error(where, ("unknown preset '%s'. Known: %s"):format(ref, presetNames(ctx.spec)))
		return {}
	end
	return Resolve.pose(builtin, ctx, where .. " preset '" .. ref .. "'", "add")
end

-- kf fields used: pose | base, blend = {a, b, t}, mirror, joints (replace fields), add (offsets)
function Resolve.keyframe(kf, ctx, where, depth)
	depth = depth or 0
	if depth > 8 then
		ctx.report:error(where, "presets reference each other too deeply (loop?)")
		return {}
	end
	local ref = kf.pose or kf.base
	local pose
	if kf.blend ~= nil then
		if ref ~= nil then
			ctx.report:error(where, "use either 'pose' or 'blend', not both")
		end
		local b = kf.blend
		local a, bb, t = b and (b[1] or b.a or b.from), b and (b[2] or b.b or b.to), b and (b[3] or b.t)
		if type(b) ~= "table" or a == nil or bb == nil or type(t) ~= "number" then
			ctx.report:error(where, "blend must be {poseA, poseB, t} with t between 0 and 1")
			pose = {}
		else
			if t < 0 or t > 1 then
				ctx.report:warn(("%s: blend t=%g clamped to 0..1"):format(where, t))
				t = math.clamp(t, 0, 1)
			end
			pose = PoseMath.blend(base(a, ctx, where, depth), base(bb, ctx, where, depth), t)
		end
	elseif ref ~= nil then
		pose = base(ref, ctx, where, depth)
	else
		pose = {}
	end
	if kf.mirror == true then
		pose = PoseMath.mirror(pose)
	end
	if kf.joints ~= nil then
		Resolve.pose(kf.joints, ctx, where .. " joints", "override", pose)
	end
	if kf.add ~= nil then
		Resolve.pose(kf.add, ctx, where .. " add", "add", pose)
	end
	return pose
end

return Resolve
