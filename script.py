import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    edges = []
    step = 0.1
    for command in commands:
        #print command
        if command[0] == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(edges,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(edges,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'box':
            #print 'BOX\t' + str(args)
            add_box(edges,
                    float(command[1]), float(command[2]), float(command[3]),
                    float(command[4]), float(command[5]), float(command[6]))
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)

        elif command[0] == 'hermite' or command[0] == 'bezier':
            #print 'curve\t' + command[0] + ": " + str(args)
            add_curve(edges,
                      float(command[1]), float(command[2]),
                      float(command[3]), float(command[4]),
                      float(command[5]), float(command[6]),
                      float(command[7]), float(command[8]),
                      step, command[0])

        elif command[0] == 'line':
            #print 'command[0]\t' + str(args)
            add_edge( edges,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), float(command[6]) )

        elif command[0] == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t ]

        elif command[0] == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t ]


        elif command[0] == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(command[2]) * (math.pi / 180)

            if command[1] == 'x':
                t = make_rotX(theta)
            elif command[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t ]

        elif command[0] == 'clear':
            edges = []

        elif command[0] == 'ident':
            ident(transform)

        elif command[0] == 'apply':
            matrix_mult( transform, edges )

        elif command[0] == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif command[0] == 'pop':
            stack.pop()

        elif command[0] == 'display' or command[0] == 'save':
            if command[0] == 'display':
                display(screen)
            else:
                save_extension(screen, command[1])
