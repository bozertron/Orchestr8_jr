import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def imports():
    """Import styling dependencies for testing"""
    import marimo as mo
    from IP.styles.font_injection import get_complete_head_injection
    from IP.plugins.status_helpers import (
        status_badge,
        fiefdom_indicator,
        status_icon,
        styled_status_text,
        progress_bar,
    )
    from IP.mermaid_theme import (
        generate_status_graph,
        generate_file_dependency_graph,
        generate_system_architecture,
        generate_workflow_steps,
    )

    return (
        fiefdom_indicator,
        generate_file_dependency_graph,
        generate_status_graph,
        generate_system_architecture,
        generate_workflow_steps,
        get_complete_head_injection,
        mo,
        progress_bar,
        status_badge,
        status_icon,
        styled_status_text,
    )


@app.cell
def font_injection_test(get_complete_head_injection, mo):
    """Test font injection HTML"""
    font_html = mo.Html(get_complete_head_injection())
    return (font_html,)


@app.cell
def color_swatches(mo):
    """Display all color variables as swatches"""
    colors = [
        ("Gold Metallic", "#D4AF37"),
        ("Gold Dark", "#B8860B"),
        ("Gold Saffron", "#F4C430"),
        ("Blue Dominant", "#1fbdea"),
        ("Purple Combat", "#9D4EDD"),
        ("Background Primary", "#0A0A0B"),
        ("Background Elevated", "#121214"),
        ("Background Surface", "#1a1a1c"),
        ("Text Primary", "#e8e8e8"),
        ("Text Secondary", "#a0a0a0"),
        ("Text Muted", "#666666"),
    ]

    swatch_html = "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;'>"
    for name, color in colors:
        swatch_html += f"""
        <div style="
            background-color: var(--bg-elevated);
            border: 1px solid var(--gold-dark);
            padding: 1rem;
            border-radius: 4px;
        ">
            <div style="
                width: 100%;
                height: 40px;
                background-color: {color};
                border: 1px solid rgba(255,255,255,0.1);
                margin-bottom: 0.5rem;
            "></div>
            <div style="font-family: var(--font-mono); font-size: 0.9rem; color: var(--text-primary);">
                <strong>{name}</strong><br>
                {color}
            </div>
        </div>
        """
    swatch_html += "</div>"

    color_display = mo.Html(swatch_html)
    return color_display, colors


@app.cell
def button_states_test(mo):
    """Test all button states with gold theme"""
    buttons_html = """
    <div style="padding: 2rem; background-color: var(--bg-primary);">
        <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Button States</h3>
        
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
            <button>Default Button</button>
            <button style="background-color: var(--gold-metallic); color: var(--bg-primary);">Hover/Fill</button>
            <button style="background-color: var(--gold-saffron); border-color: var(--gold-saffron);">Active</button>
        </div>
    </div>
    """
    buttons_display = mo.Html(buttons_html)
    return (buttons_display,)


@app.cell
def status_badges_test(status_badge, mo):
    """Test all status badge types"""
    badges_html = """
    <div style="padding: 2rem; background-color: var(--bg-primary);">
        <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Status Badges</h3>
        
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
    """

    statuses = [
        "working",
        "broken",
        "combat",
        "normal",
        "warning",
        "complex",
        "error",
        "unknown",
    ]
    for status in statuses:
        badges_html += status_badge(status) + "\n"

    badges_html += """
        </div>
    </div>
    """

    badges_display = mo.Html(badges_html)
    return (badges_display,)


@app.cell
def status_indicators_test(fiefdom_indicator, status_icon, mo):
    """Test status indicators and icons"""
    indicators_html = """
    <div style="padding: 2rem; background-color: var(--bg-primary);">
        <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Status Indicators & Icons</h3>
        
        <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
    """

    statuses = ["working", "broken", "combat", "normal", "warning", "complex", "error"]
    for status in statuses:
        indicators_html += f"""
        <div style="text-align: center; padding: 1rem;">
            <div>{fiefdom_indicator(status)}</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">{status.upper()}</div>
            <div style="color: var(--text-secondary); font-size: 1.2rem; margin-top: 0.25rem;">{status_icon(status)}</div>
        </div>
        """

    indicators_html += """
        </div>
    </div>
    """

    indicators_display = mo.Html(indicators_html)
    return (indicators_display,)


@app.cell
def progress_bars_test(progress_bar, mo):
    """Test progress bars with different statuses"""
    progress_html = """
    <div style="padding: 2rem; background-color: var(--bg-primary);">
        <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Progress Bars</h3>
        
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
    """

    test_cases = [
        (25, 100, "working"),
        (50, 100, "broken"),
        (75, 100, "combat"),
        (100, 100, "working"),
        (10, 50, "error"),
    ]

    for current, total, status in test_cases:
        progress_html += f"""
        <div>
            <div style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                {current}/{total} - {status.upper()}
            </div>
            {progress_bar(current, total, status)}
        </div>
        """

    progress_html += """
        </div>
    </div>
    """

    progress_display = mo.Html(progress_html)
    return (progress_display,)


@app.cell
def mermaid_graph_test(mo, generate_status_graph):
    """Test Mermaid graph generation with proper colors"""
    sample_fiefdoms = {
        "src/llm": {"status": "working", "depends_on": []},
        "src/modules": {"status": "broken", "depends_on": ["src/llm"]},
        "src/utils": {"status": "combat", "depends_on": ["src/modules"]},
        "tests": {"status": "working", "depends_on": ["src/modules", "src/utils"]},
        "docs": {"status": "working", "depends_on": []},
    }

    mermaid_code = generate_status_graph(sample_fiefdoms)

    mermaid_html = f"""
    <div style="padding: 2rem; background-color: var(--bg-primary);">
        <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Mermaid Graph Test</h3>
        
        <div class="mermaid">
            {mermaid_code}
        </div>
    </div>
    """

    mermaid_display = mo.Html(mermaid_html)
    return mermaid_display, sample_fiefdoms


@app.cell
def input_fields_test(mo):
    """Test input field styling"""
    inputs_html = """
    <div style="padding: 2rem; background-color: var(--bg-primary);">
        <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Input Fields</h3>
        
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <input type="text" placeholder="Text input" value="Sample text">
            <textarea placeholder="Text area">Sample multi-line text</textarea>
            <select>
                <option>Option 1</option>
                <option>Option 2</option>
                <option selected>Selected option</option>
            </select>
            <input type="text" placeholder="Focused input" style="border-color: var(--gold-metallic); box-shadow: 0 0 0 1px var(--gold-metallic);">
        </div>
    </div>
    """

    inputs_display = mo.Html(inputs_html)
    return (inputs_display,)


@app.cell
def main_layout(
    mo,
    color_display,
    buttons_display,
    badges_display,
    indicators_display,
    progress_display,
    mermaid_display,
    inputs_display,
):
    """Main layout for style testing"""
    tabs = mo.ui.tabs(
        {
            "Colors": color_display,
            "Buttons": buttons_display,
            "Badges": badges_display,
            "Indicators": indicators_display,
            "Progress": progress_display,
            "Mermaid": mermaid_display,
            "Inputs": inputs_display,
        }
    )

    layout = mo.vstack(
        [
            mo.md("# Orchestr8 Style Testing"),
            mo.md(
                "This notebook tests all styling components and color schemes from the MaestroView.vue design system."
            ),
            tabs,
        ]
    )
    return (layout,)


if __name__ == "__main__":
    app.run()
