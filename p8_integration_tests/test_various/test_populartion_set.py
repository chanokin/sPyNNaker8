import spynnaker8 as p

CELL_PARAMS_LIF = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 20.0,
                   'tau_refrac': 2.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
                   'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -50.0}

p.setup()
p1 = p.Population(5, p.IF_curr_exp(**CELL_PARAMS_LIF), label='pop_1')

p1.set(cm=0.2)
