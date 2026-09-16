# Blockout — validate the gameplay before anything is pretty

A blockout is placeholder geometry at real scale, in the real scene, with the real collision
and physics the gameplay needs. It answers the questions that a finished asset makes
expensive to change: does the door fit the player, does the throw arc clear the table, can
the camera see the enemy behind the pillar, does the nav mesh reach the balcony, does a
carried chair replicate correctly. Every asset flagged `blockout: true` goes through one;
the registry refuses `PRODUCTION` until it is approved.

## What a blockout validates

- **Scale** — against the scale reference (a 1.4 m or 1.8 m capsule per the Art Bible), and
  the bible's measurements: door, corridor, ceiling, step, counter heights.
- **Collision** — shapes are simple (box, capsule, cylinder, convex) and match the silhouette
  well enough that players are not blocked by air or walk through walls.
- **Navigation** — `NavigationRegion3D` bakes and reaches everywhere enemies must go.
- **Interaction & reach** — every grabbable is reachable from a standing player; every
  interactive surface is at the height the spec says.
- **Visibility & camera** — sightlines, occlusion, first-person clipping into geometry,
  third-person camera collision.
- **Physics** — masses, throw arcs, stacking, what happens at 4 players throwing at once.
- **Multiplayer** — authority for held/thrown objects, what the late joiner sees.

Anything that fails here is fixed by moving a box, not by re-exporting a model.

## Building one — by script, never by hand-written `.tscn`

The scene-file guard in this pack denies structural `.tscn` writes, and for good reason. A
blockout is *generated*: a script constructs the nodes and saves the scene. That also makes it
reproducible and diffable. Two ways:

**`EditorScript`** (`res://tools/blockout_dining_room.gd`, run from the editor with
File → Run, or headless as below):

```gdscript
@tool
extends EditorScript

const PALETTE := {
	"walkable": Color(0.55, 0.55, 0.6),   # floors, stairs
	"blocker":  Color(0.35, 0.35, 0.4),   # walls, ceilings
	"interact": Color(1.0, 0.6, 0.1),     # grabbable / usable
	"hazard":   Color(0.9, 0.2, 0.2),
	"trigger":  Color(0.2, 0.6, 1.0),
	"scale":    Color(0.2, 1.0, 0.3),     # the reference capsule
}

func _run() -> void:
	var root := Node3D.new()
	root.name = "DiningRoomBlockout"
	_box(root, "Floor", Vector3(8, 0.2, 6), Vector3(0, -0.1, 0), "walkable")
	_box(root, "WallN", Vector3(8, 3.2, 0.2), Vector3(0, 1.6, -3.1), "blocker")
	_box(root, "Table", Vector3(2.4, 0.85, 1.0), Vector3(0, 0.425, 0), "blocker")
	_rigid_box(root, "Chair_01", Vector3(0.45, 0.9, 0.45), Vector3(1.6, 0.45, 0.8), 6.0)
	_capsule(root, "REF_SCALE_HUMAN", 1.4, 0.25, Vector3(-3, 0.7, 2))
	var packed := PackedScene.new()
	var err := packed.pack(root)
	assert(err == OK)
	err = ResourceSaver.save(packed, "res://scenes/blockout/dining_room_blockout.tscn")
	assert(err == OK)
	print("saved dining_room_blockout.tscn")

func _material(role: String) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = PALETTE[role]
	return m

func _box(parent: Node3D, name: String, size: Vector3, pos: Vector3, role: String) -> StaticBody3D:
	var body := StaticBody3D.new()
	body.name = name
	body.position = pos
	parent.add_child(body)
	body.owner = parent
	var mesh := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	mesh.mesh = bm
	mesh.material_override = _material(role)
	body.add_child(mesh)
	mesh.owner = parent
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	col.shape = shape
	body.add_child(col)
	col.owner = parent
	return body

func _rigid_box(parent: Node3D, name: String, size: Vector3, pos: Vector3, mass: float) -> RigidBody3D:
	var body := RigidBody3D.new()
	body.name = name
	body.position = pos
	body.mass = mass
	parent.add_child(body)
	body.owner = parent
	var mesh := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	mesh.mesh = bm
	mesh.material_override = _material("interact")
	body.add_child(mesh)
	mesh.owner = parent
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	col.shape = shape
	body.add_child(col)
	col.owner = parent
	return body

func _capsule(parent: Node3D, name: String, height: float, radius: float, pos: Vector3) -> void:
	var mi := MeshInstance3D.new()
	mi.name = name
	mi.position = pos
	var cm := CapsuleMesh.new()
	cm.height = height
	cm.radius = radius
	mi.mesh = cm
	mi.material_override = _material("scale")
	parent.add_child(mi)
	mi.owner = parent
```

`owner` must be set on every node or `pack()` silently drops it. Pivot convention: the body's
`position` is the *centre*, so a 0.9 m tall chair sits at y = 0.45 to rest on the floor —
for the real asset the pivot will be centre-bottom; note the difference in the spec.

**Headless** (no editor open): the same construction in a script that `extends SceneTree`,
run with `godot --headless --path . -s res://tools/blockout_dining_room.gd`, calling `quit()`
at the end. Then, always:

```bash
godot --headless --path . --import && godot --headless --path . --quit ; echo "exit: $?"
```

2D blockouts use `ColorRect`/`Polygon2D` + `CollisionShape2D` on `StaticBody2D`/`RigidBody2D`,
a `TileMapLayer` of solid-colour tiles at the decided tile size, and a player rectangle at the
decided sprite height. The equivalent of the scale capsule is a jump-height and jump-distance
marker so platform spacing is validated before any tile is drawn.

## The colour code

Function, not material: walkable grey, blocker dark grey, interactive orange, hazard red,
trigger volume blue, scale reference green. A tester reads the room's affordances at a glance
and nobody mistakes a blockout for a finished asset in a screenshot. Keep the palette in one
script and reuse it.

## The walk-through with the user

Blockouts are approved by *playing them*, not by looking at a screenshot. Ask the user to
run the scene and check the list; write the answers into the entry:

```markdown
Blockout walk-through — ENV_ROOM_DINING_01
- [ ] Player fits every doorway without crouching; no head clipping under the chandelier
- [ ] Every chair reachable and liftable from standing; thrown chair clears the table
- [ ] Camera at eye height sees the far door from the entrance (the ambush sightline)
- [ ] Nav bake reaches all four corners; the stalker paths around the table
- [ ] Four rigid chairs thrown at once: no tunnelling through walls
- [ ] Second client sees held chairs move; late joiner sees final positions
```

Then `registry.py review ENV_ROOM_DINING_01 approve --note "walked 2026-09-12; door widened to 1.0 m"`
and record any bible measurement that changed. Only now does the room enter PRODUCTION.

## What a blockout is not

Not a concept (it has no look). Not the place for materials beyond the colour code. Not
finished when it "looks about right" — it is finished when the checklist is walked in the
running game. And not something to skip for a "simple" prop the player carries: the chair's
mass and size are gameplay, and gameplay is validated in blockout.
