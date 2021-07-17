from app.auth.auth_bearer import JWTBearer
from app.repositories.bitcoin import get_bitcoin_info, handle_block_sub
from app.routers.bitcoin_docs import blocks_sub_doc, get_bitcoin_info_desc
from app.sse_starlette import EventSourceResponse
from app.utils import bitcoin_rpc
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.params import Depends

router = APIRouter(
    prefix="/bitcoin",
    tags=["Bitcoin Core"]
)


@router.get("/getblockcount", summary="Get the current block count",
            description="See documentation on [bitcoincore.org](https://bitcoincore.org/en/doc/0.21.0/rpc/blockchain/getblockcount/)",
            response_description="""A JSON String with relevant information.\n
```json
{
  \"result\": 682621,
  \"error\": null,
  \"id\": 0
}
""",
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def getblockcount():
    r = bitcoin_rpc("getblockcount")

    if(r.status_code == status.HTTP_200_OK):
        return r.content
    else:
        raise HTTPException(r.status_code, detail=r.reason)


@router.get("/getblockchaininfo", summary="Get the current blockchain status",
            description="See documentation on [bitcoincore.org](https://bitcoincore.org/en/doc/0.21.0/rpc/blockchain/getblockchaininfo/)",
            response_description="A JSON String with relevant information.",
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def getblockchaininfo():
    r = bitcoin_rpc("getblockchaininfo")

    if(r.status_code == status.HTTP_200_OK):
        return r.content
    else:
        raise HTTPException(r.status_code, detail=r.reason)


@router.get("/getbitcoininfo", summary="Get general information about bitcoin core",
            description=get_bitcoin_info_desc,
            response_description="A JSON String with relevant information.",
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
async def getbitcoininfo():
    try:
        return await get_bitcoin_info()
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.reason)


@router.get("/getnetworkinfo", summary="Get information about the network",
            description="See documentation on [bitcoincore.org](https://bitcoincore.org/en/doc/0.21.0/rpc/network/getnetworkinfo/)",
            response_description="A JSON String with relevant information.",
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def getnetworkinfo():
    r = bitcoin_rpc("getnetworkinfo")

    if(r.status_code == status.HTTP_200_OK):
        return r.content
    else:
        raise HTTPException(r.status_code, detail=r.reason)


@router.get("/block_sub", summary="Subscribe to incoming blocks.",
            description=blocks_sub_doc,
            response_description="A JSON object with information about the new block.",
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
async def zmq_sub(request: Request, verbosity: int = 1):
    return EventSourceResponse(handle_block_sub(request, verbosity))
