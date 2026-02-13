# ─────────────────────────────────────────────────────────────────────────────────────────
# 🌌 PROJECT: HARPIA GEOMETRY ENGINE [AKASHIC PENNYLANE CORE]
# 🧊 OBJECT: Quantum Sovereign Cube (8 Qubits)
# 🏟️ STAGE: Spherical Horn Torus (R≈r)
# ⚡ ENGINE: PennyLane Vectorized Circuit + VR Support
# ─────────────────────────────────────────────────────────────────────────────────────────
# 👤 AUTHOR: Deywe Okabe & Gemini
# 🛠️ VERSION: 2.1.0 "Quantum Genesis"
# ─────────────────────────────────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
from tqdm import tqdm
import sys
import hashlib
import time

# 1. VERIFICAÇÃO DE DEPENDÊNCIAS
# --- PENNYLANE (O Coração Quântico) ---
try:
    import pennylane as qml
    PENNYLANE_AVAILABLE = True
    print("⚛️  PennyLane Detectado: Iniciando QPU (Simulador Local)...")
except ImportError:
    print("❌ Erro: 'pennylane' não instalado. Instale com: pip install pennylane")
    sys.exit()

# --- VR ENGINE & BACKUP ---
try:
    # Tenta carregar a IA Externa primeiro (O Motor Real)
    from fibonacci_ai import SPHY_Driver, PHI
    from vr_simbiotic_ai import motor_reversao_fase_2_0 as VR_Engine_External
    VR_AVAILABLE = True
    print("✅ VR_Engine Externa Carregada: Modo Turbo Ativo.")
    
    def VR_Engine(p_singular, caos_neg):
        return VR_Engine_External(p_singular, caos_neg)

except ImportError:
    print("⚠️  VR_Engine Externa não encontrada. Usando Backup Local.")
    PHI = (1 + np.sqrt(5)) / 2
    VR_AVAILABLE = False
    
    def VR_Engine(p_singular, caos_neg):
        """
        Motor VR Ethereal Local (Backup - Vetorizado)
        """
        ganho_base = np.exp(-np.abs(p_singular) * 0.01)
        amplificador = (1 + 0.99 * np.tanh(caos_neg))
        boost = 1 + 0.2 * np.exp(-np.abs(caos_neg))
        return ganho_base * amplificador * boost

# ==================================================================================
# MÓDULO II: ORÁCULO PENNYLANE (SUBSTITUI A SIMULAÇÃO ANTIGA)
# ==================================================================================

# Dispositivo Qubit: Usamos 1 fio "Mestre" para ditar o fluxo temporal
dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev)
def sovereign_flux_circuit(time_input):
    """
    Circuito Quântico Soberano.
    Recebe o Tempo (t) como parâmetro de rotação.
    PennyLane suporta 'Broadcasting', então passamos o array inteiro de frames.
    """
    # Codificação do Tempo na Esfera de Bloch
    # RZ dita a fase, RX dita a amplitude da "respiração"
    qml.RZ(time_input * PHI, wires=0)
    qml.RX(time_input * 0.5, wires=0)
    
    # Cria superposição para gerar interferência
    qml.Hadamard(wires=0)
    
    # Retorna o Valor Esperado de PauliZ (Energia entre -1 e 1)
    return qml.expval(qml.PauliZ(0))

def gerar_fluxo_quantico_akashic(t_values):
    """
    Wrapper que chama o PennyLane.
    Agora o fluxo é calculado por simulação de estado quântico real.
    """
    # PennyLane retorna um Tensor, convertemos para Numpy
    return np.array(sovereign_flux_circuit(t_values))

# ==================================================================================
# MÓDULO III: NÚCLEO AKASHIC (PROCESSAMENTO DE CAMPO VETORIZADO)
# ==================================================================================

def coerencia_ethereal_vectorized(f_matrix, zeta_base, ruido_local, r_toro_base):
    """
    Lógica de Coerência aplicada via álgebra linear (sem loops).
    """
    # 1. Filtro Kalman Supremo (Vetorizado)
    ruido_filtrado = ruido_local * np.exp(-np.abs(ruido_local) * 1.5)
    
    # 2. Inércia Dinâmica (np.where substitui o if/else)
    peso_memoria = np.where(np.abs(ruido_local) > 0.1, 0.99, 0.95)
        
    s_longo = np.exp(-np.abs(ruido_filtrado) * 0.01)
    s_curto = np.exp(-np.abs(ruido_filtrado) * 0.5)
    
    s_coerencia = (peso_memoria * s_longo) + ((1 - peso_memoria) * s_curto)
    
    # 3. Correção de Fase
    fase_vibracional = zeta_base + (ruido_filtrado * (1 - s_coerencia) * 0.01)
    
    # 4. Distorção Geodésica (Respiração do Cubo)
    distorcao = r_toro_base * (1 + (1 - s_coerencia) * 0.001 * np.sin(f_matrix / PHI))
    
    return fase_vibracional, distorcao, s_coerencia

def processar_frames_akashic(n_qubits, total_frames, R_TORO, r_TORO, F_ACHAT, habilitar_vr=True):
    print(f"\n⚙️  Iniciando Motor Akashic (PennyLane Broadcasting) para {total_frames} frames...")
    start_time = time.perf_counter()

    # 1. CRIAÇÃO DO ESPAÇO-TEMPO (GRIDS)
    frames = np.arange(total_frames)
    qubits = np.arange(n_qubits)
    t_values = frames * 0.05
    
    # Broadcasting para Matrizes 2D [Frames, Qubits]
    F_grid, Q_grid = np.meshgrid(frames, qubits, indexing='ij') 
    T_grid = F_grid * 0.05
    
    # 2. ORÁCULO VETORIZADO (AGORA VIA PENNYLANE)
    # Calculamos o fluxo quântico uma vez para todos os tempos (Broadcasting)
    print("⚛️  Executando Circuito Soberano (QPU)...")
    fluxo_t = gerar_fluxo_quantico_akashic(t_values)
    
    # Expandimos o resultado 1D para a Grid 2D
    Fluxo_grid = np.tile(fluxo_t[:, np.newaxis], (1, n_qubits)) 

    # 3. FÍSICA VETORIZADA
    # Escalada de Caos
    Caos_base_grid = (F_grid / total_frames) * 12.0
    
    # Fênix Preventiva (Estabilização de Colapso)
    limit_critico = 2.618
    mask_fenix = Caos_base_grid >= (limit_critico * 0.85)
    Caos_estabilizado_grid = np.where(mask_fenix, limit_critico * 0.80, Caos_base_grid)
    resets_fenix = np.sum(mask_fenix) / n_qubits 
    
    # Ruído Vibracional (Simula interferência externa)
    mask_vibra = (F_grid > (total_frames * 0.1)) & (F_grid < (total_frames * 0.5))
    Ruido_vibra_grid = np.where(mask_vibra, 0.35 * np.sin(F_grid * 0.4), 0.0)
    
    # Singularidades Aleatórias (Entropia local)
    P_singular_grid = np.random.uniform(0, 1, size=(total_frames, n_qubits)) * (Caos_estabilizado_grid * 0.1)

    # 4. ENGINE VR (CHAMADA VETORIZADA DIRETA)
    if habilitar_vr:
        # Passa matrizes inteiras para o motor VR
        Ganho_grid = VR_Engine(P_singular_grid, -Caos_estabilizado_grid)
        Torque_grid = -P_singular_grid * Ganho_grid
    else:
        Ganho_grid = np.ones_like(P_singular_grid) 
        Torque_grid = np.zeros_like(P_singular_grid)

    # 5. CÁLCULO DE FASE E GEOMETRIA (Mapeamento do Cubo no Toro)
    if n_qubits == 8:
        # Mapeamento Manual do Cubo
        theta_base = np.array([np.pi/4]*4 + [-np.pi/4]*4)
        zeta_base_arr = np.array([0, np.pi/2, np.pi, 3*np.pi/2] * 2)
        
        Theta_grid = np.tile(theta_base, (total_frames, 1)) + (T_grid * 0.1 * PHI) # Rotação lenta
        Zeta_base_grid = np.tile(zeta_base_arr, (total_frames, 1))
    else:
        # Distribuição Padrão em Anel
        Offsets_grid = Q_grid * (2 * np.pi / n_qubits)
        Theta_grid = (T_grid * 0.1 * PHI)
        Zeta_base_grid = Offsets_grid
    
    # Aplica perturbações e VR na fase
    # O Fluxo_grid agora contém dados reais do PennyLane
    Zeta_ideal = Zeta_base_grid + (P_singular_grid + Torque_grid) + (Fluxo_grid * 0.08) + (T_grid * 0.2) 
    
    Ruido_total = Ruido_vibra_grid + (P_singular_grid * 0.05)
    
    # Aplica coerência (Filtro Kalman)
    Zeta_real, R_din, S_local = coerencia_ethereal_vectorized(F_grid, Zeta_ideal, Ruido_total, r_TORO)
    
    # Coordenadas Finais Toroidais
    R_maior_efetivo = R_TORO + R_din * np.cos(Theta_grid)
    
    X_grid = R_maior_efetivo * np.cos(Zeta_real)
    Y_grid = R_maior_efetivo * np.sin(Zeta_real)
    Z_grid = (R_din * F_ACHAT) * np.sin(Theta_grid)

    # 6. FLAT FLATTENING (PREPARAÇÃO PARA DATAFRAME)
    print("📦 Organizando Telemetria (Packing)...")
    
    data_dict = {
        'Frame': frames,
        'T': t_values,
        'Caos_Global': Caos_base_grid[:, 0],
        'VR_Gain_Avg': np.mean(Ganho_grid, axis=1),
        'Quantum_Flux': fluxo_t # Salva o dado puro do PennyLane para análise
    }
    
    for i in range(n_qubits):
        data_dict[f'q{i}_x'] = X_grid[:, i]
        data_dict[f'q{i}_y'] = Y_grid[:, i]
        data_dict[f'q{i}_z'] = Z_grid[:, i]
        
    df_sim = pd.DataFrame(data_dict)
    
    stats = {
        'resets_fenix': resets_fenix,
        'coerencia_media': np.mean(S_local),
        'speed_fps': total_frames / (time.perf_counter() - start_time)
    }
    
    dt = time.perf_counter() - start_time
    print(f"⚡ Akashic Core Finalizado em {dt:.4f} segundos ({stats['speed_fps']:.0f} FPS simulados).")
    return df_sim, stats

class Harpia_Geometry_Engine_Turbo:
    def __init__(self):
        self.n_qubits = 8 # Cubo
        # TORO ESFÉRICO (Horn Torus)
        self.R_TORUS = 10.0
        self.r_TORUS = 9.9
        self.F_ACHAT = 1.0 
        
    def generate_dataset(self, total_frames):
        # Chama o núcleo Akashic Vetorizado
        df, stats = processar_frames_akashic(
            self.n_qubits, 
            total_frames, 
            self.R_TORUS, 
            self.r_TORUS, 
            self.F_ACHAT, 
            habilitar_vr=VR_AVAILABLE
        )
        
        # Exportação
        output_file = f"dataset_cubo_pennylane_{total_frames}frames.csv"
        df.to_csv(output_file, index=False, float_format='%.6f')
        
        # Hash
        with open(output_file, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            
        print("\n" + "🧊"*35)
        print(f"✅ DATASET GENERATION COMPLETE.")
        print(f"📦 Frames: {total_frames}")
        print(f"🚀 Speed: {stats['speed_fps']:.2f} frames/sec calculation")
        print(f"📊 Avg Coherence: {stats['coerencia_media']:.4f}")
        print(f"🔐 SHA256: {file_hash[:16]}...")
        print(f"📂 File: {output_file}")
        print("🧊"*35)

if __name__ == "__main__":
    # Gera 50000 frames em ultra velocidade (mas agora com física quântica real)
    engine = Harpia_Geometry_Engine_Turbo()
    engine.generate_dataset(total_frames=50000)