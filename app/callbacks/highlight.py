"""
Highlighting support for the parallel-coordinates visualization.

This module provides interaction logic to visually identify a user-selected
simulation result within a Plotly parallel-coordinates plot. Due to intrinsic
limitations of Plotly's `parcoords` trace (e.g., the lack of per-line styling
such as line width or dash patterns), highlighting is implemented using
Plotly's native brushing and filtering mechanism (`constraintrange`).

When a simulation result is selected via the image grid, the corresponding
parameter combination is mapped back to the underlying dataframe. The
parallel-coordinates plot is then constrained to a narrow value range around
the selected parameters. As a result, the selected polyline remains in full
color while all non-matching lines are automatically de-emphasized by Plotly
(i.e., rendered in a greyed or semi-transparent style).
"""

import dash
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go


def _find_selected_index(dff: pd.DataFrame, selected: dict) -> int | None:
    """
    Identify the dataframe row index corresponding to a selected record.

    Attempts to locate the row in a dataframe that matches a user-selected result.
    The selection is provided as a dictionary (e.g., originating from an image grid or metadata store)
    containing a subset of column–value pairs.

    Parameters
    ----------
    dff : pandas.DataFrame
        The dataframe containing all simulation results.
    selected : dict
        A dictionary representing the selected simulation result, typically
        consisting of parameter names and their corresponding values.

    Returns
    -------
    int or None
        The index of the first matching dataframe row if a match is found;
        otherwise, None.
    """
    common_cols = [c for c in selected.keys() if c in dff.columns]
    if not common_cols:
        return None

    mask = pd.Series(True, index=dff.index)
    for c in common_cols:
        v = selected.get(c)
        if pd.isna(v):
            mask &= dff[c].isna()
        else:
            mask &= (dff[c] == v)

    if not mask.any():
        return None
    return int(dff.index[mask][0])


def _make_eps(v, col_min, col_max) -> float:
    """
    Compute a small epsilon value for defining a narrow constraint window.

    The returned epsilon is used to construct a minimal interval around a
    selected value when applying Plotly `constraintrange`, such that only
    the corresponding polyline (or as few as possible) satisfies the constraint.
    """
    span = float(col_max - col_min) if (col_max is not None and col_min is not None) else 0.0
    if span <= 0:
        # fallback
        return 1e-9
    # 1e-6 of span
    return max(span * 1e-6, 1e-9)


@dash.callback(
    Output("parallel-coordinates", "figure", allow_duplicate=True),
    Input("selected-image-data", "data"),
    State("parallel-coordinates", "figure"),
    State("df", "data"),
    State("labels", "data"),
    prevent_initial_call=True,
)
def constrain_to_selected(selected_records, fig_dict, df_records, labels):
    """
    Set constraintrange for each dimension to a tiny window around the selected value.
    This "brushes" the parcoords so the selected line becomes easy to spot.
    Also add an annotation label with selected info.
    """
    if not fig_dict or not df_records:
        return dash.no_update

    dff = pd.DataFrame.from_records(df_records)
    fig = go.Figure(fig_dict)

    # find base parcoords trace
    base_par = None
    for tr in fig.data:
        if tr.type == "parcoords":
            base_par = tr
            break
    if base_par is None:
        return dash.no_update

    # If no selection, clear any existing constraintrange + annotation
    if not selected_records:
        try:
            # clear constraintrange for all dimensions
            dims = []
            for dim in base_par.dimensions:
                dj = dim.to_plotly_json()
                if "constraintrange" in dj:
                    dj.pop("constraintrange", None)
                dims.append(dj)
            base_par.dimensions = dims
        except Exception:
            pass

        fig.update_layout(annotations=[])
        return fig

    selected = selected_records[0]
    sel_idx = _find_selected_index(dff, selected)
    if sel_idx is None:
        return dash.no_update

    # build label -> col mapping
    label_to_col = {}
    if isinstance(labels, dict):
        for col, lab in labels.items():
            label_to_col[str(lab)] = col
            label_to_col[str(col)] = col

    # Apply constraintrange per dimension
    new_dims = []
    for dim in base_par.dimensions:
        dj = dim.to_plotly_json()
        dim_label = str(dj.get("label", ""))

        col = label_to_col.get(dim_label)
        if col is None and dim_label in dff.columns:
            col = dim_label

        # If not possible to map this dimension back to a df column, keep as-is
        if col is None or col not in dff.columns:
            dj.pop("constraintrange", None)
            new_dims.append(dj)
            continue

        # Only numeric dimensions can be constrained reliably
        if not pd.api.types.is_numeric_dtype(dff[col]):
            dj.pop("constraintrange", None)
            new_dims.append(dj)
            continue

        v = float(dff.loc[sel_idx, col])
        col_min = float(dff[col].min())
        col_max = float(dff[col].max())
        eps = _make_eps(v, col_min, col_max)

        dj["constraintrange"] = [v - eps, v + eps]
        new_dims.append(dj)

    base_par.dimensions = new_dims

    # Add a label (annotation) to know what is selected
    # Use first few keys from selected dict
    try:
        show_keys = list(selected.keys())[:5]
        info = ", ".join([f"{k}={selected.get(k)}" for k in show_keys])
    except Exception:
        info = f"row={sel_idx}"

    fig.update_layout(
        annotations=[
            dict(
                text=f"Selected: {info}",
                x=1,
                y=1,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                showarrow=False,
                bgcolor="rgba(200,200,200,0.85)",
                bordercolor="rgba(0,0,0,0.25)",
                borderwidth=1,
                font=dict(size=12),
            )
        ]
    )

    return fig
