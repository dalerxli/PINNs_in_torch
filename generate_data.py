import torch 
import torch.nn as nn
import torch.autograd as autograd
import numpy as np
import time

from copy import copy

# tag: -1 for ICs, 0 for BCs, 1 for domain
# solve u_t + u*u_x - (0.01/pi)u_xx = 0, -1 <= x <= 1, 0 <= t <= 1
# u(0, x) = -sin(pi * x), u(t, -1) = u(t, 1) = 0

def make_tensor(x, requires_grad=True):
    t = torch.from_numpy(x)
    t.requires_grad=requires_grad
    t = t.float()
    return t

def make_training_initial_data(i_size):
    
    x_i = np.random.uniform(low=-1.0, high=1.0, size=(i_size, 1))
    u_i = make_tensor(-np.sin(np.pi * x_i))
    t_i = make_tensor(np.zeros((i_size, 1)))
    x_i = make_tensor(x_i)
    tag = make_tensor(np.ones((i_size, 1)) * -1, requires_grad=False)

    return [torch.cat([x_i, t_i], axis=1), u_i, tag]

def make_training_boundary_data(b_size):
    x_b = make_tensor(np.vstack(((-1) * np.ones((b_size // 2, 1)), np.ones((b_size - b_size // 2, 1)))))
    t_b = make_tensor(np.random.uniform(low=0.0, high=1.0, size=(b_size, 1)))
    u_b = make_tensor(np.zeros((b_size, 1)))
    tag = make_tensor(np.ones((b_size, 1)) * 0)

    return [torch.cat([x_b, t_b], axis=1), u_b, tag]

def make_training_domain_data(f_size):
    x_f = make_tensor(np.random.uniform(low=-1.0, high=1.0, size=(f_size, 1)))
    t_f = make_tensor(np.random.uniform(low=0.0, high=1.0, size=(f_size, 1)))
    u_f = make_tensor(np.zeros((f_size, 1)))
    tag = make_tensor(np.ones((f_size, 1)) * 1)

    return [torch.cat([x_f, t_f], axis=1), u_f, tag]

def generate_data(i_size, b_size, f_size):
    i_set = make_training_initial_data(i_size)
    b_set = make_training_boundary_data(b_size)
    f_set = make_training_domain_data(f_size)

    return i_set, b_set, f_set
    


