import re 

def parse_chemical_equation(equation):
    # Define the regular expression patterns for splitting reactants and products
    arrow_pattern = re.compile(r'\s*[-−−−−−−−−−−−−−−−−−−−−−−−−−−−>]+\s*')
    plus_pattern = re.compile(r'\s*\+\s*')

    # Split the equation into reactants and products based on the arrow pattern
    reactants, products = arrow_pattern.split(equation)
    
    # Split reactants and products by the plus pattern and strip whitespace
    reactants = [reactant.strip() for reactant in plus_pattern.split(reactants)]
    products = [product.strip() for product in plus_pattern.split(products)]
    
    return reactants, products

def unique_elements_in_sublists(list_of_lists):
    unique_elements = []
    for sublist in list_of_lists:
        unique_elements.append(sublist[0])  # Since each sublist contains the same value repeated
    return unique_elements


def parse_compound_formula(formula):
    # Regular expression to match elements and their counts
    pattern = r'([A-Z][a-z]*)(\d*)'
    matches = re.findall(pattern, formula)
    el_dict = {}

    for match in matches:
        element, count = match
        el_dict[element] = 1 if count == '' else int(count)

    return el_dict

def combine_dictionaries(dicts):
    
    combined_dict = {}
    
    for dictionary in dicts:
        for key, value in dictionary.items():
            if key in combined_dict:
                # If key already exists, aggregate the values
                combined_dict[key] += value
            else:
                # If key is not present, add it to the combined dictionary
                combined_dict[key] = value
    
    return combined_dict

def multiply_dictionary_values(dictionary, multiplier):
    
    multiplied_dictionary = {key: value * multiplier for key, value in dictionary.items()}
    
    return multiplied_dictionary

def compare_scales(R, P, B):
    
    results = []
    
    for key in R.keys():
        if not B.get(key, False):
            quotient = max(R[key], P[key]) / min(R[key], P[key])
            if quotient.is_integer():
                results.insert(0, (key, quotient))
            else:
                results.append((key, quotient))
    
    for key, quotient in results:
        print(f"{key}: {quotient}")
    
    return results

def initialize_equation(reactants, products):
    
    before = [parse_compound_formula(val) for val in reactants]    
    after=[parse_compound_formula(val) for val in products]
    
    return before, after 

def aggregate(before, after):
    
    R = combine_dictionaries(before)
    P = combine_dictionaries(after)
    B = {}
    
    for key in R.keys():
        B[key] = R[key] == P[key]
    
    return R, P, B

def determine_changes(R, P, results):
    
    target_elem = results[0][0]
    scale_factor = results[0][1]
    target_list = ''
    
    if R[target_elem] > P[target_elem]:
        target_list = 'after'
    elif R[target_elem] < P[target_elem]:
        target_list = 'before'
    
    return target_elem, scale_factor, target_list 

def handle_lin_comb(sep, agg_start, agg_targ, target_elem):
    
    start_value = agg_start[target_elem]
    goal_value = agg_targ[target_elem]
    
    for val in sep:
        scale = (goal_value-(start_value - val[target_elem]))/val[target_elem]
        if scale.is_integer():
            idx = sep.index(val)
            sep[idx] = multiply_dictionary_values(sep[idx], scale)
    
    return sep 

def handle_int_scale(sep, target_elem, scale_factor):
    
    for val in sep:
        if target_elem in val.keys():
            new_val = multiply_dictionary_values(val, scale_factor)
            idx = sep.index(val)
            sep[idx] = new_val
    
    return sep 

def apply_changes(before, after, R, P, target_elem, scale_factor, target_list):
    
    if target_list == 'before':
        if scale_factor.is_integer():
            before = handle_int_scale(before, target_elem, scale_factor)
        else:
            before = handle_lin_comb(before, R, P, target_elem)
    
    elif target_list == 'after':
        if scale_factor.is_integer():
            after = handle_int_scale(after, target_elem, scale_factor)
        else:
            after = handle_lin_comb(after, P, R, target_elem)
    
    return before, after

def recursive_balancing(before, after):
    R, P, B = aggregate(before, after)
    results = compare_scales(R, P, B)
    
    if not results:
        return before, after
    
    target_elem, scale_factor, target_list = determine_changes(R, P, results)
    before, after = apply_changes(before, after, R, P, target_elem, scale_factor, target_list)
    
    return recursive_balancing(before, after)

def balance_equation(reactants, products):
    REACT, PROD = initialize_equation(reactants, products)
    R_COPY = REACT.copy()
    P_COPY = PROD.copy()
    
    final_before, final_after = recursive_balancing(R_COPY, P_COPY)
    print(f"Original Equation")
    print(f"{REACT} --> {PROD}")
    print(f"----------------------------------")
    print(f"Balanced Equation")
    print(f"{final_before} --> {final_after}")
    
    return final_before, final_after, REACT, PROD

def divide_corresponding_values(list1, list2):
    result = []

    for dict1, dict2 in zip(list1, list2):
        divided_values = []
        for key in dict1.keys():
            divided_values.append(dict2[key] / dict1[key])
        result.append(divided_values)

    return result

def compound_formula_from_dict(element_dict):
    formula = ''
    for element, count in element_dict.items():
        formula += element
        if count > 1:
            formula += str(count)
    return formula

def finaL_display_setup(r_coef, reactants, p_coef, products):
    left_elems = []
    right_elems = []
    
    for i in range(len(r_coef)):
        left_elems.append(f"{int(r_coef[i][0])}{reactants[i]}")
    
    for i in range(len(p_coef)):
        right_elems.append(f"{int(p_coef[i][0])}{products[i]}")
    
    left_side = ' + '.join(left_elems)
    right_side = ' + '.join(right_elems)
    return f"{left_side} --> {right_side}"

def eq_to_eq_report(eq_string):
    ### Get reactants and products
    reactants, products = parse_chemical_equation(eq_string)
    print(f"REACTANTS : {', '.join(reactants)}")
    print(f"PRODUCTS : {', '.join(products)}")
    print('')
    print('')
    
    ### Balance Equation
    final_before, final_after, REACT, PROD = balance_equation(reactants, products)
    print('')
    print('')
    
    ### Get final coefficients 
    r_coef = divide_corresponding_values(REACT, final_before)
    p_coef = divide_corresponding_values(PROD, final_after)
    print('----------------------------------------------------')
    print(f'Final Coefficients for Reactants - {unique_elements_in_sublists(r_coef)}')
    print(f'Final Coefficients for Products - {unique_elements_in_sublists(p_coef)}')
    print('')
    print('')
    
    ### Final display
    print("----------------------------------------------------")
    print('Original Equation: ')
    print(eq_string)
    print('Balanced Equation: ')
    print(finaL_display_setup(r_coef, reactants, p_coef, products))
    
    return r_coef, reactants, p_coef, products

