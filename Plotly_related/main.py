import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Mesh3d(
        # Order of vertex matters! in this case is: A-B-C-D-DRONE
        x=[3, 9, 1, 3, 0],
        y=[9, 3, 3, 1, 0],
        z=[0, 0, 0, 0, 6],
        colorbar_title='z',
        # i, j and k give the vertices of triangles
        # here we represent the 4 triangles of the tetrahedron surface
        i=[0, 0, 0, 1, 2, 0],
        j=[2, 1, 1, 3, 3, 2],
        k=[3, 3, 4, 4, 4, 4],
        name='y',
        showscale=True,
        opacity=0.40,
        color="#FF0000"
    )
])

fig.show()