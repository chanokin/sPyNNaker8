import numpy
import spynnaker8 as sim
from spynnaker.pyNN.exceptions import SpynnakerException
from p8_integration_tests.base_test_case import BaseTestCase

SOURCES = 5
DESTINATIONS = 10
OVERFLOW = 6


class ConnectorsTest(BaseTestCase):

    def spike_received_count(self, v_line):
        print(v_line)
        counts = []
        for v in v_line:
            if v < -64:
                counts.append(0)
            elif v < -62.5:  # -63.0
                counts.append(1)
            elif v < -60.5:  # -61.0
                counts.append(2)
            elif v < -58:  # 59.0
                counts.append(3)
            elif v < -56:  # -57.0
                counts.append(4)
            elif v < -54:  # --55.0
                counts.append(5)
            else:
                counts.append(OVERFLOW)
        return counts

    def calc_spikes_received(self, v):
        counts = list()
        counts.append(self.spike_received_count(v[2]))
        counts.append(self.spike_received_count(v[22]))
        counts.append(self.spike_received_count(v[42]))
        counts.append(self.spike_received_count(v[62]))
        counts.append(self.spike_received_count(v[82]))
        return counts

    def check_connection(self, projection, destination, connections, repeats):
        neo = destination.get_data(["v"])
        v = neo.segments[0].filter(name="v")[0]
        weights = projection.get(["weight"], "list")
        self.assertEqual(connections * SOURCES, len(weights))
        counts = self.calc_spikes_received(v)
        for count in counts:
            if not repeats:
                self.assertEqual(1, max(count))
        if max(count) < OVERFLOW:
            self.assertEqual(connections, sum(count))
        expected = numpy.zeros([SOURCES, DESTINATIONS])
        for (src, dest, _) in weights:
            expected[src][dest] += 1
        print(expected)
        assert numpy.array_equal(expected, counts)

    def check_connector(self, connector, connections, repeats):
        sim.setup(1.0)
        # sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 2)

        input = sim.Population(SOURCES, sim.SpikeSourceArray(
            spike_times=[[0], [20], [40], [60], [80]]), label="input")
        destination = sim.Population(
            DESTINATIONS, sim.IF_curr_exp(tau_syn_E=1, tau_refrac=0,  tau_m=1),
            {}, label="destination")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            input, destination, connector, synapse_type=synapse_type)
        destination.record("v")
        sim.run(100)
        self.check_connection(projection, destination, connections, repeats)
        sim.end()

    def test_fix_number_post_connector_with_replacement(self):
        connections = 7
        with_replacement = True
        self.check_connector(
            sim.FixedNumberPostConnector(
                connections, with_replacement=with_replacement),
            connections,  with_replacement)

    def test_fix_number_post_connector_no_replacement(self):
        connections = 7
        with_replacement = False
        self.check_connector(
            sim.FixedNumberPostConnector(
                connections, with_replacement=with_replacement),
            connections, with_replacement)

    def test_fix_number_post_connector_many_connection_with_replacement(self):
        connections = 12
        with_replacement = True
        self.check_connector(
            sim.FixedNumberPostConnector(
                connections, with_replacement=with_replacement),
            connections,  with_replacement)

    def test_fix_number_post_connector_too_many_no_replacement(self):
        connections = 12
        with_replacement = False
        with self.assertRaises(SpynnakerException):
            self.check_connector(
                sim.FixedNumberPostConnector(
                    connections, with_replacement=with_replacement),
                connections, with_replacement)
