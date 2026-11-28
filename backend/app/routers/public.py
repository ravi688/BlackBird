from fastapi import APIRouter


router = APIRouter(
	prefix="/public",
	tags=["Public"]
	)

@router.get("/check-for-update")
async def check_for_update():
	return { "message" : "ok" }

@router.post("/device-update-status")
async def device_update_status():
	return { "message" : "ok" }
