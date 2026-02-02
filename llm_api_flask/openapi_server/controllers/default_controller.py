from llm_function.main_llm import _Parse

def parse_file(file=None):  # noqa: E501
    """parse_file

     # noqa: E501

    :param file: Resume file
    :type file: str

    :rtype: Union[object, Tuple[object, int], Tuple[object, int, Dict[str, str]]
    """
    return _Parse(file)
