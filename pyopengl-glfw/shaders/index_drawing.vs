# version 440

layout(location = 0) in vec3 a_position;

out vec3 v_color;

void main()
{
    gl_Position = vec4(a_position, 1.0);
}