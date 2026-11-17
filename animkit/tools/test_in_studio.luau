-- AnimKit Studio self-test. Run via MCP execute_luau (Edit mode) AFTER dist/install_animkit.luau.
-- Creates AnimKitDummyR15 / AnimKitDummyR6, builds every example on both, checks structure,
-- tries a short preview and poseAt, then removes the dummies. Touches nothing else.

local Players = game:GetService("Players")
local AnimKit = require(game.ServerStorage.AnimKit)
local out = {}
local function log(s) table.insert(out, s) end

local function dummy(rigType, x)
	local m = Players:CreateHumanoidModelFromDescription(Instance.new("HumanoidDescription"), rigType)
	m.Name = "AnimKitDummy" .. (rigType == Enum.HumanoidRigType.R15 and "R15" or "R6")
	m:PivotTo(CFrame.new(x, 5, 0))
	m.HumanoidRootPart.Anchored = true
	m.Parent = workspace
	return m
end

local ok, err = pcall(function()
	for _, rt in ipairs({ Enum.HumanoidRigType.R15, Enum.HumanoidRigType.R6 }) do
		local rig = dummy(rt, rt == Enum.HumanoidRigType.R15 and 2000 or 2008)
		local info = assert(AnimKit.inspectRig(rig))
		log(("%s: %s, missing joints: %s"):format(rig.Name, info.rigType, table.concat(info.missing, ",")))
		for name, spec in pairs(AnimKit.Examples) do
			local s = table.clone(spec)
			s.rig = info.rigType
			local seq, res = AnimKit.build(s, rig)
			log(("  %-12s ok=%s kfs=%d warn=%d clamp=%d %s"):format(name, tostring(res.ok),
				seq and #seq:GetKeyframes() or 0, #res.warnings, #res.clamped, res.ok and "" or res.text))
			if seq then seq:Destroy() end
		end
		local before = rig.Head.Position
		AnimKit.poseAt(rig, AnimKit.Examples.jump, 0.2)
		task.wait()
		log(("  poseAt jump crouch: head moved %.2f studs"):format((rig.Head.Position - before).Magnitude))
		AnimKit.resetPose(rig)
		local h = AnimKit.preview(rig, AnimKit.Examples.wave, { loop = true })
		task.wait(0.5)
		log(("  preview wave: track playing=%s t=%.2f"):format(tostring(h.track.IsPlaying), h.track.TimePosition))
		h.Stop()
		local bad = AnimKit.validate({ rig = "R15", length = 1, keyframes = {
			{ time = 0.5, pose = { lefft_elbow = { flex = 400 } } }, { time = 0.2, pose = "nope" } } }, rig)
		log("  bad spec report:\n" .. bad.text)
		rig:Destroy()
	end
end)
for _, n in ipairs({ "AnimKitDummyR15", "AnimKitDummyR6" }) do
	local m = workspace:FindFirstChild(n)
	if m then m:Destroy() end
end
if not ok then log("TEST ERROR: " .. tostring(err)) end
return table.concat(out, "\n")
