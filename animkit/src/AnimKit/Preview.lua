-- Preview: play a KeyframeSequence on a rig (Edit mode or Play), or freeze the rig at one time.
-- Edit mode needs manual stepping (Animator:StepAnimations, plugin/command bar security).

local KeyframeSequenceProvider = game:GetService("KeyframeSequenceProvider")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local Builder = require(script.Parent.Builder)
local Rig = require(script.Parent.Rig)

local Preview = {}
local active = {} -- [model] = handle

local function ease(alpha, style, direction)
	if style == "Constant" then return 0 end
	if style == "Linear" then return alpha end
	local s = (style == "CubicV2") and "Cubic" or style
	return TweenService:GetValue(alpha, Enum.EasingStyle[s], Enum.EasingDirection[direction])
end

-- Interpolated transforms at time t (seconds). Pure; uses AnimKit easing approximation.
function Preview.sample(anim, rigInfo, t)
	local kfs = anim.keyframes
	if anim.looped and anim.length > 0 then t = t % anim.length end
	if t <= kfs[1].time then return Builder.transforms(kfs[1], rigInfo) end
	for i = 1, #kfs - 1 do
		local a, b = kfs[i], kfs[i + 1]
		if t <= b.time then
			local alpha = ease((t - a.time) / (b.time - a.time), a.style, a.direction)
			local ca, cb = Builder.transforms(a, rigInfo), Builder.transforms(b, rigInfo)
			local out = {}
			for part, cf in pairs(ca) do out[part] = cf:Lerp(cb[part], alpha) end
			return out
		end
	end
	return Builder.transforms(kfs[#kfs], rigInfo)
end

-- Freeze the rig at time t by writing Motor6D.Transform (good for screenshots). Undo with Preview.reset.
function Preview.poseAt(rigInfo, anim, t)
	Preview.stop(rigInfo.model)
	local cfs = Preview.sample(anim, rigInfo, t)
	for part, m in pairs(rigInfo.motors) do
		if m.motor and cfs[part] then m.motor.Transform = cfs[part] end
	end
end

function Preview.reset(rigInfo)
	Preview.stop(rigInfo.model)
	Rig.resetPose(rigInfo)
end

local function findAnimator(model, temps)
	local owner = model:FindFirstChildOfClass("Humanoid") or model:FindFirstChildOfClass("AnimationController")
	if not owner then
		owner = Instance.new("AnimationController")
		owner.Name = "AnimKitPreviewController"
		owner.Parent = model
		table.insert(temps, owner)
	end
	local animator = owner:FindFirstChildOfClass("Animator")
	if not animator then
		animator = Instance.new("Animator")
		animator:SetAttribute("AnimKitTemp", true)
		animator.Parent = owner
		table.insert(temps, animator)
	end
	return animator
end

-- Plays seq on the rig. opts: { loop = bool, speed = number }. Returns handle with :Stop().
function Preview.play(rigInfo, seq, opts)
	opts = opts or {}
	local model = rigInfo.model
	Preview.stop(model)
	local temps = {}
	local id = KeyframeSequenceProvider:RegisterKeyframeSequence(seq)
	local anim = Instance.new("Animation")
	anim.Name = "AnimKitPreview"
	anim.AnimationId = id
	local animator = findAnimator(model, temps)
	local track = animator:LoadAnimation(anim)
	track.Looped = opts.loop ~= false
	track:Play(0, 1, opts.speed or 1)

	local conn
	if not RunService:IsRunning() then
		conn = RunService.Heartbeat:Connect(function(dt)
			animator:StepAnimations(dt)
		end)
	end
	local handle = {}
	function handle.Stop()
		if active[model] == handle then active[model] = nil end
		if conn then conn:Disconnect() end
		pcall(function() track:Stop(0) end)
		if not RunService:IsRunning() then pcall(function() animator:StepAnimations(0) end) end
		Rig.resetPose(rigInfo)
		for i = #temps, 1, -1 do temps[i]:Destroy() end
		anim:Destroy()
	end
	handle.track = track
	active[model] = handle
	return handle
end

function Preview.stop(model)
	local h = model and active[model]
	if h then h.Stop() end
end

return Preview
