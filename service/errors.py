class Errors:
    """Class which allows to generate errors and to save them 
    in order to recover them later

    Returns:
        dict: All errors saved
    """

    def __init__(self):
        self.errors = []

    def add(self, code=0, input='', message=''):
        """Add method that allows to add errors

        Args:
            code (int, optional): 
                code 0: blocking errors, 
                code 1: major errors,
                code 2: minor erros.
                Defaults to 0.
            input (str, optional): id or name of input for retrieve in front. Defaults to ''.
            message (str, optional): message the user will see. Defaults to ''.

        Returns:
            dict: All errors saved
        """
        self.errors.append({
            'code': code,
            'input': input,
            'message': message
        })
        return self.errors

    def get_errors(self):
        return self.errors

    def get_dict_erros(self):
        if self.has_errors():
            return {'errors': self.get_errors()}
        return {}
    
    def has_errors(self):
        if self.errors:
            return True
        return False