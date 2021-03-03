# First Line/Compartment
absorptivity_rate_0 = 0.000734
reflectivity_rate_0 = 0.999261
transmissivity_rate_0 = 0.000005
absorption_0 = 0
transmission_down_1 = 0
light_1 = 0

# Second Line/Compartment
absorptivity_rate_1 = 0.06
reflectivity_rate_1 = 0.09
transmissivity_rate_1 = 0.85
absorption_1 = 0
transmission_up_2 = 0
transmission_down_2 = 0
light_2 = 0

# Third Line/Compartment
absorptivity_rate_2 = 0.075
reflectivity_rate_2 = 0.75
transmissivity_rate_2 = 0.175
absorption_2 = 0
transmission_up_3 = 0
transmission_down_3 = 0
light_3 = 0

# Fourth Line/Compartment
absorptivity_rate_3 = 0.16
reflectivity_rate_3 = 0.84
absorption_3 = 0
transmission_up_4 = 0
light_4 = 0

remaining_light = 109100000       # initially 109.1*10^6 watts
light_1 = remaining_light*transmissivity_rate_0
absorption_0 = remaining_light*absorptivity_rate_0

external_incrementer = 0    # tracking overall outer iterations

while remaining_light > 0.000001: # while light still exists within

    # Compartment 1: Lines 0 and 1
    if external_incrementer > 0:
        light_1 = transmission_up_2 # from previous iteration
        transmission_up_2 = 0

    internal_incrementer = 0

    while light_1 > 0.0000003:
        # hitting bottom line of compartment 1 on first go
        if internal_incrementer%2 == 0 and external_incrementer == 0:
            temp_light = light_1
            light_1 = light_1*reflectivity_rate_1
            absorption_1 = absorption_1 + (temp_light*absorptivity_rate_1)
            transmission_down_1 = transmission_down_1 + (temp_light*transmissivity_rate_1)

        # hitting bottom line of compartment 1 every subsequent iteration
        elif internal_incrementer%2 == 1 and external_incrementer > 0:
            temp_light = light_1
            light_1 = light_1*reflectivity_rate_1
            absorption_1 = absorption_1 + (temp_light*absorptivity_rate_1)
            transmission_down_1 = transmission_down_1 + (temp_light*transmissivity_rate_1)

        #hitting top line of compartment 1
        else:
            temp_light = light_1
            light_1 = light_1*reflectivity_rate_0
            absorption_0 = absorption_0 + (temp_light*absorptivity_rate_0)

        td1_tracker = transmission_down_1

        internal_incrementer += 1

################################################################################

    # Compartment 2: Lines 1 and 2
    light_2 = transmission_up_3 + transmission_down_1

    light_from_3 = transmission_up_3
    light_from_1 = transmission_down_1

    transmission_down_1 = 0 # from current iteration
    transmission_up_3 = 0   # from prev iterations

    internal_incrementer = 0

    while light_from_1 + light_from_3 > 0.0000003:
        # simultaneous transmission_down_1 and transmission_up_3 calculations
        # since light from above hits bottom first and vice versa from below
        if internal_incrementer%2 == 0:
            # light_from_1 hitting bottom
            temp_light_from_1 = light_from_1
            light_from_1 = light_from_1*reflectivity_rate_2
            absorption_2 = absorption_2 + (temp_light_from_1*absorptivity_rate_2)
            transmission_down_2 = transmission_down_2 + (temp_light_from_1*transmissivity_rate_2)

            # light_from_3 hitting top
            temp_light_from_3 = light_from_3
            light_from_3 = light_from_3*reflectivity_rate_1
            absorption_1 = absorption_1 + (temp_light_from_3*absorptivity_rate_1)
            transmission_up_2 = transmission_up_2 + (temp_light_from_3*transmissivity_rate_1)

        else: # light from above is now hitting top and vice versa
            # light_from_3 hitting bottom
            temp_light_from_3 = light_from_3
            light_from_3 = light_from_3*reflectivity_rate_2
            absorption_2 = absorption_2 + (temp_light_from_3*absorptivity_rate_2)
            transmission_down_2 = transmission_down_2 + (temp_light_from_3*transmissivity_rate_2)

            # light_from_1 hitting top
            temp_light_from_1 = light_from_1
            light_from_1 = light_from_1*reflectivity_rate_1
            absorption_1 = absorption_1 + (temp_light_from_1*absorptivity_rate_1)
            transmission_up_2 = transmission_up_2 + (temp_light_from_1*transmissivity_rate_1)

        internal_incrementer += 1

################################################################################

    # Compartment 3: Lines 2 and 3
    light_3 = transmission_down_2 # from current iteration

    td2_tracker = transmission_down_2
    transmission_down_2 = 0

    internal_incrementer = 0

    while light_3 > 0.0000003:
        # hitting bottom line of compartment 3
        if internal_incrementer%2 == 0:
            temp_light = light_3
            light_3 = light_3*reflectivity_rate_3
            absorption_3 = absorption_3 + (temp_light*absorptivity_rate_3)

        # hitting top line of compartment 3
        if internal_incrementer%2 == 1:
            temp_light = light_3
            light_3 = light_3*reflectivity_rate_2
            absorption_2 = absorption_2 + (temp_light*absorptivity_rate_2)
            transmission_up_3 = transmission_up_3 + (temp_light*transmissivity_rate_2)

        internal_incrementer += 1

################################################################################

    remaining_light = td1_tracker + transmission_up_2 + td2_tracker + transmission_up_3

    external_incrementer += 1

print('\nAbsorption0: ', absorption_0, '  Watts')
print('Absorption1: ', absorption_1, ' Watts')
print('Absorption2: ', absorption_2, ' Watts')
print('Absorption3: ', absorption_3, ' Watts\n')
