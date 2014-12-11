import unittest;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from support import read_sample;

from clustering.cure import cure;

class Test(unittest.TestCase):
    def template_cluster_allocation(self, path, cluster_sizes, number_cluster, number_represent_points = 5, compression = 0.5, ccore_flag = False):
        sample = read_sample(path);
        
        cure_instance = cure(sample, number_cluster, ccore = ccore_flag);
        cure_instance.process();
        clusters = cure_instance.get_clusters();

        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        
        total_length = sum(obtained_cluster_sizes);
        assert total_length == len(sample);
        
        cluster_sizes.sort();
        obtained_cluster_sizes.sort();
        assert cluster_sizes == obtained_cluster_sizes;

    def testClusterAllocationSampleSimple1(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2);
    
    def testClusterAllocationSampleSimple2(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3);
        
    def testClusterAllocationSampleSimple3(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4);
        
    def testClusterAllocationSampleSimple4(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5);
        
    def testClusterAllocationSampleSimple5(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4);

    def testClusterAllocationSampleTwoDiamonds(self):
        self.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [399, 401], 2);

    def testClusterAllocationSampleLsun(self):
        self.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_LSUN, [100, 101, 202], 3);

    def testClusterAllocationByCore(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4, 5, 0.5, True);
        self.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [399, 401], 2, 5, 0.5, True);


    def testOneClusterAllocation(self):
        # Bug with one cluster allocation (issue #122).
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [75], 1);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [60], 1);
        
    def testOneClusterAllocationByCore(self):
        # Bug with one cluster allocation (issue #123).
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [75], 1, 5, 0.5, True);
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [60], 1, 5, 0.5, True);
        

if __name__ == "__main__":
    unittest.main();