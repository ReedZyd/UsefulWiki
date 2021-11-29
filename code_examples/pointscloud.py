def pcwrite(xyz_pts, filename, rgb_pts=None):
    assert xyz_pts.shape[1] == 3, 'input XYZ points should be an Nx3 matrix'
    if rgb_pts is None:
        rgb_pts = np.ones(xyz_pts.shape).astype(np.uint8)*255
    assert xyz_pts.shape == rgb_pts.shape, 'input RGB colors should be Nx3 matrix and same size as input XYZ points'

    # Write header for .ply file
    with open(filename, 'w') as pc_file:
        pc_file.write('ply\n')
        pc_file.write("format ascii 1.0\n")
        pc_file.write("element vertex %d\n"%(xyz_pts.shape[0]))
        pc_file.write('property float x\n')
        pc_file.write('property float y\n')
        pc_file.write('property float z\n')
        pc_file.write('property uchar red\n')
        pc_file.write('property uchar green\n')
        pc_file.write('property uchar blue\n')
        pc_file.write('end_header\n')

        # Write 3D points to .ply file
        for i in range(xyz_pts.shape[0]):
            pc_file.write("%f %f %f %d %d %d\n"%(
            xyz_pts[i, 0], xyz_pts[i, 1], xyz_pts[i, 2],
            rgb_pts[i, 0], rgb_pts[i, 1], rgb_pts[i, 2],
            ))
