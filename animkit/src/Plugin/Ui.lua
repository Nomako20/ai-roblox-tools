-- Ui: builds the AnimKit dock widget contents. No logic here; Main wires the buttons.

local Ui = {}

local function color(guide)
	local ok, c = pcall(function()
		return settings().Studio.Theme:GetColor(guide)
	end)
	return ok and c or Color3.fromRGB(46, 46, 46)
end

local function make(class, props, parent)
	local inst = Instance.new(class)
	for k, v in pairs(props) do inst[k] = v end
	inst.Parent = parent
	return inst
end

local function button(text, order, parent)
	return make("TextButton", {
		Name = text, Text = text, LayoutOrder = order, AutoButtonColor = true,
		Size = UDim2.new(0, 0, 0, 24), AutomaticSize = Enum.AutomaticSize.X,
		Font = Enum.Font.SourceSansSemibold, TextSize = 15,
		BackgroundColor3 = color(Enum.StudioStyleGuideColor.Button),
		TextColor3 = color(Enum.StudioStyleGuideColor.ButtonText),
		BorderSizePixel = 0,
	}, parent)
end

local function padded(parent)
	make("UIPadding", { PaddingLeft = UDim.new(0, 8), PaddingRight = UDim.new(0, 8) }, parent)
end

function Ui.build(widget)
	local bg = make("Frame", {
		Size = UDim2.fromScale(1, 1), BorderSizePixel = 0,
		BackgroundColor3 = color(Enum.StudioStyleGuideColor.MainBackground),
	}, widget)
	make("UIListLayout", { Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder }, bg)
	make("UIPadding", { PaddingTop = UDim.new(0, 6), PaddingLeft = UDim.new(0, 6),
		PaddingRight = UDim.new(0, 6), PaddingBottom = UDim.new(0, 6) }, bg)

	local textColor = color(Enum.StudioStyleGuideColor.MainText)
	local refs = { buttons = {} }

	refs.rigLabel = make("TextLabel", {
		LayoutOrder = 1, Size = UDim2.new(1, 0, 0, 20), BackgroundTransparency = 1,
		Text = "Rig: none (select a character model)", TextXAlignment = Enum.TextXAlignment.Left,
		Font = Enum.Font.SourceSans, TextSize = 15, TextColor3 = textColor,
	}, bg)

	local row1 = make("Frame", { LayoutOrder = 2, Size = UDim2.new(1, 0, 0, 24), BackgroundTransparency = 1 }, bg)
	make("UIListLayout", { FillDirection = Enum.FillDirection.Horizontal, Padding = UDim.new(0, 4),
		SortOrder = Enum.SortOrder.LayoutOrder }, row1)
	for i, name in ipairs({ "Use Selected Rig", "Load Selected Module", "Example" }) do
		refs.buttons[name] = button(name, i, row1)
		padded(refs.buttons[name])
	end

	local boxFrame = make("ScrollingFrame", {
		LayoutOrder = 3, Size = UDim2.new(1, 0, 0.5, -40), CanvasSize = UDim2.new(),
		AutomaticCanvasSize = Enum.AutomaticSize.XY, ScrollBarThickness = 6,
		BackgroundColor3 = color(Enum.StudioStyleGuideColor.InputFieldBackground), BorderSizePixel = 0,
	}, bg)
	refs.specBox = make("TextBox", {
		Size = UDim2.fromScale(1, 1), AutomaticSize = Enum.AutomaticSize.XY,
		MultiLine = true, ClearTextOnFocus = false, TextEditable = true,
		TextXAlignment = Enum.TextXAlignment.Left, TextYAlignment = Enum.TextYAlignment.Top,
		Font = Enum.Font.Code, TextSize = 13, TextColor3 = textColor, BackgroundTransparency = 1,
		PlaceholderText = "Paste a JSON spec here, or select a ModuleScript that returns a spec table",
		Text = "",
	}, boxFrame)

	local row2 = make("Frame", { LayoutOrder = 4, Size = UDim2.new(1, 0, 0, 24), BackgroundTransparency = 1 }, bg)
	make("UIListLayout", { FillDirection = Enum.FillDirection.Horizontal, Padding = UDim.new(0, 4),
		SortOrder = Enum.SortOrder.LayoutOrder }, row2)
	for i, name in ipairs({ "Validate", "Preview", "Stop", "Save" }) do
		refs.buttons[name] = button(name, i, row2)
		padded(refs.buttons[name])
	end

	local outFrame = make("ScrollingFrame", {
		LayoutOrder = 5, Size = UDim2.new(1, 0, 0.5, -40), CanvasSize = UDim2.new(),
		AutomaticCanvasSize = Enum.AutomaticSize.XY, ScrollBarThickness = 6,
		BackgroundColor3 = color(Enum.StudioStyleGuideColor.InputFieldBackground), BorderSizePixel = 0,
	}, bg)
	refs.output = make("TextLabel", {
		Size = UDim2.fromScale(1, 0), AutomaticSize = Enum.AutomaticSize.XY, BackgroundTransparency = 1,
		TextXAlignment = Enum.TextXAlignment.Left, TextYAlignment = Enum.TextYAlignment.Top,
		Font = Enum.Font.Code, TextSize = 13, TextColor3 = textColor, TextWrapped = false,
		Text = "AnimKit ready. Made by Nomako20 with Claude.",
	}, outFrame)
	return refs
end

return Ui
