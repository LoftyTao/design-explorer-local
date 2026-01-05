import streamlit as st
import hiplot as hip
import pandas as pd
import os
import zipfile
import io
from PIL import Image

# -------------------------------------------------------
# 1. Global Page Configuration
# -------------------------------------------------------
st.set_page_config(
    layout="wide", 
    page_title="Design Analytics Pro",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# 2. Session State Management
# -------------------------------------------------------
if 'current_view_uid' not in st.session_state:
    st.session_state['current_view_uid'] = None
if 'active_view_name' not in st.session_state:
    st.session_state['active_view_name'] = None

# -------------------------------------------------------
# 3. Sidebar: Data Management & Ingestion
# -------------------------------------------------------
with st.sidebar:
    st.header("Data Management")
    source_type = st.radio("Entry Source:", ["Built-in Samples", "Local ZIP Archive"])
    st.divider()

    df_raw, img_mode, active_zip, base_dir, case_name = None, None, None, "", ""

    if source_type == "Built-in Samples":
        ROOT = "samples"
        if os.path.exists(ROOT):
            folders = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d))]
            if folders:
                selected = st.selectbox("Select Project Dataset:", sorted(folders))
                case_name = selected
                img_mode = 'local'
                base_dir = os.path.join(ROOT, selected)
                csv_p = os.path.join(base_dir, "data.csv")
                if os.path.exists(csv_p):
                    df_raw = pd.read_csv(csv_p, sep=None, engine='python')
            else:
                st.warning("No built-in samples detected in the directory.")
        else:
            st.error("Missing 'samples' root directory.")
    else:
        uploaded = st.file_uploader("Upload Project Archive (.zip):", type="zip")
        if uploaded:
            active_zip = zipfile.ZipFile(uploaded)
            all_paths = active_zip.namelist()
            csv_entries = [p for p in all_paths if p.endswith('data.csv')]
            
            if not csv_entries:
                st.error("Invalid Archive: 'data.csv' not found.")
            else:
                if len(csv_entries) > 1:
                    path_map = {p: (os.path.dirname(p) if os.path.dirname(p) else "Root") for p in csv_entries}
                    target = st.selectbox("Multiple Datasets Detected - Select Case:", list(path_map.keys()), format_func=lambda x: path_map[x])
                else:
                    target = csv_entries[0]
                
                with active_zip.open(target) as f:
                    df_raw = pd.read_csv(f, sep=None, engine='python')
                
                base_dir = os.path.dirname(target)
                case_name = os.path.dirname(target) if os.path.dirname(target) else "Uploaded Project"
                img_mode = 'zip'

    # Logic to process and clean data upon successful loading
    clean_vars = []
    rename_map = {}
    if df_raw is not None:
        if 'uid' not in df_raw.columns: 
            df_raw['uid'] = range(len(df_raw))
        
        # Standardize headers
        df_raw.columns = [str(c).strip() for c in df_raw.columns]
        
        # Numeric conversion for analysis columns
        for col in df_raw.columns:
            if not col.startswith('img:') and 'uid' not in col.lower():
                df_raw[col] = pd.to_numeric(df_raw[col], errors='ignore')

        metric_cols = [c for c in df_raw.columns if not c.startswith('img:') and 'uid' not in c.lower()]
        clean_vars = [c.split(':', 1)[1] if ':' in c else c for c in metric_cols]
        rename_map = {c: (c.split(':', 1)[1] if ':' in c else c) for c in df_raw.columns if not c.startswith('img:') and c != 'uid'}

# -------------------------------------------------------
# 4. Main Analytics Dashboard Logic
# -------------------------------------------------------
if df_raw is not None:
    df_disp = df_raw.rename(columns=rename_map)
    img_cols = [c for c in df_raw.columns if c.startswith('img:')]
    
    st.header(f"Analytics Workspace: {case_name}")

    # Synchronize HiPlot color with the selected metric from the selection pool
    current_metric = st.session_state.get('pool_metric', clean_vars[0] if clean_vars else None)

    # --- PHASE 1: Multi-Dimensional Data Exploration (HiPlot) ---
    with st.container(border=True):
        st.subheader("1. Performance Filtering & Trend Analysis")
        exp = hip.Experiment.from_dataframe(df_disp)
        hide_tech = ['uid', 'from_uid'] + img_cols
        
        plot_conf = {'hide': hide_tech}
        if current_metric:
            plot_conf['colorBy'] = current_metric
            
        exp.display_data(hip.Displays.PARALLEL_PLOT).update(plot_conf)
        exp.display_data(hip.Displays.TABLE).update({'hide': hide_tech})
        
        selected_uids = exp.to_streamlit(key=f"engine_{case_name}", ret="selected_uids").display()

    # --- PHASE 2: Candidate Selection Pool ---
    if selected_uids is None:
        df_filtered = df_disp
    else:
        # Match against string-converted UIDs for robust filtering
        mask = df_disp['uid'].astype(str).isin([str(u) for u in selected_uids])
        df_filtered = df_disp[mask]

    st.write("")
    with st.container(border=True):
        # Header controls for sorting and analytics metadata
        col_title, col_metric, col_order = st.columns([2, 1.5, 1])
        
        with col_title:
            st.subheader(f"2. Candidate Pool")
            
        with col_metric:
            selected_metric = st.selectbox(
                "Optimization Metric:", 
                options=clean_vars, 
                key='pool_metric'
            )
            
        with col_order:
            sort_order = st.radio(
                "Rank Priority:", 
                options=["Descending", "Ascending"], 
                horizontal=True,
                key='pool_sort_order'
            )
        
        # Display selection coverage for visual density feedback
        coverage = len(df_filtered) / len(df_disp) if len(df_disp) > 0 else 0
        st.progress(coverage, text=f"Selection Coverage: {len(df_filtered)} / {len(df_disp)} ({coverage:.1%})")
        
        st.caption("Instructions: Scroll vertically within the area below to explore filtered candidates.")
        st.divider()
        
        curr_uid = st.session_state['current_view_uid']
        
        # Sorting logic applied to the visible grid
        is_ascending = (sort_order == "Ascending")
        if selected_metric and selected_metric in df_filtered.columns:
            df_pool = df_filtered.sort_values(selected_metric, ascending=is_ascending)
        else:
            df_pool = df_filtered.sort_values('uid')

        # Vertical scrolling container for large-scale grid exploration
        with st.container(height=400):
            display_limit = 500
            grid_cols = st.columns(10)
            for idx, (_, row) in enumerate(df_pool.head(display_limit).iterrows()):
                uid = row['uid']
                with grid_cols[idx % 10]:
                    is_active = (curr_uid == uid)
                    btn_label = f"#{uid}"
                    if st.button(btn_label, key=f"btn_{uid}", type="primary" if is_active else "secondary", use_container_width=True):
                        st.session_state['current_view_uid'] = uid
                        st.rerun()

    # --- PHASE 3: Technical Diagnostic View ---
    st.write("")
    if curr_uid is not None and curr_uid in df_raw['uid'].values:
        row_raw = df_raw[df_raw['uid'] == curr_uid].iloc[0]
        row_disp = df_disp[df_disp['uid'] == curr_uid].iloc[0]

        with st.container(border=True):
            st.subheader(f"3. Technical Diagnostic Detail: #{curr_uid}")
            
            if img_cols:
                view_names = [c.split(':')[-1] for c in img_cols]
                
                # Default selection to first view if not set
                if st.session_state['active_view_name'] not in view_names:
                    st.session_state['active_view_name'] = view_names[0]
                
                # Refined View Selector: Modern button group logic
                btn_cols = st.columns([1] * len(view_names) + [6]) # Align buttons to the left
                for i, v_name in enumerate(view_names):
                    is_view_active = (st.session_state['active_view_name'] == v_name)
                    if btn_cols[i].button(
                        v_name, 
                        key=f"view_nav_{v_name}", 
                        type="primary" if is_view_active else "secondary",
                        use_container_width=True
                    ):
                        st.session_state['active_view_name'] = v_name
                        st.rerun()
                
                # Content Rendering based on Button Group state
                view_idx = view_names.index(st.session_state['active_view_name'])
                c_viz, c_metrics = st.columns([2, 1], gap="large")
                
                with c_viz:
                    with st.container(border=True):
                        img_name = str(row_raw.get(img_cols[view_idx], '')).strip()
                        try:
                            if img_mode == 'zip' and active_zip:
                                full_img_p = os.path.join(base_dir, img_name).replace("\\", "/")
                                if full_img_p in active_zip.namelist():
                                    with active_zip.open(full_img_p) as f:
                                        st.image(Image.open(f), use_column_width=True)
                                else:
                                    st.warning(f"Visual asset missing: {img_name}")
                            else:
                                path = os.path.join(base_dir, img_name)
                                if os.path.exists(path):
                                    st.image(Image.open(path), use_column_width=True)
                                else:
                                    st.info("Visual resource unavailable for this viewpoint.")
                        except:
                            st.error("Engine failed to render the visual asset.")
                
                with c_metrics:
                    # Parameter grid aligned with the visual viewport
                    with st.container(border=True, height=520):
                        disp_vars = [c for c in df_disp.columns if c not in ['uid', 'from_uid'] and c not in img_cols]
                        for v in disp_vars:
                            val = row_disp[v]
                            fmt_val = f"{val:.4f}" if isinstance(val, float) else str(val)
                            col_left, col_right = st.columns([3, 2])
                            col_left.markdown(f"**{v}**")
                            col_right.text(fmt_val)
            else:
                # Fallback layout for non-visual datasets
                _, c_metrics_only, _ = st.columns([1, 2, 1])
                with c_metrics_only:
                    with st.container(border=True):
                        disp_vars = [c for c in df_disp.columns if c not in ['uid', 'from_uid'] and c not in img_cols]
                        for v in disp_vars:
                            val = row_disp[v]
                            fmt_val = f"{val:.4f}" if isinstance(val, float) else str(val)
                            st.write(f"**{v}**: {fmt_val}")
else:
    st.info("System Ready. Please load a project dataset from the sidebar to begin analysis.")