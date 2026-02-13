# ─────────────────────────────────────────────────────────────────────────────
# 🌌 HARPIA VISUALIZER v3.3 [CUBE FOCUS EDITION]
# 👁️ VIEW: Pure rotating Quantum Cube (12 Edges Only)
# ─────────────────────────────────────────────────────────────────────────────
from ursina import *
from ursina.prefabs.trail_renderer import TrailRenderer
import pandas as pd
import numpy as np
import sys

# 1. CONFIGURAÇÃO DA JANELA
app = Ursina(title='Harpia Quantum Cube', vsync=True, show_fps=True)
window.color = color.black # Vácuo absoluto
window.size = (1536, 864)
window.borderless = False

# 2. CARREGAMENTO DE DADOS
csv_file = 'dataset_cubo_turbo_5000frames.csv'
print(f"⚡ Lendo Telemetria do Cubo: {csv_file}...")

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"❌ Erro: Arquivo {csv_file} não encontrado.")
    sys.exit()

total_frames = df['Frame'].max() + 1
n_qubits = 8 # Essencial ser 8 para um cubo
print(f"✅ Matrix Carregada: {total_frames} Frames.")

# Conversão para Matriz Numpy
data_matrix = np.zeros((total_frames, n_qubits, 3))
for q in range(n_qubits):
    data_matrix[:, q, 0] = df[f'q{q}_x'].values
    data_matrix[:, q, 1] = df[f'q{q}_y'].values
    data_matrix[:, q, 2] = df[f'q{q}_z'].values

# 3. CENÁRIO (Campo Toroidal Minimalista)
print("🏟️  Gerando Palco...")
# Apenas o equador para referência de rotação
equator = Entity(model=Circle(radius=18, thickness=0.05), color=color.cyan, rotation_x=90)
equator.alpha = 0.15
equator.unlit = True

# 4. ATORES: QUBITS (Vértices)
qubit_spheres = []
# Cores alternadas para Base e Topo do cubo
qubit_colors = [color.cyan]*4 + [color.magenta]*4 

for i in range(n_qubits):
    sphere = Entity(
        model='sphere', 
        color=qubit_colors[i], 
        scale=0.5, # Um pouco menores para destacar as linhas
        texture='white_cube',
        unlit=True
    )
    # Rastros mais curtos para não poluir a forma do cubo
    try:
        sphere.add_script(TrailRenderer(thickness=2, color=qubit_colors[i], length=5, alpha=0.6))
    except:
        pass
    qubit_spheres.append(sphere)

# As linhas de conexão (Arestas do Cubo)
# Cor branca pura, brilhante
line_entity = Entity(model=Mesh(mode='line', thickness=3, static=False), color=color.white)
line_entity.unlit = True

# 5. LOOP DE ANIMAÇÃO
current_frame = 0
camera_angle = 0

# HUD Limpo
Text(text='QUANTUM SOVEREIGN CUBE', position=(-0.85, 0.45), scale=1.2, color=color.cyan)
status_bar = Text(text='GEOMETRY: STABLE', position=(-0.85, 0.40), scale=0.9, color=color.lime)

def update():
    global current_frame, camera_angle
    
    if held_keys['escape']: quit()
    
    # Avança Frame (Shift acelera)
    spd = 3 if held_keys['shift'] else 1
    current_frame = (current_frame + spd) % total_frames
    idx = int(current_frame)
    
    positions = data_matrix[idx]
    verts_for_lines = []
    
    # Atualiza Qubits
    for i in range(n_qubits):
        # Mapeamento: CSV(X,Z,Y) -> Ursina(X,Y,Z)
        # IMPORTANTE: Trocamos Y e Z aqui para o cubo ficar "em pé" corretamente na Ursina
        target = Vec3(positions[i][0], positions[i][2], positions[i][1])
        
        qubit_spheres[i].position = target
        
        # Pulsação sutil baseada na distância do centro (respiração)
        dist = target.length()
        qubit_spheres[i].scale = 0.5 + (dist * 0.005)
        
        verts_for_lines.append(target)

    # --- AQUI ESTÁ A MÁGICA DO CUBO PURO ---
    # Definimos EXATAMENTE as 12 arestas de um cubo.
    # Assumindo que 0-3 é a base e 4-7 é o topo.
    line_verts = []
    if n_qubits == 8:
        connections = [
            # Base (Anel inferior)
            (0,1), (1,2), (2,3), (3,0),
            # Topo (Anel superior)
            (4,5), (5,6), (6,7), (7,4),
            # Pilares (Conectando base ao topo)
            (0,4), (1,5), (2,6), (3,7)
        ]
        
        for p1, p2 in connections:
            line_verts.append(verts_for_lines[p1])
            line_verts.append(verts_for_lines[p2])

    line_entity.model.vertices = line_verts
    line_entity.model.generate()

    # Rotação da Câmera (Mais rápida para enfatizar o giro)
    camera_angle += 20 * time.dt 
    radius = 30
    # Câmera oscila suavemente para cima e para baixo para dar noção 3D
    height = 5 + np.sin(time.time() * 0.5) * 10 
    
    camera.position = (np.sin(np.radians(camera_angle)) * radius, 
                       height, 
                       np.cos(np.radians(camera_angle)) * radius)
    camera.look_at((0,0,0))
    
    # HUD Update
    try:
        vr_gain = df["VR_Gain_Avg"][idx]
        status_bar.text = f'FRAME: {idx} | SYNC: {vr_gain:.4f}'
    except:
        pass

print("🚀 Launching CUBE VISUALIZER...")
app.run()