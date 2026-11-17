-- AnimKit plugin entry: toolbar button + dock widget. Logic lives in AnimKit modules.
-- Made by Nomako20 with Claude.

local Selection = game:GetService("Selection")
local HttpService = game:GetService("HttpService")
local ChangeHistoryService = game:GetService("ChangeHistoryService")

local AnimKit = require(script.AnimKit)
local Ui = require(script.Ui)

local toolbar = plugin:CreateToolbar("AnimKit")
local toggle = toolbar:CreateButton("AnimKit", "Declarative animation builder", "")
toggle.ClickableWhenViewportHidden = true

local widget = plugin:CreateDockWidgetPluginGui("AnimKitWidget",
	DockWidgetPluginGuiInfo.new(Enum.InitialDockState.Float, false, false, 380, 520, 280, 320))
widget.Title = "AnimKit"
local ui = Ui.build(widget)

local state = { rig = nil, moduleSpec = nil, exampleIndex = 0 }

local function say(text)
	ui.output.Text = text
end

local function findRig(inst)
	while inst and inst ~= game do
		if inst:IsA("Model") and (inst:FindFirstChildOfClass("Humanoid") or inst:FindFirstChildOfClass("AnimationController")) then
			return inst
		end
		inst = inst.Parent
	end
	return nil
end

local function currentSpec()
	if state.moduleSpec and ui.specBox.Text == state.moduleText then
		return state.moduleSpec
	end
	return ui.specBox.Text
end

local function guarded(fn)
	return function()
		local ok, err = pcall(fn)
		if not ok then say("ERROR " .. tostring(err)) end
	end
end

toggle.Click:Connect(function()
	widget.Enabled = not widget.Enabled
end)
widget:GetPropertyChangedSignal("Enabled"):Connect(function()
	toggle:SetActive(widget.Enabled)
end)

ui.buttons["Use Selected Rig"].MouseButton1Click:Connect(guarded(function()
	local rig = findRig(Selection:Get()[1])
	if not rig then return say("Select a character model (or any part inside it).") end
	local info, err = AnimKit.inspectRig(rig)
	if not info then return say("ERROR " .. err) end
	state.rig = rig
	ui.rigLabel.Text = ("Rig: %s (%s)"):format(rig.Name, info.rigType)
	say(#info.missing > 0 and ("Rig is missing joints: " .. table.concat(info.missing, ", ")) or "Rig OK.")
end))

ui.buttons["Load Selected Module"].MouseButton1Click:Connect(guarded(function()
	local m = Selection:Get()[1]
	if not (m and m:IsA("ModuleScript")) then return say("Select a ModuleScript that returns a spec table.") end
	local clone = m:Clone() -- fresh require every time
	local ok, spec = pcall(require, clone)
	clone:Destroy()
	if not ok or type(spec) ~= "table" then return say("ERROR module did not return a table: " .. tostring(spec)) end
	state.moduleSpec = spec
	state.moduleText = HttpService:JSONEncode(spec)
	ui.specBox.Text = state.moduleText
	say("Loaded " .. m:GetFullName())
end))

ui.buttons.Example.MouseButton1Click:Connect(guarded(function()
	local names = {}
	for k in pairs(AnimKit.Examples) do table.insert(names, k) end
	table.sort(names)
	state.exampleIndex = state.exampleIndex % #names + 1
	local name = names[state.exampleIndex]
	state.moduleSpec = nil
	ui.specBox.Text = HttpService:JSONEncode(AnimKit.Examples[name])
	say("Example: " .. name .. " (press again for the next one)")
end))

ui.buttons.Validate.MouseButton1Click:Connect(guarded(function()
	say(AnimKit.validate(currentSpec(), state.rig).text)
end))

ui.buttons.Preview.MouseButton1Click:Connect(guarded(function()
	if not state.rig then return say("Pick a rig first (Use Selected Rig).") end
	local seq, res = AnimKit.build(currentSpec(), state.rig)
	if not seq then return say(res.text) end
	AnimKit.preview(state.rig, seq, { loop = true })
	say(res.text .. "\nPreviewing (looping). Press Stop to end.")
end))

ui.buttons.Stop.MouseButton1Click:Connect(guarded(function()
	if state.rig then AnimKit.resetPose(state.rig) end
	say("Stopped.")
end))

ui.buttons.Save.MouseButton1Click:Connect(guarded(function()
	local recording = ChangeHistoryService:TryBeginRecording("AnimKit Save")
	local res = AnimKit.create(currentSpec(), state.rig)
	if recording then
		ChangeHistoryService:FinishRecording(recording, Enum.FinishRecordingOperation.Commit)
	end
	if res.saved then Selection:Set({ res.saved }) end
	say(res.text)
end))

plugin.Unloading:Connect(function()
	if state.rig then pcall(AnimKit.resetPose, state.rig) end
end)
