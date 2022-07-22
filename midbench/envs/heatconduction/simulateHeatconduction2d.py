import glob, os, sys
import time as tm
import numpy as np
import time as tm
from math import floor
with open(r"sim_var.txt", 'r') as fp:
    lines = fp.read()
    lines2=lines.split("\t")
NN = int(lines2[2])
step = 1.0/float(NN)
x_values = np.zeros((NN+1)) #horizontal dir (x(0))
y_values = np.zeros((NN+1)) #vertical dir (x(1))
x_values=np.linspace(0,1,num=NN+1)
y_values=np.linspace(0,1,num=NN+1)
max_run_it=floor(NN/200)+3
vol_f = float(lines2[0])
width = float(lines2[1])
os.system('rm sim_var.txt')
with open(r"sim_design.txt", 'r') as des:
    init_g = des.read()
    init_gu=init_g.split("\t")
init_guess=init_gu[0]
init_guess_size=int(init_gu[1])
os.system('rm sim_design.txt')
#Now set up and run optimization sets
from fenics import *
from fenics_adjoint import *
try:
    from pyadjoint import ipopt  # noqa: F401
except ImportError:
    print("""This example depends on IPOPT and Python ipopt bindings. \
    When compiling IPOPT, make sure to link against HSL, as it \
    is a necessity for practical problems.""")
    raise
for run_it in range(max_run_it):
    # turn off redundant output in parallel
    parameters["std_out_all_processes"] = False
    V = Constant(vol_f)  # volume bound on the control.   Default = 0.4
    p = Constant(5)  # power used in the solid isotropic material.  Default = 5
    eps = Constant(1.0e-3)  # epsilon used in the solid isotropic material
    alpha = Constant(1.0e-8)  # regularisation coefficient in functional


    def k(a):
        return eps + (1 - eps) * a ** p

    mesh = UnitSquareMesh(NN, NN)
    A = FunctionSpace(mesh, "CG", 1)  # function space for control
    P = FunctionSpace(mesh, "CG", 1)  # function space for solution

    lb_2 = 0.5 - width/2; #lower bound on section of bottom face which is adiabatic
    ub_2 = 0.5 + width/2; #Upper bound on section of bottom face which is adiabatic

    class WestNorth(SubDomain):

        def inside(self, x, on_boundary):
            return (x[0] == 0.0 or x[1] == 1.0 or x[0] == 1.0 or ( x[1] == 0.0 and  (x[0] < lb_2 or x[0] > ub_2)  )  ) # modified from Fuge
    T_bc = 0.0;
    bc = [DirichletBC(P, T_bc, WestNorth())]
    f_val = 1.0e-2 #Default = 1.0e-2
    f = interpolate(Constant(f_val), P)  # the volume source term for the PDE


    def forward(a):
        """Solve the forward problem for a given material distribution a(x)."""
        T = Function(P, name="Temperature")
        v = TestFunction(P)
        F = inner(grad(v), k(a) * grad(T)) * dx - f * v * dx
        solve(F == 0, T, bc, solver_parameters={"newton_solver": {"absolute_tolerance": 1.0e-7,"maximum_iterations": 20}})
        return T
    if __name__ == "__main__":
        if run_it==0:
            s_xmdf=init_guess
            mesh1a=UnitSquareMesh(init_guess_size, init_guess_size)
        else:
            s_xmdf="./midbench/envs/heatconduction/RES/TEMP.xdmf"
            mesh1a=UnitSquareMesh(NN, NN)
        #Adapted from https://fenicsproject.discourse.group/t/read-mesh-from-xdmf-file-write-checkpoint/3458/3
        #mesh1 = UnitSquareMesh(NN, NN)
        V1 =  FunctionSpace(mesh1a, "CG", 1)
        sol = Function(V1)
        with XDMFFile(s_xmdf) as infile:
            #infile.read(mesh1)
            infile.read_checkpoint(sol, "u")
        MM = sol
        a = interpolate(MM, A)  # initial guess.
        T = forward(a)  # solve the forward problem once.
        controls = File("./midbench/envs/heatconduction/RES/control_iterations"+str(run_it)+".pvd")
        a_viz = Function(A, name="ControlVisualisation")
    J = assemble(f * T * dx + alpha * inner(grad(a), grad(a)) * dx)
    J_CONTROL=Control(J)
    m = Control(a)
    Jhat = ReducedFunctional(J, m)
    lb = 0.0
    ub = 1.0
    class VolumeConstraint(InequalityConstraint):

        def __init__(self, V):
            self.V = float(V)
            self.smass = assemble(TestFunction(A) * Constant(1) * dx)
            self.tmpvec = Function(A)

        def function(self, m):
            from pyadjoint.reduced_functional_numpy import set_local
            set_local(self.tmpvec, m)
            integral = self.smass.inner(self.tmpvec.vector())
            if MPI.rank(MPI.comm_world) == 0:
                #print("Current control integral: ", integral)
                return [self.V - integral]

        def jacobian(self, m):
            return [-self.smass]

        def output_workspace(self):
            return [0.0]

        def length(self):
            """Return the number of components in the constraint vector (here, one)."""
            return 1
    problem = MinimizationProblem(Jhat, bounds=(lb, ub), constraints=VolumeConstraint(V))

    parameters = {"acceptable_tol": 1.0e-3, "maximum_iterations": 100}
    solver = IPOPTSolver(problem, parameters=parameters)
    a_opt = solver.solve()

    mesh1 = UnitSquareMesh(NN, NN)
    V1 =  FunctionSpace(mesh1, "CG", 1)
    sol1 = a_opt
    with XDMFFile("./midbench/envs/heatconduction/RES/TEMP.xdmf") as outfile:
        outfile.write(mesh1)
        outfile.write_checkpoint(sol1, "u", 0, append=True)



    #-------------------------------------------------------------------------------------------
    #Discretize results

    if run_it==max_run_it-1: #if final run reached

        #Now store the results of this run (x,y,v,w,a)
        results = np.zeros(((NN+1)**2,5))
        ind = 0
        for xs in x_values:
            for ys in y_values:
                results[ind,0] = xs
                results[ind,1] = ys
                results[ind,2] = vol_f
                results[ind,3] = width
                results[ind,4] = a_opt(xs,ys)
                ind = ind+1
        #Naming convention: hr_data_v=0.5_w=0.5_.npy, for example
        filename = "./midbench/envs/heatconduction/RES/hr_data_v="+str(vol_f)+"_w="+str(width)+"_.npy"
        np.save(filename,results)
        xdmf_filename = XDMFFile(MPI.comm_world, "./midbench/envs/heatconduction/RES/final_solution_v="+str(vol_f)+"_w="+str(width)+"_.xdmf")
        xdmf_filename.write(a_opt)
        print("v="+ "{}".format(vol_f))
        print("w="+ "{}".format(width))
        with open('./midbench/envs/heatconduction/RES/Performance.txt', 'w') as f:
            f.write('%.14f'%J_CONTROL.tape_value())
            f.close()
        os.system('rm ./midbench/envs/heatconduction/RES/TEMP*')     
