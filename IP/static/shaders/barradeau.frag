// ═══════════════════════════════════════════════════════════════════════════════
// BARRADEAU FRAGMENT SHADER
// ═══════════════════════════════════════════════════════════════════════════════
//
// Features:
// - Soft glow falloff (Barradeau style)
// - Circular particle with smooth edges
//
// Reference: void-phase0-buildings.html lines 1077-1121
// CONSTRAINT: Must work with canonical colors

varying float vOpacity;
varying float vDistance;

uniform vec3 color;
uniform float time; // For potential future use (NOT for breathing)

void main() {
    // Create circular point with soft falloff
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);
    
    // Soft edge falloff (Barradeau style)
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
    alpha *= vOpacity;
    
    // Add subtle glow
    float glow = exp(-dist * 3.0) * 0.5;
    
    vec3 finalColor = color + glow * color;
    
    // Discard transparent fragments for performance
    if (alpha < 0.01) discard;
    
    gl_FragColor = vec4(finalColor, alpha);
}
