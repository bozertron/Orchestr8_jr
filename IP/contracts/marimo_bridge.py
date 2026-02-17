"""Shared marimo DOM bridge helpers for JS/Python event channels."""

from __future__ import annotations


def build_marimo_bridge_runtime_js(namespace: str = "__orchestr8Bridge") -> str:
    """Return JS runtime helpers for marimo bridge input resolution."""
    ns = (namespace or "__orchestr8Bridge").replace('"', "").strip()
    if not ns:
        ns = "__orchestr8Bridge"

    return f"""
(function(global) {{
    const key = "{ns}";
    if (global[key]) return;

    function resolveBridgeInput(bridgeId) {{
        const direct = document.querySelector(
            `marimo-ui-element[object-id="${{bridgeId}}"] input, marimo-ui-element[object-id="${{bridgeId}}"] textarea`
        );
        if (direct) return direct;

        const hosts = document.querySelectorAll(
            `marimo-ui-element[object-id="${{bridgeId}}"], marimo-ui-element[data-object-id="${{bridgeId}}"], [object-id="${{bridgeId}}"]`
        );
        for (const host of hosts) {{
            const localInput = host.querySelector?.("input, textarea");
            if (localInput) return localInput;
            const shadowInput = host.shadowRoot?.querySelector?.("input, textarea");
            if (shadowInput) return shadowInput;
        }}
        return null;
    }}

    function writePayloadToBridge(bridgeId, payload, label) {{
        const bridgeInput = resolveBridgeInput(bridgeId);
        if (!bridgeInput) {{
            console.error((label || "Bridge") + " bridge element not found", {{ bridgeId }});
            return false;
        }}
        bridgeInput.value = JSON.stringify(payload);
        bridgeInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
        return true;
    }}

    global[key] = {{
        resolveBridgeInput,
        writePayloadToBridge,
    }};
}})(window);
""".strip()
