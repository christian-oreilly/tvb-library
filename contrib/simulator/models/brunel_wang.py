# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2017, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Based on the Brunel and Wang model.


.. moduleauthor:: Paula Sanz Leon <Paula@tvb.invalid>
.. moduleauthor:: Marmaduke Woodman <Marmaduke@tvb.invalid>
.. moduleauthor:: Stuart A. Knock <Stuart@tvb.invalid>

"""
from tvb.basic.profile import TvbProfile
TvbProfile.set_profile(TvbProfile.TEST_LIBRARY_PROFILE)

import inspect
import numpy
import tvb.datatypes.arrays as arrays
import tvb.datatypes.lookup_tables as lookup_tables
import tvb.basic.traits.types_basic as basic 
import tvb.simulator.models as models
from tvb.simulator.common import get_logger

LOG = get_logger(__name__)


class BrunelWang(models.Model):
    """
    .. [DJ_2012] Deco G and Jirsa V. *Ongoing Cortical
        Activity at Rest: Criticality, Multistability, and Ghost Attractors*.
        Journal of Neuroscience 32, 3366-3375, 2012.

    .. [BW_2001] Brunel N and Wang X-J. *Effects of neuromodulation in a cortical
       network model of object working memory dominated by recurrent inhibition*.
       Journal of Computational Neuroscience 11, 63–85, 2001.

    Each node consists of one excitatory (E) and one inhibitory (I) pool.

    At a global level, it uses Hagmann's 2008 connectome 66 areas(hagmann_struct.csv)
    with a global scaling weight (W) of 1.65.


    """

    _ui_name = "Deco-Jirsa (Mean-Field Brunel-Wang)"
    ui_configurable_parameters = ['tau', 'calpha', 'cbeta', 'cgamma', 'tauNMDArise',
                                  'tauNMDAdecay', 'tauAMPA', 'tauGABA',
                                  'VE', 'VI', 'VL', 'Vthr', 'Vreset', 'gNMDA_e',
                                  'gNMDA_i', 'gGABA_e', 'gGABA_i', 'gAMPArec_e',
                                  'gAMPArec_i', 'gAMPAext_e', 'gAMPAext_i',
                                  'gm_e', 'gm_i', 'Cm_e', 'Cm_i', 'taum_e',
                                  'taum_i', 'taurp_e', 'taurp_i', 'Cext', 'C',
                                  'nuext', 'wplus', 'wminus', 'W']

    #Define traited attributes for this model, these represent possible kwargs.
    tau = arrays.FloatArray(
        label = ":math:`\\tau`",
        default = numpy.array([1.25,]),
        range = basic.Range(lo = 0.01, hi = 5.0, step = 0.01),
        doc = """A time-scale separation between the fast, :math:`V`, and slow,
        :math:`W`, state-variables of the model.""",
        order = 1)

    calpha = arrays.FloatArray(
        label = ":math:`c_{\\alpha}`",
        default = numpy.array([0.5,]),
        range = basic.Range(lo = 0.4, hi = 0.5, step = 0.05),
        doc = """NMDA saturation parameter (kHz)""",
        order = 2)

    cbeta = arrays.FloatArray(
        label = ":math:`c_{\\beta}`",
        default = numpy.array([0.062,]),
        range = basic.Range(lo = 0.06, hi = 0.062, step = 0.002),
        doc = """Inverse MG2+ blockade potential(mV-1)""",
        order = 3)

    cgamma = arrays.FloatArray(
        label = ":math:`c_{\\gamma}`",
        default = numpy.array([0.2801120448,]),
        range = basic.Range(lo = 0.2801120440, hi = 0.2801120448, step = 0.0000000001),
        doc = """Strength of Mg2+ blockade""",
        order = -1)

    tauNMDArise = arrays.FloatArray(
        label = ":math:`\\tau_{NMDA_{rise}}`",
        default = numpy.array([2.0,]),
        range = basic.Range(lo = 0.0, hi = 2.0, step = 0.5),
        doc="""NMDA time constant (rise) (ms)""",
        order = 4)

    tauNMDAdecay = arrays.FloatArray(
        label = ":math:`\\tau_{NMDA_{decay}}`",
        default = numpy.array([100.,]),
        range = basic.Range(lo = 50.0, hi = 100.0, step = 10.0),
        doc = """NMDA time constant (decay) (ms)""",
        order = 5)

    tauAMPA = arrays.FloatArray(
        label = ":math:`\\tau_{AMPA}`",
        default = numpy.array([2.0,]),
        range = basic.Range(lo = 1.0, hi = 2.0, step = 1.0),
        doc = """AMPA time constant (decay) (ms)""",
        order = 6)

    tauGABA = arrays.FloatArray(
        label = ":math:`\\tau_{GABA}`",
        default = numpy.array([10.0,]),
        range = basic.Range(lo = 5.0, hi = 15.0, step = 1.0),
        doc = """GABA time constant (decay) (ms)""",
        order = 7)

    VE = arrays.FloatArray(
        label = ":math:`V_E`",
        default = numpy.array([0.0,]),
        range = basic.Range(lo = 0.0, hi = 10.0, step = 2.0),
        doc = """Extracellular potential (mV)""",
        order = 8)

    VI = arrays.FloatArray(
        label = ":math:`V_I`",
        default = numpy.array([-70.0,]),
        range = basic.Range(lo = -70.0, hi = -50.0, step = 5.0),
        doc = """.""",
        order = -1)

    VL = arrays.FloatArray(
        label = ":math:`V_L`",
        default = numpy.array([-70.0,]),
        range = basic.Range(lo = -70.0, hi = -50.0, step = 5.0),
        doc = """Resting potential (mV)""",
        order = -1)

    Vthr = arrays.FloatArray(
        label = ":math:`V_{thr}`",
        default = numpy.array([-50.0,]),
        range = basic.Range(lo = -50.0, hi = -30.0, step = 5.0),
        doc = """Threshold potential (mV)""",
        order = -1)

    Vreset = arrays.FloatArray(
        label = ":math:`V_{reset}`",
        default = numpy.array([-55.0,]),
        range = basic.Range(lo = -70.0, hi = -30.0, step = 5.0),
        doc = """Reset potential (mV)""",
        order = 9)

    gNMDA_e = arrays.FloatArray(
        label = ":math:`g_{NMDA_{e}}`",
        default = numpy.array([0.327,]),
        range = basic.Range(lo = 0.320, hi = 0.350, step = 0.0035),
        doc = """NMDA conductance on post-synaptic excitatory (nS)""",
        order = -1)

    gNMDA_i = arrays.FloatArray(
        label = ":math:`g_{NMDA_{i}}`",
        default = numpy.array([0.258,]),
        range = basic.Range(lo = 0.250, hi = 0.270, step = 0.002),
        doc = """NMDA conductance on post-synaptic inhibitory (nS)""",
        order = -1)

    gGABA_e = arrays.FloatArray(
        label = ":math:`g_{GABA_{e}}`",
        default = numpy.array([1.25 * 3.5, ]),
        range = basic.Range(lo = 1.25, hi = 4.375, step = 0.005),
        doc = """GABA conductance on excitatory post-synaptic (nS)""",
        order = 10)

    gGABA_i = arrays.FloatArray(
        label = ":math:`g_{GABA_{i}}`",
        default = numpy.array([0.973 * 3.5, ]),
        range = basic.Range(lo = 0.9730, hi = 3.4055, step = 0.0005),
        doc = """GABA conductance on inhibitory post-synaptic (nS)""",
        order = 11)

    gAMPArec_e = arrays.FloatArray(
        label = ":math:`g_{AMPA_{rec_e}}`",
        default = numpy.array([0.104,]),
        range = basic.Range(lo = 0.1, hi = 0.11, step = 0.001),
        doc = """AMPA(recurrent) cond on post-synaptic (nS)""",
        order = -1)

    gAMPArec_i = arrays.FloatArray(
        label = ":math:`g_{AMPA_{rec_i}}`",
        default = numpy.array([0.081,]),
        range = basic.Range(lo = 0.081, hi = 0.1, step = 0.001),
        doc = """AMPA(recurrent) cond on post-synaptic (nS)""",
        order = -1)

    gAMPAext_e = arrays.FloatArray(
        label = ":math:`g_{AMPA_{ext_e}}`",
        default = numpy.array([2.08 * 1.2,]),
        range = basic.Range(lo = 2.08, hi = 2.496, step = 0.004),
        doc = """AMPA(external) cond on post-synaptic (nS)""",
        order = 12)

    gAMPAext_i = arrays.FloatArray(
        label = ":math:`g_{AMPA_{ext_i}}`",
        default = numpy.array([1.62 * 1.2,]),
        range = basic.Range(lo = 1.62, hi = 1.944, step = 0.004),
        doc = """AMPA(external) cond on post-synaptic (nS)""",
        order = 13)

    gm_e = arrays.FloatArray(
        label = ":math:`gm_e`",
        default = numpy.array([25.0,]),
        range = basic.Range(lo = 20.0, hi = 25.0, step = 1.0),
        doc = """Excitatory membrane conductance (nS)""",
        order = 13)

    gm_i = arrays.FloatArray(
        label = ":math:`gm_i`",
        default = numpy.array([20.,]),
        range = basic.Range(lo = 15.0, hi = 21.0, step = 1.0),
        doc = """Inhibitory membrane conductance (nS)""",
        order = 14)

    Cm_e = arrays.FloatArray(
        label = ":math:`Cm_e`",
        default = numpy.array([500.,]),
        range = basic.Range(lo = 200.0, hi = 600.0, step = 50.0),
        doc = """Excitatory membrane capacitance (mF)""",
        order = 15)

    Cm_i = arrays.FloatArray(
        label = ":math:`Cm_i`",
        default = numpy.array([200.,]),
        range = basic.Range(lo = 150.0, hi = 250.0, step = 50.0),
        doc = """Inhibitory membrane capacitance (mF)""",
        order = 16)

    taum_e = arrays.FloatArray(
        label = ":math:`\\tau_{m_{e}}`",
        default = numpy.array([20.,]),
        range = basic.Range(lo = 10.0, hi = 25.0, step = 5.0),
        doc = """Excitatory membrane leak time (ms)""",
        order = 17)

    taum_i = arrays.FloatArray(
        label = ":math:`\\tau_{m_{i}}`",
        default = numpy.array([10.0,]),
        range = basic.Range(lo = 5.0, hi = 15.0, step = 5.),
        doc = """Inhibitory Membrane leak time (ms)""",
        order = 18)

    taurp_e = arrays.FloatArray(
        label = ":math:`\\tau_{rp_{e}}`",
        default = numpy.array([2.0,]),
        range = basic.Range(lo = 0.0, hi = 4.0, step = 1.),
        doc = """Excitatory absolute refractory period (ms)""",
        order = 19)

    taurp_i = arrays.FloatArray(
        label = ":math:`\\tau_{rp_{i}}`",
        default = numpy.array([1.0,]),
        range = basic.Range(lo = 0.0, hi = 2.0, step = 0.5),
        doc= """Inhibitory absolute refractory period (ms)""",
        order = 20)

    Cext = arrays.IntegerArray(
        label = ":math:`C_{ext}`",
        default = numpy.array([800,]),
        range = basic.Range(lo = 500, hi = 1200, step = 100),
        doc = """Number of external (excitatory) connections""",
        order = -1)

    C = arrays.IntegerArray(
        label = ":math:`C`",
        default = numpy.array([200,]),
        range = basic.Range(lo = 100, hi = 500, step = 100),
        doc = "Number of neurons for each node",
        order = -1)

    nuext = arrays.FloatArray(
        label = ":math:`\\nu_{ext}`",
        default = numpy.array([0.003,]),
        range = basic.Range(lo = 0.002, hi = 0.01, step = 0.001),
        doc = """External firing rate (kHz)""",
        order = -1)

    wplus = arrays.FloatArray(
        label = ":math:`w_{+}`",
        default = numpy.array([1.5,]),
        range = basic.Range(lo = 0.5, hi = 3., step = 0.05),
        doc = """Synaptic coupling strength [w+] (dimensionless)""",
        order = -1)

    wminus = arrays.FloatArray(
        label = ":math:`w_{-}`",
        default = numpy.array([1.,]),
        range = basic.Range(lo = 0.2, hi = 2., step = 0.05),
        doc = """Synaptic coupling strength [w-] (dimensionless)""",
        order = -1)


    NMAX = arrays.IntegerArray(
        label = ":math:`N_{MAX}`",
        default = numpy.array([8, ], dtype=numpy.int32),
        range = basic.Range(lo = 2, hi = 8, step=1),
        doc = """This is a magic number as given in the original code.
        It is used to compute the phi and psi -- computationally expensive --
        functions""",
        order = -1)

    pool_nodes = arrays.FloatArray(
        label = ":math:`p_{nodes}`",
        default = numpy.array([74.0, ]),
        range = basic.Range(lo = 1.0, hi = 74.0, step = 1.0),
        doc = """Scale coupling weight sby the number of nodes in the network""",
        order = 23)

    a = arrays.FloatArray(
        label = ":math:`a`",
        default = numpy.array([0.80823563, ]),
        range = basic.Range(lo = 0.80, hi = 0.88, step = 0.01),
        doc = """.""",
        order = -1)

    b = arrays.FloatArray(
        label = ":math:`b`",
        default = numpy.array([67.06177975, ]),
        range =  basic.Range(lo = 66.0, hi = 69.0, step = 0.5 ),
        doc = """.""",
        order = -1)

    ve = arrays.FloatArray(
        label = ":math:`ve`",
        default = numpy.array([- 52.5, ]),
        range = basic.Range(lo = -50.0, hi = -45.0, step = 0.2),
        doc = """.""",
        order = -1)

    vi = arrays.FloatArray(
        label = ":math:`vi`",
        default = numpy.array([- 52.5,]),
        range = basic.Range(lo = -50.0, hi = -45.0, step = 0.2 ),
        doc = """.""",
        order = -1)

    W = arrays.FloatArray(
        label = ":math:`W`",
        default = numpy.array([1.65,]),
        range = basic.Range(lo = 1.4, hi = 1.9, step = 0.05),
        doc = """Global scaling weight [W] (dimensionless)""",
        order = -1)

    variables_of_interest = basic.Enumerate(
        label="Variables watched by Monitors",
        options=["E", "I"],
        default=["E"],
        select_multiple=True,
        doc="""This represents the default state-variables of this Model to be
                                    monitored. It can be overridden for each Monitor if desired. The
                                    corresponding state-variable indices for this model are :math:`E = 0`
                                    and :math:`I = 1`.""",
        order=21)

        #Informational attribute, used for phase-plane and initial()
    state_variable_range = basic.Dict(
        label = "State Variable ranges [lo, hi]",
        default = {"E": numpy.array([0.001, 0.01]),
                   "I": numpy.array([0.001, 0.01])},
        doc = """The values for each state-variable should be set to encompass
            the expected dynamic range of that state-variable for the current
            parameters, it is used as a mechanism for bounding random initial
            conditions when the simulation isn't started from an explicit
            history, it is also provides the default range of phase-plane plots.
            The corresponding state-variable units for this model are kHz.""",
        order = 22)


    # psi_table = lookup_tables.PsiTable(required=True,
    #                                    default=lookup_tables.PsiTable(),
    #                                    label="Psi Table",
    #                                    doc="""Psi Table (description).""")
    #
    # nerf_table = lookup_tables.NerfTable(required=True,
    #                                      default=lookup_tables.NerfTable(),
    #                                      label="Nerf Table",
    #                                      doc="""Nerf Table (description).""")


    def __init__(self, **kwargs):
        """
        May need to put kwargs back if we can't get them from trait...

        """

        LOG.info("%s: initing..." % str(self))

        super(BrunelWang, self).__init__(**kwargs)

        #self._state_variables = ["E", "I"]
        self._nvar = 2

        self.cvar = numpy.array([0, 1], dtype=numpy.int32)

        #Derived parameters
        self.crho1_e  = None
        self.crho1_i  = None
        self.crho2_e  = None
        self.crho2_i  = None
        self.csigma_e = None
        self.csigma_i = None
        self.tauNMDA  = None

        self.Text_e   = None
        self.Text_i   = None
        self.TAMPA_e  = None
        self.TAMPA_i  = None
        self.T_ei     = None
        self.T_ii     = None

        self.pool_fractions = None


        #NOTE: We could speed up this model simplifying some the phi and psi functions
        #above. However it was decided that functions should be the same as
        # in the original paper.

        # integral
        #self.vector_nerf = lambda z: numpy.exp(z**2) * (scipy.special.erf(z) + 1)
        #integral = lambda x : numpy.float64(quad(self.vector_nerf, float('-Inf') , x, full_output = True)[0])
        #self.vint = numpy.vectorize(integral)

        LOG.debug('%s: inited.' % repr(self))



    def configure(self):
        """  """
        super(BrunelWang, self).configure()
        self.update_derived_parameters()

        self.psi_table = lookup_tables.PsiTable(load_default=True, use_storage=False)
        self.nerf_table = lookup_tables.NerfTable(load_default=True, use_storage=False)
        # configure look up tables
        self.psi_table.configure()
        self.nerf_table.configure()

        #self.optimize()

    def optimize(self, fnname='optdfun'):
        """
        Optimization routine when we have too many self.parameters
        within dfun
        """

        decl = "def %s(state_variables, coupling, local_coupling=0.0):\n" % (fnname,)

        NoneType = type(None)
        for k in dir(self):
            attr = getattr(self, k)
            if not k[0] == '_' and type(attr) in (numpy.ndarray, NoneType):
                decl += '        %s = %r\n' % (k, attr)

        decl += '\n'.join(inspect.getsource(self.dfun).split('\n')[1:]).replace("self.", "")
        dikt = {'vint': self.vint, 'array': numpy.array, 'int32': numpy.int32, 'numpy': numpy}
        #print decl
        exec decl in dikt
        self.dfun = dikt[fnname]

    def dfun(self, state_variables, coupling, local_coupling=0.0):
        """
        .. math::
             \tau_e*\\dot{\nu_e}(t) &= -\nu_e(t) + \\phi_e \\\\
             \tau_i*\\dot{\nu_i}(t) &= -\nu_i(t) + \\phi_i \\\\
             ve &= - (V_thr - V_reset) \\, \nu_e \\, \tau_e + \\mu_e \\\\
             vi &= - (V_thr - V_reset) \\, \nu_i \\, \tau_i + \\mu_i \\\\

             \tau_X &= \\frac{C_m_X}{g_m_x  \\, S_X} \\\\
             S_X &= 1 + Text \\, \nu_ext + T_ampa \\, \nu_X + (rho_1 + rho_2)
                     \\, \\psi(\nu_X) + T_XI \\, \\nu_I \\\\
             \\mu_X &= \\frac{(Text \\, \\nu_X + T_AMPA \\, \\nu_X + \\rho_1 \\,
                        \\psi(\nu_X)) \\, (V_E - V_L)}{S_X} +
                        \\frac{\\rho_2 \\, \\psi(\nu_X) \\,(\\bar{V_X} - V_L) +
                        T_xI \\, \\nu_I \\, (V_I - V_L)}{S_X} \\\\
            sigma_X^2 &= \\frac{g_AMPA_ext^2(\\bar{V_X} - V_X)^2 \\, C_ext \\, nu_ext
                        \\tau_AMPA^2 \\, \\tau_X}{g_m_X^2 * \\tau_m_X^2} \\\\
            \\rho_1 &= {g_NMDA * C}{g_m_X * J} \\\\
            \\rho_2 &= \\beta \\frac{g_NMDA * C (\\bar{V_X} - V_E)(J - 1)}
                        {g_m_X * J^2} \\\\
            J_X &= 1 + \\gamma \\,\exp(-\\beta*\\bar{V_X}) \\\\
            \\phi(\mu_X, \\sigma_X) &= (\\tau_rp_X + \\tau_X \\, \\int
                                         \exp(u^2) * (\\erf(u) + 1))^-1

        The NMDA gating variable
        .. math::
            \\psi(\\nu)
        has been approximated by the exponential function:
        .. math::
            \\psi(\\nu) &= a * (1 - \exp(-b * \\nu)) \\\\
            a &= 0.80823563 \\\\
            b &= 67.06177975

        The post-synaptic rate as described by the :math:`\\phi` function
        constitutes a non-linear input-output relationship between the firing
        rate of the post-synaptic neuron and the average firing rates
        :math:`\\nu_{E}` and :math:`\\nu_{I}` of the pre-synaptic excitatory and
        inhibitory neural populations. This input-output function is
        conceptually equivalent to the simple threshold-linear or sigmoid
        input-output functions routinely used in firing-rate models. What it is
        gained from using the integral form is a firing-rate model that captures
        many of the underlying biophysics of the real spiking neurons.[BW_2001]_

        """

        E = state_variables[0, :]
        I = state_variables[1, :]
        #A = state_variables[2, :]

        # where and how to add local coupling

        c_0 = coupling[0, :]
        c_2 = coupling[1, :]

        # AMPA synapses (E --> E, and E --> I)
        vn_e = c_0
        vn_i = E * self.wminus * self.pool_fractions

        # NMDA synapses (E --> E, and E --> I)
        vN_e = c_2
        vN_i = E * self.wminus * self.pool_fractions

        # GABA (A) synapses (I --> E, and I --> I)
        vni_e = self.wminus * I  # I --> E
        vni_i = self.wminus * I  # I --> I

        J_e = 1 + self.cgamma * numpy.exp(-self.cbeta * self.ve)
        J_i = 1 + self.cgamma * numpy.exp(-self.cbeta * self.vi)

        rho1_e = self.crho1_e / J_e
        rho1_i = self.crho1_i / J_i
        rho2_e = self.crho2_e * (self.ve - self.VE) * (J_e - 1) / J_e ** 2
        rho2_i = self.crho2_i * (self.vi - self.VI) * (J_i - 1) / J_i ** 2

        vS_e = 1 + self.Text_e * self.nuext + self.TAMPA_e * vn_e + \
               (rho1_e + rho2_e) * vN_e + self.T_ei * vni_e
        vS_i = 1 + self.Text_i * self.nuext + self.TAMPA_i * vn_i + \
               (rho1_i + rho2_i) * vN_i + self.T_ii * vni_i

        vtau_e = self.Cm_e / (self.gm_e * vS_e)
        vtau_i = self.Cm_i / (self.gm_i * vS_i)

        vmu_e = (rho2_e * vN_e * self.ve + self.T_ei * vni_e * self.VI + \
                 self.VL) / vS_e

        vmu_i = (rho2_i * vN_i * self.vi + self.T_ii * vni_i * self.VI + \
                 self.VL) / vS_i

        vsigma_e = numpy.sqrt((self.ve - self.VE) ** 2 * vtau_e * \
                              self.csigma_e * self.nuext)
        vsigma_i = numpy.sqrt((self.vi - self.VE) ** 2 * vtau_i * \
                              self.csigma_i * self.nuext)

        #tauAMPA_over_vtau_e
        k_e = self.tauAMPA / vtau_e
        k_i = self.tauAMPA / vtau_i


        #integration limits
        alpha_e = (self.Vthr - vmu_e) / vsigma_e * (1.0 + 0.5 * k_e) + \
                  1.03 * numpy.sqrt(k_e) - 0.5 * k_e
        alpha_e = numpy.where(alpha_e > 19, 19, alpha_e)
        alpha_i = (self.Vthr - vmu_i) / vsigma_i * (1.0 + 0.5 * k_i) + \
                  1.03 * numpy.sqrt(k_i) - 0.5 * k_i
        alpha_i = numpy.where(alpha_i > 19, 19, alpha_i)

        beta_e = (self.Vreset - vmu_e) / vsigma_e
        beta_e = numpy.where(beta_e > 19, 19, beta_e)

        beta_i = (self.Vreset - vmu_i) / vsigma_i
        beta_i = numpy.where(beta_i > 19, 19, beta_i)

        v_ae = self.nerf_table.search_value(alpha_e)
        v_ai = self.nerf_table.search_value(alpha_i)
        v_be = self.nerf_table.search_value(beta_e)
        v_bi = self.nerf_table.search_value(beta_e)

        v_integral_e = v_ae - v_be
        v_integral_i = v_ai - v_bi

        Phi_e = 1 / (self.taurp_e + vtau_e * numpy.sqrt(numpy.pi) * v_integral_e)
        Phi_i = 1 / (self.taurp_i + vtau_i * numpy.sqrt(numpy.pi) * v_integral_i)

        self.ve = - (self.Vthr - self.Vreset) * E * vtau_e + vmu_e
        self.vi = - (self.Vthr - self.Vreset) * I * vtau_i + vmu_i

        dE = (-E + Phi_e) / vtau_e
        dI = (-I + Phi_i) / vtau_i

        derivative = numpy.array([dE, dI])
        return derivative

    def update_derived_parameters(self):
        """
        Derived parameters

        """

        self.pool_fractions = 1. / (self.pool_nodes * 2)

        self.tauNMDA = self.calpha * self.tauNMDArise * self.tauNMDAdecay
        self.Text_e = (self.gAMPAext_e * self.Cext * self.tauAMPA) / self.gm_e
        self.Text_i = (self.gAMPAext_i * self.Cext * self.tauAMPA) / self.gm_i
        self.TAMPA_e = (self.gAMPArec_e * self.C * self.tauAMPA) / self.gm_e
        self.TAMPA_i = (self.gAMPArec_i * self.C * self.tauAMPA) / self.gm_i
        self.T_ei = (self.gGABA_e * self.C * self.tauGABA) / self.gm_e
        self.T_ii = (self.gGABA_i * self.C * self.tauGABA) / self.gm_i

        self.crho1_e = (self.gNMDA_e * self.C) / self.gm_e
        self.crho1_i = (self.gNMDA_i * self.C) / self.gm_i
        self.crho2_e = self.cbeta * self.crho1_e
        self.crho2_i = self.cbeta * self.crho1_i

        self.csigma_e = (self.gAMPAext_e ** 2 * self.Cext * self.tauAMPA ** 2) / \
                        (self.gm_e * self.taum_e) ** 2
        self.csigma_i = (self.gAMPAext_i ** 2 * self.Cext * self.tauAMPA ** 2) / \
                        (self.gm_i * self.taum_i) ** 2


if __name__ == "__main__":
    # Do some stuff that tests or makes use of this module...
    LOG.info("Testing %s module..." % __file__)
    
    # Check that the docstring examples, if there are any, are accurate.
    import doctest
    doctest.testmod()
    
    #Initialise Models in their default state:
    BW = BrunelWang()
        
    LOG.info("Model initialised in its default state without error...")
    
    LOG.info("Testing phase plane interactive ... ")
    
    # Check the Phase Plane
    from tvb.simulator.plot.phase_plane_interactive import PhasePlaneInteractive
    import tvb.simulator.integrators
        
    INTEGRATOR = tvb.simulator.integrators.HeunDeterministic(dt=2**-5)
    ppi_fig = PhasePlaneInteractive(model=BW, integrator=INTEGRATOR)
    ppi_fig.show()

    
