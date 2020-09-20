//vertex
#version 420 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

sample smooth out vec2 f_TexCoord;
out vec3 f_vertexPos;

uniform mat4 u_modelMatrix;
uniform mat4 u_viewMatrix;
uniform mat4 u_projectionMatrix;

void main()
{
    mat4 mv_matrix = u_viewMatrix * u_modelMatrix;

    gl_Position = u_projectionMatrix * mv_matrix * vec4(aPos, 1.0);
    f_TexCoord = aTexCoord;
    f_vertexPos = aPos;
}
