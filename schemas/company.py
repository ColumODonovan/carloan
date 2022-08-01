import pydantic
from pydantic import BaseModel, ValidationError
from typing import Optional
from typing_extensions import Literal
import sys

#constants
VALUE_1 = "1-9"
VALUE_2 = "10-99"
VALUE_3 = "99+"
VALUE_4 = "unknown"



class Company(BaseModel):
    name: str
    employees: Optional[Literal[VALUE_1, VALUE_2, VALUE_3, VALUE_4]]
    

    @pydantic.validator("employees", pre=True)
    @classmethod
    def is_employees_valid(cls, value):
        
        r1 = range(1,10)
        r2 = range(10,100)
        r3 = range(100, sys.maxsize)
        ranges = [(r1,VALUE_1), (r2, VALUE_2) , (r3, VALUE_3)]

        nums = [int(s) for s in value.replace(" ", "").split("-") if s.isdigit()]
        
        if len(nums)==1:
            for r in ranges:
                if nums[0] in r[0]:
                    return r[1]
        return value


if __name__ == '__main__':
    data = {'name': 'Good Company B.V.', 'employees': ' 9'}
    try:
        company = Company(**data)
        print(f"{company.name} has {company.employees} number of employees")
    except ValidationError:
        print(f"Invalid data supplied")
        raise