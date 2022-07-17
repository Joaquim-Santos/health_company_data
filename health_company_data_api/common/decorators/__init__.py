import os


if os.environ["STAGE"].capitalize() in ["Test"]:
    from health_company_data_api.common.decorators.validate_request_local import (
        validate_request_local as validate_request,
    )
else:
    from health_company_data_api.common.decorators.validate_request import (
        validate_request,
    )
