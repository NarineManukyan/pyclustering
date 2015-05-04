"""!

@brief Unit-tests for Oscillatory Neural Network based on Kuramoto model.

@authors Andrei Novikov (spb.andr@yandex.ru)
@date 2014-2015
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import unittest;

from pyclustering.nnet import *;
from pyclustering.nnet.sync import sync_network;

from scipy import pi;


class Test(unittest.TestCase):
    def testCreate(self):
        network = sync_network(10, 1);
        assert network.num_osc == 10;
    
    
    def testCreationDeletionByCore(self):
        # Crash occurs in case of memory leak
        for iteration in range(0, 15):
            network = sync_network(4096, 1, type_conn = conn_type.ALL_TO_ALL, ccore = True);
            del network;
      
    
    def testSyncOrderSingleOscillator(self):
        # Check for order parameter of network with one oscillator
        network = sync_network(1, 1);
        assert network.sync_order() == 1;
      
      
    def testSyncOrderNetwork(self):
        # Check for order parameter of network with several oscillators
        network = sync_network(2, 1);
           
        sync_state = 1;
        tolerance = 0.1;
           
        network.simulate(50, 20, solve_type.RK4);
        assert (abs(network.sync_order() - sync_state) < tolerance) == True;        
      
      
    def testSyncLocalOrderSingleOscillator(self):
        network = sync_network(1, 1);
        assert network.sync_local_order() == 0;   
     
     
    def testOutputNormalization(self):
        network = sync_network(20, 1);
         
        output_dynamic = network.simulate(50, 20, solve_type.RK4);
        
        t = output_dynamic.time;
        dyn = output_dynamic.output;
        
        for iteration in range(len(dyn)):
            for index_oscillator in range(len(dyn[iteration])):
                assert (dyn[iteration][index_oscillator] >= 0);
                assert (dyn[iteration][index_oscillator] <= 2.0 * pi);
     
      
    def templateSimulateTest(self, nodes = 10, weight = 1, solution = solve_type.FAST, ccore_flag = False):
        sim_time = 20;
        sim_steps = 50;
        tolerance = 0.01;
          
        network = sync_network(nodes, weight, ccore = ccore_flag);
                
        output_dynamic = network.simulate(sim_steps, sim_time, solution);
        
        dyn_phase = output_dynamic.output;
        
        index = len(dyn_phase) - 1;
        value = dyn_phase[index][0];
          
        for item in dyn_phase[index]:
            if ((abs(item - value) < tolerance) != True):
                print(dyn_phase[:][0]);
                
            assert (abs(item - value) < tolerance) == True;
      
    def testFastSolution(self):
        # Check for convergence when solution using fast way of calculation of derivative
        self.templateSimulateTest(10, 1, solve_type.FAST);
          
    def testFastSolutionByCore(self):
        self.templateSimulateTest(10, 1, solve_type.FAST, ccore_flag = True);
      
    def testRK4Solution(self):
        # Check for convergence when solution using RK4 function of calculation of derivative
        self.templateSimulateTest(10, 1, solve_type.RK4);   
      
    def testRK4SolutionByCore(self):
        self.templateSimulateTest(10, 1, solve_type.RK4, ccore_flag = True);
      
    def testRKF45SolutionByCore(self):
        self.templateSimulateTest(10, 1, solve_type.RKF45, ccore_flag = True);    
      
    def testLargeNetwork(self):
        # Check for convergence of phases in large network - network that contains large number of oscillators
        self.templateSimulateTest(128, 1, solve_type.FAST);           
      
      
      
    def templateDynamicSimulationConnectionTypeTest(self, num_osc, weight, connection_type):
        network = sync_network(num_osc, weight, type_conn = connection_type);
        output_dynamic = network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
          
        clusters = output_dynamic.allocate_sync_ensembles(0.1);
        assert len(clusters) == 1;
          
    def testDynamicSimulationAllToAll(self):
        self.templateDynamicSimulationConnectionTypeTest(10, 1, conn_type.ALL_TO_ALL);
        self.templateDynamicSimulationConnectionTypeTest(50, 1, conn_type.ALL_TO_ALL);
          
    def testDynamicSimulationGridFour(self):
        self.templateDynamicSimulationConnectionTypeTest(9, 1, conn_type.GRID_FOUR);
        self.templateDynamicSimulationConnectionTypeTest(25, 1, conn_type.GRID_FOUR);
  
    def testDynamicSimulationGridEight(self):
        self.templateDynamicSimulationConnectionTypeTest(9, 1, conn_type.GRID_FOUR);
        self.templateDynamicSimulationConnectionTypeTest(25, 1, conn_type.GRID_FOUR);
  
    def testDynamicSimulationBidir(self):
        self.templateDynamicSimulationConnectionTypeTest(5, 1, conn_type.LIST_BIDIR);
        self.templateDynamicSimulationConnectionTypeTest(10, 1, conn_type.LIST_BIDIR);


    def templateDynamicSimulationConvergence(self, num_osc, weight, connection_type, ccore_flag):
        network = sync_network(num_osc, weight, type_conn = connection_type, initial_phases=initial_type.EQUIPARTITION, ccore = ccore_flag);
        output_dynamic = network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
        
        clusters = output_dynamic.allocate_sync_ensembles(0.1);
        assert len(clusters) == 1;
        
    def testTwoOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(2, 1, conn_type.ALL_TO_ALL, False);
         
    def testTwoOscillatorDynamicByCore(self):
        self.templateDynamicSimulationConvergence(2, 1, conn_type.ALL_TO_ALL, True);
         
    def testThreeOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(3, 1, conn_type.ALL_TO_ALL, False);
     
    def testThreeOscillatorDynamicByCore(self):
        self.templateDynamicSimulationConvergence(3, 1, conn_type.ALL_TO_ALL, True);
 
    def testFourOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(4, 1, conn_type.ALL_TO_ALL, False);
     
    def testFourOscillatorDynamicByCore(self):
        self.templateDynamicSimulationConvergence(4, 1, conn_type.ALL_TO_ALL, True);
  
    def testFiveOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(5, 1, conn_type.ALL_TO_ALL, False);
     
    def testFiveOscillatorDynamicByCore(self):
        self.templateDynamicSimulationConvergence(5, 1, conn_type.ALL_TO_ALL, True);
          
    def testSixOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(6, 1, conn_type.ALL_TO_ALL, False);
     
    def testSixOscillatorDynamicByCore(self):
        self.templateDynamicSimulationConvergence(6, 1, conn_type.ALL_TO_ALL, True);
  
    def testSevenOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(7, 1, conn_type.ALL_TO_ALL, False);
    
    def testSevenOscillatorDynamicByCore(self):
        self.templateDynamicSimulationConvergence(7, 1, conn_type.ALL_TO_ALL, True);
        

if __name__ == "__main__":
    unittest.main();
