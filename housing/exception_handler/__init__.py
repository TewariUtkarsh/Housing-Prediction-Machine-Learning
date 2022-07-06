import os
import sys

class HousingException(Exception):

    def __init__(self, error_message:Exception, error_detail:sys):
        """
        error_message: Exception object/instance, 
                       any exception occurs that will 
                       create an exception object

        error_detail: current code execution deatils 
                      is stored in sys module like which
                      line and file are cauing error

        """

        super().__init__(error_message)
        self.error_message = HousingException.get_detailed_error_message(error_message=error_message,
                                                                        error_detail=error_detail)

    
    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_detail:sys) -> str:
        _, _, exec_tb = error_detail.exc_info()
        exception_block_line_number = exec_tb.tb_frame.f_lineno
        try_block_line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"""
Error Occurred in script:
[ {file_name} ] at 
try block line number: [{try_block_line_number}] and 
exception block line number: [{exception_block_line_number}]  
error message: [ {error_message} ]"""
        return error_message


    def __str__(self) -> str:
        """
        Prints the error message associated with the object created. Used for getting better understanding of code.

        E.g.: print(Demo())
        """
        return self.error_message

    
    def __repr__(self) -> str:
        """
        Object representation. Used for getting better understanding of code.

        E.g.: Demo()
        """
        return HousingException.__name__.str()