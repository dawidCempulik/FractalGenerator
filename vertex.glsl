#version 460
in vec3 aVertex;
//attribute vec2 aTexCoord;

//varying vec2 resolution;

void main()
{
    //vTexCoord = aTexCoord;
    gl_Position = vec4(aVertex.xyz, 1.0);
}