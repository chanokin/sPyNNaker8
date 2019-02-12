import spynnaker8 as sim
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    # SpiNNaker setup
    sim.setup(timestep=1.0, min_delay=1.0, max_delay=10.0)

    # +-------------------------------------------------------------------+
    # | General Parameters                                                |
    # +-------------------------------------------------------------------+

    # Population parameters
    model = sim.IF_curr_exp
    cell_params = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 10.0,
                   'tau_refrac': 2.0, 'tau_syn_E': 2.5, 'tau_syn_I': 2.5,
                   'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -55.4}

    delta_t = 10
    time_between_pairs = 150
    num_pre_pairs = 10
    num_pairs = 100
    num_post_pairs = 10
    pop_size = 1

    pairing_start_time = (num_pre_pairs * time_between_pairs) + delta_t
    pairing_end_time = pairing_start_time + (num_pairs * time_between_pairs)
    sim_time = pairing_end_time + (num_post_pairs * time_between_pairs)

    # +-------------------------------------------------------------------+
    # | Creation of neuron populations                                    |
    # +-------------------------------------------------------------------+
    # Neuron populations
    pre_pop = sim.Population(pop_size, model, cell_params)
    post_pop = sim.Population(pop_size, model, cell_params)

    # Stimulating populations
    pre_stim = sim.Population(pop_size, sim.SpikeSourceArray,
                              {'spike_times':
                               [[i for i in range(0, sim_time,
                                                  time_between_pairs)], ]})
    post_stim = sim.Population(pop_size, sim.SpikeSourceArray,
                               {'spike_times':
                                [[i for i in range(pairing_start_time,
                                                   pairing_end_time,
                                                   time_between_pairs)], ]})

    # +-------------------------------------------------------------------+
    # | Creation of connections                                           |
    # +-------------------------------------------------------------------+
    # Connection type between noise poisson generator and
    # excitatory populations
    ee_connector = sim.OneToOneConnector()
    synapse_type = sim.StaticSynapse(weight=2)

    sim.Projection(pre_stim, pre_pop, ee_connector, synapse_type=synapse_type,
                   receptor_type='excitatory')
    sim.Projection(post_stim, post_pop, ee_connector,
                   synapse_type=synapse_type, receptor_type='excitatory')

    # Plastic Connections between pre_pop and post_pop
    stdp_model = sim.STDPMechanism(
      timing_dependence=sim.SpikePairRule(tau_plus=20.0, tau_minus=50.0,
                                          A_plus=0.02, A_minus=0.02),
      weight_dependence=sim.AdditiveWeightDependence(w_min=0, w_max=1))

    sim.Projection(pre_pop, post_pop, sim.OneToOneConnector(),
                   synapse_type=stdp_model)

    # Record spikes
    pre_pop.record("spikes")
    post_pop.record("spikes")

    # Run simulation
    sim.run(sim_time)

    neo = pre_pop.get_data("spikes")
    pre_spikes = neo_convertor.convert_spikes(neo)

    neo = post_pop.get_data("spikes")
    post_spikes = neo_convertor.convert_spikes(neo)

    # End simulation on SpiNNaker
    sim.end()

    return (pre_spikes, post_spikes)


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        do_run()


if __name__ == '__main__':
    do_run()
