def draw_heatmap(img_path, means, sigmas, weights, objects, width, height, output_path, gt=None):
    def transparent_cmap(cmap, N=255):
        "Copy colormap and set alpha values"
        mycmap = cmap
        mycmap._init()
        mycmap._lut[:, -1] = np.clip(np.linspace(0, 1.0, N + 4), 0, 1.0)
        return mycmap

    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    # draw history
    tranparency = {0: 0.2, 1: 0.5, 2: 1.0}
    for i in range(3):
        overlay = img.copy()
        cv2.rectangle(overlay, (int(objects[i, 0, 0, 0, 0]), int(objects[i, 0, 0, 1, 0])),
                      (int(objects[i, 0, 0, 2, 0]), int(objects[i, 0, 0, 3, 0])), (255, 0, 0), -1)
        img = cv2.addWeighted(overlay, tranparency[i], img, 1 - tranparency[i], 0)

    gt_width = gt[0, 0, 2, 0] - gt[0, 0, 0, 0]
    gt_height = gt[0, 0, 3, 0] - gt[0, 0, 1, 0]
    mapped_means = []
    mapped_sigmas = []
    for i in range(len(means)):
        center_mean = means[i][:, 0:2, :, :] + [gt_width/2, gt_height/2]
        center_sigma = sigmas[i][:, 0:2, :, :]
        mapped_means.append(center_mean)
        mapped_sigmas.append(center_sigma)

    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    X, Y = np.meshgrid(x, y)
    XX = np.array([X.ravel(), Y.ravel()]).T
    if gt is not None:
        cv2.rectangle(img, (int(gt[0, 0, 0, 0]), int(gt[0, 0, 1, 0])),
                      (int(gt[0, 0, 2, 0]), int(gt[0, 0, 3, 0])), (255, 0, 255), -1)

    # construct the GMM
    c_means = np.stack([mapped_means[i][0,0:2,0,0] for i in range(len(mapped_means))], axis=0)  # (4,2)
    c_sigmas = np.stack([mapped_sigmas[i][0,0:2,0,0] for i in range(len(mapped_sigmas))], axis=0)  # (4,2)
    c_weights = np.concatenate(weights, axis=0)[:,0,0,0]  # (4)

    clf = mixture.GaussianMixture(n_components=4, covariance_type='diag')
    var = c_sigmas * c_sigmas * 2
    precisions_cholesky = _compute_precision_cholesky(var, 'diag')
    clf.weights_ = c_weights
    clf.means_ = c_means
    clf.precisions_cholesky_ = precisions_cholesky
    clf.covariances_ = var

    Z = np.exp(clf.score_samples(XX))

    Z = Z.reshape(X.shape)

    vmax = np.max(Z)
    vmin = np.min(Z)
    plt.imshow(img)
    plt.contourf(X, Y, Z, cmap=transparent_cmap(plt.cm.jet), vmin=vmin, vmax=vmax)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.clf()

    from scipy.stats import multivariate_normal
def gauss_fun(X, Y):
    mux = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
    muy = [1.2, 1.7, 2.2, 2.7, 3.2, 3.7]
    sx = [0.5, 0.6, 0.65, 0.55, 0.7, 0.8]
    sy = [1.0, 1.2, 1.2, 1.15, 0.9, 0.8]
    rho = [0.1, 0.2, 0.2, 0.19, 0.2, 0.2]
    d = np.dstack([X, Y])
    z = None
    for i in range(len(mux)):
        mean = [mux[i], muy[i]]
        # Extract covariance matrix
        cov = [[sx[i] * sx[i], rho[i] * sx[i] * sy[i]], [rho[i] * sx[i] * sy[i], sy[i] * sy[i]]]
        gaussian = multivariate_normal(mean = mean, cov = cov)
        z_ret = gaussian.pdf(d)
        if z is None:
            z = z_ret
        else:
            z += z_ret
    return z
