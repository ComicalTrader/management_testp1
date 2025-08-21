
from fastapi import APIRouter, Request
router = APIRouter(prefix="/webhook", tags=["whatsapp"])

@router.post("/whatsapp")
async def whatsapp_webhook(req: Request):
    payload = await req.json()
    # Exemplo esperado:
    # {"name":"João","phone":"+55...","service":"corte","start_at":"2025-08-20T14:00:00"}
    # TODO: validar/normalizar e criar Appointment via mesma lógica do router
    
    return {"received": True}
