# Dump a scene's tree for an integration review: node types, scripts, collision shapes and
# sizes, body masses, mesh surfaces and material types, particle counts, animation lists,
# synchronizers, and each mesh's AABB.
#
#   godot --headless --path <project> -s <path-to>/inspect_scene.gd ++ res://scenes/props/chair.tscn
#
# Godot 4.x. STATUS: written against the 4.3 API and not yet executed against an engine in
# this repository — if your version rejects the absolute script path, copy this file into
# res://tools/ and pass that path to -s. Report what it actually printed.
extends SceneTree


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.is_empty():
		push_error("usage: -s inspect_scene.gd ++ res://path/to/scene.tscn")
		quit(2)
		return
	var path: String = args[0]
	var packed := load(path) as PackedScene
	if packed == null:
		push_error("could not load %s" % path)
		quit(1)
		return
	var root := packed.instantiate()
	print("== %s ==" % path)
	_dump(root, 0)
	root.free()
	quit(0)


func _dump(n: Node, depth: int) -> void:
	var line := "%s%s : %s" % ["  ".repeat(depth), n.name, n.get_class()]
	var scr := n.get_script()
	if scr != null and scr is Script:
		line += "  script=%s" % (scr as Script).resource_path
	line += _details(n)
	print(line)
	for c in n.get_children():
		_dump(c, depth + 1)


func _details(n: Node) -> String:
	var d := ""
	if n is CollisionShape3D:
		var s := (n as CollisionShape3D).shape
		d += "  shape=%s" % (s.get_class() if s else "NONE")
		if s is BoxShape3D:
			d += " size=%s" % (s as BoxShape3D).size
		elif s is CapsuleShape3D:
			d += " r=%.3f h=%.3f" % [(s as CapsuleShape3D).radius, (s as CapsuleShape3D).height]
		elif s is SphereShape3D:
			d += " r=%.3f" % (s as SphereShape3D).radius
		elif s is ConvexPolygonShape3D:
			d += " points=%d" % (s as ConvexPolygonShape3D).points.size()
		elif s is ConcavePolygonShape3D:
			d += " TRIMESH faces=%d" % ((s as ConcavePolygonShape3D).get_faces().size() / 3)
	if n is CollisionShape2D:
		var s2 := (n as CollisionShape2D).shape
		d += "  shape=%s" % (s2.get_class() if s2 else "NONE")
	if n is RigidBody3D:
		d += "  mass=%.2f" % (n as RigidBody3D).mass
	if n is RigidBody2D:
		d += "  mass=%.2f" % (n as RigidBody2D).mass
	if n is MeshInstance3D:
		var mi := n as MeshInstance3D
		if mi.mesh:
			d += "  mesh=%s surfaces=%d aabb=%s" % [mi.mesh.get_class(), mi.mesh.get_surface_count(), mi.get_aabb()]
			for i in mi.mesh.get_surface_count():
				var m := mi.get_active_material(i)
				d += " mat%d=%s" % [i, (m.get_class() + ("[" + m.resource_path.get_file() + "]" if m.resource_path != "" else "[embedded]")) if m else "none"]
		else:
			d += "  mesh=NONE"
	if n is GPUParticles3D:
		var p := n as GPUParticles3D
		d += "  amount=%d lifetime=%.2f one_shot=%s" % [p.amount, p.lifetime, p.one_shot]
	if n is GPUParticles2D:
		var p2 := n as GPUParticles2D
		d += "  amount=%d lifetime=%.2f one_shot=%s" % [p2.amount, p2.lifetime, p2.one_shot]
	if n is AnimationPlayer:
		d += "  animations=%s" % [(n as AnimationPlayer).get_animation_list()]
	if n is AnimationTree:
		d += "  tree_root=%s" % ((n as AnimationTree).tree_root.get_class() if (n as AnimationTree).tree_root else "NONE")
	if n is Skeleton3D:
		d += "  bones=%d" % (n as Skeleton3D).get_bone_count()
	if n is MultiplayerSynchronizer:
		var cfg := (n as MultiplayerSynchronizer).replication_config
		d += "  replicated=%d props" % (cfg.get_properties().size() if cfg else 0)
	if n is NavigationAgent3D:
		d += "  radius=%.2f height=%.2f" % [(n as NavigationAgent3D).radius, (n as NavigationAgent3D).height]
	if n is Node3D:
		var n3 := n as Node3D
		if not n3.scale.is_equal_approx(Vector3.ONE):
			d += "  SCALE=%s" % n3.scale
	return d
