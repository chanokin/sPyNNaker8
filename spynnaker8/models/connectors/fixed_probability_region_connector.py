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

from spynnaker.pyNN.models.neural_projections.connectors import (
    FixedProbabilityRegionConnector as CommonFixedProbabilityRegionConnector)
from spynnaker.pyNN.models.neural_projections.connectors.FixedProbabilityRegionConnector import (
    CIRCLE, SQUARE)

class FixedProbabilityRegionConnector(CommonFixedProbabilityRegionConnector):
    """
    """
    __slots__ = []

    def __init__(
            self, pre_shape, post_shape, max_distance, p_connect, 
            circle_or_square=CIRCLE, allow_self_connections=True, safe=True,
            verbose=False, rng=None, callback=None):
        """ For each pair of pre-post cells, the connection probability is\
            constant. Cell pairs outside the maximum (euclidean) distance do \
            not connect.

        :param pre_shape: shape (rows, columns, cells per coordinate) for the \
        pre-synaptic population.
        :type pre_shape: iterable
        
        :param post_shape: shape (rows, columns, cells per coordinate) for the \
        post-synaptic population.
        :type post_shape: float
        
        :param max_distance: maximum distance between cell pairs for them \
        to be able to establish a connection
        :type max_distance: float

        :param p_connect: a number between zero and one. Each potential\
            connection is created with this probability.
        :type p_connect: float

        :param circle_or_square: an identifier to know what the maximum distance \
        boundary is. Square will take the distance along the axis while Circle does \
        the straight line between cells.
        :type circle_or_square: int

        :param allow_self_connections: if the connector is used to connect a\
            Population to itself, this flag determines whether a neuron is\
            allowed to connect to itself, or only to other neurons in the\
            Population.
        :param safe: if True, check that weights and delays have valid\
            values. If False, this check is skipped.
        :param space: a Space object, needed if you wish to specify\
            distance-dependent weights or delays - not implemented
        :param verbose:
        :param rng:
        :param callback:
        """
        # pylint: disable=too-many-arguments
        CommonFixedProbabilityRegionConnector.__init__(
            self, pre_shape=pre_shape, post_shape=post_shape, max_distance=max_distance, 
            p_connect=p_connect, circle_or_square=circle_or_square,
            allow_self_connections=allow_self_connections, safe=safe,
            verbose=verbose, rng=rng)


    @property
    def p_connect(self):
        return self._p_connect

    @p_connect.setter
    def p_connect(self, new_value):
        self._p_connect = new_value

    @property
    def pre_shape(self):
        return self._pre_shape

    @pre_shape.setter
    def pre_shape(self, new_value):
        self._pre_shape = new_value

    @property
    def post_shape(self):
        return self._post_shape

    @post_shape.setter
    def post_shape(self, new_value):
        self._post_shape = new_value
    
    @property
    def max_distance(self):
        return self._max_distance

    @max_distance.setter
    def max_distance(self, new_value):
        self._max_distance = new_value
