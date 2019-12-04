# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralStatic as StaticStructuralBaseClass
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralCommon as CommonSP


class SynapseDynamicsStructuralStatic(StaticStructuralBaseClass):

    __slots__ = []

    def __init__(
            self, partner_selection, formation, elimination,
            f_rew=CommonSP.DEFAULT_F_REW,
            initial_weight=CommonSP.DEFAULT_INITIAL_WEIGHT,
            initial_delay=CommonSP.DEFAULT_INITIAL_DELAY,
            s_max=CommonSP.DEFAULT_S_MAX, seed=None,
            weight=PyNNStaticSynapse.default_parameters['weight'], delay=None):
        """
        :param partner_selection: The partner selection rule
        :type partner_selection: \
            ~spynnaker.pyNN.models.neuron.structural_plasticity.synaptogenesis.partner_selection.AbstractPartnerSelection
        :param formation: The formation rule
        :type formation: \
            ~spynnaker.pyNN.models.neuron.structural_plasticity.synaptogenesis.formation.AbstractFormation
        :param elimination: The elimination rule
        :type elimination: \
            ~spynnaker.pyNN.models.neuron.structural_plasticity.synaptogenesis.elimination.AbstractElimination
        :param int f_rew: How many rewiring attempts will be done per second.
        :param float initial_weight: \
            Weight assigned to a newly formed connection
        :param initial_delay:\
            Delay assigned to a newly formed connection; a single value means\
            a fixed delay value, or a tuple of two values means the delay will\
            be chosen at random from a uniform distribution between the given\
            values
        :type initial_delay: float or tuple(float, float)
        :param int s_max: Maximum fan-in per target layer neuron
        :param int seed: seed the random number generators
        :param float weight: The weight of connections formed by the connector
        :param delay: The delay of connections formed by the connector
        :type delay: float or None
        """
        if delay is None:
            delay = globals_variables.get_simulator().min_delay
        StaticStructuralBaseClass.__init__(
            self, partner_selection, formation, elimination, f_rew=f_rew,
            initial_weight=initial_weight, initial_delay=initial_delay,
            s_max=s_max, seed=seed, weight=weight, delay=delay)
