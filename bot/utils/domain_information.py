from datetime import datetime
import asyncwhois

from bot.utils.translations import translations


def domain(domain_name, language):
    try:
        result = asyncwhois.whois_domain(domain_name)

        expires = datetime.strptime((result.parser_output['expires']).strftime("%Y/%m/%d %H:%M:%S"),
                                    "%Y/%m/%d %H:%M:%S")
        created = datetime.strptime((result.parser_output["created"]).strftime("%Y/%m/%d %H:%M:%S"),
                                    "%Y/%m/%d %H:%M:%S")
        updated = datetime.strptime((result.parser_output["updated"]).strftime("%Y/%m/%d %H:%M:%S"),
                                    "%Y/%m/%d %H:%M:%S")

        if type(result.parser_output['expires']) == list:
            date = result.parser_output['expires'][0] - datetime.now()
        else:
            date = expires - datetime.now()

        lines = [
            f'{translations[language]["domain_data"]} {domain_name}',
            f'{translations[language]["domain_expires"]} : {date.days}',
            f'{translations[language]["domain_creation"]} : {created}',
            f'{translations[language]["domain_update"]} : {updated}',
            f'{translations[language]["domain_hosting"]} : {result.parser_output["registrar_url"]}',
            f'{translations[language]["hosting_company"]} : {result.parser_output["registrar"]}',
            f'{translations[language]["country_reg"]} : {result.parser_output["registrant_country"]}',
            f'{translations[language]["hosting_phone"]} : {result.parser_output["registrar_abuse_phone"]}'
        ]

        return '\n'.join(lines)
    except Exception as e:
        print(e)
        return 'Не вдалося знайти данні :( \nСпробуйте ще раз або введіть інший домен!'
