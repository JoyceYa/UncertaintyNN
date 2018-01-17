from data import sample_generators

import numpy as np
import plotting

from training.mixture_training import mixture_training


def mixture_evaluation(x, y, dropout, learning_rate, epochs, n_mixtures):
    sess, x_placeholder, dropout_placeholder = \
        mixture_training(x, y, dropout, learning_rate, epochs, n_mixtures)

    prediction_op = sess.graph.get_collection("prediction")
    uncertainty_op = sess.graph.get_collection("uncertainties")
    gmm_op = sess.graph.get_collection("gmm")

    x_eval = np.linspace(1.1 * np.min(x), 1.1 * np.max(x), 100).reshape([-1, 1])
    feed_dict = {x_placeholder: x_eval,
                 dropout_placeholder: 0}

    y_eval, uncertainties_eval = sess.run([prediction_op, uncertainty_op], feed_dict)
    y_eval = y_eval[0].flatten()

    aleatoric_eval, epistemic_eval = uncertainties_eval[0]
    total_uncertainty_eval = aleatoric_eval + epistemic_eval

    fig, ax, = plotting.plot_mean_vs_truth(x, y,
                                           x_eval, y_eval, total_uncertainty_eval)

    return fig, ax


def mixture_osband_sin_evaluation(dropout, learning_rate, epochs, n_mixtures):
    x, y = sample_generators.generate_osband_sin_samples()
    fig, ax = mixture_evaluation(x, y, dropout, learning_rate, epochs, n_mixtures)
    return fig, ax


def mixture_osband_nonlinear_evaluation(dropout, learning_rate, epochs, n_mixtures):
    x, y = sample_generators.generate_osband_nonlinear_samples()
    fig, ax = mixture_evaluation(x, y, dropout, learning_rate, epochs, n_mixtures)
    return fig, ax


if __name__ == "__main__":
    # f, a = mixture_osband_sin_evaluation(0.3, 1e-3, n_mixtures=5, epochs=10000)
    f, a = mixture_osband_nonlinear_evaluation(0.3, 1e-4, n_mixtures=10, epochs=20000)
    from IPython import embed
    embed()



