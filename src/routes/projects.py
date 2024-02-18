from fastapi import APIRouter

router = APIRouter(
    prefix="/project",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_data = {
    "projects": [
        {
            "id": 1,
            "name": "test_data",
            "description": "sample description",
            "documents": [
                "asd1",
                "asd2",
                "asd3",
                "asd4",
            ],
        }
    ]
}

# @router.get("/")
# async def read_projects():
#     return fake_data
