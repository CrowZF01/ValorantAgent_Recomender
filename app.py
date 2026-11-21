import json
import base64
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# KONFIGURASI HALAMAN (TRACKER.GG VALORANT ESPORTS THEME)
# ==============================================================================
st.set_page_config(
    page_title="Valorant Tracker | Draft AI Recommender",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Authentic Tracker.gg Valorant UI
st.markdown("""
<style>
    /* Sembunyikan sidebar dan kontrolnya */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Beri jarak atas agar konten tidak tertabrak header bawaan Streamlit */
    .block-container {
        max-width: 1400px;
        padding-top: 3.5rem !important;
        padding-bottom: 1.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Tracker.gg Hero Header */
    .tracker-hero {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(180deg, #121824 0%, #0E131C 100%);
        border: 1px solid #1E2738;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 12px;
    }
    .hero-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .hero-title {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 1.5px;
        color: #FFFFFF;
        margin: 0;
        line-height: 1;
        text-transform: uppercase;
    }
    .hero-title .highlight-red {
        color: #FF4655;
    }
    .hero-subtitle {
        font-size: 12px;
        color: #8B97A8;
        margin-top: 4px;
        letter-spacing: 0.4px;
    }
    .hero-roles {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    .role-pill-trn {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #CBD5E1;
        background: #161D2B;
        border: 1px solid #232D3F;
        padding: 4px 10px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .dot-duelist { width: 7px; height: 7px; border-radius: 50%; background: #FF4655; display: inline-block; }
    .dot-initiator { width: 7px; height: 7px; border-radius: 50%; background: #00B4D8; display: inline-block; }
    .dot-controller { width: 7px; height: 7px; border-radius: 50%; background: #8B5CF6; display: inline-block; }
    .dot-sentinel { width: 7px; height: 7px; border-radius: 50%; background: #2EC4B6; display: inline-block; }

    /* 3. Navigation Tabs Tracker.gg */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid #1E2738;
        margin-bottom: 12px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #8B97A8;
        padding: 8px 18px;
        border-radius: 4px 4px 0 0;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom: 2px solid #FF4655 !important;
        background: rgba(255, 70, 85, 0.06) !important;
    }

    /* 4. Card Containers & Headers */
    .tracker-card-header {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #8B97A8;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* 5. 5-Slot Team Roster Cards */
    .tracker-slot {
        background: #141A25;
        border: 1px solid #232C3C;
        border-radius: 6px;
        padding: 8px 4px;
        text-align: center;
        min-height: 108px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .tracker-slot:hover {
        border-color: #38465C;
    }
    .tracker-slot-empty {
        background: #0D121A;
        border: 1px dashed #2C384B;
    }
    .tracker-slot-avatar {
        border-radius: 50%;
        margin-bottom: 4px;
        border: 1.5px solid #2D3748;
    }
    .tracker-slot-name {
        font-size: 12px;
        font-weight: 800;
        color: #FFFFFF;
    }
    .tracker-role-pill {
        font-size: 8px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        padding: 1px 6px;
        border-radius: 3px;
        color: #FFFFFF;
        margin-top: 3px;
        display: inline-block;
    }
    
    /* Team Composition Status Row */
    .comp-bar {
        display: flex;
        justify-content: space-between;
        background: #0E131C;
        border: 1px solid #1C2432;
        border-radius: 4px;
        padding: 8px 14px;
        margin-top: 10px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* 6. Tracker.gg Leaderboard Row */
    .tracker-rec-row {
        background: #141A25;
        border: 1px solid #1E2737;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: background 0.15s ease, border-color 0.15s ease;
    }
    .tracker-rec-row:hover {
        background: #18202D;
        border-color: #38465C;
    }
    .rec-rank-badge {
        font-size: 13px;
        font-weight: 900;
        min-width: 24px;
    }
    .rec-rank-1 { color: #EAB308; } /* Gold #1 */
    .rec-rank-2 { color: #00B4D8; } /* Silver / Cyan */
    .rec-rank-3 { color: #8B5CF6; } /* Purple */
    .rec-rank-4 { color: #64748B; }
    .rec-rank-5 { color: #64748B; }
    .rec-rank-6 { color: #64748B; }
    
    .rec-agent-meta {
        display: flex;
        align-items: center;
        gap: 10px;
        flex: 1;
    }
    .rec-stats-box {
        text-align: right;
        min-width: 120px;
        padding-right: 10px;
    }
    .rec-prob-val {
        font-size: 15px;
        font-weight: 900;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .rec-prob-bar-bg {
        background: #202938;
        border-radius: 2px;
        height: 3px;
        width: 100%;
        margin-top: 3px;
        overflow: hidden;
    }
    .rec-prob-bar-fill {
        background: #FF4655;
        height: 100%;
    }
    .rec-wr-text {
        font-size: 10px;
        font-weight: 700;
        margin-top: 2px;
    }
    .wr-positive { color: #10B981; }
    .wr-average { color: #F59E0B; }
    
    /* 7. Tracker.gg Button */
    .stButton > button {
        background-color: #1A2332 !important;
        color: #CBD5E1 !important;
        border: 1px solid #28354A !important;
        border-radius: 4px !important;
        font-size: 11px !important;
        font-weight: 800 !important;
        letter-spacing: 0.6px !important;
        text-transform: uppercase !important;
        padding: 5px 12px !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #FF4655 !important;
        border-color: #FF4655 !important;
        color: #FFFFFF !important;
    }
    
    /* 8. Callout Banner */
    .tracker-callout {
        background: #0E131C;
        border-left: 3px solid #00B4D8;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 11px;
        color: #CBD5E1;
        letter-spacing: 0.3px;
        margin-bottom: 10px;
    }
    .tracker-callout-red {
        border-left-color: #FF4655;
    }
    
    /* 9. Slot Action Buttons (Hapus & Pilih Popover) */
    div[data-testid="stColumn"] div[data-testid="stPopover"] > button {
        background-color: #121824 !important;
        color: #8B97A8 !important;
        border: 1px dashed #28354A !important;
        border-radius: 4px !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        height: 26px !important;
        min-height: 26px !important;
        margin-top: 4px !important;
        padding: 2px 4px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stColumn"] div[data-testid="stPopover"] > button:hover {
        border-color: #00B4D8 !important;
        color: #FFFFFF !important;
        background-color: #1A2334 !important;
    }
</style>
""", unsafe_allow_html=True)

HASIL_DIR = Path("hasil")

# ==============================================================================
# LOAD MODEL & ASSETS
# ==============================================================================
@st.cache_resource
def load_assets():
    with open(HASIL_DIR / "meta_model.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    
    if (HASIL_DIR / "model_final_2023_2026.joblib").exists():
        model = joblib.load(HASIL_DIR / "model_final_2023_2026.joblib")
    else:
        model = joblib.load(HASIL_DIR / "model_terbaik_2023_2025.joblib")
        
    df_wr = pd.read_csv(HASIL_DIR / "winrate_agent_per_map.csv")
    df_role = pd.read_csv(HASIL_DIR / "peran_agent.csv")
    
    df_wr_full = df_wr.merge(df_role, left_on="Agent", right_on="agent", how="left").drop(columns=["agent"])
    df_wr_full["win_rate_halus"] = (df_wr_full["Total Wins By Map"] + 10 * 0.5) / (df_wr_full["dimainkan"] + 10)
    
    gambar_data = {"agents": {}, "maps": {}}
    if (HASIL_DIR / "gambar_valorant_local.json").exists():
        with open(HASIL_DIR / "gambar_valorant_local.json", "r", encoding="utf-8") as f:
            gambar_data = json.load(f)
    elif (HASIL_DIR / "gambar_valorant.json").exists():
        with open(HASIL_DIR / "gambar_valorant.json", "r", encoding="utf-8") as f:
            gambar_data = json.load(f)
            
    return meta, model, df_wr_full, gambar_data

try:
    meta, model, df_wr_full, GAMBAR = load_assets()
    AGENTS = meta["AGENTS"]
    MAPS = meta["MAPS"]
    FITUR = meta["FITUR"]
    PERAN = meta.get("PERAN", ["Duelist", "Initiator", "Controller", "Sentinel"])
    ROLE_DICT = meta.get("ROLE", {})
    NM, NA = len(MAPS), len(AGENTS)
except Exception as e:
    st.error(f"Gagal memuat aset model dari folder 'hasil/': {e}")
    st.stop()

# Warna Peran Resmi Tracker.gg
ROLE_COLORS = {
    "Duelist": "#FF4655",     # Merah Duelist
    "Initiator": "#00B4D8",   # Biru Langit Initiator
    "Controller": "#8B5CF6",  # Ungu Controller
    "Sentinel": "#2EC4B6"     # Hijau Teal Sentinel
}

@st.cache_data
def get_base64_data_uri(file_path):
    if not file_path:
        return ""
    p = Path(file_path)
    if p.exists():
        with open(p, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        ext = p.suffix.lstrip(".").lower()
        mime = "image/webp" if ext == "webp" else f"image/{ext}"
        return f"data:{mime};base64,{encoded}"
    return str(file_path)

def get_agent_icon(agent_name):
    ag_data = GAMBAR.get("agents", {}).get(agent_name.lower(), {})
    path = ag_data.get("icon")
    return get_base64_data_uri(path)

def get_agent_portrait(agent_name):
    ag_data = GAMBAR.get("agents", {}).get(agent_name.lower(), {})
    path = ag_data.get("portrait") or ag_data.get("icon")
    if path and Path(path).exists():
        return str(Path(path))
    return path

def get_map_splash(map_name):
    m_data = GAMBAR.get("maps", {}).get(map_name, {})
    path = m_data.get("splash")
    if path and Path(path).exists():
        return str(Path(path))
    return path

def format_agent_name(name):
    if not name:
        return ""
    if name.lower() == "kayo":
        return "KAY/O"
    return name.capitalize()

# Inisialisasi Session State Formasi Tim
if "picked_multiselect" not in st.session_state:
    st.session_state["picked_multiselect"] = ["jett", "killjoy"] if {"jett", "killjoy"}.issubset(set(AGENTS)) else []

def add_agent_to_roster(ag):
    curr = list(st.session_state.get("picked_multiselect", []))
    if ag not in curr and len(curr) < 5:
        st.session_state["picked_multiselect"] = curr + [ag]

def remove_agent_from_roster(ag):
    curr = list(st.session_state.get("picked_multiselect", []))
    if ag in curr:
        st.session_state["picked_multiselect"] = [a for a in curr if a != ag]

def reset_roster():
    st.session_state["picked_multiselect"] = []

# ==============================================================================
# HEADER TRACKER.GG (100% KHUSUS VALORANT)
# ==============================================================================
st.markdown(
    f"""
    <div class="tracker-hero">
        <div class="hero-left">
            <svg width="34" height="26" viewBox="0 0 100 80" fill="#FF4655" style="filter: drop-shadow(0 0 6px rgba(255,70,85,0.4));">
                <path d="M0 0 L40 0 L100 80 L60 80 Z" opacity="0.95"/>
                <path d="M72 0 L100 0 L100 38 Z"/>
            </svg>
            <div>
                <h1 class="hero-title">VALORANT <span class="highlight-red">DRAFT AI</span></h1>
                <div class="hero-subtitle">Pro Esports Match Intelligence &bull; VCT Official Tournament 2023–2026</div>
            </div>
        </div>
        <div class="hero-roles">
            <span class="role-pill-trn"><span class="dot-duelist"></span> DUELIST</span>
            <span class="role-pill-trn"><span class="dot-initiator"></span> INITIATOR</span>
            <span class="role-pill-trn"><span class="dot-controller"></span> CONTROLLER</span>
            <span class="role-pill-trn"><span class="dot-sentinel"></span> SENTINEL</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 3. NAVIGASI TAB TRACKER.GG
# ==============================================================================
tab_rekomendasi, tab_leaderboard, tab_profil, tab_tentang = st.tabs([
    "Draft Recommender", 
    "Map Agent Tier & WR", 
    "Agent Performance", 
    "Model Insights"
])

# ==============================================================================
# TAB 1: DRAFT RECOMMENDER (TRACKER.GG SPLIT-SCREEN DASHBOARD)
# ==============================================================================
with tab_rekomendasi:
    # Dua Kolom Seimbang: Kiri (Team Setup 52%) & Kanan (Live Recommendations 48%)
    col_setup, col_recs = st.columns([5.2, 4.8], gap="large")
    
    # --------------------------------------------------------------------------
    # KOLOM KIRI: SETUP TIM & FORMASI
    # --------------------------------------------------------------------------
    with col_setup:
        # Pilihan Peta dengan Banner Kompak
        col_m_ctrl, col_m_img = st.columns([2.0, 1.2], vertical_alignment="center")
        with col_m_ctrl:
            st.markdown("<div style='font-size:11px; font-weight:800; letter-spacing:0.8px; color:#8B97A8; text-transform:uppercase; margin-bottom:4px;'>COMPETITIVE MAP POOL</div>", unsafe_allow_html=True)
            selected_map = st.selectbox(
                "Map Selection:", 
                MAPS, 
                index=MAPS.index("Ascent") if "Ascent" in MAPS else 0,
                label_visibility="collapsed"
            )
        with col_m_img:
            map_img = get_map_splash(selected_map)
            if map_img:
                st.image(map_img, use_container_width=True)

        # Multi-select Input Agen Tim
        st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px; font-weight:800; letter-spacing:0.8px; color:#8B97A8; text-transform:uppercase; margin-bottom:4px;'>CURRENT TEAM ROSTER (MAX 5 PICKS)</div>", unsafe_allow_html=True)
        current_picked = st.multiselect(
            "Select Picked Agents:",
            options=sorted(AGENTS),
            key="picked_multiselect",
            max_selections=5,
            label_visibility="collapsed"
        )
        
        k_picked = len(current_picked)
        slot_sisa = 5 - k_picked
        
        # 5 Kotak Slot Formasi Tim ala Tracker.gg
        slot_cols = st.columns(5)
        roles_current = {"Duelist": 0, "Initiator": 0, "Controller": 0, "Sentinel": 0}
        
        for ag in current_picked:
            r = ROLE_DICT.get(ag)
            if r in roles_current:
                roles_current[r] += 1
                
        for i in range(5):
            with slot_cols[i]:
                if i < k_picked:
                    ag_name = current_picked[i]
                    ag_role = ROLE_DICT.get(ag_name, "-")
                    ag_icon = get_agent_icon(ag_name)
                    r_color = ROLE_COLORS.get(ag_role, "#64748B")
                    
                    st.markdown(
                        f"""
                        <div class='tracker-slot' style='border-top: 3px solid {r_color};'>
                            <img src='{ag_icon}' width='38' class='tracker-slot-avatar' style='border-color:{r_color};'><br>
                            <span class='tracker-slot-name'>{format_agent_name(ag_name)}</span><br>
                            <span class='tracker-role-pill' style='background-color:{r_color};'>{ag_role}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.button(
                        "✕ Hapus",
                        key=f"btn_del_slot_{ag_name}_{i}",
                        on_click=remove_agent_from_roster,
                        args=(ag_name,),
                        use_container_width=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class='tracker-slot tracker-slot-empty'>
                            <div style='font-size:20px; color:#64748B; font-weight:300; line-height:1;'>+</div>
                            <span style='font-size:11px; color:#8B97A8; font-weight:700; margin-top:2px;'>SLOT #{i+1}</span>
                            <span style='font-size:9px; color:#546274; text-transform:uppercase;'>VACANT</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    with st.popover("+ Pilih", key=f"pop_vacant_slot_{i}", use_container_width=True):
                        st.markdown(f"<div style='font-size:11px; font-weight:800; color:#CBD5E1; text-transform:uppercase; margin-bottom:6px;'>PILIH AGEN SLOT #{i+1}</div>", unsafe_allow_html=True)
                        available_for_slot = [a for a in sorted(AGENTS) if a not in current_picked]
                        chosen_agent = st.selectbox(
                            f"Pilih Agen Slot #{i+1}:",
                            available_for_slot,
                            index=None,
                            placeholder="Cari nama agen...",
                            format_func=lambda a: f"{format_agent_name(a)} ({ROLE_DICT.get(a, '-')})",
                            key=f"sel_cand_slot_{i}",
                            label_visibility="collapsed"
                        )
                        if chosen_agent:
                            add_agent_to_roster(chosen_agent)
                            st.rerun()
                    
        # Segmented Role Composition Status
        st.markdown(
            f"""
            <div class='comp-bar'>
                <div><span style='color:{ROLE_COLORS["Duelist"]};'>&bull;</span> DUELIST: <span style='color:#FFFFFF;'>{roles_current["Duelist"]}</span></div>
                <div><span style='color:{ROLE_COLORS["Initiator"]};'>&bull;</span> INITIATOR: <span style='color:#FFFFFF;'>{roles_current["Initiator"]}</span></div>
                <div><span style='color:{ROLE_COLORS["Controller"]};'>&bull;</span> CONTROLLER: <span style='color:#FFFFFF;'>{roles_current["Controller"]}</span></div>
                <div><span style='color:{ROLE_COLORS["Sentinel"]};'>&bull;</span> SENTINEL: <span style='color:#FFFFFF;'>{roles_current["Sentinel"]}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        prioritas_role = st.toggle("Prioritize Missing Roles", value=True)
        top_k = 5
            
        if k_picked > 0:
            st.button("RESET ROSTER", on_click=reset_roster, use_container_width=True)

    # --------------------------------------------------------------------------
    # KOLOM KANAN: LIVE AI RECOMMENDATIONS (TRACKER.GG LEADERBOARD STYLE)
    # --------------------------------------------------------------------------
    with col_recs:
        st.markdown(
            f"""
            <div class='tracker-card-header'>
                <span>TOP 5 AI RECOMMENDATIONS</span>
                <span>REMAINING SLOTS: <b style='color:#FF4655;'>{slot_sisa}</b> / 5</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if k_picked >= 5:
            st.markdown(
                f"""
                <div class='tracker-callout' style='border-left-color: #10B981;'>
                    <b>TEAM FORMATION COMPLETE (5/5 AGENTS)</b><br>
                    All 5 roster slots are locked for <b>{selected_map}</b>. Full draft synergy analysis is ready.
                </div>
                """,
                unsafe_allow_html=True
            )
            team_summary = []
            for ag in current_picked:
                wr_row = df_wr_full[(df_wr_full["Map"] == selected_map) & (df_wr_full["Agent"] == ag)]
                wr_val = (wr_row.iloc[0]["win_rate_halus"] * 100) if not wr_row.empty else 50.0
                matches_cnt = wr_row.iloc[0]["dimainkan"] if not wr_row.empty else 0
                team_summary.append({
                    "Agent": format_agent_name(ag),
                    "Role": ROLE_DICT.get(ag, "-"),
                    "Map Win Rate (%)": f"{wr_val:.1f}%",
                    "VCT Matches": matches_cnt
                })
            st.markdown("<div style='font-size:11px; font-weight:800; letter-spacing:0.8px; color:#8B97A8; text-transform:uppercase; margin-top:10px; margin-bottom:6px;'>LOCKED ROSTER STATS ON THIS MAP</div>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(team_summary), hide_index=True, use_container_width=True)
        else:
            # Model Predict Probs
            x = np.zeros((1, len(FITUR)), dtype=np.float32)
            x[0, MAPS.index(selected_map)] = 1.0
            x[0, NM + NA] = k_picked
            for ag in current_picked:
                x[0, NM + AGENTS.index(ag)] = 1.0
                r_idx = PERAN.index(ROLE_DICT[ag])
                x[0, NM + NA + 1 + r_idx] += 1.0

            prob = np.zeros(NA)
            prob[model.classes_] = model.predict_proba(x)[0]
            for ag in current_picked:
                prob[AGENTS.index(ag)] = -1.0

            role_kosong = [p for p, c in roles_current.items() if c == 0]

            if prioritas_role and len(role_kosong) > 0 and slot_sisa <= len(role_kosong):
                kandidat_prioritas = [idx for idx in np.argsort(-prob) if prob[idx] >= 0 and ROLE_DICT.get(AGENTS[idx]) in role_kosong]
                kandidat_lain = [idx for idx in np.argsort(-prob) if prob[idx] >= 0 and ROLE_DICT.get(AGENTS[idx]) not in role_kosong]
                urutan = kandidat_prioritas + kandidat_lain
                st.markdown(
                    f"<div class='tracker-callout tracker-callout-red'><b>ROLE BALANCE PRIORITY:</b> Elevating missing roles (<b>{', '.join(role_kosong)}</b>) due to limited remaining team slots.</div>",
                    unsafe_allow_html=True
                )
            else:
                urutan = [idx for idx in np.argsort(-prob) if prob[idx] >= 0]
                st.markdown(
                    "<div class='tracker-callout'><b>PRO MATCH PREDICTION:</b> Probability ranks driven purely by historical VCT championship team compositions.</div>",
                    unsafe_allow_html=True
                )

            top_recs = urutan[:top_k]
            
            # Baris Rekomendasi Agen ala Tracker.gg
            for rank_no, idx in enumerate(top_recs, start=1):
                ag_name = AGENTS[idx]
                ag_role = ROLE_DICT.get(ag_name, "-")
                skor_pct = prob[idx] * 100
                r_color = ROLE_COLORS.get(ag_role, "#64748B")
                ag_icon = get_agent_icon(ag_name)
                
                wr_row = df_wr_full[(df_wr_full["Map"] == selected_map) & (df_wr_full["Agent"] == ag_name)]
                if not wr_row.empty:
                    wr_h = wr_row.iloc[0]["win_rate_halus"] * 100
                    main_cnt = wr_row.iloc[0]["dimainkan"]
                else:
                    wr_h = 50.0
                    main_cnt = 0
                
                wr_class = "wr-positive" if wr_h >= 50.0 else "wr-average"
                
                r_col1, r_col2 = st.columns([3.8, 1.2], vertical_alignment="center")
                
                with r_col1:
                    st.markdown(
                        f"""
                        <div class='tracker-rec-row'>
                            <div class='rec-agent-meta'>
                                <span class='rec-rank-badge rec-rank-{rank_no}'>#{rank_no}</span>
                                <img src='{ag_icon}' width='40' style='border-radius:4px; border-left:3px solid {r_color};'>
                                <div>
                                    <div style='font-size:14px; font-weight:800; color:#FFFFFF;'>{format_agent_name(ag_name)}</div>
                                    <span class='tracker-role-pill' style='background:{r_color}; font-size:8px;'>{ag_role}</span>
                                </div>
                            </div>
                            <div class='rec-stats-box'>
                                <div class='rec-prob-val'>{skor_pct:.1f}%</div>
                                <div class='rec-prob-bar-bg'>
                                    <div class='rec-prob-bar-fill' style='width:{min(skor_pct * 1.5, 100.0):.1f}%;'></div>
                                </div>
                                <div class='rec-wr-text {wr_class}'>{wr_h:.1f}% WR &bull; {main_cnt} M</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with r_col2:
                    st.button(
                        "+ PICK",
                        key=f"btn_pick_{ag_name}",
                        on_click=add_agent_to_roster,
                        args=(ag_name,),
                        use_container_width=True
                    )

            # Collapsible Full Stats Table
            with st.expander("DETAILED PROBABILITY MATRIX", expanded=False):
                tabel_data = []
                for r_i, idx in enumerate(urutan[:12], start=1):
                    ag = AGENTS[idx]
                    wr_r = df_wr_full[(df_wr_full["Map"] == selected_map) & (df_wr_full["Agent"] == ag)]
                    wr_val = (wr_r.iloc[0]["win_rate_halus"] * 100) if not wr_r.empty else 50.0
                    tabel_data.append({
                        "Rank": f"#{r_i}",
                        "Agent": format_agent_name(ag),
                        "Role": ROLE_DICT.get(ag, "-"),
                        "AI Score (%)": round(prob[idx] * 100, 2),
                        "Map Win Rate (%)": round(wr_val, 2)
                    })
                st.dataframe(pd.DataFrame(tabel_data), hide_index=True, use_container_width=True)

# ==============================================================================
# TAB 2: MAP AGENT TIER & WIN RATE
# ==============================================================================
with tab_leaderboard:
    st.markdown("<div class='tracker-card-header'><span>MAP PERFORMANCE & AGENT WIN RATES</span></div>", unsafe_allow_html=True)
    
    col_lb_ctrl1, col_lb_ctrl2 = st.columns([1.5, 2])
    with col_lb_ctrl1:
        map_lb = st.selectbox("Select Map Pool:", MAPS, key="lb_map")
    with col_lb_ctrl2:
        min_main_lb = st.slider("Minimum Matches Filter:", min_value=1, max_value=50, value=5)
    
    sub_map = df_wr_full[df_wr_full["Map"] == map_lb].copy()
    sub_map = sub_map[sub_map["dimainkan"] >= min_main_lb].sort_values("win_rate_halus", ascending=False).reset_index(drop=True)
    sub_map["Peringkat"] = range(1, len(sub_map) + 1)
    
    col_chart, col_tbl = st.columns([1.8, 2.2], gap="medium")
    with col_chart:
        st.markdown(f"<div style='font-size:12px; font-weight:800; color:#8B97A8; text-transform:uppercase; margin-bottom:6px;'>TOP 10 WIN RATES ON {map_lb.upper()}</div>", unsafe_allow_html=True)
        top10_plot = sub_map.head(10)[["Agent", "win_rate_halus"]].copy()
        top10_plot["WR (%)"] = top10_plot["win_rate_halus"] * 100
        st.bar_chart(data=top10_plot.set_index("Agent")["WR (%)"], height=280)
        
    with col_tbl:
        st.markdown("<div style='font-size:12px; font-weight:800; color:#8B97A8; text-transform:uppercase; margin-bottom:6px;'>LEADERBOARD TABLE</div>", unsafe_allow_html=True)
        table_lb = sub_map[["Peringkat", "Agent", "peran", "dimainkan", "win_rate_halus"]].copy()
        table_lb.columns = ["Rank", "Agent", "Role", "Matches", "Bayes WR (%)"]
        table_lb["Agent"] = table_lb["Agent"].apply(format_agent_name)
        table_lb["Bayes WR (%)"] = (table_lb["Bayes WR (%)"] * 100).round(2)
        st.dataframe(table_lb, hide_index=True, use_container_width=True, height=280)

# ==============================================================================
# TAB 3: AGENT PERFORMANCE PROFILE
# ==============================================================================
with tab_profil:
    st.markdown("<div class='tracker-card-header'><span>INDIVIDUAL AGENT METRICS</span></div>", unsafe_allow_html=True)
    
    selected_agent = st.selectbox(
        "Select Agent:", 
        sorted(AGENTS), 
        index=sorted(AGENTS).index("jett") if "jett" in AGENTS else 0,
        format_func=format_agent_name,
        label_visibility="collapsed"
    )
    
    col_ag_pic, col_ag_info = st.columns([1, 3], gap="medium")
    
    with col_ag_pic:
        ag_portrait = get_agent_portrait(selected_agent)
        if ag_portrait:
            st.image(ag_portrait, use_container_width=True)
            
    with col_ag_info:
        sub_agent = df_wr_full[df_wr_full["Agent"] == selected_agent].sort_values("win_rate_halus", ascending=False).reset_index(drop=True)
        total_played = sub_agent["dimainkan"].sum()
        total_won = sub_agent["Total Wins By Map"].sum()
        overall_wr = (total_won / total_played * 100) if total_played > 0 else 0.0
        ag_role = ROLE_DICT.get(selected_agent, "-")
        r_badge_col = ROLE_COLORS.get(ag_role, "#64748B")
        
        st.markdown(
            f"""
            <div style='display:flex; align-items:center; gap:12px; margin-bottom:10px;'>
                <h2 style='margin:0; font-size:24px; font-weight:900; color:#FFFFFF; text-transform:uppercase;'>{format_agent_name(selected_agent)}</h2>
                <span class='tracker-role-pill' style='background-color:{r_badge_col}; font-size:10px; padding:3px 8px;'>{ag_role}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        m_c1, m_c2, m_c3 = st.columns(3)
        m_c1.metric("Total Matches (VCT)", f"{total_played:,}")
        m_c2.metric("Total Wins", f"{total_won:,}")
        m_c3.metric("Global Win Rate", f"{overall_wr:.2f}%")
        
        st.markdown("<div style='font-size:11px; font-weight:800; color:#8B97A8; text-transform:uppercase; margin-top:10px; margin-bottom:4px;'>MAP WIN RATE BREAKDOWN</div>", unsafe_allow_html=True)
        sub_agent_chart = sub_agent[["Map", "win_rate_halus"]].copy()
        sub_agent_chart["Win Rate (%)"] = sub_agent_chart["win_rate_halus"] * 100
        st.bar_chart(data=sub_agent_chart.set_index("Map")["Win Rate (%)"], height=190)

# ==============================================================================
# TAB 4: MODEL INSIGHTS & BATASAN MODEL
# ==============================================================================
with tab_tentang:
    st.markdown("<div class='tracker-card-header'><span>MACHINE LEARNING ARCHITECTURE, DATASET & LIMITATIONS</span></div>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1, 1], gap="large")
    
    with col_t1:
        st.markdown(
            r"""
            #### Arsitektur Model & Metodologi
            Sistem ini memprediksi pemilihan agen berikutnya pada fase *draft pick* berbasis analisis pola sinergi tim dan preferensi peta dari turnamen resmi **VCT 2023–2026**.
            
            * **Model Terbaik:** Random Forest Classifier (Multi-Label Probabilistic)
            * **Top-3 Accuracy:** **85.0%** (Mengungguli baseline acak 26.6% dan baseline map 79.0%)
            * **Top-1 Accuracy:** **65.3%**
            * **Macro-F1 Score:** **0.261**
            * **Dimensi Fitur (46 Kolom):**
              - 12 Fitur Peta (*One-Hot Encoding*)
              - 29 Fitur Agen Terpilih (*Binary Multi-Hot*)
              - 1 Fitur Jumlah Agen Terpilih (*Draft Progress*)
              - 4 Fitur Hitungan Peran Tim (*Duelist, Initiator, Controller, Sentinel*)

            #### Dataset & Ekspansi Data
            * **Komposisi Valid:** 8.192 tim kompetitif turnamen VCT (5 agen unik per tim).
            * **Ekspansi Situasi Draft:** Tiap komposisi diekspansi menjadi 31 kombinasi situasi ($k = 0 \dots 4$ agen diketahui), menghasilkan lebih dari **500.000 sampel latih**.
            
            #### Bayesian Laplace Smoothing
            Win rate peta dihaluskan untuk mencegah distorsi pada sampel sedikit:
            $$\text{Win Rate Halus} = \frac{\text{Total Wins} + 10 \times 0.5}{\text{Total Matches} + 10}$$
            """
        )
        
    with col_t2:
        st.markdown(
            """
            #### Batasan Model (Model Limitations)
            Pengguna disarankan memahami beberapa batasan inheren dari model machine learning ini:

            1. **Perbedaan Meta Pro VCT vs Ranked Match Publik**  
               Model dilatih menggunakan data turnamen pro VCT di mana strategi mengutamakan koordinasi tim, set-piece utilitas, dan komunikasi suara terstruktur (seperti KAY/O, Breach, Sova). Pada mode Ranked publik (Solo/Duo Queue), gaya bermain cenderung lebih mengandalkan duel mandiri (seperti Reyna atau Iso) yang di level turnamen pro jarang digunakan.

            2. **Dinamika Pembaruan Patch (Patch Drift)**  
               Riot Games secara berkala merilis patch update yang mengubah kekuatan agen (buff/nerf) dan layout peta. Dataset mencakup data turnamen rentang 2023 hingga 2026 yang merefleksikan tren rata-rata historis, bukan kondisi patch spesifik minggu berjalan.

            3. **Tantangan Cold-Start pada Agen & Peta Baru**  
               Agen yang baru dirilis (seperti Waylay, Tejo, Miks, Veto) atau peta baru (seperti Abyss, Corrode) memiliki jumlah pertandingan kompetitif yang jauh lebih sedikit dibanding agen veteran (seperti Jett, Omen, Killjoy). Hal ini membuat estimasi probabilitas agen baru cenderung lebih konservatif.

            4. **Faktor Subjektif Pemain & Counter-Picking**  
               Model memberikan rekomendasi murni berdasarkan statistik sinergi tim dan peta. Model tidak memperhitungkan tingkat kenyamanan individual pemain (*comfort pick* / *player mastery*), strategi melawan agen musuh (*enemy counter-pick*), maupun urutan giliran menyerang/bertahan (*Attacker/Defender first*).
            """
        )
