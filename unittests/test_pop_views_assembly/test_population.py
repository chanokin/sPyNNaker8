from unittest import SkipTest

from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim


class Test_Population(BaseTestCase):

        def test_properties(self):
            n_neurons = 5
            label = "pop_1"
            sim.setup(timestep=1.0)
            pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
            self.assertEquals(n_neurons, pop_1.size)
            self.assertEquals(label, pop_1.label)
            self.assertEquals(sim.IF_curr_exp.build_model(),
                              type(pop_1.celltype))
            v_init = -60
            pop_1.initialize(v=v_init)
            initial_values = pop_1.initial_values
            self.assertDictContainsSubset(
                dict({"v": [-60, -60, -60, -60, -60]}), initial_values)
            v_init = [60 + index for index in xrange(n_neurons)]
            pop_1.initialize(v=v_init)
            initial_values = pop_1.initial_values
            self.assertDictContainsSubset(dict({"v": v_init}), initial_values)

            try:
                print pop_1.all_cells
            except NotImplementedError:
                pass

            try:
                print pop_1.local_cells
            except NotImplementedError:
                pass

            self.assertEquals(n_neurons, pop_1.local_size)

            print pop_1.structure

        def test_position_generator(self):
            n_neurons = 5
            label = "pop_1"
            sim.setup(timestep=1.0)
            pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
            try:
                gen = pop_1.position_generator
                print gen(0)
            except AttributeError:
                msg = "Depends on https://github.com/SpiNNakerManchester" \
                      "/sPyNNaker8/pull/73"
                raise SkipTest(msg)
            sim.end()

        def test_set(self):
            n_neurons = 5
            label = "pop_1"
            sim.setup(timestep=1.0)
            pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
            pop_1.set(v=2)
            sim.end()

        def test_selector(self):
            n_neurons = 5
            label = "pop_1"
            sim.setup(timestep=1.0)
            pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
            pop_1.set(tau_m=2)
            values = pop_1.get("tau_m")
            self.assertEqual([2, 2, 2, 2, 2], values)
            values = pop_1.get_by_selector(slice(1, 3), "tau_m")
            self.assertEquals([2, 2], values)
            pop_1.set_by_selector(slice(1, 3), "tau_m", 3)
            values = pop_1.get("tau_m")
            self.assertEqual([2, 3, 3, 2, 2], values)
            sim.end()
