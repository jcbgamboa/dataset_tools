# Defines several types of regression for me to play with

def polynomial_regression(polynomial_degree, X, y):
    # Polynomial Regression
    # X.shape = (20, 1)
    # y.shape = (20,)

    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import Ridge

    model = make_pipeline(PolynomialFeatures(polynomial_degree), Ridge())
    model.fit(X, y)

    # Then you can use
    # y_hat = model.predict(X_test)
    # e.g., to predict the values for 0 and 1:
    # model.predict([[0], [1]])
    return model

def kernel_ridge_regression(X, y):
    # Kernel Ridge regression
    # X.shape = (10, 1)
    # y.shape = (10,)
    # Notice that X could have more features. E.g., (10, 5)

    from sklearn.kernel_ridge import KernelRidge

    model = KernelRidge(alpha=1.0)
    model.fit(X, y)

    # See `polynomial_regression` for how to use it
    return model

def support_vector_regression(X, y):
    from sklearn.svm import SVR
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    model.fit(X, y)
    return model

