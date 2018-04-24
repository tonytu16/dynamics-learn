from dynamics import *
from controllers import randController, MPController
from dynamics_ionocraft import IonoCraft
from utils_plot import *
from utils_data import *
from models import LeastSquares

# Plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


dt = .01
iono1 = IonoCraft(dt, x_noise = .001)

m = 67e-6
g = 9.81

mgo4 = m*g/4

x0 = np.zeros(12)
u0 = np.array([mgo4,mgo4,mgo4,mgo4]) #np.zeros(4)

x1 = iono1.simulate(x0,u0)
x2 = iono1.simulate(x1,u0)
print('Original Test Simulation Steps')
print(x1)
print(x2)
print('\n')

# Generate lightly rnadom trajectory for plotting
# t = 0.5
# n = int(t/dt)
# T = np.linspace(0,t,n+1)
# X = np.array([x0])
# for i in range(n):
#     u = np.array([mgo4,mgo4,mgo4,mgo4]) + np.random.normal(scale = .0000005, size=4)
#     x0 = X[-1]
#     xnew = iono1.simulate(x0,u)
#     X = np.append(X, [xnew],axis=0)

length = 25
rand1 = randController(iono1, variance = .000005)
X, U = generate_data(iono1, sequence_len=length, num_iter=100, controller = rand1)

X = np.array(X)
# Choose dimensions to optimize over eg is staying near origin
dim_to_eval = [0, 1, 2]
origin_xyz_norm = Objective(np.linalg.norm, maxORmin = 'min', dim = 3,  dim_to_eval = dim_to_eval, data=X)
min_idx = origin_xyz_norm.compute_ARGmm()
min_val = origin_xyz_norm.compute_mm()

print('TESTING ACTION GENERATION')
N = 50
T = 5
rand_controller = randController(iono1)
rrr = rand_controller.update()
actions = np.array([rand_controller.update() for i in range(N)])
actions_seq = np.dstack((actions,actions,actions))
a = actions
action_list = []
for i in range(T):
    action_list.append(actions)

actions_seq = np.dstack(action_list)
print(np.shape(np.swapaxes(actions_seq,1,2)))

print('_---___-_--_-____---')
print('\n')
# actions_seq = [np.dstack((actions,a)) for i in range(T)]


# actions_seq = np.repeat(actions,5,axis=2)
# print(np.shape(actions_seq))
lin1 = LeastSquares()
data = sequencesXU2array(X,U)
lin1.train(l2array(data[:,0]),l2array(data[:,1]),l2array(data[:,2]))

mpc1 = MPController(lin1, iono1, origin_xyz_norm)
hmm = mpc1.control(x0)
print(hmm)
# T = np.linspace(0,length*iono1.get_dt,length)
# # X = X[0]
# print(np.shape(X))
# print(np.shape(U))
# dim_x, _ = iono1.get_dims
#
# data_arr = l2array(data[:,0])
# # print(np.shape(data_arr))
# # delta = states_to_delta(X)
# print(np.shape(lin1.reg.coef_))
# lin1.train()

# plot12(X,T)
#
# plot_trajectory(X,T)

# quad = CrazyFlie(dt)