
def prepareResponse(meta=[], data=[], state=True):

    if (state == True):
        meta['items'] = data
    else:
        # to be done later
        meta['trace_id'] = "ABCDEFG123456"

        if (meta['status'] == 404):
            meta['title'] = "Record not found"
            meta['detail'] = "Id is not exist or deleted from the database"
            meta['type'] = "https://httpstatuses.com/404"
            data = {"id": ["Id is not exist or deleted from the database"]}
        if (meta['status'] == 422):
            meta['title'] = "Unprocessable entity"
            meta['detail'] = "Validation errors"
            meta['type'] = "https://httpstatuses.com/422"

        meta['errors'] = data

    return meta
