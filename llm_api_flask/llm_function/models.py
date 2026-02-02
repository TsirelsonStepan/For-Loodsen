from typing import Optional
from pydantic import BaseModel, Field
import json

class ResumeDetails(BaseModel):
    """Structure of the output of the LLM"""

    name : str = Field(description="type: String, description: Full name")
    email : str = Field(description="type: String, description: Email addres")
    phone : str = Field(description="type: String, description: Phone number")
    position : Optional[str] = Field(description="type: Optional(String), description: Desired position in a company")
    education : Optional[str] = Field(description="type: Optional(String), descripiton: Education")
    experience : Optional[str] = Field(description="type: Optional(String), description: Work experience")
    hoursPerWeek : Optional[int] = Field(description="type: Optional(Integer), description: Desired amount of hours worked per week. Only between 20 and 40 hours")
    employmentType : Optional[str] = Field(description="type: Optional(Integer), description: Desired type of employment. Only one of the following: 'в офисе', 'гибрид', 'удалённо'")
    links : Optional[str] = Field(description="type: Optional(String), description: Links")
    skills : str = Field(description="type: String, description: List of skills separated by this symbol: ', '")

    def ToJSON(self):
        answer = {}
        for i in self.__annotations__:
            answer[i] = (getattr(self, i))
            #if i == "skills": answer[i] = answer[i].split('|')
        return json.dumps(answer, ensure_ascii=False)
        
