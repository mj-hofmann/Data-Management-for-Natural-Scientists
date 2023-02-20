# required imports
import re
import datetime
import os
import pandas as pd


def read_file_content_as_string(filename):
    """
    Reads the file specified via "filename" and returns its content
    as str.

    Parameters
    ----------
    filename : str
        path to experimental surface tension file to be read.

    Returns
    -------
    file content as string.

    """
    
    # initialize results variable of type string
    results = ""
    
    # open the file for reading "r" with encoding utf-8
    with open(filename, "r", encoding="utf-8") as f:
        # read file line by line
        while True:
            # read line
            line = f.readline()
            # append to string
            results = results + line
            # end of file reached
            if not line:
                print(type(line))
                # break infinite while loop
                break
    
    # return file content as string
    return results


def get_data_from_experimental_string(experimental_string,
                                      show_info=True):
    """
    Extracts "data" from the experimetal results string and returns a
    pd.DataFrame.

    Parameters
    ----------
    string : str
        string holding the experimental file content.

    Returns
    -------
    data : pd.DataFrame
        pd.DataFrame with columns 
            - "concentration_g_l" and
            - "surface_tension_mN_m"

    """
    
    # patterns as derived via regex101.com
    pattern = "(.*),(\d+.*)"    
    
    # find pattern in string "experimental_string"
    findings = re.findall(
                    pattern,
                    experimental_string
                )
    
    # import pandas module to use the DataFrame with alias pd
    import pandas as pd
    
    # initialize empty pandas.DataFrame data
    data = pd.DataFrame()
    
    # initialize empty list of concentrations
    concentration_g_l = []
    # loop through findings to get concentrations
    for _finding in findings:
        # info
        if show_info:
            print(_finding)
        # get the first element of the "_finding" (string) and 
        # convert to float
        _c_g_l = float(_finding[0])
        # append extracted concentration to list of concentrations
        concentration_g_l.append(_c_g_l)
        
    # use concentration list as column in the defined DataFrame
    data["concentration_g_l"] = concentration_g_l
    
    # use surface tension as column (via list comprehension)
    data["surface_tension_mN_m"] = [float(i[1]) for i in findings]

    # return pd.DataFrame holding experimental "data"
    return data


def get_information_from_experimental_string(experimental_string, 
                                             show_info=True):
    """
    Extracts "information" from the experimetal results string and
    # returns a
    pd.DataFrame.


    Parameters
    ----------
    experimental_string : str
        string holding the experimental file content.
    show_info : bool, optional
        flag for further information. The default is True.

    Returns
    -------
    information : pd.DataFrame
        pd.DataFrame with columns "parameter" and "value"

    """

    # define regex pattern
    pattern = "(?P<parameter>[\w ]+): (?P<value>.*)"
    
    # find pattern in string "experimental_string" as iterator 
    # "findings_parameters"
    findings_parameters = re.finditer(
        pattern,
        experimental_string
        )
    
    # initialize list of "parameters" and "values"
    parameters = []
    values = []
    
    # loop over iterable to get parameter name and value
    for _f in findings_parameters:
        # info
        if show_info:
            print(_f)
        # get dict for this finding
        _dict = _f.groupdict()
        # extract "parameter" and "value" and append to list
        parameters.append(_dict["parameter"])
        values.append(_dict["value"])
    
    # build pd.DataFrame "information" from the extracted list
    information = pd.DataFrame({
        "parameter" : parameters,
        "value" : values
        })
        
    # return pd.DataFrame holding experimental "information"
    return information


def add_further_information(information, medium=None,
                            temperature=None):
    """
    Adds pieces of information to "information" pd.DataFrame and 
    returns the modified pd.DataFrame "information".
    

    Parameters
    ----------
    information : pd.DataFrame
        DataFrame holding information.
    medium : str, optional
        information on sample medium ("solvent phase"). The default 
        is None.
    temperature : float|int, optional
        information on temperature during the experiment. The default
        is None.

    Returns
    -------
    information : pd.DataFrame
        Enriched DataFrame holding additional pieces of information.

    """

    # define columns
    _par = "parameter"
    _val = "value"
    
    # solvent medium (add new row dict)
    if medium:
        information = information.append({
            _par : "Solvent medium",
            _val : medium
            }, ignore_index=True
            )
    if temperature:
        # experimental temperature (add new row pd.DataFrame)
        information = information.append(pd.DataFrame({
            _par : "Experimental temperature degree C]",
            _val : float(temperature) # temperature of the room/lab
            }, index=[len(information)+1])
            )
    # processing timestamp (add new row dict)
    information = information.append({
        _val : datetime.datetime.now().\
            replace(microsecond=0),  # timestamp
        _par : "File processed on"
        }, ignore_index=True
        )
    # operator (add new row pd.DataFrame)
    information = information.append(pd.DataFrame({
        _val : os.getlogin(),  # get logged in user
        _par : "File processed by"
        }, index=[len(information)+1])
        )
        
    # return modified ("enriched") information pd.DataFrame
    return information
