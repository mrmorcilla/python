from ursina import *
import random
from ursina.lights import DirectionalLight
from ursina.shaders import lit_with_shadows_shader

'''
autor:

andrés

version:

0.1.1

nota de cambio:

- Los atomos ahora usan archivos .glb con su propio modelo 3D.
- Se usa el shader lit_with_shadows_shader para los modelos.

'''

app = Ursina()

combinations = {
    ('H', 'O'): {'type': 'H2O', 'scale': 0.7},
    ('H', 'H'): {'type': 'H2', 'scale': 0.6},
    ('O', 'O'): {'type': 'O2', 'scale': 0.8},
}

atoms = []
space = 5
bounds = (-space, space, -space, space, -space, space)

# conf luz
light = DirectionalLight()
light.look_at(Vec3(1, -1, -1))

def spawn_atom(atom_type, scale):
    model_file = f'{atom_type}.glb'
    
    try:
        atom = Entity(
            model=model_file,
            scale=scale,
            position=(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2)),
            collider='sphere',  # coll esferico
            type=atom_type,
            velocity=Vec3(random.uniform(-0.02, 0.02), random.uniform(-0.02, 0.02), random.uniform(-0.02, 0.02)),
            energy=1.0,
            shader=lit_with_shadows_shader  # shader
        )
        atoms.append(atom)
    except Exception as e:
        print(f"Error al cargar el modelo {model_file}: {e}")

def input(key):
    if key == '1':
        spawn_atom('H', 0.5)
    elif key == '2':
        spawn_atom('O', 0.5)
    elif key == '3':
        spawn_atom('He', 0.5)
    elif key == '4':
        spawn_atom('C', 0.5)

def update():
    for atom in atoms:
        atom.x += atom.velocity.x
        atom.y += atom.velocity.y
        atom.z += atom.velocity.z

        # rbt limite
        if atom.x < bounds[0] or atom.x > bounds[1]:
            atom.velocity.x *= -1
        if atom.y < bounds[2] or atom.y > bounds[3]:
            atom.velocity.y *= -1
        if atom.z < bounds[4] or atom.z > bounds[5]:
            atom.velocity.z *= -1

        for other in atoms:
            if atom != other and atom.intersects(other).hit:
                pair = tuple(sorted([atom.type, other.type]))
                if pair in combinations:
                    new_data = combinations[pair]
                    new_atom = Entity(
                        model='sphere',
                        scale=new_data['scale'],
                        position=atom.position,
                        type=new_data['type'],
                        velocity=(atom.velocity + other.velocity) / 2,
                        shader=lit_with_shadows_shader
                    )
                    atoms.append(new_atom)
                    destroy(atom)
                    destroy(other)
                    atoms.remove(atom)
                    atoms.remove(other)
                    print(f"¡Se formó {new_data['type']}!")
                else:
                    # rbt
                    normal = (atom.position - other.position).normalized()
                    atom.velocity = normal * atom.velocity.length()
                    other.velocity = -normal * other.velocity.length()

camera = EditorCamera()
app.run()
