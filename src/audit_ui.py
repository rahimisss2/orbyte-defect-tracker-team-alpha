"""Presentation-only rendering for Orbyte's audit history."""

import html

import streamlit as st


_COLUMNS = (
    "Claim ID",
    "Created",
    "Supplier",
    "Item",
    "Qty",
    "Claimed value",
    "Decision",
    "Authorized by",
)
_DECISIONS = {
    "Pending review": "pending",
    "Authorized · demo": "authorized",
}


def render_audit_records(rows: list[dict]) -> None:
    """Render audit records as a responsive table and mobile record cards."""
    table_rows = []
    for row in rows:
        cells = []
        for column in _COLUMNS:
            value = html.escape(str(row.get(column, "")), quote=True)
            if column == "Decision":
                label = row.get(column, "")
                decision_class = _DECISIONS.get(label)
                if decision_class:
                    value = (
                        f'<span class="orbyte-audit__badge '
                        f'orbyte-audit__badge--{decision_class}">{value}</span>'
                    )
                else:
                    value = f'<span class="orbyte-audit__badge">{value}</span>'
            cells.append(
                f'<td data-label="{html.escape(column, quote=True)}" '
                f'class="orbyte-audit__cell--{_COLUMNS.index(column)}">{value}</td>'
            )
        table_rows.append("<tr>" + "".join(cells) + "</tr>")

    headers = "".join(f"<th scope=\"col\">{html.escape(column, quote=True)}</th>" for column in _COLUMNS)
    body = "".join(table_rows)
    if not body:
        body = (
            '<tr class="orbyte-audit__empty"><td colspan="8">'
            "No audit records match these filters.</td></tr>"
        )

    st.markdown(
        f"""
        <style>
          .orbyte-audit {{
            width: 100%;
            overflow: hidden;
            border: 1px solid #354a5b;
            border-radius: 12px;
            background: linear-gradient(145deg, #1b2b3b, #172635);
            box-shadow: 0 12px 28px rgba(3, 11, 19, .18), inset 0 1px rgba(220, 246, 244, .035);
          }}
          .orbyte-audit__table {{
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            color: #d5e0e3;
            font: 500 .78rem/1.5 var(--orbyte-display, sans-serif);
          }}
          .orbyte-audit__table th {{
            padding: .8rem .7rem;
            border-bottom: 1px solid #405567;
            background: rgba(28, 51, 67, .82);
            color: #adc2c8;
            font: 500 .62rem/1.4 var(--orbyte-mono, monospace);
            letter-spacing: .045em;
            text-align: left;
            vertical-align: bottom;
          }}
          .orbyte-audit__table td {{
            padding: .8rem .7rem;
            border-bottom: 1px solid rgba(70, 92, 108, .55);
            overflow-wrap: anywhere;
            vertical-align: top;
          }}
          .orbyte-audit__table tbody tr:last-child td {{ border-bottom: 0; }}
          .orbyte-audit__table tbody tr:not(.orbyte-audit__empty):hover {{
            background: rgba(75, 150, 145, .075);
          }}
          .orbyte-audit__cell--0 {{
            color: #a9dfd7;
            font: 500 .72rem/1.5 var(--orbyte-mono, monospace);
            overflow-wrap: anywhere;
          }}
          .orbyte-audit__cell--4,
          .orbyte-audit__cell--5 {{
            color: #e5eff0;
            font: 500 .76rem/1.5 var(--orbyte-mono, monospace);
            font-variant-numeric: tabular-nums;
          }}
          .orbyte-audit__badge {{
            display: inline-block;
            max-width: 100%;
            padding: .22rem .48rem;
            border: 1px solid #52616a;
            border-radius: 999px;
            color: #d4e0e2;
            background: rgba(105, 123, 132, .16);
            font: 500 .66rem/1.35 var(--orbyte-mono, monospace);
            overflow-wrap: anywhere;
          }}
          .orbyte-audit__badge--pending {{
            border-color: rgba(228, 183, 109, .48);
            color: #f0ce8f;
            background: rgba(161, 113, 44, .19);
          }}
          .orbyte-audit__badge--authorized {{
            border-color: rgba(120, 208, 162, .42);
            color: #a5e3bd;
            background: rgba(46, 119, 83, .2);
          }}
          .orbyte-audit__empty td {{
            padding: 1.4rem;
            color: #afc1c6;
            text-align: center;
          }}
          @media (max-width: 767px) {{
            .orbyte-audit {{
              overflow: visible;
              border: 0;
              background: transparent;
              box-shadow: none;
            }}
            .orbyte-audit__table,
            .orbyte-audit__table tbody {{ display: block; }}
            .orbyte-audit__table thead {{ display: none; }}
            .orbyte-audit__table tr:not(.orbyte-audit__empty) {{
              display: block;
              margin: 0 0 .75rem;
              padding: .38rem .8rem;
              border: 1px solid #354a5b;
              border-radius: 12px;
              background: linear-gradient(145deg, #1b2b3b, #172635);
              box-shadow: 0 8px 20px rgba(3, 11, 19, .15);
            }}
            .orbyte-audit__table td {{
              display: grid;
              grid-template-columns: minmax(5.8rem, 34%) minmax(0, 1fr);
              gap: .7rem;
              padding: .63rem 0;
              border-bottom: 1px solid rgba(70, 92, 108, .48);
              overflow-wrap: anywhere;
            }}
            .orbyte-audit__table td:last-child {{ border-bottom: 0; }}
            .orbyte-audit__table td::before {{
              content: attr(data-label);
              color: #a9bec4;
              font: 500 .61rem/1.5 var(--orbyte-mono, monospace);
              letter-spacing: .025em;
            }}
            .orbyte-audit__table .orbyte-audit__empty {{ display: block; }}
            .orbyte-audit__empty td {{ display: block; }}
          }}
          @media (max-width: 360px) {{
            .orbyte-audit__table tr:not(.orbyte-audit__empty) {{ padding-inline: .68rem; }}
            .orbyte-audit__table td {{
              grid-template-columns: minmax(4.9rem, 31%) minmax(0, 1fr);
              gap: .5rem;
              font-size: .74rem;
            }}
          }}
        </style>
        <div class="orbyte-audit">
          <table class="orbyte-audit__table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{body}</tbody>
          </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
