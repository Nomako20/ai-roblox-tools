-- PoseMath: joint value parsing, mirror, blend, merge, clamp and CFrame conversion.
-- A "pose" here is { [rigPartName] = { flex, abduct, twist, pos = {x,y,z} } } in anatomical degrees.

local Joints = require(script.Parent.Joints)

local PoseMath = {}

local FIELDS = { "flex", "abduct", "twist" }
local ANAT_KEYS = { flex = "flex", abduct = "abduct", twist = "twist",
	bend = "flex", pitch = "flex", side = "abduct", tilt = "abduct", out = "abduct",
	turn = "twist", yaw = "twist", rotate = "twist" }

local function num(v)
	return type(v) == "number" and v == v and v or nil
end

-- Parse one joint value into anatomical form. Accepts:
--   { flex=, abduct=, twist=, pos={x,y,z} }   (anatomical, recommended)
--   { x=, y=, z= }  or  {x, y, z}              (raw parent-part axes, degrees)
-- Returns value, errString
function PoseMath.parseValue(raw, def)
	if type(raw) ~= "table" then
		return nil, "joint value must be a table like {flex=30}"
	end
	local v = { flex = 0, abduct = 0, twist = 0 }
	local rx, ry, rz = raw.x or raw[1], raw.y or raw[2], raw.z or raw[3]
	if rx ~= nil or ry ~= nil or rz ~= nil then
		if (rx ~= nil and not num(rx)) or (ry ~= nil and not num(ry)) or (rz ~= nil and not num(rz)) then
			return nil, "raw x/y/z must be numbers"
		end
		v.flex = (rx or 0) * def.sx
		v.twist = (ry or 0) * def.sy
		v.abduct = (rz or 0) * def.sz
	end
	for key, val in pairs(raw) do
		local field = type(key) == "string" and ANAT_KEYS[string.lower(key)]
		if field then
			if not num(val) then
				return nil, ("'%s' must be a number"):format(key)
			end
			v[field] += val
		elseif key == "pos" or key == "position" or key == "offset" then
			local p = val
			if type(p) ~= "table" then
				return nil, "pos must be {x, y, z} in studs"
			end
			local px, py, pz = p.x or p[1] or 0, p.y or p[2] or 0, p.z or p[3] or 0
			if not (num(px) and num(py) and num(pz)) then
				return nil, "pos values must be numbers"
			end
			v.pos = { px, py, pz }
		elseif type(key) == "string" and not (key == "x" or key == "y" or key == "z") then
			return nil, ("unknown field '%s' (use flex/abduct/twist/pos or x/y/z)"):format(key)
		end
	end
	return v
end

function PoseMath.copyValue(v)
	local c = { flex = v.flex or 0, abduct = v.abduct or 0, twist = v.twist or 0 }
	if v.pos then c.pos = { v.pos[1], v.pos[2], v.pos[3] } end
	return c
end

function PoseMath.copy(pose)
	local out = {}
	for k, v in pairs(pose) do out[k] = PoseMath.copyValue(v) end
	return out
end

-- Swap left/right. Limb values are side aware so they move as-is;
-- center joints flip their sideways tilt and turn; positions flip x.
function PoseMath.mirror(pose)
	local out = {}
	for part, v in pairs(pose) do
		local c = PoseMath.copyValue(v)
		if Joints.isCenter(part) then
			c.abduct = -c.abduct
			c.twist = -c.twist
		end
		if c.pos then c.pos[1] = -c.pos[1] end
		out[Joints.mirrorName(part)] = c
	end
	return out
end

-- Linear blend; joints missing on one side count as neutral.
function PoseMath.blend(a, b, t)
	local out = {}
	local zero = { flex = 0, abduct = 0, twist = 0 }
	local keys = {}
	for k in pairs(a) do keys[k] = true end
	for k in pairs(b) do keys[k] = true end
	for k in pairs(keys) do
		local va, vb = a[k] or zero, b[k] or zero
		local c = {}
		for _, f in ipairs(FIELDS) do
			c[f] = (va[f] or 0) + ((vb[f] or 0) - (va[f] or 0)) * t
		end
		if va.pos or vb.pos then
			local pa, pb = va.pos or { 0, 0, 0 }, vb.pos or { 0, 0, 0 }
			c.pos = { pa[1] + (pb[1] - pa[1]) * t, pa[2] + (pb[2] - pa[2]) * t, pa[3] + (pb[3] - pa[3]) * t }
		end
		out[k] = c
	end
	return out
end

-- Override: fields present in `src` (the raw user table) replace fields in `dst`.
function PoseMath.override(dst, part, parsed, raw)
	local cur = dst[part] or { flex = 0, abduct = 0, twist = 0 }
	local hasRaw = raw.x or raw.y or raw.z or raw[1] or raw[2] or raw[3]
	for _, f in ipairs(FIELDS) do
		local given = hasRaw
		for key in pairs(raw) do
			if type(key) == "string" and ANAT_KEYS[string.lower(key)] == f then given = true end
		end
		if given then cur[f] = parsed[f] end
	end
	if parsed.pos then cur.pos = parsed.pos end
	dst[part] = cur
end

function PoseMath.add(dst, part, parsed)
	local cur = dst[part] or { flex = 0, abduct = 0, twist = 0 }
	for _, f in ipairs(FIELDS) do cur[f] = (cur[f] or 0) + parsed[f] end
	if parsed.pos then
		local p = cur.pos or { 0, 0, 0 }
		cur.pos = { p[1] + parsed.pos[1], p[2] + parsed.pos[2], p[3] + parsed.pos[3] }
	end
	dst[part] = cur
end

-- Clamp in place; returns list of "field value -> clamped" strings.
function PoseMath.clamp(v, def)
	local notes = {}
	for _, f in ipairs(FIELDS) do
		local lim = def.limits[f]
		local val = v[f]
		if val < lim[1] or val > lim[2] then
			local c = math.clamp(val, lim[1], lim[2])
			table.insert(notes, ("%s %g -> %g (range %g..%g)"):format(f, val, c, lim[1], lim[2]))
			v[f] = c
		end
	end
	if v.pos then
		local p = Vector3.new(v.pos[1], v.pos[2], v.pos[3])
		if p.Magnitude > def.maxPos then
			local c = p.Unit * def.maxPos
			table.insert(notes, ("pos length %.2f -> %.2f studs"):format(p.Magnitude, def.maxPos))
			v.pos = { c.X, c.Y, c.Z }
		end
	end
	return notes
end

-- Rotation in the parent part's axes, around the joint pivot.
function PoseMath.localCFrame(v, def)
	local rx = math.rad(v.flex * def.sx)
	local ry = math.rad(v.twist * def.sy)
	local rz = math.rad(v.abduct * def.sz)
	local r
	if def.order == "spine" then
		r = CFrame.Angles(0, ry, 0) * CFrame.Angles(0, 0, rz) * CFrame.Angles(rx, 0, 0)
	else
		r = CFrame.Angles(rx, 0, 0) * CFrame.Angles(0, 0, rz) * CFrame.Angles(0, ry, 0)
	end
	if v.pos then
		r = CFrame.new(v.pos[1], v.pos[2], v.pos[3]) * r
	end
	return r
end

-- Motor6D.Transform (= Pose.CFrame) so that `localCF` is applied in Part0 axes at the joint:
-- Part1 = Part0 * C0 * T * C1:Inverse(), and C0 = pos * c0rot  =>  T = c0rot^-1 * L * c0rot
function PoseMath.toTransform(localCF, c0rot)
	if not c0rot then return localCF end
	return c0rot:Inverse() * localCF * c0rot
end

return PoseMath
