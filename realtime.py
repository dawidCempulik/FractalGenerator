from __future__ import division
from OpenGL.GL import *
import numpy as np
import pygame
import textwrap
from PIL import Image

vertex_shader_source = textwrap.dedent(open("vertex.glsl", "r").read())

fragment_shader_source = textwrap.dedent(open("fragment.glsl", "r").read())


def load_program(vertex_source, fragment_source):
    vertex_shader = load_shader(GL_VERTEX_SHADER, vertex_source)
    if vertex_shader == 0:
        return 0

    fragment_shader = load_shader(GL_FRAGMENT_SHADER, fragment_source)
    if fragment_shader == 0:
        return 0

    program = glCreateProgram()

    if program == 0:
        return 0

    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)

    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS, None) == GL_FALSE:
        glDeleteProgram(program)
        return 0

    return program


def load_shader(shader_type, source):
    shader = glCreateShader(shader_type)

    if shader == 0:
        return 0

    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS, None) == GL_FALSE:
        info_log = glGetShaderInfoLog(shader)
        print(info_log)
        glDeleteProgram(shader)
        return 0

    return shader


def load_texture(width, height):
    img = Image.new("RGB", (width, height), (0, 0, 0))
    img_data = np.array(img, dtype=np.uint8)
    w, h = img.size

    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return texture


_vertices = [
    (-1.000000, 1.000000),
    (1.000000, 1.000000),
    (-1.000000, -1.000000),
    (1.000000, -1.000000),
]

_texcoords = [
    (-1.000000, 1.000000),
    (1.000000, 1.000000),
    (-1.000000, -1.000000),
    (1.000000, -1.000000),
]
_vertex_triangles = [
    (0, 1, 2),
    (1, 2, 3),
]

_texture_triangles = [
    (0, 1, 2),
    (1, 2, 3),
]

vertices = np.array([
    _vertices[index]
    for indices in _vertex_triangles
    for index in indices
])

texcoords = np.array([
    _texcoords[index]
    for indices in _texture_triangles
    for index in indices
])

if __name__ == "__main__":
    width, height = 1920, 1080
    pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL | pygame.HWSURFACE)

    glViewport(0, 0, width, height)
    view_matrix = np.identity(4, dtype=np.float32)
    view_matrix[-1, :-1] = (0, 0, -10)

    program = load_program(vertex_shader_source, fragment_shader_source)

    aVertex = glGetAttribLocation(program, "aVertex")

    glUseProgram(program)
    glEnableVertexAttribArray(aVertex)

    glUniform2f(glGetUniformLocation(program, "resolution"), width, height)

    texture = load_texture(width, height)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)

    running = True
    clock = pygame.time.Clock()

    pos = [0, -350]
    scale = 0.2

    posadd = [0, 0]
    scaleadd = 0
    scalefactor = 0.01

    while running:
        glClear(GL_COLOR_BUFFER_BIT)

        glVertexAttribPointer(aVertex, 2, GL_FLOAT, GL_FALSE, 0, vertices)

        glUniform2f(glGetUniformLocation(program, "pos"), pos[0], pos[1])
        glUniform1f(glGetUniformLocation(program, "scale"), scale)

        glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    posadd[1] = -1
                if event.key == pygame.K_s:
                    posadd[1] = 1
                if event.key == pygame.K_a:
                    posadd[0] = 1
                if event.key == pygame.K_d:
                    posadd[0] = -1

                if event.key == pygame.K_SPACE:
                    scaleadd = 1
                if event.key == pygame.K_LSHIFT:
                    scaleadd = -1

                if event.key == pygame.K_q:
                    scalefactor /= 10
                if event.key == pygame.K_e:
                    scalefactor *= 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    posadd[1] = 0
                if event.key == pygame.K_s:
                    posadd[1] = 0
                if event.key == pygame.K_a:
                    posadd[0] = 0
                if event.key == pygame.K_d:
                    posadd[0] = 0

                if event.key == pygame.K_SPACE:
                    scaleadd = 0
                if event.key == pygame.K_LSHIFT:
                    scaleadd = 0

        pos = [pos[0] + posadd[0] / scale, pos[1] + posadd[1] / scale]
        scale += scaleadd * scalefactor
