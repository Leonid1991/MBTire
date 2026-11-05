from collections import deque
import json 
import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as irr
import math as m
import time
import pychrono.pardisomkl as mkl          # at the top

# =============================================================================
veh.SetVehicleDataPath(chrono.GetChronoDataPath() + 'vehicle/')
tire_json = "C:/Data/Chrono/Callibration/HMMWV_MBTire_modified.json"
wheel_json = veh.GetVehicleDataFile("hmmwv/wheel/HMMWV_Wheel.json")
simulation = True   
Visualization = False
g = 9.8
initia_div = 40
############################################################################################################
# Load_list_kg = [902.9, 1358.7, 1812.3, 2251.1, 2704.5, 3165.8, 3614.3, 4069.9, 4501.1, 4509.8]
# displacements= [0.0082, 0.0121, 0.0161, 0.0202, 0.0243, 0.0284, 0.0325, 0.0366, 0.0407, 0.0448]
Load_list_kg = [902.9, 1358.7]

division = 40
step_size = 1e-5

pressure = 9e5
Stiffness = False
threashhold = 0.004
LoadSpeed = 0.005
time_delay_length = 0.25 # time delay after contact for setteling the system
avg_window = 1000   

'''
all = False
if all:
    cr = 115e5
    cc = 3e6 
    ct = 105e4
    ccb = 105e3
    cct = 105e3
else:
'''

stiff = 5e7
cr = stiff
cc = stiff  * 1e-1
ct = stiff  * 1e-1
ccb = stiff * 1e-3 # standard
cct = stiff * 1e-3

load_sum = 0.0
disp_sum = 0.0
# -------------------------------- Rewrite the JSON file  ------------------
with open(tire_json, 'r') as f: # Open and load JSON content
    tire_json_data = json.load(f)

print(chrono.__file__)
print(tire_json)

tire_json_data["Numerical Settings"]["Stiff"] = Stiffness 
tire_json_data["Default Pressure"] = pressure
tire_json_data["Geometry"]["Number Divisions"] = division
E_contact = 2e6 # here it is initial values, but just to make sure it stays!!!!!!!  
tire_json_data["Contact Material"]["Properties"]["Young Modulus"] = E_contact

# we need to adjust the spring properties based on the division factor 
tire_json_data["Spring Properties"]["Radial"][0] = cr 
tire_json_data["Spring Properties"]["Circumferential"][0] = cc
tire_json_data["Spring Properties"]["Transversal"][0] = ct
tire_json_data["Spring Properties"]["Circumferential Bending"][0] = ccb
tire_json_data["Spring Properties"]["Transversal Bending"][0] = cct

coef = 1e-3 # viscous 
tire_json_data["Spring Properties"]["Radial"][1] = cr * coef
tire_json_data["Spring Properties"]["Circumferential"][1] = cc * coef
tire_json_data["Spring Properties"]["Transversal"][1] = ct * coef

# visco = 1e3 # control visco separately
# tire_json_data["Spring Properties"]["Radial"][1] = visco
# tire_json_data["Spring Properties"]["Circumferential"][1] = visco    
# tire_json_data["Spring Properties"]["Transversal"][1] = visco

with open(tire_json, 'w') as f: # Save back to file (overwrite)
    json.dump(tire_json_data, f, indent=2)
     
# ------------------------------- Constants --------------------------------
disp = 0
nominalLoad_fake = 100000000 * g # just not to leave the programm to quickly 
Load_list_N = [x * g for x in Load_list_kg]
FLAG_LIST = [0] * len(Load_list_kg)
Result_array = []
# -------------------------------- Saving mechanisms ------------------ 
 
def main():
    global disp, step_size, LoadSpeed, nominalLoad_fake, pressure, g, Load_list_N, FLAG_LIST, Result_array, load_sum, disp_sum, avg_window

    # --------------------------------
    # Create wheel and tire subsystems
    # --------------------------------

    print("Create wheel and tire")

    wheel = veh.ReadWheelJSON(wheel_json)
    tire = veh.ReadTireJSON(tire_json)

    # Set tire contact surface
    collision_family = 7
    surface_dim = 0.0
    # surface_dim = 0.01 # to compare with some oither experiments 
    
    tire.SetContactSurfaceType(surface_type, surface_dim, collision_family)

    # ----------------------------
    # Create system and set solver
    # ----------------------------truct

    print("Create Chrono system")

    sys = chrono.ChSystemSMC()
    sys.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)

    tire.SetStepsize(step_size)
    if Stiffness:
        sys.SetSolver(mkl.ChSolverPardisoMKL())    # instead of line 114
    else:    
        sys.SetSolverType(chrono.ChSolver.Type_PSOR)
    

    sys.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_PROJECTED)
    #sys.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_LINEARIZED)

    num_threads_chrono = 4     # Number of OpenMP threads used in Chrono (SCM ray-casting and FEA)
    num_threads_collision = 4  # Number of threads used in collision detection
    num_threads_eigen = 1      # Number of threads used by Eigen
    num_threads_pardiso = 4    # Number of threads used by PardisoMKL
    sys.SetNumThreads(num_threads_chrono, num_threads_collision, num_threads_eigen)

    print("Create test rig")
    rig = veh.ChTireStaticTestRig(wheel, tire, sys)
    rig.SetGravitationalAcceleration(g)
    # Set tire options
    rig.SetTireStepsize(step_size)
    rig.SetTireVisualizationType(chrono.VisualizationType_MESH)
    # Set rig options
    rig.SetPlateMaterialProperties(0.8, 0, 2e7)
    # Set test parameters
    rig.SetNominalRadialLoad(nominalLoad_fake)
    rig.SetStateTransitionDelay(0.2)
    rig.SetRadialLoadSpeed(LoadSpeed)
    rig.SetLongitudinalLoadSpeed(0.1)
    rig.SetLateralLoadSpeed(0.1)
    rig.SetTorsionalLoadSpeed(0.1)

    # Initialize the tire test rig
    rig.Initialize(test_mode)

    if Visualization:
        print("Create visualization system")
        vis = irr.ChVisualSystemIrrlicht()
        vis.AttachSystem(sys)
        vis.SetCameraVertical(chrono.CameraVerticalDir_Z)
        vis.SetWindowSize(1024, 768)
        vis.SetWindowTitle('Tire Test Rig')
        vis.Initialize()
        vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
        vis.AddSkyBox()
        vis.AddCamera(chrono.ChVector3d(1, 2.5, 1), rig.GetWheelPos())
        vis.AddTypicalLights()
     

    # ---------------
    # Simulation loop
    # ---------------

    # Timers and counters
    timer = chrono.ChTimer() # timer for measuring total run time
    time = 0                 # simulated time
    sim_time = 0             # simulation time
    fps = 120                # rendering frequency
    render_frame = 0         # render frame counter
    time_delay = 0
    timer.start()
    fl = 0
    i = 0

    n_avg = max(1, avg_window)  # Ensure n_avg is at least 1 to avoid division by zero
    load_window = deque(maxlen=n_avg)            
    disp_window = deque(maxlen=n_avg)
    
    while simulation:    

        time = sys.GetChTime()       
        state = rig.GetState()   
        
        if Visualization:
            if not vis.Run():
                break
            if time >= render_frame / fps:
                vis.BeginScene()
                vis.Render()
                vis.EndScene()            


        if state == 2 and fl == 0: # If the tire is in contact with the plate, set the reference position
           fl = 1 # fix the reference position at the first contact only
           m_spindle_z_ref = rig.GetWheelPos().z
           time_delay_start = time # time delay starts

        currentLoad = rig.GetLoad() 


        # idea to make average across several outcomes, just for smoothing the results
        if state > 1:
            time_delay = time - time_delay_start
            disp = m_spindle_z_ref - rig.GetWheelPos().z  
            if len(load_window) == n_avg:        # oldest value leaves the window
                load_sum -= load_window[0]
                disp_sum -= disp_window[0]
            load_window.append(currentLoad)
            disp_window.append(disp)
            load_sum += currentLoad
            disp_sum += disp
        avgLoad = load_sum / n_avg if load_window else 0.0
        avgDisp = disp_sum / n_avg if disp_window else 0.0
          

        if m.isnan(currentLoad): # just a preserving
            print("Load is NaN, stopping simulation.")
            break
 
        print(f"{avgDisp:>20.6f} {avgLoad:>20.10f} {state:>8} {time_delay:>10.6f} {time:>10.6f}") 
        
        if avgLoad > Load_list_N[i] and state != 1 and avgDisp>threashhold:
            FLAG_LIST[i] = 1
            Result_array.append((pressure, round(avgLoad,2), round(avgDisp,5), n_avg))
            i += 1

        if sum(FLAG_LIST) == len(FLAG_LIST):
            print("==========================")
            for row in Result_array:
                print(", ".join(str(x) for x in row))
            break

        if fl == 1 and time_delay < time_delay_length:
           rig.SetRadialLoadSpeed(0)
        else:
           rig.SetRadialLoadSpeed(LoadSpeed)
           time_delay = time_delay_length 
        
        
        rig.Advance(step_size)
                        
        sim_time = sim_time + sys.GetTimerStep()    

    timer.stop()
    step_time = timer.GetTimeSeconds()


surface_type = veh.ChTire.ContactSurfaceType_TRIANGLE_MESH # Tire contact model (nodes or faces)
test_mode = veh.ChTireStaticTestRig.Mode_TEST_R # Test mode

debug_output = False
start = time.perf_counter()
main()
end = time.perf_counter()
print(f"Total run time: {end - start:.2f} seconds")