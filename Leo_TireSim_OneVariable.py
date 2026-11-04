import json 
import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as irr
import errno
import os
import math as m
import numpy as np
import scipy as sp
import pymc as pm
import matplotlib.pyplot as plt
import pytensor.tensor as tt
import arviz as az
# =============================================================================
debug_output = False
veh.SetVehicleDataPath(chrono.GetChronoDataPath() + 'vehicle/')
tire_json = veh.GetVehicleDataFile("hmmwv/tire/HMMWV_MBTire_modified.json") # modified tire file
#tire_json = veh.GetVehicleDataFile("hmmwv/tire/HMMWV_MBTire.json")
wheel_json = veh.GetVehicleDataFile("hmmwv/wheel/HMMWV_Wheel.json")
surface_type = veh.ChTire.ContactSurfaceType_NODE_CLOUD # Tire contact model (nodes or faces)
test_mode = veh.ChTireStaticTestRig.Mode_TEST_R # Test mode
collision_family = 7
surface_dim = 0.0
# ======================= Set the simulation parameters =======================
'''
parameters_bend = 5e4
division = 200
LoadSpeed = 0.005
step_size = 1e-6
pressure = 9e5
'''

parameters_bend = 1e4
division = 40
LoadSpeed = 0.005
step_size = 10e-6
pressure = 9e5
     
# ------------------------------- Data --------------------------------
#data         = [0.0082, 0.0121, 0.0160, 0.0196, 0.0233,  0.027, 0.0305, 0.0340, 0.0365, 0.0365]
#Load_list_kg = [ 902.9, 1358.7, 1812.3, 2251.1, 2704.5, 3165.8, 3614.3, 4069.9, 4501.1, 4509.8]

#data         = [0.0121, 0.0160, 0.0196]
#Load_list_kg = [1358.7, 1812.3, 2251.1]

data         = [0.0121]
Load_list_kg = [1358.7]


data_np = np.array(data)
# -------------------------------- Saving mechanisms ------------------ 
Load_list_N = [x * 9.8 for x in Load_list_kg]


def simulation(parameters_test):

    FLAG_LIST = [0] * len(Load_list_kg)
    # parameters = [5e5, 1e3, 5e5, 1e3, 5e5, 1e3, 5e4] # all included, but used only the last one 

    global surface_type, test_mode, collision_family, surface_dim # parameters for the simulation of the set 
    global step_size, LoadSpeed, Load_list_N, pressure, division # nonchageble parameters

    Result_array_all = []
    Result_array = []
    # -------------------------------- Rewrite the JSON file  ------------------
    with open(tire_json, 'r') as f: # Open and load JSON content
        tire_json_data = json.load(f)
    '''
    tire_json_data["Default Pressure"] = pressure
    tire_json_data["Geometry"]["Number Divisions"] = division
    tire_json_data["Spring Properties"]["Radial"][0] = parameters[0]
    tire_json_data["Spring Properties"]["Radial"][1] = parameters[1]
    tire_json_data["Spring Properties"]["Circumferential"][0] = parameters[2]    
    tire_json_data["Spring Properties"]["Circumferential"][1] = parameters[3]    
    tire_json_data["Spring Properties"]["Transversal"][0] = parameters[4]
    tire_json_data["Spring Properties"]["Transversal"][1] = parameters[5]
    '''

    tire_json_data["Spring Properties"]["Bending"][0] = parameters_test

    with open(tire_json, 'w') as f: # Save back to file (overwrite)
        json.dump(tire_json_data, f, indent=2)

    tire = veh.ReadTireJSON(tire_json)

    disp = 0 
    
    wheel = veh.ReadWheelJSON(wheel_json)
    # Set tire contact surface1
    tire.SetContactSurfaceType(surface_type, surface_dim, collision_family)
    sys = chrono.ChSystemSMC()
    sys.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)
    tire.SetStepsize(step_size)
    sys.SetSolverType(chrono.ChSolver.Type_PSOR)
    sys.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_PROJECTED)

    num_threads_chrono = 4     # Number of OpenMP threads used in Chrono (SCM ray-casting and FEA)
    num_threads_collision = 4  # Number of threads used in collision detection
    num_threads_eigen = 1      # Number of threads used by Eigen
    num_threads_pardiso = 4    # Number of threads used by PardisoMKL
    sys.SetNumThreads(num_threads_chrono, num_threads_collision, num_threads_eigen)

    # print("Create test rig")
    rig = veh.ChTireStaticTestRig(wheel, tire, sys)
    rig.SetGravitationalAcceleration(9.8)
    # Set tire options
    rig.SetTireStepsize(step_size)
    rig.SetTireVisualizationType(chrono.VisualizationType_MESH)
    # Set rig options
    rig.SetPlateMaterialProperties(0.8, 0, 2e7)
    # Set test parameters
    rig.SetNominalRadialLoad(1000000000) # just not to leave the programm to quickly
    rig.SetStateTransitionDelay(0.2)
    rig.SetRadialLoadSpeed(LoadSpeed)
    rig.SetLongitudinalLoadSpeed(0.1)
    rig.SetLateralLoadSpeed(0.1)
    rig.SetTorsionalLoadSpeed(0.1)

    # Initialize the tire test rig
    rig.Initialize(test_mode)

    # ---------------
    # Simulation loop
    # ---------------

    # Timers and counters
    timer = chrono.ChTimer() # timer for measuring total run time
    time = 0                 # simulated time
    sim_time = 0             # simulation time
    fps = 120                # rendering frequency
    render_frame = 0         # render frame counter

    timer.start()
    fl = 0
    i = 0
    simulation = True 
    state = rig.GetState()
    
    while simulation:    

        time = sys.GetChTime()

        state = rig.GetState()      

        if state == 2 and fl == 0: # If the tire is in contact with the plate, set the reference position
           fl = 1 # fix the reference position at the first contact only
           m_spindle_z_ref = rig.GetWheelPos().z

        if state > 1:
            disp = m_spindle_z_ref - rig.GetWheelPos().z  
            
        currentLoad = rig.GetLoad()   

        if m.isnan(currentLoad):
            print("Load is NaN, stopping simulation.")
            break

        # print(" load: ", currentLoad, " state: ", state)  # Print the Z position of the spindle    
                
        if currentLoad > Load_list_N[i] and FLAG_LIST[i] == 0 and state != 1 and disp>0.002:
            FLAG_LIST[i] = 1
            Result_array.append(round(disp,5))
            Result_array_all.append((round(currentLoad,2), round(disp,5)))
            i += 1

        if sum(FLAG_LIST) == len(FLAG_LIST):
            break

        rig.Advance(step_size)
        sim_time = sim_time + sys.GetTimerStep()    

    timer.stop()
    step_time = timer.GetTimeSeconds()

    return np.array(Result_array)


'''  
# Simple run to check
res = simulation(parameters_bend)
print("Simulation result:", res)
print("Data:", data_np)
print("mod.shape =", res.shape)
print("data.shape =", data_np.shape)
'''

# Gaussian log likelihood
def loglike(theta,data):
	
	# Data collection 
    n = data.shape[0]  

    sigmas_2 = theta[-1]**2
    mod = simulation(theta[0])  
    
    # log-likelihood
    norm_factor = np.linalg.norm(data)  # scalar 
    squared_error = (mod - data) ** 2   # squared differences
    log_values =  -np.sum(((n*np.log(2*np.pi * sigmas_2) /2) + np.sum(squared_error/(2.*sigmas_2)))/norm_factor)
    return log_values

#The gradient of the log likelihood using finite differences
def grad_loglike(theta,data):
	def ll(theta,data):
		return loglike(theta,data)
	
	#We are not doing finite difference approximation and we define delx as the finite precision 
	eps = np.sqrt(np.finfo(float).eps)
	delx = eps * np.sqrt(np.abs(theta) )

	return sp.optimize.approx_fprime(theta,ll,delx,data)

# Likelihood function
class LogLike(tt.Op):
	itypes = [tt.dvector] # expects a vector of parameter values when called
	otypes = [tt.dscalar] # outputs a single scalar value (the log likelihood)

	def __init__(self, loglike, data):

		# add inputs as class attributes
		self.likelihood = loglike
		self.data = data
		self.loglike_grad = LoglikeGrad(self.data)

	def perform(self, node, inputs, outputs):
		# the method that is used when calling the Op
		theta, = inputs  # this will contain my variables

		# call the log-likelihood function
		logp = self.likelihood(theta,self.data)

		outputs[0][0] = np.array(logp) # output the log-likelihood

	def grad(self,inputs,grad_outputs):
		theta, = inputs
		grads = self.loglike_grad(theta)
		return [grad_outputs[0] * grads]

#Similarly wrapper class for loglike gradient
class LoglikeGrad(tt.Op):
	itypes = [tt.dvector]
	otypes = [tt.dvector]

	def __init__(self,data):
		self.der_likelihood = grad_loglike
		self.data = data

	def perform(self, node, inputs, outputs):
		(theta,) = inputs
		grads = self.der_likelihood(theta,self.data)
		outputs[0][0] = grads

# The Baysian Inference model		
if __name__ == "__main__":

    like = LogLike(loglike,data_np)

    ndraws = 10
    nburn = int(ndraws/2)
	
    with pm.Model() as model:
        cb = pm.Uniform("cb", lower=1e4, upper=2e4)        
        sigma = pm.HalfNormal("sigma", sigma = 0.05)
        theta_ = [cb, sigma]
        theta = tt.as_tensor_variable(theta_)
        pm.Potential("like",like(theta))
        trace = pm.sample(ndraws, step=pm.Metropolis(), tune=nburn, discard_tuned_samples=True, 
                return_inferencedata=True, chains=1, cores=2)	    
     
    axes = az.plot_trace(
        trace, var_names=["cb", "sigma"], kind="trace", figsize=(12, 6),
        chain_prop={"color": ["red", "blue", "green", "black"]})

    for ax_row in axes:  
        for ax in ax_row:  
            ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)  
            ax.minorticks_on() 
            ax.grid(True, which="minor", linestyle=":", linewidth=0.3, alpha=0.3)  
                       
    summary = az.summary(trace, var_names=["cb", "sigma"], kind="stats")

    cb_mean = summary.loc["cb", "mean"]
    cb_sd   = summary.loc["cb", "sd"]

    sigma_mean = summary.loc["sigma", "mean"]
    sigma_sd   = summary.loc["sigma", "sd"]

    print(f"cb = {cb_mean:.6f} ± {cb_sd:.6f}")
    print(f"sigma = {sigma_mean:.6f} ± {sigma_sd:.6f}")
    
    plt.show()  