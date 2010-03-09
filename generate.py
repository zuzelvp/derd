import pydot


if __name__ == '__main__':
    erd = pydot.Dot(graph_type='graph', bgcolor='transparent')
    student = pydot.Node('STUDENT', shape='box', style='filled', fillcolor='green')
    student_id = pydot.Node('STUDENT_ID', style='filled', fillcolor='green')
    student_name = pydot.Node('STUDENT_NAME', style='filled', fillcolor='green')
    major = pydot.Node('MAJOR', style='filled', fillcolor='pink')
    credits = pydot.Node('CREDITS', style='filled', fillcolor='green')
    student_2_student_id = pydot.Edge('STUDENT', 'STUDENT_ID')
    student_2_student_name = pydot.Edge('STUDENT', 'STUDENT_NAME')
    major_2_student = pydot.Edge('MAJOR', 'STUDENT', label=' = \'MATH\'')
    student_2_credits = pydot.Edge('STUDENT', 'CREDITS')
    erd.add_node(student)
    erd.add_node(student_id)
    erd.add_node(student_name)
    erd.add_node(major)
    erd.add_node(credits)
    erd.add_edge(student_2_student_id)
    erd.add_edge(student_2_student_name)
    erd.add_edge(major_2_student)
    erd.add_edge(student_2_credits)
    order = [major, major_2_student, student, student_2_student_name,
        student_name, student_2_student_id, student_id, student_2_credits,
        credits]
    for i, obj in enumerate(reversed(order)):
        erd.write_png('student%s.png' % (len(order) - i))
        obj.style = 'invis'
        obj.fontcolor = 'transparent'
    else:
        i += 1
        erd.write_png('student%s.png' % (len(order) - i))
