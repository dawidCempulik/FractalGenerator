#version 330 core
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif

uniform vec2 resolution;
uniform vec2 pos;
uniform float scale;

#define MAX_ITERATIONS 400

int get_iterations()
{
    float real = (gl_FragCoord.x / resolution.x - 0.5) / scale - pos.x / 100f;
    float imag = (gl_FragCoord.y / resolution.x - 1.0) / scale - pos.y / 100f;

    int iterations = 0;
    float const_real = real;
    float const_imag = imag;

    while (iterations < MAX_ITERATIONS)
    {
        float tmp_real = real;
        real = (real * real - imag * imag) + const_real;
        imag = (2.0 * tmp_real * imag) + const_imag;

        float dist = real * real + imag * imag;

        if (dist > 4.0)
        break;

        ++iterations;
    }
    return iterations;
}

vec4 return_color()
{
    int iter = get_iterations();
    if (iter == MAX_ITERATIONS)
    {
        return vec4(0.0, 0.0, 0.0, 1.0);
    }

    float iterations = float(iter) / float(MAX_ITERATIONS);
    return vec4(0.0, iterations, 0.0, 1.0);
}

void main(void) {
    gl_FragColor = return_color();
    //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}