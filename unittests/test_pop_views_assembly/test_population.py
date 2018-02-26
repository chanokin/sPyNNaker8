import pytest
from unittest import SkipTest

from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim

from spynnaker8.models.populations.population import Population


class Test_Population(BaseTestCase):

    def test_properties(self):
        n_neurons = 5
        label = "pop_1"
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
        self.assertEquals(n_neurons, pop_1.size)
        self.assertEquals(label, pop_1.label)
        self.assertEquals(sim.IF_curr_exp, type(pop_1.celltype))
        v_init = -60
        pop_1.initialize(v=v_init)
        initial_values = pop_1.initial_values
        vs = initial_values["v"]
        assert [-60, -60, -60, -60, -60] == vs
        v_init = [-60 + index for index in xrange(n_neurons)]
        pop_1.initialize(v=v_init)
        initial_values = pop_1.initial_values
        vs = initial_values["v"]
        assert [-60, -59, -58, -57, -56] == vs

        pop_1.all_cells
        pop_1.local_cells

        self.assertEquals(n_neurons, pop_1.local_size)

        pop_1.structure
        sim.end()

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
        values = pop_1.get(["cm", "v_thresh"])
        self.assertEqual([1.0, 1.0, 1.0, 1.0, 1.0], values['cm'])
        self.assertEqual(
            [-50.0, -50.0, -50.0, -50.0, -50.0], values["v_thresh"])
        values = pop_1.get_by_selector([1, 3, 4], ["cm", "v_thresh"])
        self.assertEqual([1.0, 1.0, 1.0], values['cm'])
        self.assertEqual(
            [-50.0, -50.0, -50.0], values["v_thresh"])
        sim.end()

    def test_init_by_in(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(4, sim.IF_curr_exp())
        assert [-65.0, -65.0, -65.0, -65.0] == pop.get_initial_value("v")
        pop.set_initial_value(variable="v", value=-60, selector=1)
        assert [-65, -60, -65, -65] == pop.get_initial_value("v")
        pop.set_initial_value(variable="v", value=12, selector=2)
        assert [-60] == pop.get_initial_value("v", selector=1)
        sim.end()

    def test_initial_values(self):
        sim.setup(timestep=1.0)
        pop = sim.Population.create(4, sim.IF_curr_exp(), label="LABEL")
        initial_values = pop.initial_values
        assert "v" in initial_values
        initial_values = pop.get_initial_values(selector=3)
        assert {"v": [-65, -65, -65, -65]} == initial_values
        sim.end()

    def test_iter(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(4, sim.IF_curr_exp(), label="a label")

        iterator = iter(pop)
        self.assertEqual(0, iterator.next().id)
        self.assertEqual(1, iterator.next().id)
        self.assertEqual(2, iterator.next().id)
        self.assertEqual(3, iterator.next().id)
        with pytest.raises(StopIteration):
            iterator.next()

        iterator = pop.all()
        self.assertEqual(0, iterator.next().id)
        self.assertEqual(1, iterator.next().id)
        self.assertEqual(2, iterator.next().id)
        self.assertEqual(3, iterator.next().id)
        with pytest.raises(StopIteration):
            iterator.next()

        sim.end()
