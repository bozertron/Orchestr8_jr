// ═══════════════════════════════════════════════════════════════════════════════
// BARRADEAU VERTEX SHADER
// ═══════════════════════════════════════════════════════════════════════════════
// 
// Features:
// - Size attenuation based on camera distance
// - Opacity from layer (higher layers = more transparent)
// - Position from BuildingData
//
// CONSTRAINT: NO sin/cos oscillation (no breathing)
// Things EMERGE, not animate.

attribute float size;
attribute float opacity;

varying float vOpacity;
varying float vDistance;

void main() {
    vOpacity = opacity;
    
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    vDistance = -mvPosition.z;
    
    // Size attenuation: closer = larger
    gl_PointSize = size * (300.0 / vDistance);
    gl_PointSize = clamp(gl_PointSize, 1.0, 50.0);
    
    gl_Position = projectionMatrix * mvPosition;
}
