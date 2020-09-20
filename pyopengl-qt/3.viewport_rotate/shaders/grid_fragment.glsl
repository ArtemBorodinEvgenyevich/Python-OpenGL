//fragment
#version 420 core

out vec4 fragColor;

sample smooth in vec2 f_TexCoord;
in vec3 f_vertexPos;

vec4 gridColor;

void main()
{
    //Main grid pattern
    if(fract(f_TexCoord.x / 0.0005f) < 0.025f || fract(f_TexCoord.y / 0.0005f) < 0.025f)
        gridColor = vec4(0.75, 0.75, 0.75, 1.0);
    else
        gridColor = vec4(0);
    // Check for alpha transparency
    if(gridColor.a != 1)
        discard;

    vec2 point_center = vec2(0.5, 0.5);
    float distance = length(f_TexCoord.xy - vec2(0.5, 0.5));
    gridColor *= mix(vec4(0.75, 0.75, 0.75, 1.0), vec4(0.25,0.25,0.25,1.), distance);

    fragColor = gridColor;
}
