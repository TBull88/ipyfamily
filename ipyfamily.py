import json
import os
from time import sleep
from typing import List, Tuple, Dict
global my_current_id
my_current_id = 0
global living_only_flag
living_only_flag = False

'''
Utilizes information loaded from a json file to allow users to search for
values based on user input. Program returns the results in human readable
format
'''


def read_in_json_file(family_data: Dict) -> Dict:
    '''load json file as dictionary of dictionaries'''
    with open(family_data) as fd:
        family_db = json.load(fd)

    return family_db


def create_main_menu() -> str:
    '''menu that contains options for submenus people, misc, and exit'''
    main_selection = input((f"=============================\n"
                            f"            MAIN\n"
                            f"=============================\n"
                            f"1. People\n"
                            f"2. Misc\n"
                            f"3. Exit\n\n"
                            f"==> "))
    os.system('clear')
    return main_selection


def create_people_menu() -> str:
    '''
    menu that contains options to search data by name, id, search, siblings,
    ancestors, and descendants
    '''
    global current_id
    current_id = ''
    people_selection = input((f"=============================\n"
                              f"           PEOPLE\n"
                              f"=============================\n"
                              f"1. By Name\n"
                              f"2. By ID\n"
                              f"3. Search\n"
                              f"4. Siblings\n"
                              f"5. Ancestors\n"
                              f"6. Descendants\n"
                              f"7. Main\n\n"
                              f"==> "))
    print()
    return people_selection


def search_by_name(family_data: Dict) -> List[str]:
    '''search data by name and return(and remember) ID number'''
    global current_person
    by_name_id_list = []
    name_search_input = input("Enter all or part of a Name: ")

    try:
        for keys, values in family_data.items():
            if name_search_input != '':
                for key, val in values.items():
                    if (key == "lastname" and name_search_input.lower() in
                        val.lower()
                        or key == "firstname" and name_search_input.lower()
                            in val.lower()
                        or key == "middlename" and name_search_input.lower()
                            in val.lower()):
                        by_name_id_list.append(keys)
            else:
                raise ValueError

    except ValueError:
        os.system('clear')
        print(f"**********************************************\n"
              f"*   Your input was not recognized as valid.  *\n"
              f"*     Please select another option below     *\n"
              f"**********************************************")

    return by_name_id_list


def search_by_id(family_data: Dict) -> List[str]:
    '''search by id and return name of current person'''
    current_id_list = []
    id_search_input = input("Enter id (<Enter> for current ID): ")
    try:
        if int(id_search_input) in range(len(family_data) + 1):
            for key in family_data.keys():
                if key == id_search_input:
                    current_id_list.append(key)

        else:
            raise ValueError

    except ValueError:
        os.system('clear')
        print(f"**********************************************\n"
              f"*   Your input was not recognized as valid.  *\n"
              f"*     Please select another option below     *\n"
              f"**********************************************")
    global my_current_id
    my_current_id = id_search_input
    return current_id_list


def search_any_fields(family_data: Dict) -> List[str]:
    '''re.search all dicts for input'''
    os.system('clear')
    generic_search_id_list = []
    selection_dict = {'1': 'title',
                      '2': 'firstname',
                      '3': 'lastname',
                      '4': 'suffix',
                      '5': 'motherid',
                      '6': 'fatherid',
                      '7': 'gender',
                      '8': 'spouseid',
                      '9': 'hobby',
                      '10': 'dateofbirth',
                      '11': 'dateofdeath'}

    while True:
        print(f" ==========================================================\n",
              f"    Please enter number of the field you wish to search:  \n",
              f"==========================================================\n",
              f"1. Title\n",
              f"2. First Name\n",
              f"3. Last Name\n",
              f"4. Suffix\n",
              f"5. Mother ID\n",
              f"6. Father ID\n",
              f"7. Gender\n",
              f"8. Spouse ID\n",
              f"9. Hobby\n",
              f"10. Date of Birth\n",
              f"11. Date of Death\n")

        try:
            field_selection = input("==> ")
            if int(field_selection) <= (len(selection_dict) + 1):
                option = selection_dict[field_selection]
                break

            else:
                raise ValueError

        except ValueError:
            print("\033[2J\033[;H", end='')
            print(f"**********************************************\n"
                  f"*   Your input was not recognized as valid.  *\n"
                  f"*     Please select another option below     *\n"
                  f"**********************************************")

    specified_search = input("What would you like to search for?: ")
    if specified_search != '':
        for id, values in family_data.items():
            if values.get(option) != '' and values.get(option).lower()\
                    == specified_search.lower():
                generic_search_id_list.append(id)

    return generic_search_id_list


def search_siblings_by_id(family_data: Dict) -> List[str]:
    '''
    search siblings by id. if parent id == other parent id
    returns siblings (if any)
    '''
    sibling_id_list = []
    global my_current_id
    sibling_id = input("Please enter an ID to search for siblings: ")
    if sibling_id == '' and current_id != 0:
        sibling_id = my_current_id

    try:
        if int(sibling_id) in range(len(family_data)):
            father_id = family_data.get(sibling_id).get('fatherid')
            mother_id = family_data.get(sibling_id).get('motherid')
            for id_num, attributes in family_data.items():
                if sibling_id == id_num:
                    continue
                elif (father_id == attributes.get('fatherid') or
                        mother_id == attributes.get('motherid')):
                    sibling_id_list.append(id_num)
        else:
            raise ValueError

    except ValueError:
        os.system('clear')
        print(f"**********************************************\n"
              f"*   Your input was not recognized as valid.  *\n"
              f"*     Please select another option below     *\n"
              f"**********************************************")

    my_current_id = sibling_id
    return sibling_id_list


def search_ancestors_by_id(family_data: Dict) -> List[str]:
    '''
    returns a list of id's based off mother and father id. Appends new id
    once mother or father id matches another id's mother or father id
    '''
    while True:
        ancestor_list = []
        global my_current_id
        ancestor_id = input("Please enter an ID to search for ancestors: ")
        if ancestor_id == '' and current_id != 0:
            ancestor_id = my_current_id

        try:
            if int(ancestor_id) <= (len(family_data)):
                if (family_data.get(ancestor_id).get('fatherid') != '' and
                        family_data.get(ancestor_id).get('motherid') != ''):
                    father_id = \
                        family_data.get(ancestor_id).get('fatherid')
                    mother_id = \
                        family_data.get(ancestor_id).get('motherid')

                    ancestor_list.append(father_id)
                    ancestor_list.append(mother_id)

                else:
                    return ancestor_list

                for ancestor in ancestor_list:
                    father_id = family_data.get(ancestor).get('fatherid')
                    mother_id = family_data.get(ancestor).get('motherid')
                    if father_id != '':
                        ancestor_list.append(father_id)
                    elif mother_id != '':
                        ancestor_list.append(mother_id)
                ancestor_set = set(ancestor_list)
                sorted_ancsestor_list = sorted(list(ancestor_set),
                                               key=lambda x: int(x),
                                               reverse=True)
                break

            else:
                raise ValueError

        except ValueError:
            os.system('clear')
            print(f"**********************************************\n"
                  f"*   Your input was not recognized as valid.  *\n"
                  f"*   Please enter a valid ID between 1 & 48   *\n"
                  f"**********************************************")

    my_current_id = ancestor_id
    return sorted_ancsestor_list


def search_decendants_by_id(family_data: Dict) -> List[str]:
    '''
    Iterates through dictionary and appends matching id to list. Then iterates
    through list and compares id in dictionary to mother or father id. Appends
    id's to list if match is present
    '''
    while True:
        descendants_list = []
        global my_current_id
        descendant_id = input("Please enter an ID to search descendants: ")
        if descendant_id == '' and current_id != 0:
            descendant_id = my_current_id
        try:
            if int(descendant_id) <= (len(family_data)):
                for id_num, values in family_data.items():
                    if (descendant_id == values.get('fatherid') or
                            descendant_id == values.get('motherid')):
                        descendants_list.append(id_num)

                    for descendant in descendants_list:
                        if descendant == values.get('fatherid'):
                            descendants_list.append(id_num)
                        elif descendant == values.get('motherid'):
                            descendants_list.append(id_num)
                descendant_set = set(descendants_list)
                sorted_descendant_list = sorted(list(descendant_set),
                                                key=lambda x: int(x))
                break
            else:
                raise ValueError

        except ValueError:
            os.system('clear')
            print(f"**********************************************\n"
                  f"*   Your input was not recognized as valid.  *\n"
                  f"*   Please enter a valid ID between 1 & 48   *\n"
                  f"**********************************************")

    my_current_id = descendant_id
    return sorted_descendant_list


def create_misc_menu() -> str:
    '''
    menu that contains options to list all, intermarriages, and toggle
    living only flag
    '''
    misc_selection = input((f"===============================\n"
                            f"             MISC\n"
                            f"===============================\n"
                            f"1. List all\n"
                            f"2. Intermarriages\n"
                            f"3. Toggle Living-only Flag\n"
                            f"4. Main\n\n"
                            f"==> "))
    print()
    return misc_selection


def list_id_and_names(family_data: Dict) -> List[str]:
    '''Display a list of all id numbers and corresponding names'''
    id_name_list = []
    for id in family_data.keys():
        id_name_list.append(id)

    return id_name_list


def list_intermarriages(family_data: Dict) -> List[str]:
    '''get input for two family names, show all intermarriages between input'''
    family_list_1 = []
    family_list_2 = []
    marriages_list = []
    family_name_dict = {'1': 'Spamford',
                        '2': 'Who',
                        '3': 'Hamworth',
                        '4': 'Quagglemogg',
                        '5': 'Toastley',
                        '6': 'Eggerey'}
    while True:
        print(f"============================================================\n"
              f"       Select number of families to see intermarriages      \n"
              f"============================================================\n"
              f" 1. Spamford\n",
              f"2. Who\n",
              f"3. Hamworth\n",
              f"4. Quagglemogg\n",
              f"5. Toastley\n",
              f"6. Eggerey\n")

        try:
            family_name_1 = input('==> ')
            family_name_2 = input('==> ')
            if (int(family_name_1) <= (len(family_name_dict)) and
                    int(family_name_2) <= (len(family_name_dict))):
                option_1 = family_name_dict[family_name_1]
                option_2 = family_name_dict[family_name_2]
                break

            else:
                raise ValueError

        except ValueError:
            os.system('clear')
            print(f"**********************************************\n"
                  f"*   Your input was not recognized as valid.  *\n"
                  f"*    Please select from the options below    *\n"
                  f"**********************************************")
    for id, values in family_data.items():
        if option_1 == values.get('lastname'):
            family_list_1.append(id)
        elif option_2 == values.get('lastname'):
            family_list_2.append(id)
        # print(marriages_list)
    for spouse_1 in family_list_1:
        for spouse_2 in family_list_2:
            if spouse_1 == family_data[spouse_2]['spouseid']:
                marriages_list.append(spouse_1)
                marriages_list.append(spouse_2)

    return marriages_list


def toggle_living_only_flag(family_data: Dict) -> List[str]:
    '''toggle value of living-only flag. When true only show living persons'''
    living_only_list = []

    for id, value in family_data.items():
        if value.get('dateofdeath') == '':
            living_only_list.append(id)
    return living_only_list


def print_function(family_data: Dict,
                   result_list: List[str],
                   living_only_flag: bool) -> None:
    '''function to handle all printing in a more human readable format'''
    if not living_only_flag:
        os.system('clear')
        print(f"--------- SEARCH RESULT(S) ---------\n")
        for id, values in family_data.items():
            for result in result_list:
                if id == result:
                    print(f"{id}: {values.get('firstname')}",
                          f"{values.get('middlename')}",
                          f"{values.get('lastname')}")
        print()
    else:
        os.system('clear')
        print(f"--------- SEARCH RESULT(S) ---------\n")
        for id, values in family_data.items():
            for result in result_list:
                if id == result and family_data[result]['dateofdeath'] == '':
                    print(f"{id}: {values.get('firstname')}",
                          f"{values.get('middlename')}",
                          f"{values.get('lastname')}")
        print()

    if not result_list:
        print("THE INFORMATION YOU REQUESTED WAS NOT FOUND\n\n")


def main():
    '''main function to handle main logic of program '''
    family_db = read_in_json_file('familydata.json')
    global living_only_flag
    living_only_flag = False
    global my_current_id
    my_current_id = 0

    while True:
        main_selection = create_main_menu()

        people_menu_dict = {'1': search_by_name,
                            '2': search_by_id,
                            '3': search_any_fields,
                            '4': search_siblings_by_id,
                            '5': search_ancestors_by_id,
                            '6': search_decendants_by_id,
                            '': (my_current_id, living_only_flag)}

        misc_menu_dict = {'1': list_id_and_names,
                          '2': list_intermarriages,
                          '3': toggle_living_only_flag,
                          '4': create_people_menu,
                          '': (my_current_id, living_only_flag)}

        if main_selection == '':
            print(f"Current person set to: {my_current_id}")
            print(f"Current status of living-only flag = {living_only_flag}")
        elif main_selection == '1':
            while True:
                people_selection = create_people_menu()
                if people_selection == '':
                    os.system('clear')
                    print(f"Current person set to: {my_current_id}")
                    print(f"Current status of living-only flag =",
                          f"{living_only_flag}")
                elif people_selection == '7':
                    os.system('clear')
                    break
                else:
                    try:
                        result_list = \
                            people_menu_dict[people_selection](family_db)
                        print_function(family_db, result_list,
                                       living_only_flag)
                    except KeyError:
                        print(f"Your input was invalid. Please choose a valid"
                              f"selection")

        elif main_selection == '2':
            while True:
                misc_selection = create_misc_menu()
                os.system('clear')
                if misc_selection == '':
                    os.system('clear')
                    print(f"Current person set to: {my_current_id}")
                    print(f"Current status of living-only flag:",
                          f"{living_only_flag}")

                elif misc_selection == '3':
                    toggle = input(f"Press Enter to toggle living only flag "
                                   f"\u23CE'\n")
                    if not living_only_flag and toggle == '':
                        living_only_flag = True
                    elif living_only_flag and toggle == '':
                        living_only_flag = False
                    os.system('clear')
                elif misc_selection == '4':
                    os.system('clear')
                    break

                else:
                    try:
                        result_list = misc_menu_dict[misc_selection](family_db)
                        print_function(family_db, result_list,
                                       living_only_flag)
                    except KeyError:
                        print("Please enter a valid selection")

        elif main_selection == '3':
            os.system('clear')
            print(f"==========================================\n"
                  f"                  ADIOS\n"
                  f"==========================================\n")
            exit()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(": DON'T INTERRUPT ME!!")
        sleep(1.50)
        os.system('clear')
        print("JUST KIDDING! HAVE A WONDERFUL DAY!")
