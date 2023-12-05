from pydantic import BaseModel

from datetime import datetime
import asyncwhois

class DomainInfo(BaseModel):
	expires: datetime
	created: datetime
	updated : datetime
	

	@classmethod
	def from_domain(cls, domain_name: str):
		try:
			result = asyncwhois.whois_domain(domain_name)

			expires = datetime.strptime((result.parser_output['expires']).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
			created = datetime.strptime((result.parser_output["created"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
			updated = datetime.strptime((result.parser_output["updated"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
			
			return cls(expires,created,updated)
		except:
			pass 

