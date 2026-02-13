# ─────────────────────────────────────────────────────────────────────────────
# 🌌 HARPIA VISUALIZER v3.4 [PYRAMID EDITION]
# 👁️ VIEW: Quantum Sovereign Pyramid (Tetrahedron)
# ─────────────────────────────────────────────────────────────────────────────
from ursina import *
from ursina.prefabs.trail_renderer import TrailRenderer
import pandas as pd
import numpy as np
import sys

# 1. CONFIGURAÇÃO DA JANELA
app = Ursina(title='Harpia Quantum Pyramid', vsync=True, show_fps=True)
window.color = color.black # Vácuo
window.size = (1536, 864)
window.borderless = False

# 2. CARREGAMENTO DE DADOS
# Certifique-se que este é o nome do arquivo gerado pelo script da pirâmide
csv_file = 'dataset_piramide_pennylane_50000frames.csv' 
print(f"⚡ Lendo Telemetria da Pirâmide: {csv_file}...")

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"❌ Erro: Arquivo {csv_file} não encontrado.")
    sys.exit()

total_frames = df['Frame'].max() + 1
# MUDANÇA CRUCIAL: 4 Qubits para a Pirâmide
n_qubits = 4 
print(f"✅ Matrix Carregada: {total_frames} Frames. Qubits: {n_qubits}")

# Conversão para Matriz Numpy
data_matrix = np.zeros((total_frames, n_qubits, 3))
for q in range(n_qubits):
    data_matrix[:, q, 0] = df[f'q{q}_x'].values
    data_matrix[:, q, 1] = df[f'q{q}_y'].values
    data_matrix[:, q, 2] = df[f'q{q}_z'].values

# 3. CENÁRIO
print("🏟️  Gerando Palco...")
equator = Entity(model=Circle(radius=15, thickness=0.05), color=color.cyan, rotation_x=90)
equator.alpha = 0.15
equator.unlit = True

# 4. ATORES: QUBITS
qubit_spheres = []
# Qubit 0 é o topo (Amarelo/Ouro), os outros são a base (Azul/Ciano)
qubit_colors = [color.gold, color.cyan, color.cyan, color.cyan] 

for i in range(n_qubits):
    sphere = Entity(
        model='sphere', 
        color=qubit_colors[i], 
        scale=0.6, 
        texture='white_cube',
        unlit=True
    )
    try:
        sphere.add_script(TrailRenderer(thickness=2, color=qubit_colors[i], length=8, alpha=0.6))
    except: pass
    qubit_spheres.append(sphere)

# As linhas de conexão (Arestas da Pirâmide)
line_entity = Entity(model=Mesh(mode='line', thickness=3, static=False), color=color.white)
line_entity.unlit = True

# 5. LOOP DE ANIMAÇÃO
current_frame = 0
camera_angle = 0

# HUD
Text(text='QUANTUM SOVEREIGN PYRAMID', position=(-0.85, 0.45), scale=1.2, color=color.gold)
status_bar = Text(text='GEOMETRY: STABLE', position=(-0.85, 0.40), scale=0.9, color=color.lime)

def update():
    global current_frame, camera_angle
    
    if held_keys['escape']: quit()
    
    # Avança Frame
    spd = 3 if held_keys['shift'] else 1
    current_frame = (current_frame + spd) % total_frames
    idx = int(current_frame)
    
    positions = data_matrix[idx]
    verts_for_lines = []
    
    # Atualiza Qubits
    for i in range(n_qubits):
        # Mapeamento: X->X, Y->Z, Z->Y (Ursina Y-UP)
        target = Vec3(positions[i][0], positions[i][2], positions[i][1])
        
        qubit_spheres[i].position = target
        
        # Respiração
        dist = target.length()
        qubit_spheres[i].scale = 0.6 + (dist * 0.005)
        
        verts_for_lines.append(target)

    # --- GEOMETRIA DA PIRÂMIDE (TETRAEDRO) ---
    # Qubit 0 = Topo
    # Qubit 1, 2, 3 = Base
    line_verts = []
    if n_qubits == 4:
        connections = [
            # Base (Triângulo)
            (1, 2), (2, 3), (3, 1),
            # Arestas Verticais (Conectando topo à base)
            (0, 1), (0, 2), (0, 3)
        ]
        
        for p1, p2 in connections:
            line_verts.append(verts_for_lines[p1])
            line_verts.append(verts_for_lines[p2])

    line_entity.model.vertices = line_verts
    line_entity.model.generate()

    # Rotação da Câmera
    camera_angle += 15 * time.dt 
    radius = 25
    height = 5 + np.sin(time.time() * 0.5) * 5 
    
    camera.position = (np.sin(np.radians(camera_angle)) * radius, 
                       height, 
                       np.cos(np.radians(camera_angle)) * radius)
    camera.look_at((0,0,0))
    
    # HUD Update
    try:
        vr_gain = df["VR_Gain_Avg"][idx]
        status_bar.text = f'FRAME: {idx} | SYNC: {vr_gain:.4f}'
    except: pass

print("🚀 Launching PYRAMID VISUALIZER...")
app.run()