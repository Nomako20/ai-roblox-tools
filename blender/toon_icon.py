"""Toon icon kit for Blender (4.x / 5.x, EEVEE). Run inside Blender (Text editor, or an MCP execute call).

The look big Roblox games use for shop icons: simple chunky model, 3 HARD tones (no soft realistic shading),
a thick black outline (inverted hull), one key light, orthographic 3/4 camera, transparent background.

    exec(open(r'.../blender/toon_icon.py').read())
    setup_scene()
    root = new_icon('cash')
    finish(box('bill', 2.0, 1.1, .55, root), [toon('green', '#5FE36A', '#2DB84A', '#15803A')])
    finish(box('band', .42, 1.16, .6, root), [toon('yellow', '#FFE24A', '#FFB800', '#D07A00')], outline=.05).location = (.35, 0, 0)
    root.rotation_euler = (math.radians(24), 0, math.radians(-22))   # +X tilts the top toward the camera
    render_icon(root, r'C:/out/cash.png')

Rules that made it work (and what failed):
- Hard ramp (CONSTANT) with 4 stops: dark .00, mid .15, light .36, spec .90. Soft shading = looks AI.
- Outline = Solidify, negative thickness, flipped normals, material_offset -> black emission, backface culling ON.
- Show the TOP of flat things (cash, coins): tilt them toward the camera, otherwise they read as a side view.
- Piles of many items -> render one, pile copies in 2D (kit/flat.py img_pile). Single hero icons -> 2.5D SVG
  (kit/flat.py cash_icon / gem_icon) often look cleaner than a 3D render.
"""
import bpy, bmesh, math, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

def lin(h):
    h = h.lstrip('#'); return [(int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)] + [1]

def setup_scene(res=512):
    sc = bpy.context.scene
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'
    cam = sc.camera
    if cam is None:
        cam = bpy.data.objects.new('IconCam', bpy.data.cameras.new('IconCam')); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'
    dirv = Vector((1.0, -1.25, .85)).normalized()
    cam.location = dirv * 60; cam.rotation_euler = (-dirv).to_track_quat('-Z', 'Y').to_euler()
    if 'IconKey' not in bpy.data.objects:
        l = bpy.data.objects.new('IconKey', bpy.data.lights.new('IconKey', 'SUN')); sc.collection.objects.link(l)
        l.data.energy = 3.2; l.rotation_euler = (math.radians(40), 0, math.radians(-35))
    w = sc.world or bpy.data.worlds.new('IconWorld'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.0
    col = bpy.data.collections.get('Icons') or bpy.data.collections.new('Icons')
    if col.name not in sc.collection.children: sc.collection.children.link(col)
    return col

def toon(name, hi, mid, lo, spec='#FFFFFF'):
    m = bpy.data.materials.get('T_' + name) or bpy.data.materials.new('T_' + name)
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); s2r = nt.nodes.new('ShaderNodeShaderToRGB')
    ramp = nt.nodes.new('ShaderNodeValToRGB'); emit = nt.nodes.new('ShaderNodeEmission'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
    cr.elements[0].position = 0; cr.elements[0].color = lin(lo)
    cr.elements[1].position = .15; cr.elements[1].color = lin(mid)
    cr.elements.new(.36).color = lin(hi); cr.elements.new(.90).color = lin(spec)
    nt.links.new(dif.outputs[0], s2r.inputs[0]); nt.links.new(s2r.outputs['Color'], ramp.inputs[0])
    nt.links.new(ramp.outputs['Color'], emit.inputs[0]); nt.links.new(emit.outputs[0], out.inputs[0])
    return m

def outline_mat():
    m = bpy.data.materials.get('ToonOutline')
    if m: return m
    m = bpy.data.materials.new('ToonOutline'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (0, 0, 0, 1)
    nt.links.new(e.outputs[0], nt.nodes.new('ShaderNodeOutputMaterial').inputs[0])
    m.use_backface_culling = True
    return m

def new_icon(name):
    col = setup_scene()
    old = bpy.data.objects.get('ICON_' + name)
    if old:
        for c in list(old.children_recursive): bpy.data.objects.remove(c, do_unlink=True)
        bpy.data.objects.remove(old, do_unlink=True)
    r = bpy.data.objects.new('ICON_' + name, None); col.objects.link(r); return r

def _obj(name, bm, parent):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.data.collections['Icons'].objects.link(o); o.parent = parent; return o

def box(name, sx, sy, sz, parent):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1); bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts); return _obj(name, bm, parent)

def cylinder(name, r1, r2, h, parent, seg=32):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=h); return _obj(name, bm, parent)

def sphere(name, r, parent):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=r); return _obj(name, bm, parent)

def extrude(name, pts_xz, depth, parent):
    """closed outline in the XZ plane -> solid of given depth along Y (front faces the camera)"""
    bm = bmesh.new(); f = bm.faces.new([bm.verts.new((x, 0, z)) for x, z in pts_xz])
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)], vec=(0, depth, 0))
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, -depth / 2, 0)); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(name, bm, parent)

def finish(o, mats, outline=.07, bevel=.05, smooth=True):
    me = o.data
    for m in mats: me.materials.append(m)
    me.materials.append(outline_mat())
    for p in me.polygons: p.use_smooth = smooth
    if bevel:
        b = o.modifiers.new('Bevel', 'BEVEL'); b.width = bevel; b.segments = 2; b.limit_method = 'ANGLE'
    if outline:
        s = o.modifiers.new('Outline', 'SOLIDIFY'); s.thickness = -outline; s.use_flip_normals = True
        s.offset = 1; s.material_offset = len(me.materials) - 1; s.use_rim = False
    return o

def render_icon(root, path, pad=1.14):
    """frame the icon tightly (camera-space bounds), hide every other mesh, render a transparent PNG"""
    sc = bpy.context.scene; cam = sc.camera
    for o in bpy.data.objects:
        if o.type == 'MESH': o.hide_render = True
    for c in root.children_recursive: c.hide_render = False
    cam.data.ortho_scale = 6; root.location = (0, 0, 0); bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in root.children_recursive if o.type == 'MESH' for c in o.bound_box]
    vs = [world_to_camera_view(sc, cam, p) for p in pts]
    cx = (min(v.x for v in vs) + max(v.x for v in vs)) / 2 - .5; cy = (min(v.y for v in vs) + max(v.y for v in vs)) / 2 - .5
    span = max(max(v.x for v in vs) - min(v.x for v in vs), max(v.y for v in vs) - min(v.y for v in vs))
    S = cam.data.ortho_scale; R3 = cam.matrix_world.to_3x3()
    root.location = -(R3 @ Vector((1, 0, 0)) * cx * S + R3 @ Vector((0, 1, 0)) * cy * S); cam.data.ortho_scale = S * span * pad
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
    return path
