from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.utils import aware_utcnow

DATE_FORMAT = '%Y/%m/%d %H:%M'
ALPHABET_START = 'A'
ZERO_COMPENSATOR = -1


async def spreadsheets_create(
        charity_projects_quantity: int,
        wrapper_services: Aiogoogle) -> str:

    service = await wrapper_services.discover('sheets', 'v4')

    title = settings.spreadsheet_title.format(
        aware_utcnow().strftime(DATE_FORMAT)
    )
    row_quantity = (
        charity_projects_quantity +
        settings.spreadsheet_title_header_row_quantity
    )

    spreadsheet_body = {
        'properties': {'title': title,
                       'locale': 'ru_RU'},
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': title,
                'gridProperties': {
                    'rowCount': row_quantity,
                    'columnCount': settings.spreadsheet_column_quantity
                }
            }
        }]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:

    service = await wrapper_services.discover('drive', 'v3')

    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:

    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        [settings.spreadsheet_title.format(
            aware_utcnow().strftime(DATE_FORMAT)
        )]
    ]
    table_values.append(settings.spreadsheet_header)

    for project in projects:
        duration = project.close_date - project.create_date
        new_row = [
            project.name,
            duration.days,
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    row_num = len(table_values)
    column_sym = chr(
        settings.spreadsheet_column_quantity +
        ord(ALPHABET_START) +
        ZERO_COMPENSATOR
    )

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:{column_sym}{row_num}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
