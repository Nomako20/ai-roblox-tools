# AnimKit: declarative character animation for Roblox

Made by Nomako20 with Claude.

AnimKit lets an AI agent (or a person) say **what** a pose is, such as "right elbow bent 90, torso turned 20 to the right". AnimKit then handles **how**: real joint names, the Motor6D hierarchy, R15/R6 CFrame maths, human-plausible limits, and saving a real `KeyframeSequence`.

You don't write CFrames by hand or guess joint names. If something is wrong, you get a readable error instead of a broken animation.

```
spec (Luau table or JSON)
  -> Validator  (names, times, easing, presets, mirror/blend, clamps angles, reports)
  -> Builder    (KeyframeSequence with Poses nested like the Motor6D tree)
  -> save       (rig.AnimSaves, or ServerStorage.AnimSaves)
  -> preview    (Animator in Edit or Play mode)  /  poseAt (freeze one frame for a screenshot)
```

## Files

| Path | What |
|---|---|
| `src/AnimKit/init.lua` | Public API (`AnimKit.create/validate/build/save/preview/poseAt/resetPose`) |
| `src/AnimKit/Joints.lua` | Joint table, aliases, sign conventions, angle limits, R15 to R6 map |
| `src/AnimKit/PoseMath.lua` | Parses joint values, mirror, blend, clamp, angle to CFrame |
| `src/AnimKit/Presets.lua` | Named poses |
| `src/AnimKit/Resolve.lua` | Keyframe to pose (preset, inline, blend, mirror, joints, add) |
| `src/AnimKit/Validator.lua` | All checks and the report |
| `src/AnimKit/Rig.lua` | Reads a real rig's Motor6Ds (or uses the stock layout) |
| `src/AnimKit/Builder.lua` | KeyframeSequence building, structure self-check, saving |
| `src/AnimKit/Preview.lua` | Animator preview (Edit mode stepping) and `poseAt` |
| `src/AnimKit/Examples.lua` | 6 ready specs (idle, run, punch, wave, jump, sword slam) |
| `src/Plugin/Main.server.lua`, `Ui.lua` | Toolbar button and dock widget |
| `tools/build.py` | Builds `dist/` |
| `tools/test_in_studio.luau` | Self-test via MCP execute_luau: temporary `AnimKitDummyR15`/`R6` rigs, builds every example, preview, poseAt and a bad-spec report, then deletes the dummies |
| `dist/install_animkit.luau` | One script that installs `ServerStorage.AnimKit` (for MCP) |
| `dist/AnimKit.rbxmx` | The module tree as a model file |
| `dist/AnimKitPlugin.rbxmx` | The local plugin |

After editing anything in `src/`, run `python tools/build.py` again.

## Install

**A) Through MCP (for agents).** Read `dist/install_animkit.luau` and pass its full text as `code` to `mcp__Roblox_Studio__execute_luau` with `datamodel_type = "Edit"`. It creates `ServerStorage.AnimKit`.

The installer replaces an existing `ServerStorage.AnimKit` only if that one was made by the installer (it has the `AnimKitInstall` attribute). Otherwise it stops with an error. Load the MCP tools first with ToolSearch, query `Roblox_Studio`.

**B) As a model.** Drag `dist/AnimKit.rbxmx` into Studio and move it into ServerStorage.

**C) As a plugin.** Copy `dist/AnimKitPlugin.rbxmx` into `%LOCALAPPDATA%\Roblox\Plugins\`, then restart Studio. An **AnimKit** toolbar button opens the widget, which has these controls:

- **Use Selected Rig**: select a character model or any part inside it.
- **Load Selected Module**: loads a ModuleScript that returns a spec table.
- **Example**: cycles through the built-in examples.
- **Validate**, **Preview** (loops), **Stop**, **Save**.

The text box takes JSON. Luau tables need a ModuleScript, because plugins cannot run `loadstring`.

## Agent workflow (MCP execute_luau, Edit mode)

Do not stop a running playtest to do this. `execute_luau` works in Edit mode while the user plays only if Studio exposes the Edit datamodel; check `get_studio_state` first.

```lua
local AnimKit = require(game.ServerStorage.AnimKit)
local rig = workspace.AnimKitDummy            -- an R15 or R6 character Model

local spec = {
	name = "HeavySlam", rig = "R15", length = 1.4, priority = "Action",
	keyframes = {
		{ time = 0, pose = "idle" },
		{ time = 0.4, pose = "overhead_raise" },
		{ time = 0.58, pose = "overhead_slam" },
		{ time = 1.4, pose = "idle" },
	},
}

local res = AnimKit.validate(spec, rig)       -- 1. always validate first
if not res.ok then return res.text end        --    fix the errors it names, then retry
res = AnimKit.create(spec, rig)               -- 2. build + structure check + save to rig.AnimSaves
return res.text                               --    read WARN / CLAMP lines too
```

To look at a frame, freeze the rig and screenshot it:

```lua
AnimKit.poseAt(rig, spec, 0.58)   -- rig now holds the slam frame (writes Motor6D.Transform)
-- ... mcp__Roblox_Studio__screen_capture pointed at the rig ...
AnimKit.resetPose(rig)            -- always reset afterwards
```

Other calls:

- `AnimKit.preview(rig, specOrSequence, {loop = true, speed = 1})` plays it with an Animator. Edit mode is stepped with `Animator:StepAnimations` on Heartbeat. It returns a handle with `.Stop()`.
- `AnimKit.stop(rig)` stops the preview.
- `AnimKit.build(spec, rig)` returns `sequence, result` without saving.
- `AnimKit.presetNames()`, `AnimKit.jointInfo("R15")` and `AnimKit.Examples.punch` are there for inspection.

The `rig` argument is optional for `validate` and `build`. Without it, the stock R15/R6 layout is used, and saving goes to `ServerStorage.AnimSaves`.

**Saving never overwrites someone else's work.** It replaces only an earlier AnimKit-made sequence with the same name (attribute `AnimKit = true`). Otherwise it saves as `Name_2`, `Name_3` and so on. To publish, load the saved sequence in the Animation Editor (it lists rig.AnimSaves) and use its Publish to Roblox.

## Spec format

```lua
{
  name = "Punch",          -- KeyframeSequence name
  rig = "R15",             -- "R15" | "R6"
  length = 0.7,            -- seconds (0..120)
  fps = 60,                -- keyframe times snap to 1/fps (default 60)
  looped = false,          -- if true and the last keyframe < length, a copy of keyframe 1 is added at `length`
  autoClose = true,        -- set false to skip that closing keyframe
  priority = "Action",     -- Core | Idle | Movement | Action | Action2 | Action3 | Action4
  easing = "CubicV2",      -- default for all keyframes (default CubicV2 InOut)
  presets = { ... },       -- optional custom presets, see below
  keyframes = {
    {
      time = 0.15,                       -- seconds, strictly increasing
      pose = "punch_windup",             -- preset name OR inline pose table
      -- blend = { "a", "b", 0.3 },      -- instead of pose: 30% of the way from a to b
      mirror = true,                     -- swap left/right of the base pose
      joints = { right_elbow = { flex = 100 } }, -- REPLACE only the given fields
      add = { waist = { twist = 5 } },          -- ADD offsets on top
      easing = { "CubicV2", "Out" },     -- style or {style, direction}; controls the motion FROM this keyframe to the next
    },
  },
}
```

- **Missing joints are neutral (rest pose).** Every keyframe contains every joint, so nothing "sticks" from an earlier keyframe.
- **Order of a keyframe:** base (`pose` or `blend`), then `mirror`, then `joints` (replace), then `add`, then clamp.
- **Custom presets** (`spec.presets`) can be a flat pose table, or a keyframe-shaped table such as `{ base = "idle", mirror = true, joints = {...} }`. Keyframes then use them by name, like built-ins.
- **JSON** works the same way: arrays for `blend`, `pos` and `easing`. `AnimKit.validate(jsonString)` decodes it.
- **Easing styles:** Linear, Constant, Cubic, CubicV2, Elastic, Bounce. **Directions:** In, Out, InOut. Prefer `CubicV2` with `InOut`, or `Linear` for fast strikes. Older Roblox `Cubic` In/Out has had direction quirks, so InOut is the safe choice.

### Joint values: anatomical degrees (recommended)

```lua
right_shoulder = { flex = 90, abduct = 10, twist = 0, pos = { 0, 0, 0 } }
```

| Field | Limbs (arms/legs/hands/feet) | Spine: root, waist, neck |
|---|---|---|
| `flex` | shoulder/hip: + swings forward and up. elbow/knee: + bends. wrist: + bends toward the palm side. ankle: + toes up | + bends forward / nods down, - leans back / looks up |
| `abduct` | + away from the body (out to the side) | + tilts toward the character's right |
| `twist` | + rotates outward around the bone | + turns to the character's right |
| `pos` | studs, in the parent part's axes (x right, y up, z back). Small offsets only | `root.pos` moves the whole body: y < 0 crouches |

Aliases: `bend`/`pitch` = flex, `side`/`tilt`/`out` = abduct, `turn`/`yaw` = twist.

Limb values are side-aware, so `mirror` just swaps Left and Right. Raw parent-axis degrees `{x=, y=, z=}` (or `{x, y, z}`) are also accepted and converted (x = flex axis, y = twist axis, z = abduct axis). Avoid them unless you know the rig's axes.

The application order is fixed per joint:

- **Limbs:** twist, then abduct, then flex. So `{flex=90, abduct=30}` means "arm forward, angled 30 degrees outward".
- **Spine:** flex, then tilt, then turn.

### Joints and limits (degrees, values outside are clamped and reported)

| R15 part | Aliases | flex | abduct | twist |
|---|---|---|---|---|
| LowerTorso | root, hips, pelvis | -180..180 | -90..90 | -180..180 (pos up to 4 studs) |
| UpperTorso | waist, spine, chest, torso | -35..75 | -35..35 | -60..60 |
| Head | neck, head | -55..60 | -40..40 | -80..80 |
| Left/RightUpperArm | left_shoulder, l_shoulder, left_arm, left_upper_arm | -70..185 | -30..185 | -95..95 |
| Left/RightLowerArm | left_elbow, left_forearm | -5..150 | -10..10 | -90..90 |
| Left/RightHand | left_wrist, left_hand | -75..80 | -30..30 | -30..30 |
| Left/RightUpperLeg | left_hip, left_thigh, left_leg | -40..125 | -25..75 | -45..45 |
| Left/RightLowerLeg | left_knee, left_shin | -5..150 | -10..10 | -20..20 |
| Left/RightFoot | left_ankle, left_foot | -55..35 | -25..25 | -25..25 |

Short forms like `l_elbow` and `r_knee` work. Names are case- and underscore-insensitive. Unknown names are errors with "did you mean" suggestions.

**R6** has Torso (root), Head, Left/Right Arm (shoulder ranges) and Left/Right Leg (hip ranges). Aliases map across, so `left_shoulder` becomes `Left Arm` and `root` becomes `Torso`. R15-only joints (elbow, knee, wrist, ankle, waist) are ignored on R6 with a warning, which means R15 presets also work on R6. The waist is ignored there, so keep the root for the body lean.

### Presets

| Group | Presets |
|---|---|
| Basic | `neutral`, `tpose`, `idle`, `idle_inhale` |
| Run | `run_contact` (right foot strikes, left arm forward), `run_passing` (right leg under, left knee high). Use `mirror = true` for the other side |
| Fight | `fight_stance`, `punch_windup`, `punch_hit` (all right hand; mirror for left) |
| Jump | `jump_crouch`, `jump_air`, `jump_land` |
| Wave | `wave`, `wave_out`, `wave_in` (right hand; the hand swings via `right_elbow.flex` 70..115) |
| Other | `sit`, `victory`, `overhead_raise`, `overhead_slam` (two-handed weapon) |

## Worked examples

All of these are in `AnimKit.Examples`. They are short on purpose: presets do the heavy lifting, and the keyframes only override what differs.

**1. Idle breathe** (looped; the closing keyframe at 3s is auto-added):

```lua
{ name = "IdleBreathe", rig = "R15", length = 3, looped = true, priority = "Idle",
  keyframes = { { time = 0, pose = "idle" }, { time = 1.5, pose = "idle_inhale" } } }
```

**2. Run cycle** (contact, passing, mirrored contact, mirrored passing):

```lua
{ name = "Run", rig = "R15", length = 0.6, looped = true, priority = "Movement", easing = "Linear",
  keyframes = {
    { time = 0, pose = "run_contact" },
    { time = 0.15, pose = "run_passing" },
    { time = 0.3, pose = "run_contact", mirror = true },
    { time = 0.45, pose = "run_passing", mirror = true },
  } }
```

**3. Punch** (stance, windup, a fast Linear drive, hit, follow-through, recover):

```lua
{ name = "Punch", rig = "R15", length = 0.7, priority = "Action",
  keyframes = {
    { time = 0, pose = "fight_stance" },
    { time = 0.15, pose = "punch_windup", easing = "Linear" },
    { time = 0.23, pose = "punch_hit" },
    { time = 0.32, pose = "punch_hit", joints = { right_shoulder = { flex = 95 } } },
    { time = 0.7, pose = "fight_stance" },
  } }
```

**4. Wave:**

```lua
{ name = "Wave", rig = "R15", length = 2.1, priority = "Action",
  keyframes = {
    { time = 0, pose = "idle" }, { time = 0.35, pose = "wave" },
    { time = 0.6, pose = "wave_out" }, { time = 0.85, pose = "wave_in" },
    { time = 1.1, pose = "wave_out" }, { time = 1.35, pose = "wave_in" },
    { time = 1.6, pose = "wave" }, { time = 2.1, pose = "idle" },
  } }
```

**5. Jump:**

```lua
{ name = "Jump", rig = "R15", length = 1.1, priority = "Action",
  keyframes = {
    { time = 0, pose = "idle" },
    { time = 0.2, pose = "jump_crouch", easing = "Linear" },
    { time = 0.32, pose = "jump_air" },
    { time = 0.62, blend = { "jump_air", "jump_land", 0.4 } },
    { time = 0.75, pose = "jump_land" },
    { time = 1.1, pose = "idle" },
  } }
```

A fully inline pose (no presets), for a left-hand version of the punch hit:

```lua
{ time = 0.23, pose = "punch_hit", mirror = true }
-- or by hand:
{ time = 0.23, pose = {
    root = { twist = -10, pos = { 0, -0.2, -0.15 } }, waist = { twist = 25, flex = 12 },
    left_shoulder = { flex = 90, abduct = 5 }, left_elbow = { flex = 5 },
    right_shoulder = { flex = 40, abduct = 10 }, right_elbow = { flex = 125 } } }
```

## Turning a request into keyframes

Example request: "a heavy overhead sword slam".

1. **Name the beats.** Almost every action has the same four, the classic anticipation, action and follow-through principles of animation:
   - **Anticipation:** move the opposite way first, and do it slowly. Raise the sword high and lean back.
   - **Action:** the fast part. It should be only 2 to 6 frames at 60 fps for a hit.
   - **Follow-through:** overshoot past the target. The body keeps going down and the arms past the hit point.
   - **Settle:** ease back to a rest pose.
2. **Pick or write a pose for each beat.** Here that's `overhead_raise` and `overhead_slam`, with idle at both ends.
3. **Time it.** "Heavy" means a long anticipation and a short action:

   | Feel | Anticipation | Action | Follow-through + settle |
   |---|---|---|---|
   | light / quick (jab) | 0.08 to 0.15 s | 0.05 to 0.08 s | 0.2 to 0.3 s |
   | normal (punch, kick) | 0.15 to 0.25 s | 0.08 to 0.12 s | 0.3 to 0.4 s |
   | heavy (hammer, greatsword) | 0.35 to 0.5 s | 0.08 to 0.15 s | 0.5 to 0.8 s |
   | idle / breathing loops | 1.5 to 2 s per half cycle | n/a | n/a |
   | run cycle (full, 2 steps) | 0.5 to 0.7 s | n/a | n/a |

4. **Add weight with the root and spine, not only the arms.**
   - Drop `root.pos.y` on impact (-0.1 to -0.6).
   - Bend the waist into the strike.
   - Turn the waist the opposite way during windup.
   - Put the head slightly behind the motion.
5. **Hold briefly at the extremes.** Add a "hang" keyframe 0.05 to 0.1 s after the raise, with a tiny `add` offset so it isn't frozen dead.
6. **Easing.**
   - Use `Linear` on the keyframe right before a strike, so the motion into the hit is fast.
   - Use the default `CubicV2 InOut` elsewhere.
   - Use `Constant` only for snap cuts.

The result is `AnimKit.Examples.sword_slam`:

```lua
{ name = "SwordSlam", rig = "R15", length = 1.4, priority = "Action",
  keyframes = {
    { time = 0,    pose = "idle" },
    { time = 0.4,  pose = "overhead_raise" },                                          -- anticipation
    { time = 0.5,  pose = "overhead_raise", add = { waist = { flex = -5 } }, easing = "Linear" }, -- hang
    { time = 0.58, pose = "overhead_slam" },                                          -- action
    { time = 0.66, pose = "overhead_slam", add = { root = { pos = { 0, -0.1, 0 } }, waist = { flex = 5 } } }, -- impact
    { time = 1.05, blend = { "overhead_slam", "idle", 0.5 } },                         -- follow-through
    { time = 1.4,  pose = "idle" },                                                   -- settle
  } }
```

**Agent checklist:**

1. Validate.
2. Read every CLAMP line. A clamp means you asked for something a body can't do, so rethink the pose.
3. Run `poseAt` plus a screenshot at each beat.
4. Reset the pose.
5. Run `create`.

## Known limits

- Poses are forward-kinematics only, so there is no IK: feet can slide or dip during crouches. Tune `root.pos` and the hip/knee/ankle angles together. For flat feet, use ankle flex ≈ knee flex − hip flex + root flex (max 35).
- Limits are generic human ranges, not per-avatar. Rthro and custom rigs with unusual C0 rotations still work, because AnimKit uses each Motor6D's real C0 rotation, but the axes follow the parent part.
- `poseAt` uses TweenService easing as an approximation of Roblox's keyframe interpolation. The saved KeyframeSequence is the source of truth.
- Edit-mode preview depends on `Animator:StepAnimations`, which needs plugin or command-bar security. That covers MCP execute_luau and the plugin.
- Publishing to an asset id is not automated.
- The plugin text box takes JSON only.

## Credits

- Roblox Creator Docs, for the API behaviour this relies on:
  - KeyframeSequenceProvider `RegisterKeyframeSequence`: https://create.roblox.com/docs/reference/engine/classes/KeyframeSequenceProvider
  - Animator `StepAnimations` and its "Preview Animation in Studio" sample, which the Edit-mode preview follows: https://create.roblox.com/docs/reference/engine/classes/Animator
  - Pose, whose "Keyframe Generate Poses" sample walks Motor6Ds from the root (the same idea as `Rig.ordered`): https://create.roblox.com/docs/reference/engine/classes/Pose
  - PoseEasingStyle: https://create.roblox.com/docs/reference/engine/enums/PoseEasingStyle
  - Motor6D: https://create.roblox.com/docs/reference/engine/classes/Motor6D
- Anticipation, follow-through, timing and slow-in/slow-out come from the twelve basic principles of animation (Thomas and Johnston): https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation

No code was copied from other projects.

Made by Nomako20 with Claude.
